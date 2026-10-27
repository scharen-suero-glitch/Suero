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

## Actualización 2026-10-26 (sesión posterior 2): Antrazit, Schwarz Glanz y galería de detalle

- Antrazit y Schwarz Glanz llegaron como archivos adjuntos reales esta vez (los anteriores
  intentos habían sido pegados en el chat y no quedaron guardados) — ya publicados en ambos
  modelos de E-Minicar. Solo falta Weiss, nunca enviada.
- Una tercera foto enviada en el mismo mensaje resultó ser, al comparar el archivo byte a byte,
  idéntica a la foto de Hellblau ya publicada — no se duplicó ni se contó como color nuevo.
- Nueva sección "Galerie" (Innenraum & Details) añadida a ambas fichas de E-Minicar: 5 fotos
  reales de interior/detalle (Stauraum, Türverkleidung, Cockpit, Heckansicht mit geöffneten
  Türen, Ladeanschluss), recibidas como archivos adjuntos reales. Dos fotos más (detalle de
  limpiaparabrisas y de spoiler trasero) se pegaron directamente en el chat en el mismo turno y,
  igual que antes, no quedaron guardadas como archivo — reenviadas poco después como adjuntos
  reales y ya publicadas (ver entrada siguiente).

## Actualización 2026-10-26 (sesión posterior 3): limpiaparabrisas y spoiler, reenviados

- Las 2 fotos que faltaban (Scheibenwischer/limpiaparabrisas, Heckspoiler) llegaron como archivos
  adjuntos reales esta vez — añadidas a la galería "Innenraum & Details" de ambas fichas de
  E-Minicar (ahora 7 fotos en cada una).
- Nuevo campo de catálogo `gallery_imgs` y sección correspondiente en
  `tools/model_page_lib.py` — reutilizable para cualquier producto futuro que tenga fotos de
  detalle, no solo E-Minicar.

## Actualización 2026-10-26 (sesión posterior 4): E-Minicar en la página principal + bug real encontrado

El usuario avisó de dos cosas que vio en su sitio ya desplegado:

1. **E-Minicar no aparecía en el carrusel de categorías de la página principal (index.html)** — un
   gap real de código, no un problema de despliegue: ese carrusel es independiente de la sección
   `/verkauf/` y nunca se actualizó para incluir la categoría nueva. Corregido: nueva pestaña
   "E-Minicar", nueva miniatura en el carrusel superior, y un panel nuevo con las 2 fichas reales
   (con compra funcional, verificado con Playwright). También añadido `minicar` al mapa
   `ESUERO_CAT_URLS` de `main.js` (redirección en móvil).
2. **La tarjeta de E-Minicar en `/verkauf/index.html` (sección "Kategorien") seguía mostrando
   "Foto folgt in Kürze"** — bug real confirmado: nunca se actualizó esa tarjeta concreta cuando
   llegó la foto real, aunque sí se había actualizado la ficha de categoría
   (`fahrzeuge/e-minicar.html`). Corregido con la foto real (Rot Burgund).

Revisado todo el sitio (`grep -rl "photo-pending"`) para confirmar que no quedan más tarjetas con
el placeholder pendientes de actualizar — ninguna encontrada.

`tools/model_page_lib.py`: `card_html()` ahora acepta `img_base`/`link_dir` opcionales para poder
generarse también desde páginas fuera de `fahrzeuge/` (como la portada, que está en la raíz del
sitio) sin romper las rutas relativas.

## Actualización 2026-10-26 (sesión posterior 5): lista de 6 bugs reportada por el dueño

El dueño pegó una tabla con 6 problemas encontrados en el sitio ya desplegado (aparentemente de
un revisor externo). Cada uno se verificó contra el código antes de tocar nada:

1. **Botón "Produkte entdecken" de la portada llevaba al catálogo antiguo (`#products`
   dentro de `index.html`), no a la nueva página de ventas.** Confirmado en el código.
   Corregido: ahora enlaza a `verkauf/index.html`.
