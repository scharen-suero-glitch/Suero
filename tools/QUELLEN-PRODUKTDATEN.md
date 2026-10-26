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
| next-one-tsc-e-minicar (E-Minicar) | No accesible | Sigue pendiente: foto real del producto y precio real (ver tareas anteriores). Specs sin cambios. |

## Siguiente paso recomendado

Cuando `thescootercompany.ch` vuelva a ser accesible (desde este entorno o
desde el navegador del usuario), repetir la verificación ficha por ficha,
anotando aquí la URL exacta consultada por modelo y cualquier discrepancia
encontrada antes de publicar cambios de datos técnicos.
