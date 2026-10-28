"""Erzeugt fotorealistische Bilder über die Hugging Face Inference API.

Beispiele:
    python generate.py --prompt "Porträt einer alten Fischerin, Nebel, 85mm"
    python generate.py --preset portrait
    python generate.py --all-presets

Benötigt die Umgebungsvariable HF_TOKEN (https://huggingface.co/settings/tokens).
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from huggingface_hub import InferenceClient

DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"
PRESETS_FILE = Path(__file__).parent / "prompts" / "presets.yaml"
OUTPUT_DIR = Path(__file__).parent / "outputs"

# Wird an jeden Prompt angehängt, sofern nicht --no-boost gesetzt ist.
REALISM_BOOST = (
    "photorealistic, shot on a full-frame DSLR, natural lighting, "
    "realistic skin texture, fine detail, shallow depth of field, "
    "subtle film grain, true-to-life colors"
)


def load_presets() -> dict:
    with PRESETS_FILE.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def slugify(text: str, max_len: int = 40) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len] or "bild"


def generate(client, prompt, negative_prompt, width, height, steps, guidance, seed, model):
    kwargs = {"model": model, "width": width, "height": height}
    if steps:
        kwargs["num_inference_steps"] = steps
    if guidance is not None:
        kwargs["guidance_scale"] = guidance
    if seed is not None:
        kwargs["seed"] = seed
    # FLUX ignoriert Negativ-Prompts; SDXL-Modelle nutzen sie.
    if negative_prompt and "flux" not in model.lower():
        kwargs["negative_prompt"] = negative_prompt
    return client.text_to_image(prompt, **kwargs)


def save(image, prompt, meta, name):
    OUTPUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    base = OUTPUT_DIR / f"{stamp}-{slugify(name)}"
    image.save(base.with_suffix(".png"))
    # Prompt und Parameter neben dem Bild speichern, damit Ergebnisse reproduzierbar sind.
    base.with_suffix(".json").write_text(
        json.dumps({"prompt": prompt, **meta}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return base.with_suffix(".png")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt", help="Eigener Prompt (am besten auf Englisch)")
    source.add_argument("--preset", help="Name eines Presets aus prompts/presets.yaml")
    source.add_argument("--all-presets", action="store_true", help="Alle Presets nacheinander erzeugen")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--steps", type=int, default=None, help="Inferenzschritte (FLUX schnell: 4)")
    parser.add_argument("--guidance", type=float, default=None)
    parser.add_argument("--seed", type=int, default=None, help="Fester Seed für reproduzierbare Bilder")
    parser.add_argument("--negative", default="", help="Negativ-Prompt (nur für SDXL u. ä.)")
    parser.add_argument("--no-boost", action="store_true", help="Realismus-Zusatz nicht anhängen")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        sys.exit("Fehler: HF_TOKEN ist nicht gesetzt. Siehe README, Abschnitt 'Einrichtung'.")
    # Tokens ohne 'hf_' hält huggingface_hub für Anbieter-Schlüssel und schickt sie
    # direkt an den Anbieter – das endet in einem unverständlichen 401.
    if not token.strip().startswith("hf_"):
        sys.exit("Fehler: HF_TOKEN muss mit 'hf_' beginnen. Bitte nur den reinen Token "
                 "ohne Anführungszeichen oder 'HF_TOKEN=' als Secret eintragen.")
    token = token.strip()

    presets = load_presets()
    if args.all_presets:
        jobs = [(name, p) for name, p in presets.items()]
    elif args.preset:
        if args.preset not in presets:
            sys.exit(f"Unbekanntes Preset '{args.preset}'. Verfügbar: {', '.join(presets)}")
        jobs = [(args.preset, presets[args.preset])]
    else:
        jobs = [(args.prompt, {"prompt": args.prompt})]

    client = InferenceClient(token=token)
    for name, job in jobs:
        prompt = job["prompt"].strip()
        if not args.no_boost:
            prompt = f"{prompt}, {REALISM_BOOST}"
        meta = {
            "model": args.model,
            "width": job.get("width", args.width),
            "height": job.get("height", args.height),
            "steps": args.steps,
            "guidance": args.guidance,
            "seed": args.seed,
            "negative_prompt": job.get("negative", args.negative),
        }
        print(f"→ Erzeuge '{name}' mit {args.model} …")
        image = generate(client, prompt, meta["negative_prompt"], meta["width"], meta["height"],
                         meta["steps"], meta["guidance"], meta["seed"], args.model)
        print(f"  gespeichert: {save(image, prompt, meta, name)}")


if __name__ == "__main__":
    main()
