# -*- coding: utf-8 -*-
"""Canonical E-Minicar product data. No price was provided for this model,
so the site shows "Preis auf Anfrage" and an "Angebot anfragen" CTA instead
of a direct-buy button — never an invented number. No real product photo
is available yet either (flagged with no_photo=True) — the site shows an
honest placeholder instead of a stock image standing in for the real car."""

PRODUCTS = [
    {
        "id": "p-next-one-tsc-e-minicar",
        "slug": "next-one-tsc-e-minicar",
        "name": "NEXT ONE TSC e-Minicar 25 km/h Lithium Edition",
        "badges": ["25 km/h", "Führerschein laut Lieferant: Kat. M"],
        "voltage": "60 Volt",
        "colors": [],
        "color_imgs": {},
        "color_hex": {},
        "price_rappen": None,
        "variants": [],
        "no_photo": True,
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
            ("Akkuspannung", "60 Volt"),
            ("Ladezeit", "6 Std. mit Schnellladegerät*"),
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
            "* Ladezeit mit dem mitgelieferten/empfohlenen Schnellladegerät; Angabe des Lieferanten.",
            "** Führerschein- und Zulassungsanforderungen gemäss Angabe des Lieferanten — bitte vor dem "
            "Kauf persönlich mit uns bestätigen, da dies je nach Kanton und aktueller Gesetzgebung abweichen kann.",
        ],
    },
]