2. **Ficha del TSC Next One NX1 7i: 3 años de garantía y batería de 20 Ah.** Verificado:
   estos valores existen en `tools/eroller_catalog.py` desde antes de esta sesión (ronda
   anterior del proyecto, no datos inventados ahora). **No se modificaron** — no hay forma de
   reverificarlos contra el proveedor (acceso bloqueado, ver arriba). **Pendiente: el dueño
   debe confirmar personalmente que la garantía de 3 años y los 20 Ah corresponden a la unidad
   de venta normal y no a una unidad de demostración con condiciones distintas.**
3. **"Probefahrt anfragen" llevaba al formulario pero dejaba seleccionado "Beratung".**
   Confirmado: el `<select>` nunca tenía ninguna opción marcada por defecto. Corregido: todos
   los enlaces "Probefahrt anfragen" ahora llevan un atributo que selecciona automáticamente
   "Probefahrt" al hacer clic (y "Angebot anfragen" selecciona "Angebot"), vía un pequeño script
   nuevo en `assets/js/sales-form.js`. Funciona en fichas de modelo y en `verkauf/index.html`
   (mismo página). Los botones "Probefahrt anfragen" del menú de las páginas de categoría
   (E-Roller, E-Scooter, E-Bike, E-Motorräder) que saltan a `verkauf/index.html` en otra página
   siguen sin poder preseleccionar automáticamente, porque ese salto es entre páginas distintas
   y no hay forma fiable de pasar la intención sin rediseñar ese flujo — no incluido en esta
   ronda por quedar fuera de lo reportado.
4. **En la comparación del NX1 7i se recomendaba dos veces el mismo modelo de 45 km/h.**
   Confirmado y causa encontrada: la función que elige "el modelo con el precio más parecido"
   no excluía al modelo que ya se había recomendado como variante de velocidad — cuando ambos
   coincidían en precio, salía dos veces el mismo. Corregido en `tools/model_page_lib.py`
   (`find_price_neighbor` ahora excluye explícitamente al modelo ya recomendado). Verificado:
   la ficha del NX1 7i ahora recomienda el "NX1 7i 45 km/h" (variante de velocidad) y el
   "Next NX1" (modelo de precio parecido) — dos modelos distintos.
5. **"Zurück zu Fahrzeugen" en E-Roller volvía al catálogo antiguo de la portada
   (`index.html#products`).** Confirmado. Corregido — y, por consistencia, también en las otras
   tres páginas de categoría que tenían exactamente el mismo enlace antiguo (E-Scooter, E-Bike,
   E-Motorräder): todas llevan ahora a `verkauf/index.html`.
6. **Falta un acceso directo a "Werkstatt" desde el menú comercial.** Añadido un enlace
   "Werkstatt" en el menú de escritorio y en el menú móvil de todas las páginas de venta
   (`verkauf/index.html`, las 5 páginas de categoría, y todas las fichas de modelo individuales
   vía `tools/sales_chrome.py`), separado visualmente de las categorías de vehículos. La
   separación original entre venta y taller se mantiene — esto es solo un atajo, no se mezclaron
   los menús.

Nota técnica: al automatizar la inserción del enlace "Werkstatt" con una búsqueda y reemplazo
por texto, un primer intento insertó el enlace también en el pie de página (footer) por error,
duplicándolo en 3 sitios en vez de 2 en varias páginas. Detectado inmediatamente revisando el
diff antes de continuar, y corregido a mano en los 6 archivos afectados antes de seguir.

## Actualización 2026-10-26 (sesión posterior 6): traducciones EN/IT/ES en toda la sección de ventas

El dueño reportó que el selector de idioma (DE/EN/IT/ES) no traducía nada en `verkauf/`,
`fahrzeuge/*` ni en las fichas de producto — solo un par de botones cambiaban de idioma, el
resto del texto se quedaba siempre en alemán. Confirmado: esa sección del sitio nunca tuvo
etiquetas `data-i18n`, a diferencia de `index.html` (la portada), que sí las tenía desde antes.

