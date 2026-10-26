# -*- coding: utf-8 -*-
"""Canonical E-Minicar product data.

Real product photos supplied by the site owner, resized to the site's
standard 1200x800, otherwise unaltered. Note: unlike every other product
photo on the site (plain white studio background, no text), these have a
grey studio background and "E-SUERO / www.e-suero.ch / NEXT ONE e-Minicar"
baked into the image — flagged to the owner as a style mismatch, kept as
supplied since they're the only real photos available.

Colors: the owner named 6 colors (Rot Burgund, Dunkelblau, Antrazit,
Schwarz Glanz, Hellblau, Weiss). 5 now have real, usable photo files
(Rot Burgund, Dunkelblau, Hellblau added 2026-10-26; Antrazit and
Schwarz Glanz added later the same day as real file attachments — an
earlier attempt to send them pasted inline in chat never landed as a
real file in this environment, same limitation hit with the first
photo). Only Weiss remains unsent — do not add it until a real image
file arrives.

Pricing (2026-10-26): owner states list price was CHF 11'990.00, now
CHF 9'990.00 (CHF 2'000.00 off) for both models below — not independently
verified against the supplier, taken as given since it's E-Suero's own
commercial/selling price, not a technical claim.

Second model (10/20 km/h) added 2026-10-26: owner-supplied spec sheet.
FLAGGED CONTRADICTION, not resolved here — owner states Motorleistung
"1500 Watt" for this model, but also pasted the Swiss vehicle-category
description "«Leicht-Motorfahrräder» bis 500 Watt Motorleistung oder
max. 25 km/h" in the same message. These two figures don't match; the
500-Watt figure may be a regulatory class cap rather than this specific
motor's rating, but that is a guess — needs owner confirmation before
any classification label built on it is published anywhere."""

