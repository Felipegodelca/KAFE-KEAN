# Publicar KAFE KEAN en Vercel

Vercel detecta `manage.py` y el WSGI de Django automáticamente. No hace falta
crear un `vercel.json` ni una carpeta `api`.

## Plan de costo cero

La primera versión usa únicamente niveles gratuitos:

- Vercel Hobby para alojar la web.
- Supabase Free para PostgreSQL.
- GitHub Free con repositorio privado.
- HTTPS automático de Vercel.
- La imagen local incluida en el proyecto si no se configura Unsplash.

No requiere OpenAI, OpenRouter, Currency Layer, Cloudinary ni otro servicio de
pago. El dominio debe estar ya comprado; su renovación con el registrador es
el único costo externo inevitable para conservar `kafekean.com`.

## 1. Rotar los secretos expuestos

Antes de desplegar:

1. Revoca y genera de nuevo las claves de OpenAI y OpenRouter.
2. Cambia la contraseña de la base de datos de Supabase.
3. Cambia las contraseñas de GitHub, Zoho y de cualquier cuenta repetida.
4. Genera una `DJANGO_SECRET_KEY` nueva. No reutilices ninguna publicada.

La app actual no usa OpenAI, OpenRouter, Zoho ni Currency Layer. No agregues
esas credenciales a Vercel.

## 2. Preparar Supabase

En Supabase abre el proyecto y pulsa **Connect**. Para Vercel usa la conexión
**Transaction pooler**, normalmente en el puerto `6543`, con SSL. Guarda esa
URL nueva como `DATABASE_URL`.

La URL de conexión es un secreto: nunca debe entrar al repositorio ni al chat.

## 3. Variables de Vercel

En el proyecto, abre **Settings > Environment Variables** y crea estas
variables para **Production** y **Preview**:

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<clave nueva y aleatoria>
DATABASE_URL=<URL nueva del Transaction pooler con ?sslmode=require>
DJANGO_ALLOWED_HOSTS=kafe-kean.vercel.app,.vercel.app,.kafekean.com,kafekean.com,www.kafekean.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.vercel.app,https://kafekean.com,https://www.kafekean.com
UNSPLASH_ACCESS_KEY=<opcional>
```

Después de cambiar variables, crea un deployment nuevo desde `main`. Si usas
**Redeploy** sobre un deployment viejo, Vercel reconstruirá el commit viejo.

## 4. Crear tablas y administrador

Después de configurar `DATABASE_URL`, ejecuta las migraciones contra Supabase
desde una terminal segura:

```powershell
$env:DATABASE_URL = "<URL nueva>"
$env:DJANGO_SECRET_KEY = "<clave nueva>"
$env:DJANGO_DEBUG = "0"
python manage.py migrate
python manage.py createsuperuser
```

El superusuario que existía en `db.sqlite3` no se copia automáticamente a
Supabase; hay que crearlo de nuevo.

## 5. Desplegar

Sube el proyecto a un repositorio privado de GitHub e impórtalo en Vercel, o
usa la CLI:

```powershell
vercel link
vercel deploy --prod
```

Prueba primero la dirección temporal `*.vercel.app`.

## 6. Conectar el dominio

En Vercel abre **Project > Settings > Domains** y agrega:

```text
kafekean.com
www.kafekean.com
```

Elige `www.kafekean.com` como dominio principal y redirige el dominio raíz.
Vercel mostrará los registros DNS exactos. En el proveedor donde compraste el
dominio, configura el `CNAME` de `www` y el registro del dominio raíz que
Vercel indique. No borres los registros MX de Zoho: son los que mantienen
funcionando el correo.

Cuando Vercel verifique el DNS, emitirá el certificado HTTPS automáticamente.

## Archivos subidos

El sistema de archivos de una función Vercel no es permanente. Los artículos
y usuarios sí quedan en PostgreSQL. En la primera versión se debe evitar subir
imágenes desde el formulario; después se puede conectar el cupo gratuito de
Supabase Storage sin contratar otro servicio.
