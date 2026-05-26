# LinkedIn Mutual Connections Automation

Selenium-based automation that finds and lists **mutual connections** between you and a target LinkedIn profile — useful for warm-intro mapping and lead enrichment.

## How it works

`main.py` orchestrates the Selenium flow; `mutual.py` contains the mutual-connection extraction logic.

1. Authenticates to LinkedIn with your account
2. Navigates to a target profile or list of targets
3. Opens the "Mutual connections" view
4. Scrapes the visible mutual contacts and their basic profile metadata

## Quick start

```bash
pip install -r requirements.txt
python main.py
```

> ⚠️ Update `credentials.json` with your own login details. **Never commit real credentials** — keep them in a local file that's `.gitignore`d.

> ⚠️ Selenium needs a ChromeDriver matching your installed Chrome version. The bundled `chromedriver.exe` may be outdated.

## Files

```
Automation_LinkedInMutualConnections/
├── main.py              # Entry point / Selenium driver
├── mutual.py            # Mutual-connection extraction
├── credentials.json     # Placeholder for your LinkedIn login (DO NOT COMMIT REAL CREDS)
├── chromedriver.exe     # Selenium driver
└── requirements.txt
```

## Notes

- Personal-use scripting tool. Respect LinkedIn's terms of service and rate-limit aggressively.
- LinkedIn changes its DOM frequently; selectors in `mutual.py` may need updating.

## License

Portfolio / research project.
