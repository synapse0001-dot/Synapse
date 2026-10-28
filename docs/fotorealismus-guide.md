# Fotorealistische Bilder prompten – der Leitfaden

KI-Bildmodelle haben Millionen echter Fotos gesehen. Fotorealismus entsteht, wenn
dein Prompt so klingt wie die Beschreibung eines **echten Fotos** – inklusive
Kamera, Licht und kleinen Unperfektheiten.

## 1. Die Prompt-Formel

```
[Motiv] + [Details] + [Umgebung] + [Licht] + [Kamera/Objektiv] + [Stil/Stimmung]
```

| Baustein | Beispiel |
|---|---|
| Motiv | `portrait of a young carpenter` |
| Details | `sawdust on his forearms, faded blue work shirt` |
| Umgebung | `in a cluttered wooden workshop` |
| Licht | `warm afternoon sunlight through a dusty window` |
| Kamera | `50mm lens, f/2.0, eye-level` |
| Stil | `documentary photography, Kodak Portra 400` |

> Tipp: Schreib Prompts auf **Englisch**. Die meisten Modelle wurden überwiegend
> mit englischen Bildbeschreibungen trainiert.

## 2. Licht ist alles

Licht entscheidet mehr über Realismus als jedes andere Wort.

- `golden hour`, `blue hour` – warmes bzw. kühles, weiches Außenlicht
- `overcast soft light` – gleichmäßig, schmeichelhaft für Haut
- `window light from the left`, `Rembrandt lighting` – klassische Porträts
- `backlit`, `rim light` – Konturen und Atmosphäre
- `harsh midday sun` – bewusst kontrastreich, wirkt sehr „echt“

## 3. Kamera-Vokabular

| Begriff | Wirkung |
|---|---|
| `16–24mm` | Weitwinkel, Landschaft, Architektur |
| `35mm` | Reportage, Street |
| `50mm` | natürlicher Blick |
| `85mm` | Porträt, sanfte Kompression |
| `100mm macro` | Produkte, Details |
| `200–600mm` | Tiere, Sport |
| `f/1.4–f/2.8` | unscharfer Hintergrund (Bokeh) |
| `f/8–f/16` | alles scharf (Landschaft) |
| `long exposure` | weiches Wasser, Lichtspuren |

Filmlooks: `Kodak Portra 400`, `Fujifilm Pro 400H`, `Cinestill 800T` (Nacht/Neon).

## 4. Unperfektheit = Realismus

Perfekte Bilder wirken künstlich. Füge kleine Makel hinzu:

- `skin pores, fine wrinkles, freckles`, `flyaway hairs`
- `subtle film grain`, `slight motion blur`
- `scratches on the table`, `dust particles in the light`
- `candid moment`, `unposed`

## 5. Was du vermeiden solltest

- **Zu viele Stilwörter** wie `8k, ultra HD, masterpiece, trending on artstation` –
  das zieht Richtung Digital-Art statt Foto.
- **Widersprüche**: `f/1.4` + `everything in sharp focus`.
- **Mehrere komplexe Personen** in einem Bild – Hände und Gesichter leiden.
- **Text im Bild** – geht mit FLUX besser, bleibt aber fehleranfällig.

## 6. Negativ-Prompts (nur SDXL & Co.)

FLUX ignoriert Negativ-Prompts. Bei Stable-Diffusion-Modellen hilft z. B.:

```
cartoon, illustration, 3d render, painting, plastic skin, oversaturated,
deformed hands, extra fingers, blurry, watermark, text
```

## 7. Systematisch üben

1. **Seed festhalten** (`--seed 42`) und nur **ein** Wort ändern – so lernst du,
   was jedes Element bewirkt.
2. Vergleiche mit und ohne Realismus-Zusatz (`--no-boost`).
3. Gleicher Prompt, verschiedene Modelle (`--model ...`).
4. Die `.json`-Datei neben jedem Bild speichert alle Parameter – gute Ergebnisse
   kannst du so jederzeit reproduzieren.

### Übungen

- [ ] Erzeuge das Preset `portrait` mit `--seed 1` und ändere nur `85mm` → `24mm`.
- [ ] Tausche im Preset `landschaft` `golden hour` gegen `overcast`.
- [ ] Schreibe einen eigenen Produkt-Prompt nach der Formel aus Abschnitt 1.
- [ ] Vergleiche `FLUX.1-schnell` mit `stabilityai/stable-diffusion-xl-base-1.0`.

## 8. Verantwortungsvoll arbeiten

- Keine täuschend echten Bilder realer Personen ohne deren Einverständnis.
- KI-Bilder bei Veröffentlichung kennzeichnen.
- Lizenz des jeweiligen Modells beachten (FLUX.1-schnell: Apache 2.0).