Se conectó y tradujo (alemán → inglés/italiano/español) prácticamente todo el texto visible de
esa sección:
- Menú, pie de página, desplegable de idioma, migas de pan, botones de compra/Probefahrt,
  bloque de confianza, formularios de contacto — en `tools/sales_chrome.py` y
  `tools/model_page_lib.py` (plantilla compartida), así que se aplica automáticamente a las 13
  fichas de producto y a cualquier ficha futura generada con el mismo sistema.
- Las ~54 etiquetas técnicas repetidas en las tablas de especificaciones (Höchstgeschwindigkeit,
  Garantie, Akkuleistung, etc.) y ~20 valores de estado comunes (Serienmässig, Nicht
  erforderlich, "2 Jahre", etc.) — detectadas automáticamente y etiquetadas en todo el sitio.
- Todo el contenido propio de `verkauf/index.html` (hero, categorías, FAQ, proceso de compra,
  showroom, formulario) y de las 5 páginas de categoría (héroe, introducción, CTA de usados).
- Los textos de marketing de los 13 productos (lead/intro/cuerpo) y las 15 fichas de
  `gebraucht-katalog.js` (4 categorías de usados + 11 modelos Xiaomi) — el texto en alemán
  (ya aprobado en rondas anteriores) se envió a traducir sin cambiar ni un dato técnico, número
  o afirmación; solo cambia el idioma.
- `gebraucht-katalog.js` (el catálogo de usados, una sola página con rutas por hash) ahora
  vuelve a dibujarse automáticamente al cambiar de idioma sin recargar la página.

**Importante**: las traducciones a inglés/italiano/español fueron generadas por IA a partir del
texto alemán ya aprobado — no son traducciones humanas certificadas. Si se van a usar para
marketing oficial o en países donde el error de traducción tiene consecuencia legal, recomiendo
que alguien con el idioma nativo las revise antes de publicarlas de forma definitiva. Los datos
técnicos, precios y garantías no se modificaron en ningún idioma — solo el texto que los rodea.

**Pendiente, fuera de esta ronda**: las frases dinámicas que el generador construye por
producto (comparación "Im Vergleich zu anderen Modellen", preguntas frecuentes por modelo,
el texto de "Was Sie vor dem Kauf wissen sollten" cuando no hay `lead_text` propio) siguen
armándose en alemán en el momento de generar la página, no vía `data-i18n` — traducirlas
requeriría reescribir esas funciones para generar las tres variantes de idioma, que no se hizo
en esta ronda. Las fichas fictícias de E-Scooter (Urban Pro X, City Cruiser, Offroad Force,
pendientes de confirmación de datos reales) también se tradujeron en el texto corto, por
consistencia, pero siguen siendo datos ficticios.

## Actualización 2026-10-27: datos estructurados (JSON-LD) corregidos tras aviso de Search Console

El dueño reportó 11 "Product" inválidos para Merchant listings en `/fahrzeuge/e-roller.html`
(error crítico: falta `image`) y el mismo problema en `/fahrzeuge/e-bike.html` y
`/fahrzeuge/e-motorraeder.html`. Diagnóstico confirmado en el código:

- Cada página de categoría incrustaba un `ItemList` con hasta 11 objetos `Product` completos
  (con `offers`) directamente en la página de catálogo — y ninguno tenía `image`. Además sus
  URL (`offers.url`) apuntaban a anclas obsoletas de la propia página de categoría
  (`#p-slug`), ni siquiera a las fichas de producto reales que ya existen.
- El campo `brand` de cada ficha individual estaba fijado siempre a `"E-Suero"` — ese es el
  vendedor, no el fabricante. Mezclar vendedor y marca es justo el tipo de dato inconsistente
  que Google penaliza.
