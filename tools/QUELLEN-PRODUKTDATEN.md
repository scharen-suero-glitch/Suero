# Registro interno — Fuentes de datos de producto (E-Roller + E-Minicar)

Este archivo no está enlazado desde ninguna página pública y está bloqueado para
buscadores en `robots.txt` (`Disallow: /tools/`). Es un registro de trabajo, no
contenido del sitio.

## Qué se pidió (ronda 2026-10-26)

Usar https://thescootercompany.ch (proveedor) como referencia para verificar y
enriquecer las fichas de producto existentes, sin copiar texto ni mezclar
especificaciones de versiones distintas, y sin tocar precios/garantías propias
de E-Suero.

## Estado del acceso al proveedor

**Bloqueado — no se pudo verificar ningún modelo contra la fuente primaria.**

- Intentos directos desde este entorno: `curl` vía proxy → `403 connect_rejected`
  (política de red); `WebFetch` → `ENOTFOUND` (fallo de DNS). Repetido dos veces
  en momentos distintos, incluso después de que el usuario intentara ampliar el
  acceso de red del entorno.
- El usuario confirmó que **tampoco puede abrir el sitio desde su propio
  navegador**, fuera de esta sesión.
- `WebSearch` sí encontró el sitio indexado (confirma que existe y que vende
  los mismos modelos: TSC NEXT ONE NX1 7i, CityFlizzer TSC, e-Minicar 25 km/h
  Lithium Edition), pero solo como fragmentos de resumen de un motor de
  búsqueda — **no se usó como fuente de specs** porque no permite confirmar con
  precisión qué versión/batería/velocidad corresponde a cada dato (justo el
  riesgo de mezcla que se pidió evitar).
- Resultado: ningún valor técnico (velocidad, batería, autonomía, dimensiones,
  colores, accesorios, homologación) fue modificado ni añadido a partir del
  proveedor. Todos los `spec` siguen siendo exactamente los que ya estaban
  publicados y verificados en una ronda anterior del proyecto.

## Qué se hizo en su lugar

Con los datos técnicos existentes (ya verificados, sin cambios), se redactó
contenido original en alemán suizo para cada modelo: `seo_title`,
`meta_description`, `lead_text`, `marketing_intro`, `marketing_body` — en
`tools/eroller_catalog.py` y `tools/minicar_catalog.py`. Ningún texto nuevo
afirma un dato técnico, de homologación o legal que no estuviera ya en el
campo `spec` existente del mismo producto.

## Por modelo: fuente consultada y pendientes

| Modelo (slug) | Fuente del proveedor | Pendiente de confirmar |
|---|---|---|
| tsc-next-one-nx1-7i | No accesible | Ninguno nuevo — specs sin cambios |
| tsc-next-one-nx1-7i-45 | No accesible | Ninguno nuevo — specs sin cambios |
| next-nx1 | No accesible | Ninguno nuevo — specs sin cambios |
| cityflizzer-tsc | No accesible | Ninguno nuevo — specs sin cambios |
| next-nx-plus | No accesible | **Redacción de Führerschein "M ab 14 / ab 16 nicht erforderlich" marcada con "laut Hersteller-Unterlagen" en el nuevo texto — recomendable reconfirmar la categoría M con el proveedor o la autoridad cantonal cuando el sitio vuelva a estar accesible.** |
| chopper-6-0-pro | No accesible | Ninguno nuevo — specs sin cambios |
| fatbob-pro | No accesible | Ninguno nuevo — specs sin cambios |
| next-nx-plus-45 | No accesible | Ninguno nuevo — specs sin cambios |
| next-nx1-45 | No accesible | Ninguno nuevo — specs sin cambios |
| fantic-issimo-city-escooter-l1 | No accesible | El nuevo texto menciona que Fantic es un fabricante italiano — hecho de marca de conocimiento general, no verificado contra el proveedor esta ronda. No afecta specs del vehículo. |
| chopper-6-0-pro-45 | No accesible | Ninguno nuevo — specs sin cambios |
| next-one-tsc-e-minicar (E-Minicar, 25 km/h) | No accesible | Precio y foto ya resueltos (2026-10-26, ver abajo). |
| next-one-tsc-e-minicar-10-20 (E-Minicar, 10/20 km/h) | No accesible | **Nuevo modelo, creado 2026-10-26 a partir de datos dados por el dueño — nunca verificado contra el proveedor.** Ver contradicción de Motorleistung abajo. |

## Actualización 2026-10-26 (sesión posterior): fotos, precio y segundo modelo de E-Minicar

- **Colores con foto real añadidos**: Rot Burgund, Dunkelblau, Hellblau — archivos recibidos como
  adjuntos reales. El dueño mencionó 3 colores más (Antrazit, Schwarz Glanz, Weiss): Antrazit y
  Schwarz Glanz se pegaron directamente en el chat pero, igual que la primera vez con la foto roja,
  no quedaron guardados como archivo en este entorno; Weiss nunca se envió. **No publicados —
  pendientes de recibir como archivo adjunto real.**
- **Precio añadido**: el dueño indica que el precio de lista era CHF 11'990.00 y ahora es
  CHF 9'990.00 (ahorro de CHF 2'000.00) para ambos modelos de E-Minicar. Dato comercial propio de
  E-Suero, no una afirmación técnica — tomado tal cual, sin verificar contra el proveedor.
- **Segundo modelo creado**: "NEXT ONE TSC e-Minicar 10/20 km/h Lithium Edition"
  (slug `next-one-tsc-e-minicar-10-20`), a partir de la ficha de datos que dio el dueño en el chat.
  **Contradicción sin resolver, marcada con nota † en la página**: el dueño dio "Motorleistung:
  1500 Watt" para este modelo, pero en el mismo mensaje pegó el texto de clasificación vehicular
  suiza "«Leicht-Motorfahrräder» bis 500 Watt Motorleistung oder max. 25 km/h". Esas dos cifras no
  coinciden. No elegí una por mi cuenta — publiqué los 1500 Watt (el dato específico del producto)
  con una nota al pie pidiendo confirmación, y no usé la frase de clasificación como badge o hecho
  confirmado en ningún lugar de la página.
- Añadido `stripe/catalog-minicar.php` (lista blanca de precios de Stripe para E-Minicar, generada
  con el nuevo `tools/gen_stripe_catalogs.py`) y registrado en
  `stripe/create-checkout-session.php`, ya que ambos modelos de Minicar ahora tienen botón de
  compra real con Stripe (antes mostraban "Preis auf Anfrage" y no lo necesitaban).

## Siguiente paso recomendado

Cuando `thescootercompany.ch` vuelva a ser accesible (desde este entorno o
desde el navegador del usuario), repetir la verificación ficha por ficha,
anotando aquí la URL exacta consultada por modelo y cualquier discrepancia
encontrada antes de publicar cambios de datos técnicos.
