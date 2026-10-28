# -*- coding: utf-8 -*-
"""Used-vehicle listings — "Gebraucht & Geprüft" individual pages.

Each entry is one real physical unit, not a reusable product template.
`available` reflects actual stock: set it to False the moment a unit is
sold, which removes it from the catalog listing and flips its Offer's
`availability` away from InStock. Never leave a sold unit announced as
available.

Fields intentionally left out until confirmed (see
tools/QUELLEN-PRODUKTDATEN.md): Kilometerstand, Baujahr, bekannte Mängel,
mitgelieferte Ladegerät/Zubehör, ob das Topcase im Preis enthalten ist,
Garantie-Detailbedingungen.
"""

BRAND = "Vespino"
MODEL = "7i"
BATTERY_VOLTAGE = "48 V"
BATTERY_CAPACITY = "23 Ah"
RANGE_TEXT = "bis zu 60 km"
WARRANTY = "6 Monate"
PRICE_RAPPEN = 150000
LOCATION = "E-Suero, Freienbach SZ"

SERVICE_TEXT = "vollständiger mechanischer und elektronischer Service durchgeführt"

UNITS = [
    {
        "slug": "vespino-7i-schwarz",
        "title": "Vespino 7i Occasion – Schwarz",
        "color": "Schwarz",
        "color_hex": "#1a1a1a",
        "image": "vespino-7i-schwarz.jpg",
        "image_width": 1199,
        "image_height": 675,
        "alt": "Vespino 7i Occasion in Schwarz bei E-Suero in Freienbach",
        "available": True,
        "seo_title": "Vespino 7i Occasion Schwarz – CHF 1'500 | E-Suero",
        "meta_description": (
            "Vespino 7i Occasion in Schwarz für CHF 1'500. Mechanischer und elektronischer "
            "Service durchgeführt, 6 Monate Garantie. E-Suero in Freienbach SZ."
        ),
        "intro": (
            "Dieser gebrauchte Vespino 7i in Schwarz hat bei E-Suero einen vollständigen "
            "mechanischen und elektronischen Service erhalten. Mit einem 48-V-Akku mit 23 Ah "
            "und einer angegebenen Reichweite von bis zu 60 km bietet er elektrische Mobilität "
            "für den Alltag. Preis: CHF 1'500.– inklusive 6 Monaten Garantie."
        ),
    },
    {
        "slug": "vespino-7i-weiss",
        "title": "Vespino 7i Occasion – Weiss / roter Sitz",
        "color": "Weiss mit rotem Sitz",
        "color_hex": "#f2f2f2",
        # Topcase visible in the photo is NOT confirmed as included in the price —
        # never state it is (see tools/QUELLEN-PRODUKTDATEN.md).
        "image": "vespino-7i-weiss.jpg",
        "image_width": 1199,
        "image_height": 675,
        "alt": "Vespino 7i Occasion in Weiss mit rotem Sitz bei E-Suero in Freienbach",
        "available": True,
        "seo_title": "Vespino 7i Occasion Weiss – CHF 1'500 | E-Suero",
        "meta_description": (
            "Vespino 7i Occasion in Weiss mit rotem Sitz für CHF 1'500. Vollständiger "
            "mechanischer und elektronischer Service, 6 Monate Garantie. Freienbach SZ."
        ),
        "intro": (
            "Dieser gebrauchte Vespino 7i in Weiss mit rotem Sitz hat bei E-Suero einen "
            "vollständigen mechanischen und elektronischen Service erhalten. Er verfügt über "
            "einen 48-V-Akku mit 23 Ah und eine angegebene Reichweite von bis zu 60 km. "
            "Preis: CHF 1'500.– inklusive 6 Monaten Garantie."
        ),
    },
]
