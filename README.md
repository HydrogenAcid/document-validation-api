# API de Validaciones Documentales (Django + DRF)

API backend desarrollada como prueba técnica para validar documentos XLSX asociados a solicitudes internas, con autenticación JWT y extracción automática de RFC.

---

## Tecnologías utilizadas

- Python 3.x
- Django 6.x
- Django REST Framework
- SimpleJWT (JWT Authentication)
- drf-spectacular (Swagger)
- openpyxl (lectura de XLSX)

---

## Requisitos

- Python 3.10+
- pip
- Entorno virtual (venv)

---

## Instalación

### 1. Clonar repositorio

```bash
git clone 
cd docapi
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

Windows (Git Bash):

```bash
source .venv/Scripts/activate
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

```bash
pip install django djangorestframework djangorestframework-simplejwt drf-spectacular openpyxl
```

### 5. Migraciones

```bash
python manage.py migrate
```

### 6. Crear usuarios de prueba

```bash
python manage.py createsuperuser
```

Usuario principal:

```
username: demo
password: demo12345
```

Usuario secundario (para pruebas de ownership):

```
username: demo2
password: demo212345
```

---

## Ejecutar servidor

```bash
python manage.py runserver
```

Servidor disponible en:

```
http://127.0.0.1:8000/
```

---

## Documentación API (Swagger)

```
http://127.0.0.1:8000/api/docs/
```

---

## Autenticación

### Login

`POST /api/auth/login/`

Body:

```json
{
  "username": "demo",
  "password": "demo12345"
}
```

Usar el `access_token` como:

```
Authorization: Bearer <token>
```

---

## Endpoints principales

### Crear validation

`POST /api/validations/`

Body:

```json
{
  "title": "Prueba RFC"
}
```

### Listar validations (con búsqueda y paginación)

`GET /api/validations/?q=RFC&page=1&limit=10`

- `q` — búsqueda por título
- `page` — número de página
- `limit` — resultados por página

### Detalle (con ownership)

`GET /api/validations/{id}/`

Cada usuario solo puede acceder a sus propias validations. Si intenta acceder a una validation de otro usuario, retorna 404.

### Subir archivo XLSX y extraer RFC

`POST /api/validations/{id}/file/`

- Tipo: `multipart/form-data`
- Campo: `file`
- Solo acepta `.xlsx`
- Límite: 5MB

Respuesta exitosa:

```json
{
  "validation_id": "4",
  "status": "PROCESSED",
  "extracted_key": "RFC",
  "extracted_value": "PEPJ8001019Q8"
}
```

Errores uniformes:

```json
{
  "code": "FILE_INVALID",
  "message": "Only .xlsx files are supported",
  "details": {}
}
```

---

## Control de Ownership

- Cada `Validation` está asociada a un `created_by`.
- El queryset filtra automáticamente por el usuario autenticado.
- Se implementa un permission personalizado `IsOwner`.
- Un usuario no puede ver validations de otro usuario ni subir archivos a validations ajenas.
- En esos casos se retorna 404.

Esto garantiza aislamiento entre usuarios.

---

## Pruebas

```bash
python manage.py test
```

Se incluyen pruebas para:

- Ruta protegida retorna 401 sin token.
- Extractor de RFC funciona correctamente.
- Extractor falla controladamente cuando no hay RFC.

---

## Decisiones Técnicas

- Separación por dominios (`auth_app`, `validations`)
- Lógica de extracción separada en `extractor.py`
- Manejo uniforme de errores con helper `api_error`
- Paginación personalizada (`page`, `limit`)
- Búsqueda personalizada (`q`)
- Ownership implementado vía filtro por `created_by` en queryset y permission personalizado (`IsOwner`)
- Documentación automática con Swagger (drf-spectacular)

---

## Limitaciones

- Solo se soporta extracción de RFC desde archivos `.xlsx`
- No se almacena el archivo de forma persistente
- No se implementan refresh tokens
- No se incluyen endpoints de update/delete (fuera del alcance solicitado)

---

## Estado

La solución cumple con los requisitos funcionales y de calidad solicitados: autenticación JWT, protección de rutas, separación de responsabilidades, endpoints consistentes, manejo uniforme de errores, paginación y búsqueda, ownership, pruebas mínimas y documentación Swagger.

## Deploy

URL desplegada:
https://document-validation-api.onrender.com

Swagger:
https://document-validation-api.onrender.com/api/docs/