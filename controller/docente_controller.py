import unittest
import requests

BASE_URL = "http://localhost:5000"

class TestDocenteAPI(unittest.TestCase):

    def setUp(self):
        requests.delete(f"{BASE_URL}/docentes/delete_all")

    def test_001_lista_vazia(self):
        requisicao = requests.get(f"{BASE_URL}/docentes")
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json(), [])

    def test_002_adiciona_docente(self):
        docente = {
            "id": 1,
            "nome": "Carlos",
            "idade": 40,
            "materia": "Química",
            "observacoes": "Testando inserção."
        }
        requisicao = requests.post(f"{BASE_URL}/docentes", json=docente)
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json()["nome"], "Carlos")

    def test_003_get_por_id_existente(self):
        self.test_002_adiciona_docente()
        requisicao = requests.get(f"{BASE_URL}/docentes/1")
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json()["id"], 1)

    def test_004_get_por_id_inexistente(self):
        requisicao = requests.get(f"{BASE_URL}/docentes/999")
        self.assertEqual(requisicao.status_code, 404)

    def test_005_nome_obrigatorio(self):
        docente = {"id": 2}
        requisicao = requests.post(f"{BASE_URL}/docentes", json=docente)
        self.assertEqual(requisicao.status_code, 400)
        self.assertIn("Docente sem nome", requisicao.text)

    def test_006_id_duplicado(self):
        self.test_002_adiciona_docente()
        docente = {
            "id": 1,
            "nome": "Repetido",
            "idade": 50,
            "materia": "História",
            "observacoes": "Teste duplicado."
        }
        requisicao = requests.post(f"{BASE_URL}/docentes", json=docente)
        self.assertEqual(requisicao.status_code, 400)
        self.assertIn("ID em uso!", requisicao.text)

    def test_007_atualiza_docente(self):
        self.test_002_adiciona_docente()
        requisicao = requests.put(f"{BASE_URL}/docentes/1", json={"nome": "Carlos Silva"})
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json()["nome"], "Carlos Silva")

    def test_008_atualiza_sem_nome(self):
        self.test_002_adiciona_docente()
        requisicao = requests.put(f"{BASE_URL}/docentes/1", json={})
        self.assertEqual(requisicao.status_code, 400)
        self.assertIn("Docente sem nome", requisicao.text)

    def test_009_atualiza_id_inexistente(self):
        requisicao = requests.put(f"{BASE_URL}/docentes/999", json={"nome": "X"})
        self.assertEqual(requisicao.status_code, 404)

    def test_010_deleta_docente(self):
        self.test_002_adiciona_docente()
        requisicao = requests.delete(f"{BASE_URL}/docentes/1")
        self.assertEqual(requisicao.status_code, 200)

    def test_011_deleta_inexistente(self):
        requisicao = requests.delete(f"{BASE_URL}/docentes/999")
        self.assertEqual(requisicao.status_code, 404)

    def test_012_reset_lista(self):
        self.test_002_adiciona_docente()
        requisicao = requests.delete(f"{BASE_URL}/docentes/delete_all")
        self.assertEqual(requisicao.status_code, 200)
        requisicao_lista = requests.get(f"{BASE_URL}/docentes")
        self.assertEqual(len(requisicao_lista.json()), 0)

    def test_013_adiciona_varios(self):
        for i in range(3):
            docente = {
                "id": i + 10,
                "nome": f"Docente {i}",
                "idade": 35,
                "materia": "Matéria",
                "observacoes": "Obs"
            }
            requisicao = requests.post(f"{BASE_URL}/docentes", json=docente)
            self.assertEqual(requisicao.status_code, 200)

    def test_014_get_lista_apos_varios(self):
        self.test_013_adiciona_varios()
        requisicao = requests.get(f"{BASE_URL}/docentes")
        self.assertGreaterEqual(len(requisicao.json()), 3)


if __name__ == '__main__':
    unittest.main()