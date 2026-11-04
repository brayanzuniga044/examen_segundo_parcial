import os

import click
from flask import Flask, render_template

from app.extensions import db, migrate


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "medicontrol-dev-key-change-me"),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'medicontrol.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Cita, Medico, Paciente
    from app.citas import bp_citas
    from app.medicos import bp_medicos
    from app.pacientes import bp_pacientes

    app.register_blueprint(bp_medicos, url_prefix="/medicos")
    app.register_blueprint(bp_pacientes, url_prefix="/pacientes")
    app.register_blueprint(bp_citas, url_prefix="/citas")

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            total_medicos=Medico.query.count(),
            total_pacientes=Paciente.query.count(),
            total_citas=Cita.query.count(),
            proximas_citas=Cita.query.order_by(Cita.fecha, Cita.hora).limit(5).all(),
        )

    @app.cli.command("seed")
    def seed():
        """Cargar datos de demostración sin duplicar registros."""
        if Medico.query.first() or Paciente.query.first() or Cita.query.first():
            click.echo("La base de datos ya contiene registros; no se agregaron datos.")
            return

        medicos = [
            Medico(nombre="Ana García", especialidad="Cardiología"),
            Medico(nombre="Luis Mendoza", especialidad="Pediatría"),
            Medico(nombre="Carla Rojas", especialidad="Medicina general"),
        ]
        pacientes = [
            Paciente(nombre="María López", telefono="70012345"),
            Paciente(nombre="José Pérez", telefono="70123456"),
            Paciente(nombre="Sofía Herrera", telefono="70234567"),
        ]
        db.session.add_all(medicos + pacientes)
        db.session.flush()
        from datetime import date, time

        citas = [
            Cita(fecha=date.today(), hora=time(9, 0), medico=medicos[0], paciente=pacientes[0]),
            Cita(fecha=date.today(), hora=time(10, 30), medico=medicos[1], paciente=pacientes[1]),
            Cita(fecha=date.today(), hora=time(14, 0), medico=medicos[2], paciente=pacientes[2]),
        ]
        db.session.add_all(citas)
        db.session.commit()
        click.echo("Datos de demostración cargados correctamente.")

    return app
