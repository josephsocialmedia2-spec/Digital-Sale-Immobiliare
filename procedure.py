from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, List, Dict


class Stage(str, Enum):
    NUOVO = "NUOVO"
    CONTATTATO = "CONTATTATO"
    QUALIFICATO = "QUALIFICATO"
    APPUNTAMENTO_FISSATO = "APPUNTAMENTO_FISSATO"
    VALUTAZIONE_FATTA = "VALUTAZIONE_FATTA"
    PROPOSTA_INCARICO = "PROPOSTA_INCARICO"
    ACQUISITO = "ACQUISITO"
    PAUSA = "PAUSA"
    SCARTATO = "SCARTATO"


@dataclass
class Attempt:
    when: datetime
    channel: str  # "citofono", "telefono", "cartello", "database"
    outcome: str  # "no_risposta", "rifiuto", "conversazione", "richiamare"
    notes: str = ""


@dataclass
class Qualification:
    motivo: Optional[str] = None
    tempi: Optional[str] = None
    prezzo_atteso: Optional[str] = None
    jtbd: Optional[str] = None  # es. "confusione_valore", "paura_errori", ...


@dataclass
class Contact:
    id: str
    nome: str = ""
    telefono: str = ""
    indirizzo: str = ""
    stage: Stage = Stage.NUOVO
    attempts: List[Attempt] = field(default_factory=list)
    qualification: Qualification = field(default_factory=Qualification)
    postpone_count: int = 0
    pause_until: Optional[datetime] = None
    discarded_reason: Optional[str] = None


class DisciplineError(Exception):
    pass


class ProcedureController:
    def __init__(self):
        self.contacts: Dict[str, Contact] = {}

    def add_contact(self, c: Contact):
        self.contacts[c.id] = c

    def log_attempt(self, contact_id: str, channel: str, outcome: str, notes: str = ""):
        c = self._get(contact_id)
        c.attempts.append(Attempt(datetime.now(), channel, outcome, notes))

        if outcome == "conversazione" and c.stage == Stage.NUOVO:
            c.stage = Stage.CONTATTATO

    def set_qualification(self, contact_id: str, motivo: str, tempi: str,
                          prezzo_atteso: str, jtbd: str):
        c = self._get(contact_id)
        c.qualification = Qualification(
            motivo=motivo,
            tempi=tempi,
            prezzo_atteso=prezzo_atteso,
            jtbd=jtbd
        )
        c.stage = Stage.QUALIFICATO

    def schedule_appointment(self, contact_id: str, when: datetime):
        c = self._get(contact_id)
        self._assert_can_schedule(c)
        c.stage = Stage.APPUNTAMENTO_FISSATO

    def mark_postponed(self, contact_id: str, reason: str = ""):
        c = self._get(contact_id)
        c.postpone_count += 1

        if c.postpone_count >= 3:
            c.stage = Stage.PAUSA
            c.pause_until = datetime.now() + timedelta(days=14)

    def discard(self, contact_id: str, reason: str):
        c = self._get(contact_id)
        c.stage = Stage.SCARTATO
        c.discarded_reason = reason

    def daily_kpi(self, day: datetime) -> Dict[str, int]:
        start = datetime(day.year, day.month, day.day)
        end = start + timedelta(days=1)

        attempts = conversations = appointments = 0

        for c in self.contacts.values():
            for a in c.attempts:
                if start <= a.when < end:
                    attempts += 1
                    if a.outcome == "conversazione":
                        conversations += 1
            if c.stage == Stage.APPUNTAMENTO_FISSATO:
                appointments += 1

        return {
            "attempts": attempts,
            "conversations": conversations,
            "appointments": appointments
        }

    def _assert_can_schedule(self, c: Contact):
        q = c.qualification
        missing = [k for k, v in {
            "motivo": q.motivo,
            "tempi": q.tempi,
            "prezzo_atteso": q.prezzo_atteso,
            "jtbd": q.jtbd
        }.items() if not v]

        if missing:
            raise DisciplineError(
                f"Non puoi fissare appuntamento, mancano: {', '.join(missing)}"
            )

        if c.stage not in {Stage.CONTATTATO, Stage.QUALIFICATO}:
            raise DisciplineError(
                f"Stato attuale {c.stage}, avanzamento non consentito"
            )

    def _get(self, contact_id: str) -> Contact:
        if contact_id not in self.contacts:
            raise KeyError("Contatto non trovato")
        return self.contacts[contact_id]
