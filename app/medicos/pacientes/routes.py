from flask import flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import Cita, Paciente
from app.pacientes import bp_pacientes


@bp_pacientes.get("/")
def index():
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    return render_template("pacientes/index.html", pacientes=pacientes)


@bp_pacientes.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre or not telefono:
            flash("El nombre y el teléfono son obligatorios.", "danger")
        else:
            db.session.add(Paciente(nombre=nombre, telefono=telefono))
            db.session.commit()
            flash("Paciente registrado correctamente.", "success")
            return redirect(url_for("pacientes.index"))
    return render_template("pacientes/form.html", paciente=None)


@bp_pacientes.route("/<int:paciente_id>/editar", methods=["GET", "POST"])
def editar(paciente_id):
    paciente = db.get_or_404(Paciente, paciente_id)
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre or not telefono:
            flash("El nombre y el teléfono son obligatorios.", "danger")
        else:
            paciente.nombre = nombre
            paciente.telefono = telefono
            db.session.commit()
            flash("Paciente actualizado correctamente.", "success")
            return redirect(url_for("pacientes.index"))
    return render_template("pacientes/form.html", paciente=paciente)


@bp_pacientes.post("/<int:paciente_id>/eliminar")
def eliminar(paciente_id):
    paciente = db.get_or_404(Paciente, paciente_id)
    if Cita.query.filter_by(paciente_id=paciente.id).first():
        flash("No se puede eliminar: el paciente tiene citas registradas.", "danger")
    else:
        db.session.delete(paciente)
        db.session.commit()
        flash("Paciente eliminado correctamente.", "success")
    return redirect(url_for("pacientes.index"))
