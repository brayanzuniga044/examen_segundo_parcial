import unittest
from datetime import date, time

from app import create_app
from app.extensions import db
from app.models import Cita, Medico, Paciente


class MediControlTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-key",
                "SQLALCHEMY_DATABASE_URI": "sqlite://",
            }
        )
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.medico = Medico(nombre="Dra. Test", especialidad="Medicina general")
            self.paciente = Paciente(nombre="Paciente Test", telefono="70000000")
            db.session.add_all([self.medico, self.paciente])
            db.session.commit()
            self.medico_id = self.medico.id
            self.paciente_id = self.paciente.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_dashboard_and_blueprint_routes_load(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/medicos/").status_code, 200)
        self.assertEqual(self.client.get("/pacientes/").status_code, 200)
        self.assertEqual(self.client.get("/citas/").status_code, 200)

    def test_create_and_update_medico(self):
        response = self.client.post(
            "/medicos/nuevo",
            data={"nombre": "Dr. Nuevo", "especialidad": "Neurología"},
            follow_redirects=True,
        )
        self.assertIn("Dr. Nuevo", response.get_data(as_text=True))
        with self.app.app_context():
            medico_id = Medico.query.filter_by(nombre="Dr. Nuevo").first().id
        self.client.post(
            f"/medicos/{medico_id}/editar",
            data={"nombre": "Dr. Actualizado", "especialidad": "Neurología"},
        )
        with self.app.app_context():
            self.assertIsNotNone(
                Medico.query.filter_by(nombre="Dr. Actualizado").first()
            )

    def test_create_update_and_delete_paciente(self):
        response = self.client.post(
            "/pacientes/nuevo",
            data={"nombre": "Paciente Nuevo", "telefono": "70999999"},
            follow_redirects=True,
        )
        self.assertIn("Paciente Nuevo", response.get_data(as_text=True))
        with self.app.app_context():
            paciente_id = Paciente.query.filter_by(nombre="Paciente Nuevo").first().id
        self.client.post(
            f"/pacientes/{paciente_id}/editar",
            data={"nombre": "Paciente Editado", "telefono": "70888888"},
        )
        with self.app.app_context():
            self.assertIsNotNone(
                Paciente.query.filter_by(nombre="Paciente Editado").first()
            )
        self.client.post(f"/pacientes/{paciente_id}/eliminar")
        with self.app.app_context():
            self.assertIsNone(db.session.get(Paciente, paciente_id))

    def test_create_and_delete_cita(self):
        response = self.client.post(
            "/citas/nuevo",
            data={
                "fecha": "2026-11-03",
                "hora": "09:30",
                "medico_id": str(self.medico_id),
                "paciente_id": str(self.paciente_id),
            },
            follow_redirects=True,
        )
        self.assertIn("Dra. Test", response.get_data(as_text=True))
        with self.app.app_context():
            cita_id = Cita.query.one().id
        self.client.post(f"/citas/{cita_id}/eliminar")
        with self.app.app_context():
            self.assertEqual(Cita.query.count(), 0)

    def test_update_cita(self):
        self.client.post(
            "/citas/nuevo",
            data={
                "fecha": "2026-11-03",
                "hora": "09:30",
                "medico_id": str(self.medico_id),
                "paciente_id": str(self.paciente_id),
            },
        )
        with self.app.app_context():
            cita_id = Cita.query.one().id
        self.client.post(
            f"/citas/{cita_id}/editar",
            data={
                "fecha": "2026-11-04",
                "hora": "11:15",
                "medico_id": str(self.medico_id),
                "paciente_id": str(self.paciente_id),
            },
        )
        with self.app.app_context():
            cita = db.session.get(Cita, cita_id)
            self.assertEqual(cita.fecha, date(2026, 11, 4))
            self.assertEqual(cita.hora, time(11, 15))

    def test_deleting_medico_also_deletes_its_citas(self):
        with self.app.app_context():
            db.session.add(
                Cita(
                    fecha=date(2026, 11, 3),
                    hora=time(9, 30),
                    medico_id=self.medico_id,
                    paciente_id=self.paciente_id,
                )
            )
            db.session.commit()
        response = self.client.post(
            f"/medicos/{self.medico_id}/eliminar", follow_redirects=True
        )
        self.assertIn("citas asociadas eliminados", response.get_data(as_text=True))
        with self.app.app_context():
            self.assertIsNone(db.session.get(Medico, self.medico_id))
            self.assertEqual(Cita.query.count(), 0)

    def test_deleting_paciente_also_deletes_its_citas(self):
        with self.app.app_context():
            db.session.add(
                Cita(
                    fecha=date(2026, 11, 3),
                    hora=time(9, 30),
                    medico_id=self.medico_id,
                    paciente_id=self.paciente_id,
                )
            )
            db.session.commit()
        response = self.client.post(
            f"/pacientes/{self.paciente_id}/eliminar", follow_redirects=True
        )
        self.assertIn("citas asociadas eliminados", response.get_data(as_text=True))
        with self.app.app_context():
            self.assertIsNone(db.session.get(Paciente, self.paciente_id))
            self.assertEqual(Cita.query.count(), 0)

    def test_invalid_cita_date_is_reported(self):
        response = self.client.post(
            "/citas/nuevo",
            data={
                "fecha": "fecha-invalida",
                "hora": "09:30",
                "medico_id": str(self.medico_id),
                "paciente_id": str(self.paciente_id),
            },
            follow_redirects=True,
        )
        self.assertIn("formato válido", response.get_data(as_text=True))
        with self.app.app_context():
            self.assertEqual(Cita.query.count(), 0)


if __name__ == "__main__":
    unittest.main()
