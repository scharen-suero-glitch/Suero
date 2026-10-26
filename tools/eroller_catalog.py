# -*- coding: utf-8 -*-
"""
Canonical E-Roller product data — single source of truth.
Extracted verbatim from the live fahrzeuge/e-roller.html product cards
(no invented data). Feeds: individual model pages, the Stripe
server-side price whitelist, and Product/Offer JSON-LD.

variants: list of dicts (empty list => no variant selector, single price)
spec: ordered list of (label, value) tuples, exactly as shown on-site
badges: [speed_badge, license_badge] exactly as shown on-site (drives
        catalog-tools.js's speedOf()/licenseOf() filter logic)
"""

PRODUCTS = [
    {
        "id": "p-tsc-next-one-nx1-7i",
        "slug": "tsc-next-one-nx1-7i",
        "name": "TSC Next One NX1 7i",
        "badges": ["25 km/h", "Führerschein: Nicht erforderlich"],
        "voltage": "60 Volt",
        "colors": ["Schwarz", "Silber", "Blau", "Weiss"],
        "color_imgs": {
            "Schwarz": "eroller-nx1-7i-schwarz.jpg",
            "Silber": "eroller-nx1-7i-silber.jpg",
            "Blau": "eroller-nx1-7i-blau.jpg",
            "Weiss": "eroller-nx1-7i-weiss.jpg",
        },
        "color_hex": {"Schwarz": "#1a1a1a", "Silber": "#c7c9cc", "Blau": "#2f6fd6", "Weiss": "#f2f2f2"},
        "price_rappen": 299900,
        "variants": [],
        "seo_title": "TSC Next One NX1 7i kaufen – 25 km/h, führerscheinfrei | E-Suero",
        "meta_description": "TSC Next One NX1 7i bei E-Suero Freienbach: 25 km/h ohne Führerausweis-Pflicht ab 16, 60-Volt-Akku mit Samsung-Zellen, bis 60 km Reichweite, 3 Jahre Garantie. Beratung & Probefahrt vor Ort.",
        "lead_text": "Führerscheinfrei ab 16 Jahren unterwegs: Der TSC Next One NX1 7i verbindet eine Samsung-Zellen-Batterie mit Keyless-Fernbedienung und Alarmanlage ab Werk.",
        "marketing_intro": "Alltagstauglich ohne Führerausweis-Pflicht.",
        "marketing_body": (
            "Der TSC Next One NX1 7i richtet sich an alle, die in Freienbach und Umgebung ohne Führerausweis "
            "mobil sein wollen: Mit 25 km/h bleibt er in der Schweiz ab 16 Jahren führerscheinfrei. Der 60-Volt-Akku "
            "mit Samsung-Zellen ist auf eine Reichweite von bis zu 60 km ausgelegt und in rund 5 Stunden wieder "
            "vollständig geladen. Keyless-Fernbedienung und Alarmanlage gehören serienmässig dazu, ein Rückwärtsgang "
            "ist bei diesem Modell nicht vorgesehen. Erhältlich in vier Farben — Schwarz, Silber, Blau und Weiss. "
            "Wir beraten Sie in unserem Showroom in Freienbach SZ persönlich zu Zubehör wie Zusatzakku, Winterreifen "
            "oder Topcase."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "25 km/h"),
            ("Motorleistung", "500 Watt"),
            ("Garantie", "3 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 60 km"),
            ("Akkukapazität / Typ", "20 Ah / Lithium (Samsung-Zellen)"),
            ("Akkuleistung", "60 Volt"),
            ("Ladezeit", "5 Std."),
            ("Maximale Steigung", "19°"),
            ("Gewicht", "56 kg"),
            ("Nutzlast", "215 kg"),
            ("Länge / Breite / Höhe", "168 / 67.5 / 106 cm"),
            ("Rückwärtsgang", "Nicht verfügbar"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Typengenehmigung", "EEC"),
            ("Führerschein", "Ab 16 Jahren nicht erforderlich"),
            ("Kontrollschild", "Nicht erforderlich"),
            ("Optionales Zubehör", "Zusatzakku / Winterreifen / Topcase / Handyhalter"),
        ],
    },
    {
        "id": "p-tsc-next-one-nx1-7i-45",
        "slug": "tsc-next-one-nx1-7i-45",
        "name": "TSC Next One NX1 7i 45 km/h",
        "badges": ["45 km/h", "Kat. A1"],
        "voltage": "60 Volt",
        "colors": ["Schwarz", "Silber", "Blau", "Weiss"],
        "color_imgs": {
            "Schwarz": "eroller-nx1-7i-schwarz.jpg",
            "Silber": "eroller-nx1-7i-silber.jpg",
            "Blau": "eroller-nx1-7i-blau.jpg",
            "Weiss": "eroller-nx1-7i-weiss.jpg",
        },
        "color_hex": {"Schwarz": "#1a1a1a", "Silber": "#c7c9cc", "Blau": "#2f6fd6", "Weiss": "#f2f2f2"},
        "price_rappen": 299900,
        "variants": [],
        "seo_title": "TSC Next One NX1 7i 45 km/h kaufen – Kat. A1 | E-Suero Freienbach",
        "meta_description": "TSC Next One NX1 7i 45 km/h bei E-Suero: Kat.-A1-Zulassung ab 15 Jahren, 60-Volt-Akku, bis 60 km Reichweite, 3 Jahre Garantie. Kontrollschild erforderlich — Beratung in Freienbach SZ.",
        "lead_text": "Baugleich mit dem TSC Next One NX1 7i, aber für mehr Tempo ausgelegt: Mit Kat.-A1-Zulassung erreicht dieses Modell 45 km/h — Kontrollschild und passender Führerausweis sind dafür Voraussetzung.",
        "marketing_intro": "Mehr Tempo für längere Pendelstrecken.",
        "marketing_body": (
            "Wer regelmässig längere Strecken um Freienbach, Pfäffikon SZ oder an den Zürichsee pendelt, profitiert "
            "von den zusätzlichen 20 km/h gegenüber der führerscheinfreien Basisversion. Der 60-Volt-Akku und die "
            "Karosserie sind identisch zum TSC Next One NX1 7i, die Höchstgeschwindigkeit von 45 km/h setzt jedoch "
            "die Kat.-A1-Zulassung (Unterkategorie, ab 15 Jahren) sowie ein Kontrollschild voraus. Keyless-"
            "Fernbedienung und Alarmanlage sind serienmässig an Bord. Erhältlich in Schwarz, Silber, Blau und Weiss. "
            "Wir klären die genauen Zulassungsvoraussetzungen gerne persönlich mit Ihnen in unserem Showroom in "
            "Freienbach SZ."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "45 km/h"),
            ("Motorleistung", "500 Watt"),
            ("Garantie", "3 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 60 km"),
            ("Akkukapazität / Typ", "20 Ah / Lithium (Samsung-Zellen)"),
            ("Akkuleistung", "60 Volt"),
            ("Ladezeit", "5 Std."),
            ("Maximale Steigung", "19°"),
            ("Gewicht", "56 kg"),
            ("Nutzlast", "215 kg"),
            ("Länge / Breite / Höhe", "168 / 67.5 / 106 cm"),
            ("Rückwärtsgang", "Nicht verfügbar"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Typengenehmigung", "EEC"),
            ("Führerschein", "Kat. A1 ab 15 Jahren (Unterkategorie)"),
            ("Kontrollschild / Fahrzeugausweis", "Erforderlich"),
            ("Optionales Zubehör", "Zusatzakku / Winterreifen / Topcase / Handyhalter"),
        ],
    },
    {
        "id": "p-next-nx1",
        "slug": "next-nx1",
        "name": "Next NX1",
        "badges": ["25 km/h", "Führerschein: Nicht erforderlich"],
        "voltage": "48 Volt",
        "colors": ["Schwarz", "Silber", "Blau", "Weiss"],
        "color_imgs": {
            "Schwarz": "eroller-next-nx1-schwarz.jpg",
            "Silber": "eroller-next-nx1-silber.jpg",
            "Blau": "eroller-next-nx1-blau.jpg",
            "Weiss": "eroller-next-nx1-weiss.jpg",
        },
        "color_hex": {"Schwarz": "#1a1a1a", "Silber": "#c7c9cc", "Blau": "#2f6fd6", "Weiss": "#f2f2f2"},
        "price_rappen": 299900,
        "variants": [],
        "seo_title": "Next NX1 kaufen – 25 km/h führerscheinfrei | E-Suero Freienbach",
        "meta_description": "Next NX1 bei E-Suero Freienbach: 25 km/h ohne Führerausweis-Pflicht ab 16, 48-Volt-Akku, bis 60 km Reichweite, 3 Jahre Garantie, 4 Farben. Jetzt beraten lassen oder Probefahrt anfragen.",
        "lead_text": "Der Next NX1 bringt dieselbe führerscheinfreie Alltagstauglichkeit wie der TSC Next One NX1 7i mit, ausgestattet mit einem 48-Volt-Akku.",
        "marketing_intro": "Die unkomplizierte Alternative für den täglichen Weg.",
        "marketing_body": (
            "Der Next NX1 ist baugleich zum TSC Next One NX1 7i, setzt jedoch auf einen 48-Volt-Akku. Mit 25 km/h "
            "bleibt er in der Schweiz ab 16 Jahren führerscheinfrei und eignet sich damit für den Weg zur Arbeit, "
            "zum Bahnhof oder für Besorgungen in und um Freienbach. Die Reichweite liegt bei bis zu 60 km pro "
            "Akkuladung, die Ladezeit bei rund 5 Stunden. Keyless-Fernbedienung, Alarmanlage und USB-Schnittstelle "
            "gehören serienmässig dazu. Erhältlich in Schwarz, Silber, Blau und Weiss — wir beraten Sie gerne "
            "persönlich, welche der beiden NX1-Varianten besser zu Ihrem Budget passt."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "25 km/h"),
            ("Motorleistung", "500 Watt"),
            ("Garantie", "3 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 60 km"),
            ("Akkukapazität / Typ", "20 Ah / Lithium (Samsung-Zellen)"),
            ("Akkuleistung", "48 Volt"),
            ("Ladezeit", "5 Std."),
            ("Maximale Steigung", "19°"),
            ("Gewicht", "56 kg"),
            ("Nutzlast", "215 kg"),
            ("Länge / Breite / Höhe", "168 / 67.5 / 106 cm"),
            ("Rückwärtsgang", "Nicht verfügbar"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Typengenehmigung", "EEC"),
            ("Führerschein", "Ab 16 Jahren nicht erforderlich"),
            ("Kontrollschild", "Nicht erforderlich"),
            ("Optionales Zubehör", "Zusatzakku / Winterreifen / Topcase / Handyhalter"),
        ],
    },
    {
        "id": "p-cityflizzer-tsc",
        "slug": "cityflizzer-tsc",
        "name": "CityFlizzer TSC",
        "badges": ["25 km/h", "Führerschein: Nicht erforderlich"],
        "voltage": "48 Volt",
        "colors": ["Schwarz", "Weiss"],
        "color_imgs": {"Schwarz": "eroller-cityflizzer-tsc-schwarz.jpg", "Weiss": "eroller-cityflizzer-tsc-weiss.jpg"},
        "color_hex": {"Schwarz": "#1a1a1a", "Weiss": "#f2f2f2"},
        "price_rappen": 219000,
        "variants": [
            {"label": "30 Ah · ca. 75 km", "price_rappen": 219000, "price_label": "CHF 2'190.00"},
            {"label": "60 Ah · ca. 150 km", "price_rappen": 299000, "price_label": "CHF 2'990.00"},
        ],
        "seo_title": "CityFlizzer TSC kaufen – 2 Akku-Grössen, Carplay | E-Suero",
        "meta_description": "CityFlizzer TSC bei E-Suero Freienbach: 25 km/h führerscheinfrei, wählbar mit 75 km oder 150 km Reichweite, Carplay-Display, ab CHF 2'190.00. Beratung & Probefahrt in Freienbach SZ.",
        "lead_text": "Der CityFlizzer TSC ist mit zwei Akku-Grössen erhältlich und bringt als einziges Modell im Sortiment ein Carplay-Display für Apple und Android mit.",
        "marketing_intro": "Zwei Reichweiten, ein Display für Apple und Android.",
        "marketing_body": (
            "Der CityFlizzer TSC lässt Sie zwischen zwei Akku-Grössen wählen: 30 Ah für rund 75 km oder 60 Ah für "
            "rund 150 km pro Ladung — je nachdem, wie weit Ihr Alltagsweg in und um Freienbach ist. Mit 25 km/h "
            "bleibt er in der Schweiz ab 16 Jahren führerscheinfrei. Besonderheit gegenüber den anderen Modellen "
            "im Sortiment ist das serienmässige Carplay-Display für Apple und Android. Alarmanlage und USB-"
            "Schnittstelle sind ebenfalls an Bord, erhältlich in Schwarz oder Weiss. Welche Akku-Grösse für Ihre "
            "Strecke sinnvoll ist, besprechen wir gerne persönlich in unserem Showroom."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "25 km/h"),
            ("Motorleistung", "500 Watt"),
            ("Garantie", "2 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 75 / 150 km"),
            ("Akkukapazität / Typ", "30 Ah / 60 Ah Lithium"),
            ("Akkuleistung", "48 Volt"),
            ("Ladezeit", "5 Std."),
            ("Maximale Steigung", "12°"),
            ("Gewicht", "80 kg"),
            ("Nutzlast", "150 kg"),
            ("Länge / Breite / Höhe", "174 / 66 / 100 cm"),
            ("Rückwärtsgang", "Nicht verfügbar"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Carplay Display (Apple & Android)", "Serienmässig"),
            ("Typengenehmigung", "EEC"),
            ("Führerschein", "Ab 16 Jahren nicht erforderlich"),
            ("Kontrollschild / Fahrzeugausweis", "Nicht erforderlich"),
            ("Optionales Zubehör", "Zusatzakku"),
        ],
    },
    {
        "id": "p-next-nx-plus",
        "slug": "next-nx-plus",
        "name": "Next NX Plus",
        "badges": ["25 km/h", "Führerschein: Nicht erforderlich"],
        "voltage": "72 Volt",
        "colors": ["Schwarz", "Weiss"],
        "color_imgs": {"Schwarz": "eroller-next-nxplus-schwarz.jpg", "Weiss": "eroller-next-nxplus-weiss.jpg"},
        "color_hex": {"Schwarz": "#1a1a1a", "Weiss": "#f2f2f2"},
        "price_rappen": 325000,
        "variants": [
            {"label": "25 Ah · ca. 125 km", "price_rappen": 325000, "price_label": "CHF 3'250.00"},
            {"label": "50 Ah · ca. 250 km", "price_rappen": 395000, "price_label": "CHF 3'950.00"},
        ],
        "seo_title": "Next NX Plus kaufen – 72 Volt, bis 250 km, Typengeprüft CH | E-Suero",
        "meta_description": "Next NX Plus bei E-Suero Freienbach: 72-Volt-Akku, wählbar mit 125 km oder 250 km Reichweite (2 Akkupakete), 2 Sitzplätze, in der Schweiz typengeprüft. Ab CHF 3'250.00.",
        "lead_text": "Mit 72 Volt und bis zu zwei Akkupaketen ist der Next NX Plus auf Reichweite ausgelegt — wahlweise bis 125 km oder bis 250 km, bei 2 Sitzplätzen.",
        "marketing_intro": "Für Reichweite ausgelegt, Platz für zwei.",
        "marketing_body": (
            "Der Next NX Plus setzt im Sortiment auf die höchste Akkuspannung (72 Volt) und bietet als einziges "
            "Modell zwei Sitzplätze. Mit einem Akkupaket sind bis zu 125 km Reichweite möglich, mit zwei Akkupaketen "
            "bis zu 250 km — praktisch für Pendelstrecken rund um den Zürichsee oder spontane Ausflüge ohne "
            "Zwischenladen. Der Schnelllader bringt den Akku in rund 2 Stunden auf 75 % Kapazität. Das Fahrzeug ist "
            "in der Schweiz typengeprüft; laut Hersteller-Unterlagen ist ab 14 Jahren ein Führerausweis der "
            "Kategorie M erforderlich, ab 16 Jahren entfällt die Pflicht — die genauen Voraussetzungen bestätigen "
            "wir vor dem Kauf gerne persönlich mit Ihnen. Erhältlich in Schwarz oder Weiss."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "25 km/h"),
            ("Motor Nenn- / Spitzenleistung", "1200 / 1600 Watt"),
            ("Herstellergarantie", "3 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 125 / bis 250 km mit 2 Akkupaketen"),
            ("Akkukapazität / Typ", "25 Ah / Lithium"),
            ("Akkuleistung", "72 Volt"),
            ("Ladezeit", "4 Std. (75% nach 2 Std.)"),
            ("Plätze", "2"),
            ("Gewicht", "87 kg"),
            ("Nutzlast", "151 kg"),
            ("Länge / Breite / Höhe", "1810 / 720 / 1110 mm"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Typengeprüft in CH", "Ja"),
            ("Führerschein", "M ab 14 Jahren / ab 16 nicht erforderlich"),
            ("Kontrollschild / Fahrzeugausweis", "Nicht erforderlich"),
            ("Optionales Zubehör", "Zusatzakku / Winterreifen"),
        ],
    },
    {
        "id": "p-chopper-6-0-pro",
        "slug": "chopper-6-0-pro",
        "name": "Chopper 6.0 Pro",
        "badges": ["20 km/h", "Führerschein: Nicht erforderlich"],
        "voltage": "60 Volt",
        "colors": ["Schwarz Glanz", "Schwarz Matt", "Nardograu", "Hellgrau"],
        "color_imgs": {
            "Schwarz Glanz": "eroller-chopper-glanz.jpg",
            "Schwarz Matt": "eroller-chopper-matt.jpg",
            "Nardograu": "eroller-chopper-nardograu.jpg",
            "Hellgrau": "eroller-chopper-hellgrau.jpg",
        },
        "color_hex": {"Schwarz Glanz": "#0d0d0d", "Schwarz Matt": "#2b2b2b", "Nardograu": "#4a4d4f", "Hellgrau": "#9a9c9e"},
        "price_rappen": 359000,
        "variants": [],
        "seo_title": "Chopper 6.0 Pro kaufen – Chopper-Design, führerscheinfrei | E-Suero",
        "meta_description": "Chopper 6.0 Pro bei E-Suero Freienbach: markantes Chopper-Design, 20 km/h führerscheinfrei, bis 100 km Reichweite, 60-Volt-Akku, 2 Jahre Garantie. 4 Farben zur Auswahl.",
        "lead_text": "Markantes Chopper-Design statt klassischer Roller-Optik: Der Chopper 6.0 Pro bleibt mit 20 km/h führerscheinfrei und bietet bis zu 100 km Reichweite.",
        "marketing_intro": "Chopper-Optik, führerscheinfrei unterwegs.",
        "marketing_body": (
            "Der Chopper 6.0 Pro hebt sich optisch deutlich vom klassischen Rollerbild ab: langer Radstand, "
            "markante Linienführung und ein Fahrgefühl, das an einen echten Chopper erinnert. Mit 20 km/h bleibt "
            "er in der Schweiz ab 16 Jahren führerscheinfrei. Der 60-Volt-Akku ist auf bis zu 100 km Reichweite "
            "ausgelegt, die maximale Steigfähigkeit von 23° macht ihn auch für hügeligere Strecken rund um "
            "Freienbach alltagstauglich. Keyless-Fernbedienung und Alarmanlage sind serienmässig. Erhältlich in "
            "vier Lackierungen: Schwarz Glanz, Schwarz Matt, Nardograu und Hellgrau."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "20 km/h"),
            ("Motorleistung", "500 Watt"),
            ("Reichweite (pro Akkuladung)", "bis 100 km"),
            ("Akkukapazität / Typ", "45 Ah / Lithium"),
            ("Akkuleistung", "60 Volt"),
            ("Ladezeit", "4–5 Std."),
            ("Maximale Steigung", "23°"),
            ("Gewicht", "105 kg"),
            ("Nutzlast", "195 kg"),
            ("Länge / Breite / Höhe", "2120 / 970 / 1150 mm"),
            ("Bremse vorne und hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Typengenehmigung", "EEC"),
            ("Führerschein", "Ab 16 Jahren nicht erforderlich"),
            ("Kontrollschild / Fahrzeugausweis", "Nicht erforderlich"),
            ("Optionales Zubehör", "Zusatzakku"),
            ("Garantie", "2 Jahre"),
        ],
    },
    {
        "id": "p-fatbob-pro",
        "slug": "fatbob-pro",
        "name": "Fatbob Pro",
        "badges": ["25 km/h", "Führerschein: Nicht erforderlich"],
        "voltage": "60 Volt",
        "colors": ["Schwarz Glanz", "Schwarz Matt", "Nardograu"],
        "color_imgs": {
            "Schwarz Glanz": "eroller-fatbob-schwarz.jpg",
            "Schwarz Matt": "eroller-fatbob-mattschwarz.jpg",
            "Nardograu": "eroller-fatbob-nardograu.jpg",
        },
        "color_hex": {"Schwarz Glanz": "#0d0d0d", "Schwarz Matt": "#2b2b2b", "Nardograu": "#4a4d4f"},
        "price_rappen": 349000,
        "variants": [],
        "seo_title": "Fatbob Pro kaufen – Fatbike-Look mit Tretunterstützung | E-Suero",
        "meta_description": "Fatbob Pro bei E-Suero Freienbach: 25 km/h mit Tretunterstützung, führerscheinfrei, 2000-Watt-Motor, bis 100 km Reichweite, 30° Steigfähigkeit. 3 Farben, 2 Jahre Garantie.",
        "lead_text": "Der Fatbob Pro kombiniert Fatbike-Optik mit Tretunterstützung und erreicht mit 30° die höchste Steigfähigkeit unter den führerscheinfreien Modellen im Sortiment.",
        "marketing_intro": "Fatbike-Look, kräftiger Antrieb, Tretunterstützung.",
        "marketing_body": (
            "Der Fatbob Pro verbindet die breite, geländetaugliche Optik eines Fatbikes mit einem 2000-Watt-Motor "
            "und Tretunterstützung. Mit 25 km/h bleibt er in der Schweiz ab 16 Jahren führerscheinfrei, die "
            "maximale Steigfähigkeit von 30° ist die höchste unter den führerscheinfreien Modellen unseres "
            "Sortiments — praktisch für die hügeligeren Abschnitte rund um Freienbach und den Zürichsee. Der "
            "60-Volt-Akku ist auf bis zu 100 km Reichweite ausgelegt. Keyless-Fernbedienung und Alarmanlage sind "
            "serienmässig. Erhältlich in Schwarz Glanz, Schwarz Matt oder Nardograu."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "25 km/h mit Tretunterstützung"),
            ("Motorleistung", "2000 Watt"),
            ("Garantie", "2 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 100 km"),
            ("Akkukapazität / Typ", "35 Ah / Lithium"),
            ("Akkuleistung", "60 Volt"),
            ("Ladezeit", "4–5 Std."),
            ("Maximale Steigung", "30°"),
            ("Gewicht", "105 kg"),
            ("Nutzlast", "195 kg"),
            ("Länge / Breite / Höhe", "1970 / 890 / 1100 mm"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Typengenehmigung", "EEC"),
            ("Führerschein", "Ab 16 Jahren nicht erforderlich"),
            ("Kontrollschild / Fahrzeugausweis", "Nicht erforderlich"),
            ("Optionales Zubehör", "Zusatzakku"),
        ],
    },
    {
        "id": "p-next-nx-plus-45",
        "slug": "next-nx-plus-45",
        "name": "Next NX Plus 45 km/h",
        "badges": ["45 km/h", "Kat. A1"],
        "voltage": "72 Volt",
        "colors": ["Schwarz", "Weiss"],
        "color_imgs": {"Schwarz": "eroller45-next-nxplus-schwarz.jpg", "Weiss": "eroller45-next-nxplus-weiss.jpg"},
        "color_hex": {"Schwarz": "#1a1a1a", "Weiss": "#f2f2f2"},
        "price_rappen": 325000,
        "variants": [],
        "seo_title": "Next NX Plus 45 km/h kaufen – Kat. A1, Typengeprüft CH | E-Suero",
        "meta_description": "Next NX Plus 45 km/h bei E-Suero Freienbach: Kat.-A1-Zulassung, 72-Volt-Akku, bis 90 km Reichweite, 2 Sitzplätze, in der Schweiz typengeprüft. Kontrollschild erforderlich.",
        "lead_text": "Die schnellere Ausführung des Next NX Plus: 45 km/h mit Kat.-A1-Zulassung, demselben 72-Volt-Akku und Platz für zwei Personen.",
        "marketing_intro": "Mehr Tempo, gleiche Reichweiten-Technik.",
        "marketing_body": (
            "Der Next NX Plus 45 km/h teilt sich die technische Basis mit der führerscheinfreien Version — "
            "72-Volt-Akku, 2 Sitzplätze, Schnelllader mit 75 % Kapazität nach rund 2 Stunden — erreicht aber dank "
            "Kat.-A1-Zulassung 45 km/h. Die Reichweite liegt bei bis zu 90 km pro Akkuladung. Das Fahrzeug ist in "
            "der Schweiz typengeprüft, für den Betrieb sind Kontrollschild und ein Führerausweis der Kat. A1 "
            "(Unterkategorie, ab 15 Jahren) erforderlich. Erhältlich in Schwarz oder Weiss — wir beraten Sie gerne "
            "zur passenden Zulassung in unserem Showroom in Freienbach SZ."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "45 km/h"),
            ("Motor Nenn- / Spitzenleistung", "1200 / 1600 Watt"),
            ("Typengeprüft in CH", "Ja"),
            ("Reichweite (pro Akkuladung)", "bis 90 km"),
            ("Akkukapazität / Typ", "25 Ah / Lithium"),
            ("Akkuleistung", "72 Volt"),
            ("Ladezeit", "4 Std. (75% nach 2 Std.)"),
            ("Plätze", "2"),
            ("Gewicht", "87 kg"),
            ("Nutzlast", "151 kg"),
            ("Länge / Breite / Höhe", "1810 / 720 / 1110 mm"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Führerschein", "Kat. A1 ab 15 Jahren (Unterkategorie)"),
            ("Kontrollschild / Fahrzeugausweis", "Erforderlich"),
            ("Optionales Zubehör", "Zusatzakku / Winterreifen"),
        ],
    },
    {
        "id": "p-next-nx1-45",
        "slug": "next-nx1-45",
        "name": "Next NX1 45 km/h",
        "badges": ["45 km/h", "Kat. A1"],
        "voltage": "60 Volt",
        "colors": ["Schwarz", "Grau-Silber", "Blau-Royal", "Weiss"],
        "color_imgs": {
            "Schwarz": "eroller45-next-nx1-schwarz.jpg",
            "Grau-Silber": "eroller45-next-nx1-silber.jpg",
            "Blau-Royal": "eroller45-next-nx1-blau.jpg",
            "Weiss": "eroller45-next-nx1-weiss.jpg",
        },
        "color_hex": {"Schwarz": "#1a1a1a", "Grau-Silber": "#c7c9cc", "Blau-Royal": "#2f4fa6", "Weiss": "#f2f2f2"},
        "price_rappen": 299000,
        "variants": [],
        "seo_title": "Next NX1 45 km/h kaufen – Kat. A1, 800 Watt | E-Suero Freienbach",
        "meta_description": "Next NX1 45 km/h bei E-Suero Freienbach: Kat.-A1-Zulassung, 800-Watt-Motor, 60-Volt-Akku, bis 60 km Reichweite, 2 Jahre Garantie, 4 Farben. Kontrollschild erforderlich.",
        "lead_text": "Mit stärkerem 800-Watt-Motor und 60-Volt-Akku erreicht der Next NX1 45 km/h — Kat.-A1-Zulassung und Kontrollschild vorausgesetzt.",
        "marketing_intro": "Stärkerer Motor für die Kat.-A1-Klasse.",
        "marketing_body": (
            "Der Next NX1 45 km/h setzt gegenüber den führerscheinfreien NX1-Varianten auf einen stärkeren "
            "800-Watt-Motor und einen 60-Volt-Akku mit bis zu 60 km Reichweite. Die Höchstgeschwindigkeit von "
            "45 km/h setzt eine Kat.-A1-Zulassung sowie ein Kontrollschild voraus. Keyless-Fernbedienung, "
            "Alarmanlage und USB-Schnittstelle sind serienmässig an Bord. Erhältlich in Schwarz, Grau-Silber, "
            "Blau-Royal und Weiss — eine eigene Farbpalette gegenüber den führerscheinfreien Modellen. Wir klären "
            "die Zulassungsvoraussetzungen gerne persönlich mit Ihnen vor Ort in Freienbach SZ."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "45 km/h"),
            ("Motorleistung", "800 Watt"),
            ("Garantie", "2 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 60 km"),
            ("Akkukapazität / Typ", "20 Ah / Lithium"),
            ("Akkuleistung", "60 Volt"),
            ("Ladezeit", "5 Std."),
            ("Maximale Steigung", "30°"),
            ("Gewicht", "56 kg"),
            ("Nutzlast", "215 kg"),
            ("Länge / Breite / Höhe", "168 / 67.5 / 106 cm"),
            ("Rückwärtsgang", "Nicht verfügbar"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Typengenehmigung", "EEC"),
            ("Führerschein", "Kat. A1"),
            ("Kontrollschild / Fahrzeugausweis", "Nicht erforderlich"),
            ("Optionales Zubehör", "Zusatzakku"),
        ],
    },
    {
        "id": "p-fantic-issimo-city-escooter-l1",
        "slug": "fantic-issimo-city-escooter-l1",
        "name": "Fantic Issimo City E-Scooter L1",
        "badges": ["45 km/h", "Kat. A1"],
        "voltage": "60 Volt",
        "colors": ["Blau", "Rot Fantic", "Neon Grün", "Weiss"],
        "color_imgs": {
            "Blau": "eroller45-fantic-cityscooter-blau.jpg",
            "Rot Fantic": "eroller45-fantic-cityscooter-rot.jpg",
            "Neon Grün": "eroller45-fantic-cityscooter-gruen.jpg",
            "Weiss": "eroller45-fantic-cityscooter-weiss.jpg",
        },
        "color_hex": {"Blau": "#2f4fa6", "Rot Fantic": "#b3312c", "Neon Grün": "#39c463", "Weiss": "#f2f2f2"},
        "price_rappen": 489000,
        "variants": [],
        "seo_title": "Fantic Issimo City E-Scooter L1 kaufen – 3000 Watt | E-Suero",
        "meta_description": "Fantic Issimo City E-Scooter L1 bei E-Suero Freienbach: 45 km/h, 3000-Watt-Motor, bis 140 km Reichweite, Motorrad-Bereifung, Kat. A1. Das leistungsstärkste Modell im Sortiment.",
        "lead_text": "Der Fantic Issimo City E-Scooter L1 ist mit 3000 Watt das leistungsstärkste Modell im Sortiment und läuft auf echter Motorrad-Bereifung.",
        "marketing_intro": "Die stärkste Maschine im Sortiment.",
        "marketing_body": (
            "Der Fantic Issimo City E-Scooter L1 trägt den Namen des italienischen Herstellers Fantic und ist mit "
            "3000 Watt der leistungsstärkste E-Roller in unserem Sortiment. Die Reichweite liegt je nach Akku bei "
            "bis zu 70 oder bis zu 140 km, die Bereifung entspricht mit 90/80-16 vorne und 100/80-16 hinten "
            "echtem Motorrad-Format statt klassischer Rollerreifen. Mit Kat.-A1-Zulassung erreicht er 45 km/h; "
            "Kontrollschild und ein Führerausweis der Kat. A1 (ab 15 Jahren) sind Voraussetzung. Keyless-"
            "Fernbedienung und Alarmanlage gehören serienmässig dazu. Erhältlich in Blau, Rot Fantic, Neon Grün "
            "und Weiss."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "45 km/h"),
            ("Motorleistung", "3000 Watt"),
            ("Garantie", "2 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 70 / 140 km"),
            ("Akkukapazität / Typ", "2.2 kWh / 4.4 kWh Lithium"),
            ("Akkuleistung", "60 Volt"),
            ("Ladezeit", "4–5 Std."),
            ("Maximale Steigung", "30°"),
            ("Gewicht", "79 kg + 12 kg Akku"),
            ("Bereifung vorne", "90/80-16"),
            ("Bereifung hinten", "100/80-16"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Typengenehmigung", "EEC"),
            ("Führerschein", "Kat. A1 ab 15 Jahren"),
            ("Kontrollschild / Fahrzeugausweis", "Erforderlich"),
            ("Optionales Zubehör", "Zusatzakku"),
        ],
    },
    {
        "id": "p-chopper-6-0-pro-45",
        "slug": "chopper-6-0-pro-45",
        "name": "Chopper 6.0 Pro 45 km/h",
        "badges": ["45 km/h", "Kat. A1"],
        "voltage": "60 Volt",
        "colors": ["Schwarz Glanz", "Schwarz Matt", "Nardograu", "Hellgrau"],
        "color_imgs": {
            "Schwarz Glanz": "eroller45-chopper-glanz.jpg",
            "Schwarz Matt": "eroller45-chopper-matt.jpg",
            "Nardograu": "eroller45-chopper-nardograu.jpg",
            "Hellgrau": "eroller45-chopper-hellgrau.jpg",
        },
        "color_hex": {"Schwarz Glanz": "#0d0d0d", "Schwarz Matt": "#2b2b2b", "Nardograu": "#4a4d4f", "Hellgrau": "#9a9c9e"},
        "price_rappen": 399000,
        "variants": [],
        "seo_title": "Chopper 6.0 Pro 45 km/h kaufen – Kat. A1, 2000 Watt | E-Suero",
        "meta_description": "Chopper 6.0 Pro 45 km/h bei E-Suero Freienbach: Chopper-Design, Kat.-A1-Zulassung, 2000-Watt-Motor, bis 100 km Reichweite, 2 Jahre Garantie. 4 Farben zur Auswahl.",
        "lead_text": "Dieselbe markante Chopper-Optik, aber mit einem auf 2000 Watt aufgerüsteten Motor für die Kat.-A1-Klasse mit 45 km/h.",
        "marketing_intro": "Chopper-Design mit aufgerüstetem Motor.",
        "marketing_body": (
            "Der Chopper 6.0 Pro 45 km/h teilt sich Design und Fahrwerk mit der führerscheinfreien Basisversion, "
            "setzt für die Kat.-A1-Klasse aber auf einen deutlich stärkeren 2000-Watt-Motor statt der 500 Watt der "
            "20-km/h-Variante. Der 60-Volt-Akku ist auf bis zu 100 km Reichweite ausgelegt, die maximale "
            "Steigfähigkeit liegt bei 23°. Für den Betrieb mit 45 km/h sind Kontrollschild und ein Führerausweis "
            "der Kat. A1 (Unterkategorie, ab 15 Jahren) erforderlich. Erhältlich in Schwarz Glanz, Schwarz Matt, "
            "Nardograu und Hellgrau."
        ),
        "spec": [
            ("Höchstgeschwindigkeit", "45 km/h"),
            ("Motorleistung", "2000 Watt"),
            ("Garantie", "2 Jahre"),
            ("Reichweite (pro Akkuladung)", "bis 100 km"),
            ("Akkukapazität / Typ", "45 Ah / Lithium"),
            ("Akkuleistung", "60 Volt"),
            ("Ladezeit", "4–5 Std."),
            ("Maximale Steigung", "23°"),
            ("Gewicht", "114 kg"),
            ("Nutzlast", "195 kg"),
            ("Länge / Breite / Höhe", "2120 / 970 / 1150 mm"),
            ("Bremse vorne / hinten", "Scheibenbremsen"),
            ("Fernbedienung (Keyless Drive)", "Serienmässig"),
            ("Alarmanlage", "Serienmässig"),
            ("USB-Schnittstelle", "Serienmässig"),
            ("Typengenehmigung", "EEC"),
            ("Führerschein", "Kat. A1 ab 15 Jahren (Unterkategorie)"),
            ("Kontrollschild / Fahrzeugausweis", "Erforderlich"),
            ("Optionales Zubehör", "Zusatzakku"),
        ],
    },
]

if __name__ == "__main__":
    import json, sys
    print(json.dumps(PRODUCTS, ensure_ascii=False, indent=2))
