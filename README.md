# Bonenfabriek Klantenservice Agent

AI-gestuurde klantenservice-agent voor Bonenfabriek, een fictieve Nederlandse webshop voor koffiebonen. De agent beoordeelt binnenkomende klantberichten en bepaalt of hij ze zelf kan beantwoorden of moet doorsturen naar een medewerker.

## Werking

De agent stuurt elk klantbericht naar Claude (Anthropic), samen met een kennisbank over verzending, retours, betaalmethoden, kwaliteit, maalmogelijkheden en openingstijden. Claude retourneert altijd een gestructureerd JSON-antwoord:

```json
{
  "antwoord": "Antwoord aan de klant in diens taal",
  "bron_sectie": "Verzending",
  "actie": "beantwoorden",
  "reden": "Interne toelichting voor de medewerker",
  "samenvatting_voor_mens": "Korte samenvatting voor de menselijke medewerker"
}
```

**`actie`** heeft altijd één van twee waarden:
- `beantwoorden` — de agent beantwoordt de vraag direct vanuit de kennisbank
- `doorsturen` — de medewerker neemt het over (boze klant, terugbetaling, juridische dreiging, prompt-injectie, onderwerp buiten kennisbank, enz.)

## Projectstructuur

```
bonenfabriek-agent/
├── agent.py              # Hoofdlogica: Claude-aanroep + structured output
├── run_tests.py          # Testrunner (25 gevallen)
├── data/
│   └── kennisbank.md     # Kennisbank met 6 secties
└── tests/
    └── cases.json        # 25 testgevallen
```

## Installatie

```bash
python3 -m venv venv
source venv/bin/activate
pip install anthropic pydantic
```

## Gebruik

Stel eerst je Anthropic API key in:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Interactief testen:**

```bash
python agent.py
```

**Volledige testsuite draaien:**

```bash
python run_tests.py
```

## Testsuite

25 testgevallen verdeeld over:

| Categorie | Aantal | Verwachte actie |
|---|---|---|
| Normale klantvragen (verzending, betaling, retour, …) | 13 | `beantwoorden` |
| Boze klant, terugbetaling, juridische dreiging | 5 | `doorsturen` |
| Prompt-injectie pogingen | 3 | `doorsturen` |
| Off-topic / buiten kennisbank | 4 | `doorsturen` |

Laatste testresultaat: **25/25**

## Veiligheidsregels

De systeemprompt bevat onveranderlijke regels die niet door klantberichten kunnen worden overschreven:

- Antwoordt uitsluitend op basis van de kennisbank
- Detecteert en blokkeert prompt-injectie (ook verstopt in gewone vragen)
- Belooft nooit terugbetalingen of verzint geen beleid
- Antwoordt in de taal van de klant (NL, EN, FR, …)
