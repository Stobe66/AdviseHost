# Kalenterikooste-botti (Python)

Tämä pieni agentti hakee kalenterisi iCal‑syötteestä seuraavien N päivän tapaamiset ja lähettää niistä koosteen sähköpostilla. Projekti on tarkoitettu helppoon käyttöönottoon GitHub Actions -työnkululla.

Ominaisuudet
- Lukee iCal (.ics) -syötteen URL:stä
- Koostaa tapahtumat seuraaville DAYS_AHEAD päiville (oletus 2)
- Lähettää koosteen sähköpostilla SMTP:llä
- GitHub Action: ajettava manuaalisesti (workflow_dispatch) tai cronilla (suositus: kerran päivässä)

Aloitus
1. Varmista, että repository Stobe66/AdviseHost on olemassa ja että sinulla on kirjoitusoikeudet siihen.
2. Lisää GitHub‑repoon seuraavat Secrets (Settings → Secrets and variables → Actions):
   - ICAL_URL (esim. read‑only ics URL)
   - SMTP_HOST (Outlook: smtp.office365.com)
   - SMTP_PORT (esim. 587)
   - SMTP_USER (esim. ntuomas@hotmail.com)
   - SMTP_PASS (SMTP‑salasana / app‑specific password)
   - EMAIL_FROM (esim. ntuomas@hotmail.com)
   - EMAIL_TO (mihin haluat koosteen)
   - DAYS_AHEAD (valinnainen, oletus 2)
   - TZ (valinnainen, esim. Europe/Helsinki; oletus UTC)

3. Puskaa tiedostot repoon (main‑haaraan tai luo branch agent/setup).

4. Käynnistä GitHub Action manuaalisesti (Actions → Kalenterikooste‑botti → Run workflow) tai odota ajastettua ajoa.

Paikallinen ajo (testaus)
- Luo virtuaaliympäristö ja asenna riippuvuudet:
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

- Aseta ympäristömuuttujat (tai käytä .env.example) ja aja:
  python src/main.py

Muuta integraatiota
- Voimme vaihtaa iCal → Google Calendar tai käyttää Microsoft Graph (suositeltu, jos Outlook‑tilissäsi on MFA). Kerro jos haluat OAuth‑pohjaisen variantin.

Turvallisuus
- Älä tallenna salaisuuksia lähdekoodiin. Lisää GitHub Secrets‑asetukset.
- Jos käytät Outlook‑tiliä ja MFA:ta, käytä app‑specific passwordia tai Microsoft Graph API:a.