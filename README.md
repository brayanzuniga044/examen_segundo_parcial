# MediControl

Sistema monolítico modular para administrar médicos, pacientes y citas médicas con Flask, SQLAlchemy, Flask-Migrate y Bootstrap.

## Requisitos

- Python 3.10 o superior
- Dependencias de `requirements.txt`

## Instalación y ejecución en Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:FLASK_APP = "run.py"
flask db upgrade
flask seed
flask run
```

Abre <http://127.0.0.1:5000>. La base SQLite se crea en `instance/medicontrol.sqlite`.

## Migraciones

La carpeta `migrations/` contiene la migración inicial. Después de modificar los modelos:

```powershell
flask db migrate -m "Descripción del cambio"
flask db upgrade
```

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

## Estructura

```text
app/
  citas/       Blueprint y CRUD de citas
  medicos/     Blueprint y CRUD de médicos
  pacientes/   Blueprint y CRUD de pacientes
  templates/   Plantilla base y vistas
  models.py    Modelos y relaciones SQLAlchemy
  extensions.py
migrations/    Historial de migraciones Alembic
docs/          Capturas de pantalla de la aplicación
tests/
```

Al eliminar un médico o paciente también se eliminan sus citas asociadas para conservar la integridad referencial. El comando `flask seed` añade registros de demostración solo cuando las tablas están vacías.

## Entrega académica

El proyecto cubre la fábrica de aplicación, los tres Blueprints, SQLite, modelos, relaciones, migraciones y operaciones CRUD. Para completar la entrega personal, agrega tu identificación, la URL del repositorio GitHub y capturas reales de la aplicación al documento PDF solicitado por la materia.
