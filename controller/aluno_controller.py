import unittest
import requests

BASE_URL = "http://localhost:5000"

class TestAlunoAPI(unittest.TestCase):

    def setUp(self):
        requests.delete(f"{BASE_URL}/alunos/delete_all")

    def test_001_lista_vazia(self):
        requisicao = requests.get(f"{BASE_URL}/alunos")
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json(), [])

    def test_002_adiciona_aluno(self):
        aluno = {
            "id": 1,
            "nome": "Ana",
            "idade": 17,
            "turma_id": 101,
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": 9,
            "media_final": 8.5
        }
        requisicao = requests.post(f"{BASE_URL}/alunos", json=aluno)
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json()["nome"], "Ana")

    def test_003_get_por_id_existente(self):
        self.test_002_adiciona_aluno()
        requisicao = requests.get(f"{BASE_URL}/alunos/1")
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json()["id"], 1)

    def test_004_get_por_id_inexistente(self):
        requisicao = requests.get(f"{BASE_URL}/alunos/999")
        self.assertEqual(requisicao.status_code, 404)

    def test_005_nome_obrigatorio(self):
        aluno = {"id": 2}
        requisicao = requests.post(f"{BASE_URL}/alunos", json=aluno)
        self.assertEqual(requisicao.status_code, 400)
        self.assertIn("Aluno sem nome", requisicao.text)

    def test_006_id_duplicado(self):
        self.test_002_adiciona_aluno()
        aluno = {
            "id": 1,
            "nome": "Duplicado",
            "idade": 17,
            "turma_id": 101,
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": 9,
            "media_final": 8.5
        }
        requisicao = requests.post(f"{BASE_URL}/alunos", json=aluno)
        self.assertEqual(requisicao.status_code, 400)
        self.assertIn("ID em uso!", requisicao.text)

    def test_007_atualiza_nome(self):
        self.test_002_adiciona_aluno()
        requisicao = requests.put(f"{BASE_URL}/alunos/1", json={"nome": "Ana Maria"})
        self.assertEqual(requisicao.status_code, 200)
        self.assertEqual(requisicao.json()["nome"], "Ana Maria")

    def test_008_atualiza_sem_nome(self):
        self.test_002_adiciona_aluno()
        requisicao = requests.put(f"{BASE_URL}/alunos/1", json={})
        self.assertEqual(requisicao.status_code, 400)
        self.assertIn("Aluno sem nome", requisicao.text)

    def test_009_atualiza_id_inexistente(self):
        requisicao = requests.put(f"{BASE_URL}/alunos/999", json={"nome": "X"})
        self.assertEqual(requisicao.status_code, 404)

    def test_010_deleta_aluno(self):
        self.test_002_adiciona_aluno()
        requisicao = requests.delete(f"{BASE_URL}/alunos/1")
        self.assertEqual(requisicao.status_code, 200)

    def test_011_deleta_inexistente(self):
        requisicao = requests.delete(f"{BASE_URL}/alunos/999")
        self.assertEqual(requisicao.status_code, 404)

    def test_012_reset_lista(self):
        self.test_002_adiciona_aluno()
        requisicao = requests.delete(f"{BASE_URL}/alunos/delete_all")
        self.assertEqual(requisicao.status_code, 200)
        requisicao_lista = requests.get(f"{BASE_URL}/alunos")
        self.assertEqual(len(requisicao_lista.json()), 0)

    def test_013_adiciona_varios(self):
        for i in range(3):
            aluno = {
                "id": i + 10,
                "nome": f"Aluno {i}",
                "idade": 16,
                "turma_id": 101,
                "nota_primeiro_semestre": 7,
                "nota_segundo_semestre": 7,
                "media_final": 7
            }
            requisicao = requests.post(f"{BASE_URL}/alunos", json=aluno)
            self.assertEqual(requisicao.status_code, 200)

    def test_014_get_lista_apos_varios(self):
        self.test_013_adiciona_varios()
        requisicao = requests.get(f"{BASE_URL}/alunos")
        self.assertGreaterEqual(len(requisicao.json()), 3)

if __name__ == '__main__':
    unittest.main()
