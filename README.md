# TuPrimeraPagina+Macias

Plataforma de Resenas de Restaurantes desarrollada con Django (patron MVT).

## Como correr el proyecto

```bash
# Activar entorno virtual
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Aplicar migraciones (solo la primera vez)
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

Abrir en el navegador: http://127.0.0.1:8000/

---

## Orden de prueba de funcionalidades

### 1. Pagina de Inicio
- URL: `/`
- Muestra estadisticas generales y accesos rapidos.

### 2. Agregar un Restaurante
- URL: `/restaurantes/nuevo/`
- Formulario con: nombre, direccion, tipo de cocina, telefono, ciudad.

### 3. Ver lista de Restaurantes
- URL: `/restaurantes/`
- Tarjetas con todos los restaurantes, calificacion promedio y tipo de cocina.

### 4. Agregar una Resena
- URL: `/resenas/nueva/`
- Formulario con: selector de restaurante, calificacion (1-5 estrellas), comentario.

### 5. Ver detalle de Restaurante con Resenas
- URL: `/restaurantes/<id>/`
- Muestra info del restaurante, promedio de calificacion y todas sus resenas.

### 6. Registrar un Usuario
- URL: `/usuarios/nuevo/`
- Formulario con: nombre, email, selector de resena asociada.

### 7. Buscador de Restaurantes
- URL: `/buscar/`
- Busca por nombre, tipo de cocina o ciudad (con Q objects de Django).

### 8. Panel de Administracion
- URL: `/admin/`
- Requiere crear superusuario: `python manage.py createsuperuser`

---

## Modelos

| Clase        | Campos principales                                        |
|-------------|-----------------------------------------------------------|
| Restaurante | nombre, direccion, tipo_cocina, telefono, ciudad          |
| Resena      | calificacion (1-5), comentario, fecha, FK a Restaurante   |
| Usuario     | nombre, email, fecha_registro, FK a Resena                |

## Herencia de Templates

```
base.html
  ├── index.html
  ├── restaurantes_list.html
  ├── restaurante_detail.html
  ├── restaurante_form.html
  ├── resena_form.html
  ├── usuario_form.html
  └── buscar.html
```
