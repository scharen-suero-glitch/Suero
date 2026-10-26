====================================================
E-SUERO — INSTRUCCIONES DE PUBLICACIÓN (HOSTINGER)
====================================================

Este paquete contiene la web completa de E-Suero, lista para publicar:
sitio institucional, taller (Werkstatt), y la sección comercial de venta
de vehículos (E-Roller, E-Motorräder, E-Scooter, E-Bike, E-Minicar) con
pago real por Stripe y formulario de solicitud de venta/prueba. HTML,
CSS y JavaScript puro, con un pequeño backend en PHP para pagos y
correos — sin paso de compilación, sin npm, sin base de datos.

----------------------------------------------------
CÓMO PUBLICAR
----------------------------------------------------

1. Entra en Hostinger (hpanel.hostinger.com).

2. Abre "Administrador de archivos" (File Manager) en el menú "Archivos".

3. Abre la carpeta "public_html". Es la raíz web de e-suero.ch.

4. Si hay archivos por defecto de Hostinger (un index.html de muestra,
   "default.php", etc.), bórralos. NO borres la carpeta public_html en
   sí — solo su contenido.

5. Sube el ZIP dentro de public_html, haz clic derecho sobre él en el
   Administrador de archivos y elige "Extraer". Extráelo directamente
   dentro de public_html (no dentro de una subcarpeta nueva).

6. Comprueba que index.html queda directamente dentro de public_html
   — es decir, la ruta debe ser public_html/index.html, NO
   public_html/e-suero/index.html. Si el ZIP se extrajo en su propia
   subcarpeta, mueve todos los archivos y carpetas un nivel hacia
   arriba, dentro de public_html, y borra la subcarpeta vacía que quede.

7. Abre stripe/config.php con el editor de código del Administrador de
   archivos. Busca esta línea cerca del principio:

     define('STRIPE_SECRET_KEY', 'sk_live_REPLACE_WITH_YOUR_STRIPE_SECRET_KEY');

   Sustituye el texto de ejemplo por tu clave SECRETA real de Stripe
   (empieza por sk_live_...), que encuentras en
   https://dashboard.stripe.com/apikeys. Guarda el archivo. Este es el
   único paso manual obligatorio — el resto del checkout (metadatos del
   pedido, página de éxito, manejo de errores) ya está implementado y
   conectado.

   (Opcional) Si quieres activar el webhook de Stripe, sigue las
   instrucciones dentro del propio archivo stripe/config.php, en el
   bloque "WEBHOOK SETUP" — no es obligatorio para que la tienda
   funcione, solo añade una confirmación adicional del lado del servidor.

8. Visita https://e-suero.ch para confirmar que el sitio está en línea.
   Haz una compra de prueba real pequeña para confirmar que Stripe
   funciona de principio a fin, y envía una solicitud de prueba desde
   el formulario de /verkauf/index.html para confirmar que el correo de
   solicitudes de venta llega a info@e-suero.ch.

Eso es todo — no hace falta configurar variables de entorno ni ningún
comando de compilación. Cada recurso (fuentes, scripts, imágenes,
iconos) está autocontenido dentro de este paquete y se carga con rutas
relativas.

----------------------------------------------------
QUÉ CONTIENE EL PAQUETE
----------------------------------------------------

index.html              Página de inicio (sitio institucional, taller,
                         laboratorio de baterías, galería, reseñas, FAQ,
                         contacto del taller).
styles.css               Todos los estilos del sitio.
main.js                  Interactividad del sitio (animaciones, menú,
                         selector de idioma, formularios, carruseles...).
i18n.js                  Traducciones alemán/inglés/italiano/español.
manifest.json             Manifiesto PWA (icono de pantalla de inicio).
robots.txt / sitemap.xml  Reglas e indexación para buscadores.
.htaccess                 Configuración de Apache: HTTPS, caché,
                         compresión, bloqueo de archivos .log.
favicon.ico               Icono de pestaña del navegador.

verkauf/                  SECCIÓN DE VENTA (hub comercial):
    index.html                 Página principal "Fahrzeuge kaufen" —
                               portada, categorías, E-Roller destacados,
                               proceso de compra, FAQ y formulario de
                               contacto comercial.
    inquiry.php                Backend real del formulario de venta/
                               prueba: valida, envía el correo a
                               info@e-suero.ch y solo informa éxito
                               cuando realmente se envió.
    gebraucht-geprueft.html    Catálogo de vehículos de ocasión
                               revisados (Gebraucht & Geprüft).
    bestell-lieferprozess.html Explicación del proceso de pedido y
                               entrega.
    .htaccess                  Bloquea el acceso directo a los .log de
                               solicitudes (contienen datos de clientes).

fahrzeuge/                 Páginas de cada categoría de vehículo, con
                           navegación y pie de página propios de venta
                           (sin referencias al taller):
    e-roller.html / e-roller/<modelo>.html    11 modelos, cada uno con
                               su propia ficha individual, SEO propio,
                               compra directa con Stripe.
    e-minicar.html / e-minicar/<modelo>.html  Categoría E-Minicar.
    e-motorraeder.html, e-scooter.html, e-bike.html   Categorías
                               pendientes de fichas individuales
                               (ver nota más abajo).

leistungen/                Páginas de servicios del taller (diagnóstico,
                           reparación de batería, controlador,
                           mantenimiento de flotas, taller, premium care).

legal/                     Datenschutz (privacidad), Impressum, AGB.

lib/                       GSAP + ScrollTrigger (alojados en el propio
                           sitio, sin CDN externo).

