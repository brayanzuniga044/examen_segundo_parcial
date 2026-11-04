from app.extensions import db


class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    especialidad = db.Column(db.String(120), nullable=False)
    citas = db.relationship(
        "Cita", back_populates="medico", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Medico {self.nombre}>"


class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)
    citas = db.relationship(
        "Cita", back_populates="paciente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Paciente {self.nombre}>"


class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey("medico.id"), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    medico = db.relationship("Medico", back_populates="citas")
    paciente = db.relationship("Paciente", back_populates="citas")

    def __repr__(self):
        return f"<Cita {self.fecha} {self.hora}>"