- Existía código (nunca activado con los 13 productos reales, pero sí un riesgo latente) que
  usaba el logo del sitio como `image` cuando un producto no tenía foto — exactamente lo que
  se pidió evitar.

**Qué se corrigió:**
1. Las 5 páginas de categoría (E-Roller, E-Bike, E-Motorräder, E-Scooter, E-Minicar) ya no
   llevan `Product`/`Offer` incrustados. Ahora son `CollectionPage` + `ItemList` que solo
   enlazan a la URL real de cada ficha — sin datos de producto duplicados o inválidos en la
   página de catálogo. Para E-Roller y E-Minicar, el enlace va a la ficha individual real
   (`fahrzeuge/e-roller/<slug>.html`). Para E-Bike y E-Motorräder (que aún no tienen ficha
   propia, ver tarea pendiente #12) el enlace va a la sección correspondiente dentro de la
   misma página de categoría. E-Scooter (datos ficticios, ver tarea pendiente #13) se quedó
   sin lista de productos — no hay nada real que anunciar como producto comprable todavía.
2. Las 13 fichas individuales reales (`tools/model_page_lib.py`) ahora llevan:
   - `image`: la foto real del color/variante que se muestra por defecto en la página —
     nunca el logo. Si algún producto futuro no tuviera foto real, el campo se omite en vez
     de sustituirlo por el logo.
   - `brand`: solo cuando el fabricante aparece explícitamente en el propio nombre ya
     publicado del producto — `TSC` (TSC Next One NX1 7i, TSC Next One NX1 7i 45 km/h,
     CityFlizzer TSC, ambos NEXT ONE TSC e-Minicar) y `Fantic` (Fantic Issimo City E-Scooter
     L1). **Para Next NX1, Next NX1 45 km/h, Next NX Plus, Next NX Plus 45 km/h, Chopper 6.0
     Pro, Chopper 6.0 Pro 45 km/h y Fatbob Pro no hay marca de fabricante confirmada en los
     datos — el campo se omitió en vez de inventarla.** Si el dueño confirma estas marcas,
     se pueden añadir en `tools/model_page_lib.py` (`BRAND_MAP`).
   - `offers.seller`: ahora sí identifica a E-Suero como vendedor (antes esto no existía).
   - `sku`: el slug interno del producto (ya usado en la tienda, no es un dato inventado).
   - Para CityFlizzer TSC y Next NX Plus (los únicos con variantes de precio distinto por
     batería) se usa `AggregateOffer` con `lowPrice`/`highPrice` reales de cada variante, en
     vez de declarar un solo precio fijo que no reflejaba las dos opciones.
   - `availability` se mantiene `InStock` para los 13 — es el estado real y uniforme del
     negocio (pedido al proveedor, 0–3 días de tramitación), no una copia ciega sin revisar.
3. **No se añadieron** `shippingDetails` ni `hasMerchantReturnPolicy`: revisadas las AGB y la
   página de proceso de compra, no hay costo de envío publicado ni política de devolución con
   plazo concreto — solo "la recogida en el showroom es gratuita". **Para poder añadir esto
   de forma honesta, el dueño debe proporcionar**: costo de envío a domicilio (o si solo se
   ofrece recogida), transportista, plazo de entrega exacto por zona, y la política de
   devolución (días de plazo, quién paga el envío de vuelta, condiciones).
4. **No se añadió** `review` ni `aggregateRating` a ningún producto — las 13 reseñas de Google
   del negocio son generales, no por modelo, y no corresponde usarlas como si fueran
   reseñas de ese producto específico.

**No validado con Rich Results Test de Google**: este entorno no tiene acceso a internet
(confirmado repetidamente durante todo el proyecto), así que no pude ejecutar la herramienta
de Google. Validado localmente: las 18 páginas modificadas tienen JSON-LD sintácticamente
válido (parseado con `json.loads` sin errores) y ningún `Product` quedó sin `image`. Falta la
comprobación real en https://search.google.com/test/rich-results una vez subido — ver URLs
abajo.

## Actualización 2026-10-27 (revisión): correcciones a la propuesta de datos estructurados

El dueño aprobó la propuesta de JSON-LD con 5 ajustes antes de publicar. Aplicados:

1. **AggregateOffer retirado.** CityFlizzer TSC y Next NX Plus (los únicos con variantes de
   batería) ahora declaran un array `offers` con un `Offer` real por variante — cada uno con
   su propio `price` exacto y una URL con ancla (`#akku-30ah`, `#akku-60ah`, etc.) que
   selecciona esa configuración de verdad en la página, no solo un texto distinto. Se añadió
   `data-variant-slug` a cada botón de variante y lógica nueva en `main.js` que lee
   `location.hash` al cargar la página y preselecciona el botón correspondiente — mismo
   diseño visual, solo cambia cuál variante queda activada por defecto según el enlace usado.
   **Verificado con Playwright, no solo revisado visualmente**: visitar
   `cityflizzer-tsc.html#akku-60ah` muestra "CHF 2'990.00" y activa el chip de 60 Ah (antes
   mostraba 2'190.00 con el ancla ignorada); lo mismo confirmado para los 4 combos de ambos
   productos, incluida la carga sin ancla (debe mostrar la primera variante, confirmado).
2. **Marca retirada de las 13 fichas.** El dueño señaló correctamente que deducir "TSC" o
   "Fantic" solo porque aparecen en el nombre comercial no es verificación real contra
   documentación del fabricante o proveedor — y este entorno no tiene acceso a internet para
   consultar esa documentación. Se quitó `BRAND_MAP` (queda vacío con un comentario
   explicando por qué) — **ninguna de las 13 fichas declara `brand` por ahora.** `seller`
   (E-Suero) se mantiene en todas, eso sí está confirmado y no depende de verificación externa.
   **Pendiente**: si el dueño tiene una ficha técnica, factura o catálogo del proveedor que
   confirme la marca de fabricante de cada modelo, se puede añadir en una línea por producto
   en `BRAND_MAP` dentro de `tools/model_page_lib.py`.
3. **E-Bike / E-Motorräder**: confirmado con Playwright que las 4 secciones ancladas de cada
   página (`#p-fantic-issimo-fun`, `#p-molenstraat-dapper`, etc.) existen y muestran un
   producto real con nombre, specs y precio — no están vacías ni rotas. Se mantienen como
   navegación provisional dentro de la misma página de categoría (no como fichas
   independientes), tal como se aprobó.
4. **E-Scooter — confirmado, no corregido todavía**: las 3 tarjetas con datos ficticios
   (Urban Pro X CHF 890, City Cruiser CHF 1'190, Offroad Force CHF 1'690) **siguen visibles,
   sin cambios**, en `fahrzeuge/e-scooter.html`. Quitarlas del JSON-LD (ronda anterior) no las
   quitó de la página — siguen siendo visibles para cualquier visitante real con precios
   inventados. No se tocó el contenido visible en esta ronda porque el dueño pidió
   explícitamente no cambiar productos/precios visibles sin confirmar antes. **Esto sigue
   pendiente de decisión** (ver tarea #13): ¿se sustituyen por datos reales de E-Scooter que
   el dueño proporcione, se quitan las tarjetas, o se deja así temporalmente marcado como
   "próximamente"?
5. **Sin envíos, devoluciones ni valoraciones** — sin cambios, se mantiene igual que la
   ronda anterior.

## Siguiente paso recomendado

Cuando `thescootercompany.ch` vuelva a ser accesible (desde este entorno o
desde el navegador del usuario), repetir la verificación ficha por ficha,
anotando aquí la URL exacta consultada por modelo y cualquier discrepancia
encontrada antes de publicar cambios de datos técnicos.
