from datetime import datetime

from flask import flash, redirect, render_template, request, url_for

from app.citas import bp_citas
from app.extensions import db
from app.models import Cita, Medico, Paciente


def _render_form(cita):
    return render_template(
        "citas/form.html",
        cita=cita,
        medicos=Medico.query.order_by(Medico.nombre).all(),
        pacientes=Paciente.query.order_by(Paciente.nombre).all(),
    )


@bp_citas.get("/")
def index():
    citas = Cita.query.order_by(Cita.fecha.desc(), Cita.hora.desc()).all()
    return render_template("citas/index.html", citas=citas)


@bp_citas.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        try:
            fecha = datetime.strptime(request.form.get("fecha", ""), "%Y-%m-%d").date()
            hora = datetime.strptime(request.form.get("hora", ""), "%H:%M").time()
            medico = db.get_or_404(Medico, request.form.get("medico_id", type=int))
            paciente = db.get_or_404(Paciente, request.form.get("paciente_id", type=int))
        except ValueError:
            flash("La fecha y la hora deben tener un formato válido.", "danger")
        else:
            db.session.add(Cita(fecha=fecha, hora=hora, medico=medico, paciente=paciente))
            db.session.commit()
            flash("Cita registrada correctamente.", "success")
            return redirect(url_for("citas.index"))
    return _render_form(None)


@bp_citas.route("/<int:cita_id>/editar", methods=["GET", "POST"])
def editar(cita_id):
    cita = db.get_or_404(Cita, cita_id)
    if request.method == "POST":
        try:
            fecha = datetime.strptime(request.form.get("fecha", ""), "%Y-%m-%d").date()
            hora = datetime.strptime(request.form.get("hora", ""), "%H:%M").time()
            medico = db.get_or_404(Medico, request.form.get("medico_id", type=int))
            paciente = db.get_or_404(Paciente, request.form.get("paciente_id", type=int))
        except ValueError:
            flash("La fecha y la hora deben tener un formato válido.", "danger")
        else:
            cita.fecha = fecha
            cita.hora = hora
            cita.medico = medico
            cita.paciente = paciente
            db.session.commit()
            flash("Cita actualizada correctamente.", "success")
            return redirect(url_for("citas.index"))
    return _render_form(cita)


@bp_citas.post("/<int:cita_id>/eliminar")
def eliminar(cita_id):
    cita = db.get_or_404(Cita, cita_id)
    db.session.delete(cita)
    db.session.commit()
    flash("Cita eliminada correctamente.", "success")
    return redirect(url_for("citas.index"))
