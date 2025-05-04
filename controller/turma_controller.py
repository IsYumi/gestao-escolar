import unittest
import requests

BASE_URL = "http://localhost:5000"

class TestTurmaAPI(unittest.TestCase):

    def setUp(self):
        requests.delete(f"{BASE_URL}/turmas/delete_all")

    def test_001_lista_vazia(self):
        requisicao = requests.get(f"{BASE_URL}/turmas")
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json(), [])

    def test_002_adiciona_turma(self):
        turma = {
            "id": 1,
            "descricao": "Turma de Teste",
            "professor_id": 1,
            "ativo": True
        }
        requisicao = requests.post(f"{BASE_URL}/turmas", json=turma)
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json()["descricao"], "Turma de Teste")

    def test_003_get_por_id_existente(self):
        self.test_002_adiciona_turma()
        requisicao = requests.get(f"{BASE_URL}/turmas/1")
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json()["id"], 1)

    def test_004_get_por_id_inexistente(self):
        requisicao = requests.get(f"{BASE_URL}/turmas/999")
        self.assertEqual(requisicao.status_code, 404)

    def test_005_descricao_obrigatoria(self):
        turma = {"id": 2, "professor_id": 1, "ativo": True}
        requisicao = requests.post(f"{BASE_URL}/turmas", json=turma)
        self.assertEqual(requisicao.status_code, 400)
        self.assertIn("Turma sem descricao", requisicao.text)

    def test_006_id_duplicado(self):
        self.test_002_adiciona_turma()
        turma = {
            "id": 1,
            "descricao": "Repetida",
            "professor_id": 2,
            "ativo": False
        }
        requisicao = requests.post(f"{BASE_URL}/turmas", json=turma)
        self.assertEqual(requisicao.status_code, 400)
        self.assertIn("ID em uso", requisicao.text)

    def test_007_atualiza_turma(self):
        self.test_002_adiciona_turma()
        requisicao = requests.put(f"{BASE_URL}/turmas/1", json={"descricao": "Atualizada"})
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json()["descricao"], "Atualizada")

    def test_008_atualiza_sem_descricao(self):
        self.test_002_adiciona_turma()
        requisicao = requests.put(f"{BASE_URL}/turmas/1", json={})
        self.assertEqual(requisicao.status_code, 400)
        self.assertIn("Turma sem descricao", requisicao.text)

    def test_009_atualiza_id_inexistente(self):
        requisicao = requests.put(f"{BASE_URL}/turmas/999", json={"descricao": "X"})
        self.assertEqual(requisicao.status_code, 404)

    def test_010_deleta_turma(self):
        self.test_002_adiciona_turma()
        requisicao = requests.delete(f"{BASE_URL}/turmas/1")
        self.assertEqual(requisicao.status_code, 200)

    def test_011_deleta_inexistente(self):
        requisicao = requests.delete(f"{BASE_URL}/turmas/999")
        self.assertEqual(requisicao.status_code, 404)

    def test_012_reset_lista(self):
        self.test_002_adiciona_turma()
        requisicao = requests.delete(f"{BASE_URL}/turmas/delete_all")
        self.assertEqual(requisicao.status_code, 200)
        requisicao_lista = requests.get(f"{BASE_URL}/turmas")
        self.assertEqual(len(requisicao_lista.json()), 0)

    def test_013_adiciona_varios(self):
        for i in range(3):
            turma = {
                "id": i + 10,
                "descricao": f"Turma {i}",
                "professor_id": 1,
                "ativo": True
            }
            requisicao = requests.post(f"{BASE_URL}/turmas", json=turma)
            self.assertEqual(requisicao.status_code, 200)

    def test_014_get_lista_apos_varios(self):
        self.test_013_adiciona_varios()
        requisicao = requests.get(f"{BASE_URL}/turmas")
        self.assertGreaterEqual(len(requisicao.json()), 3)


if __name__ == '__main__':
    unittest.main()