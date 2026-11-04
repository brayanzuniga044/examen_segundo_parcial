from flask import flash, redirect, render_template, request, url_for

from app.extensions import db
from app.medicos import bp_medicos
from app.models import Medico


@bp_medicos.get("/")
def index():
    medicos = Medico.query.order_by(Medico.nombre).all()
    return render_template("medicos/index.html", medicos=medicos)


@bp_medicos.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        especialidad = request.form.get("especialidad", "").strip()
        if not nombre or not especialidad:
            flash("El nombre y la especialidad son obligatorios.", "danger")
        else:
            db.session.add(Medico(nombre=nombre, especialidad=especialidad))
            db.session.commit()
            flash("Médico registrado correctamente.", "success")
            return redirect(url_for("medicos.index"))
    return render_template("medicos/form.html", medico=None)


@bp_medicos.route("/<int:medico_id>/editar", methods=["GET", "POST"])
def editar(medico_id):
    medico = db.get_or_404(Medico, medico_id)
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        especialidad = request.form.get("especialidad", "").strip()
        if not nombre or not especialidad:
            flash("El nombre y la especialidad son obligatorios.", "danger")
        else:
            medico.nombre = nombre
            medico.especialidad = especialidad
            db.session.commit()
            flash("Médico actualizado correctamente.", "success")
            return redirect(url_for("medicos.index"))
    return render_template("medicos/form.html", medico=medico)


@bp_medicos.post("/<int:medico_id>/eliminar")
def eliminar(medico_id):
    medico = db.get_or_404(Medico, medico_id)
    db.session.delete(medico)
    db.session.commit()
    flash("Médico y sus citas asociadas eliminados correctamente.", "success")
    return redirect(url_for("medicos.index"))