stripe/                    Backend de pagos:
    config.php                 Clave secreta de Stripe + ajustes
                               compartidos (incluye ADMIN_EMAIL). ÚNICO
                               archivo que debes editar (paso 7 arriba).
    create-checkout-session.php Crea la sesión de pago de Stripe,
                               validando el precio contra una lista
                               blanca en catalog-eroller.php — nunca
                               confía en el precio que envía el navegador.
    catalog-eroller.php        Lista blanca de productos/precios reales
                               de E-Roller, generada a partir de
                               tools/eroller_catalog.py.
    success.php / cancel.php   Confirmación o cancelación del pago.
    webhook.php                 Confirmación adicional opcional vía
                               Stripe (ver paso 7).
    .htaccess                   Bloquea el acceso directo a los .log.
    orders.log / error.log     Se crean solos al usarse — no los crees
                               a mano.

assets/
  fonts/                   Fuentes Inter + Space Grotesk (alojadas aquí).
  icons/                   Favicon, apple-touch-icon, iconos PWA.
  images/                  Logo e imágenes generales del sitio.
  images/products/         Fotos de producto de todo el catálogo.
  js/
    catalog-tools.js        Buscador/filtros del catálogo del taller.
    stripe-checkout.js       Abre el pago de Stripe desde "Jetzt kaufen".
    sales-form.js             Envía el formulario de venta/prueba real.
    gebraucht-katalog.js      Catálogo de vehículos de ocasión.

----------------------------------------------------
CARPETA tools/ — NO ES PARTE DEL SITIO PÚBLICO
----------------------------------------------------

tools/ contiene los scripts en Python que generan las fichas de
producto (eroller_catalog.py, minicar_catalog.py, model_page_lib.py...)
y un registro interno de fuentes de datos (QUELLEN-PRODUKTDATEN.md). No
hace falta subirlos a Hostinger para que el sitio funcione — están
excluidos del ZIP de publicación. Consérvalos solo si en algún momento
quieres volver a generar o actualizar las fichas de producto desde el
repositorio de GitHub.

----------------------------------------------------
PENDIENTE — LO QUE TODAVÍA NO ESTÁ TERMINADO
----------------------------------------------------

- E-Motorräder y E-Bike: las categorías existen, pero aún no tienen
  fichas individuales por modelo como E-Roller — están pendientes de
  que me confirmes o yo extraiga los datos reales de cada modelo.

- E-Scooter: la página actual (fahrzeuge/e-scooter.html) todavía
  muestra 3 productos de ejemplo con precios inventados (Urban Pro X,
  City Cruiser, Offroad Force) — NO son datos reales, hace falta que me
  proporciones el catálogo real antes de publicarlos como venta.

- E-Minicar: la foto real ya está publicada. Sigue faltando el precio
  real (ahora mismo muestra "Preis auf Anfrage").

- Portada de la sección de venta (verkauf/index.html): ya usa tu imagen
  real, pero si cambias esa imagen más adelante, solo hace falta
  reemplazar assets/images/products/e-suero-produkte-hero.(jpg/webp/png).

----------------------------------------------------
ANTES DE PUBLICAR — REVISA ESTO
----------------------------------------------------

- Clave secreta de Stripe: ver paso 7 — imprescindible para que el
  pago funcione.

- Métodos de pago en Stripe: la tarjeta está activada por defecto. Para
  ofrecer TWINT, Apple Pay, Google Pay, Klarna o PayPal, actívalos en
  el Dashboard de Stripe → Settings → Payment methods. No hace falta
  tocar ningún código — el pago ofrece automáticamente lo que actives.

- Dominio: el sitio espera estar publicado en https://e-suero.ch (así
  están configuradas las URLs canónicas, el sitemap, robots.txt, los
  datos estructurados y la URL de retorno de Stripe). Si el dominio
  fuera otro, habría que actualizar esas referencias.

- Google Maps: la sección de contacto usa un iframe de Google Maps para
  Schwerzistrasse 34, 8807 Freienbach SZ. Funciona automáticamente en
  cuanto el sitio esté público.

- WhatsApp / teléfono / correo: todo apunta a +41 79 668 90 88 y a
  info@e-suero.ch. Si cambian, hay que actualizarlo en varios archivos.

- Formulario de contacto del taller (index.html): valida en el
  navegador y abre el cliente de correo del visitante (mailto:) — no
  tiene backend propio. El formulario de venta/prueba en verkauf/
  (inquiry.php) sí es un envío real desde el servidor.

- SSL: Hostinger emite un certificado SSL gratuito por dominio.
  Comprueba que esté activo (hPanel → SSL) — el .htaccess ya fuerza
  HTTPS.

- PHP: stripe/ e inquiry.php necesitan PHP con cURL activado, lo cual
  es estándar en el hosting compartido de Hostinger — no requiere
  configuración adicional.

----------------------------------------------------
SI ALGO NO FUNCIONA
----------------------------------------------------

Si una página se ve sin estilos o falta alguna sección después de
subirla, la causa más común es que el ZIP se extrajo una carpeta de más
(ver paso 6) — comprueba que index.html, styles.css y las carpetas
assets/lib/legal/stripe/verkauf/fahrzeuge estén directamente dentro de
public_html.

Si el pago muestra "Zahlung ist noch nicht konfiguriert", significa que
la clave secreta de Stripe todavía no se ha sustituido en
stripe/config.php (paso 7 arriba).

Si el formulario de venta/prueba en verkauf/index.html no envía correo,
comprueba que tu plan de Hostinger tenga la función mail() de PHP
habilitada (viene activada por defecto en el hosting compartido) y
revisa la carpeta de spam de info@e-suero.ch.
