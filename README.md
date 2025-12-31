# Sistema Unico (Control Center + Checklist + Manager + Feedback)

## Cos’è
È una web-app **in un solo file HTML**, che funziona **anche offline**, pensata per trasformare il lavoro quotidiano in:
- routine semplice (cosa fare oggi)
- spunte (esecuzione)
- numeri (KPI)
- stima soldi (pipeline €)
- feedback serale obbligatorio (miglioramento continuo)

I dati vengono salvati sul dispositivo (browser) tramite **localStorage**.

---

## Cosa fa (in pratica)
Il programma ha 3 sezioni principali + 1 blocco automatico serale:

### 1) HOME – Control Center
Serve per impostare (una volta):
- **Nome** (solo per visualizzazione)
- **WhatsApp** (apertura rapida)
- **Link ChatGPT** (apertura rapida)

Da qui puoi aprire velocemente WhatsApp e ChatGPT.

---

### 2) OGGI – Checklist giornaliera
Ogni giorno trovi:
- **Agenda del giorno** (focus e 2 azioni guida)
- **Checklist di 6 azioni** da spuntare:
  1. Pubblicato 1 video
  2. Inseriti contatti nuovi (numero)
  3. Fatti follow-up/richiami (numero)
  4. Parlato con 1 proprietario (sì/no)
  5. Fissato un prossimo passo (sì/no)
  6. Aggiornato i numeri (sì/no)

Obiettivo: fare **almeno 4 su 6**.

Include anche:
- **Modalità Emergenza** (quando sei stanco): compila automaticamente il minimo vitale (azioni base).
- Sezione “Soldi” opzionale: imposti
  - **Conversazioni per 1 incarico**
  - **€ medi per 1 incarico**
  e il sistema calcola una **stima €** basata sulle conversazioni.

---

### 3) MANAGER – KPI + Soldi
Mostra:
- KPI del mese (video, contatti, follow-up, conversazioni, prossimi passi, giornate OK)
- Barre di avanzamento (target medi)
- Stima incarichi e **pipeline €**
- Target mensili (target € e target incarichi)
- Indicazioni testuali su cosa migliorare (es. “serve fissare date/ore”)

---

## Feedback obbligatorio alle 18:30 (blocco)
Alle **18:30** (ora locale):
- compare un popup: **“Come ti sei trovato oggi?”**
- devi rispondere con:
  - valutazione 1–5 (obbligatoria)
  - cosa migliorare domani (testo)
  - blocco principale (opzionale)

Finché non rispondi:
- il programma resta **bloccato sulle modifiche** (soft lock)
- puoi comunque **leggere** tutto
- il blocco **rimane anche il giorno dopo** finché non invii il feedback

---

## Come vengono salvati i dati
Tutto viene salvato nel browser del dispositivo:
- Profilo: `cc_profile_v1`
- KPI/Log giornaliero: `roadmap_kpi_v1`
- Feedback giornaliero: `daily_feedback_YYYY-MM-DD`

⚠️ Nota: se cancelli i dati del browser, perdi lo storico.

---

## Per chi è pensato
Per chi vuole:
- una routine ripetitiva “senza pensare”
- fare attività ogni giorno e trasformarle in KPI
- migliorare settimana dopo settimana con feedback serale
- avere una stima concreta di pipeline e obiettivi

---

## Limitazioni (importante)
- Non è un sistema multi-utente “centralizzato”: ogni persona ha i dati sul proprio dispositivo.
- Il blocco è “interno alla pagina”: chi è tecnico può bypassare cancellando storage.
- Per un blocco “inviolabile” e team multi-utente serve un backend (login + database).

---

## Come usare (super rapido)
1. Apri il file HTML nel browser
2. Vai su **HOME** e salva il profilo
3. Ogni giorno usa **OGGI** e spunta
4. 1–2 volte a settimana controlla **MANAGER**
5. Alle 18:30 rispondi al popup feedback per sbloccare
