# Synapse – Fotorealistische KI-Bilder mit GitHub

Ein Lern-Projekt: Du schreibst Prompts, **GitHub Actions** erzeugt daraus
fotorealistische Bilder über die Hugging Face Inference API und legt sie im Repo ab.
Kein eigener Rechner mit GPU nötig.

```
Prompt  →  GitHub Actions  →  Hugging Face (FLUX.1)  →  outputs/*.png
```

## Einrichtung (5 Minuten)

1. **Hugging Face Token erstellen**
   Konto auf <https://huggingface.co> anlegen → *Settings → Access Tokens* →
   *Create new token* (Typ *Fine-grained*, Berechtigung
   „Make calls to Inference Providers“).
2. **Token als GitHub-Secret hinterlegen**
   Im Repo: *Settings → Secrets and variables → Actions → New repository secret*
   Name: `HF_TOKEN`, Wert: dein Token.
3. **Fertig.**

> Hugging Face gewährt ein kleines monatliches Gratis-Kontingent für Inferenz;
> darüber hinaus fallen geringe Kosten an (siehe HF-Preisseite).

## Bilder erzeugen

### Über GitHub (empfohlen)

1. Tab **Actions** → Workflow **„Bilder generieren“** → **Run workflow**
2. Eigenen Prompt eingeben **oder** ein Preset wählen
   (`portrait`, `landschaft`, `produkt`, `strasse`, `essen`, `tier` oder `alle`)
3. Nach ca. 1 Minute liegen die Bilder in `outputs/` und als Download-Artefakt
   am Workflow-Lauf.

### Lokal

```bash
pip install -r requirements.txt
export HF_TOKEN=hf_...
python generate.py --preset portrait
python generate.py --prompt "old lighthouse on a cliff during a storm, 35mm, f/8" --seed 42
python generate.py --all-presets
```

Wichtige Optionen: `--seed`, `--width/--height`, `--model`, `--steps`,
`--negative` (nur SDXL), `--no-boost` (Realismus-Zusatz weglassen).

## Lernen

👉 **[Leitfaden: Fotorealistische Bilder prompten](docs/fotorealismus-guide.md)** –
Prompt-Formel, Licht, Kamera-Vokabular, typische Fehler und Übungen.

## Projektstruktur

| Pfad | Inhalt |
|---|---|
| `generate.py` | Skript, das Bilder über die HF Inference API erzeugt |
| `prompts/presets.yaml` | Beispiel-Prompts zum Ausprobieren und Abwandeln |
| `.github/workflows/generate-images.yml` | GitHub-Actions-Workflow |
| `docs/fotorealismus-guide.md` | Der Lern-Leitfaden |
| `outputs/` | Erzeugte Bilder + `.json` mit allen Parametern |

## Andere Modelle

Jedes Text-to-Image-Modell auf Hugging Face mit Inference-Provider-Unterstützung
funktioniert über `--model`, z. B.:

- `black-forest-labs/FLUX.1-schnell` – schnell, sehr realistisch (Standard)
- `black-forest-labs/FLUX.1-dev` – höhere Qualität, langsamer, nicht-kommerzielle Lizenz
- `stabilityai/stable-diffusion-xl-base-1.0` – klassisch, unterstützt Negativ-Prompts