PRODUCTS = [
    {
        "id": "p-next-one-tsc-e-minicar",
        "slug": "next-one-tsc-e-minicar",
        "name": "NEXT ONE TSC e-Minicar 25 km/h Lithium Edition",
        "badges": ["25 km/h", "Führerschein laut Lieferant: Kat. M"],
        "voltage": "60 Volt",
        "colors": ["Rot Burgund", "Dunkelblau", "Antrazit", "Schwarz Glanz", "Hellblau"],
        "color_imgs": {
            "Rot Burgund": "eminicar-next-one-tsc-rot-burgund.jpg",
            "Dunkelblau": "eminicar-next-one-tsc-dunkelblau.jpg",
            "Antrazit": "eminicar-next-one-tsc-antrazit.jpg",
            "Schwarz Glanz": "eminicar-next-one-tsc-schwarz-glanz.jpg",
            "Hellblau": "eminicar-next-one-tsc-hellblau.jpg",
        },
        "color_hex": {
            "Rot Burgund": "#7a1a24", "Dunkelblau": "#1c3a5e", "Antrazit": "#4b4e52",
            "Schwarz Glanz": "#0d0d0d", "Hellblau": "#a9c6de",
        },
        "price_rappen": 999000,
        "price_before_rappen": 1199000,
        "variants": [],
        "seo_title": "NEXT ONE TSC e-Minicar 25 km/h kaufen | E-Suero Freienbach",
        "meta_description": "NEXT ONE TSC e-Minicar 25 km/h Lithium Edition bei E-Suero Freienbach: Lithium-Akku, Hill Assist, bis 140 km Reichweite laut Hersteller. Jetzt CHF 9'990.00 statt CHF 11'990.00.",
        "lead_text": "Geschlossenes Elektrofahrzeug mit Lithium-Akku statt Blei-Akku, Hill Assist und Komfort-Ausstattung ab Werk — für Wetterschutz im Alltag ohne grossen Aufwand.",
        "marketing_intro": (
            "Ob zum Einkaufen, für einen Besuch bei Freunden oder für die täglichen Wege: Der "
            "NEXT ONE TSC e-Minicar mit 25 km/h verbindet einfache Bedienung mit moderner "
            "Elektromobilität."
        ),
        "marketing_body": (
            "Der NEXT ONE TSC setzt auf einen leistungsstarken Lithium-Akku statt Blei-Akkus — "
            "eine praktische Möglichkeit, Ihre Alltagswege elektrisch und selbstständig "
            "zurückzulegen. Die überarbeitete Ausführung überzeugt mit Facelift und neu "
            "gestaltetem Frontaufbau. Der Hill Assist unterstützt Sie beim Anfahren an "
            "Steigungen und sorgt für zusätzlichen Komfort im Alltag."
        ),
        "range_disclaimer": (
            "Bis zu 140 km Reichweite laut Hersteller: abhängig von Ausführung, Temperatur, "
            "Fahrweise, Zuladung und Strecke."
        ),
        "spec": [
            ("Garantie", "2 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 140 km"),
            ("Höchstgeschwindigkeit", "25 km/h"),
            ("Motorleistung", "2000 Watt"),
            ("Akkukapazität / Typ", "104 Ah / Lithium"),
            ("Akkuleistung", "60 Volt"),
            ("Ladezeit", "6 Std. mit 10-Ah-Schnellladegerät*"),
            ("Maximale Steigung", "20 Grad"),
            ("Gewicht", "199 kg"),
            ("Nutzlast", "250 kg"),
            ("Länge / Breite / Höhe", "2120 / 970 / 1150 mm"),
            ("Bremsen vorne und hinten", "Hydraulische Scheibenbremsen"),
            ("Bordelektronik", "Bluetooth-MP3-Radio, Freisprechanlage"),
            ("Alarmanlage & Hill Assist", "Serienmässig"),
            ("Elektrische Fensterheber", "Serienmässig"),
            ("Parksensoren & Rückfahrkamera", "Serienmässig"),
            ("Führerschein", "Laut Lieferant ab 14 Jahren mit Mofaführerschein (Kat. M)**"),
            ("Kontrollschild / Fahrzeugausweis", "Laut Lieferant erforderlich"),
            ("Zubehör", "Winterreifen"),
        ],
        "footnotes": [
            "* Ladezeit mit dem mitgelieferten/empfohlenen 10-Ah-Schnellladegerät; Angabe des Lieferanten.",
            "** Führerschein- und Zulassungsanforderungen gemäss Angabe des Lieferanten — bitte vor dem "
            "Kauf persönlich mit uns bestätigen, da dies je nach Kanton und aktueller Gesetzgebung abweichen kann.",
        ],
    },
    {
        "id": "p-next-one-tsc-e-minicar-10-20",
        "slug": "next-one-tsc-e-minicar-10-20",
        "name": "NEXT ONE TSC e-Minicar 10/20 km/h Lithium Edition",
        "badges": ["10/20 km/h", "Führerschein laut Lieferant: Nicht erforderlich"],
        "voltage": "60 Volt",
        "colors": ["Rot Burgund", "Dunkelblau", "Antrazit", "Schwarz Glanz", "Hellblau"],
        "color_imgs": {
            "Rot Burgund": "eminicar-next-one-tsc-rot-burgund.jpg",
            "Dunkelblau": "eminicar-next-one-tsc-dunkelblau.jpg",
            "Antrazit": "eminicar-next-one-tsc-antrazit.jpg",
            "Schwarz Glanz": "eminicar-next-one-tsc-schwarz-glanz.jpg",
            "Hellblau": "eminicar-next-one-tsc-hellblau.jpg",
        },
        "color_hex": {
            "Rot Burgund": "#7a1a24", "Dunkelblau": "#1c3a5e", "Antrazit": "#4b4e52",
            "Schwarz Glanz": "#0d0d0d", "Hellblau": "#a9c6de",
        },
        "price_rappen": 999000,
        "variants": [],
        "seo_title": "NEXT ONE TSC e-Minicar 10/20 km/h kaufen | E-Suero Freienbach",
        "meta_description": "NEXT ONE TSC e-Minicar 10/20 km/h Lithium Edition bei E-Suero Freienbach: Lithium-Akku, Hill Assist, bis 150 km Reichweite laut Hersteller, führerscheinfrei. CHF 9'990.00.",
        "lead_text": "Die langsamere Zulassungsvariante des NEXT ONE TSC e-Minicar — laut Lieferant ohne Führerausweis-Pflicht, mit bis zu 150 km Reichweite.",
        "marketing_intro": (
            "Dieselbe Karosserie, eine andere Zulassung: Der NEXT ONE TSC e-Minicar mit 10/20 km/h "
            "richtet sich an alle, die laut Lieferant ohne Führerausweis unterwegs sein möchten."
        ),
        "marketing_body": (
            "Technisch teilt sich dieses Modell den Lithium-Akku, den Hill Assist und die "
            "Komfort-Ausstattung mit der 25-km/h-Ausführung, unterscheidet sich aber bei "
            "Höchstgeschwindigkeit (10 oder 20 km/h), Motorleistung und Nutzlast. Laut Lieferant "
            "ist dieses Modell ab 16 Jahren ohne Führerausweis und ohne Kontrollschild zugelassen — "
            "wir empfehlen, die genaue Einstufung vor dem Kauf persönlich mit uns zu bestätigen, da "
            "sie je nach Kanton abweichen kann."
        ),
        "range_disclaimer": (
            "Bis zu 150 km Reichweite laut Hersteller: abhängig von Ausführung, Temperatur, "
            "Fahrweise, Zuladung und Strecke."
        ),
        "spec": [
            ("Garantie", "2 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 150 km"),
            ("Höchstgeschwindigkeit", "10 oder 20 km/h"),
            ("Motorleistung", "1500 Watt†"),
            ("Akkukapazität / Typ", "104 Ah / Lithium"),
            ("Akkuleistung", "60 Volt"),
            ("Ladezeit", "6 Std. mit 10-Ah-Schnellladegerät*"),
            ("Maximale Steigung", "20 Grad"),
            ("Gewicht", "199 kg"),
            ("Nutzlast", "181 kg"),
            ("Länge / Breite / Höhe", "2120 / 970 / 1150 mm"),
            ("Bremsen vorne und hinten", "Hydraulische Scheibenbremsen"),
            ("Bordelektronik", "Bluetooth-MP3-Radio, Freisprechanlage"),
            ("Alarmanlage & Hill Assist", "Serienmässig"),
            ("Elektrische Fensterheber", "Serienmässig"),
            ("Parksensoren & Rückfahrkamera", "Serienmässig"),
            ("Führerschein", "Laut Lieferant ab 16 Jahren nicht erforderlich"),
            ("Kontrollschild / Fahrzeugausweis", "Laut Lieferant nicht erforderlich"),
            ("Optionales Zubehör", "Winterreifen"),
        ],
        "footnotes": [
            "* Ladezeit mit dem mitgelieferten/empfohlenen 10-Ah-Schnellladegerät; Angabe des Lieferanten.",
            "† Angabe des Lieferanten noch zu bestätigen: die mitgelieferte Fahrzeug-Kategorie-"
            "Beschreibung spricht von „Leicht-Motorfahrräder bis 500 Watt Motorleistung oder max. "
            "25 km/h“, während die Motorleistung dieses Modells mit 1500 Watt angegeben wurde. Diese "
            "beiden Angaben widersprechen sich — bitte vor Veröffentlichung einer Zulassungsklasse "
            "beim Lieferanten klären.",
            "Führerschein- und Zulassungsanforderungen gemäss Angabe des Lieferanten — bitte vor dem "
            "Kauf persönlich mit uns bestätigen, da dies je nach Kanton und aktueller Gesetzgebung "
            "abweichen kann.",
        ],
    },
]
