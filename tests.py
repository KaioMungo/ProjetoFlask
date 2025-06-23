import requests
import unittest
from professor.professor_model import Professor
from aluno.aluno_model import Student
from turma.turma_model import Classroom
from config import db, app

class TestStringMethods(unittest.TestCase):
    # ---- Testa se o GET da rotas /alunos, /professores e /turmas devolvem uma lista ---- #
    def test_000_rotas_retornam_lista(self):
        # ---- Rota alunos ---- #
        r = requests.get('http://localhost:5000/alunos')

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

        # ---- Rota professores ---- #
        r = requests.get('http://localhost:5000/professores')

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

        # ---- Rota turmas ---- #
        r = requests.get('http://localhost:5000/turmas')

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    # ---- Testa se o POST da rota /alunos está adicionando os alunos ---- #
    def test_001_adiciona_alunos(self):
        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Adicionando alunos ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Fábio",
            "class_id": 1, 
            "born_date": "2004-09-18", 
            "first_grade": 2, 
            "second_grade": 4
            })
        requests.post('http://localhost:5000/alunos',json={
            "name": "Luiz",
            "class_id": 1, 
            "born_date": "2006-06-25", 
            "first_grade": 5, 
            "second_grade": 7
            })
        
        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()

        achei_fabio = False
        achei_luiz = False
        for aluno in lista_retornada:
            if aluno['name'] == 'Fábio':
                achei_fabio = True
            if aluno['name'] == 'Luiz':
                achei_luiz = True
        
        if not achei_fabio:
            self.fail('Aluno Fábio nao apareceu na lista de alunos')
        if not achei_luiz:
            self.fail('Aluno Luiz nao apareceu na lista de alunos')
            
    # ---- Testa se o GET da rota /alunos devolve o aluno do id selecionado ---- #
    def test_002_aluno_por_id(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Adicionando alunos ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Kaio",
            "class_id": 1, 
            "born_date": "2006-04-10", 
            "first_grade": 5, 
            "second_grade": 9
            })
        requests.post('http://localhost:5000/alunos',json={
            "name": "Diego",
            "class_id": 1, 
            "born_date": "2002-06-28", 
            "first_grade": 10, 
            "second_grade": 9
            })

        resposta = requests.get('http://localhost:5000/alunos/2')
        dict_retornado = resposta.json()
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('name',dict_retornado)
        
        self.assertEqual(dict_retornado['name'],'Diego')
        
    # ---- Testa se a rota /reseta apaga todos os dados das tabelas de professores, alunos e turmas ---- #
    def test_003_reseta(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        requests.post('http://localhost:5000/alunos',json={
            "name": "Kaio",
            "class_id": 1, 
            "born_date": "2006-04-10", 
            "first_grade": 5, 
            "second_grade": 9
            })
        
        r_lista = requests.get('http://localhost:5000/professores')
        r_lista2 = requests.get('http://localhost:5000/turmas')
        r_lista3 = requests.get('http://localhost:5000/alunos')

        self.assertTrue(len(r_lista.json()) > 0)
        self.assertTrue(len(r_lista2.json()) > 0)
        self.assertTrue(len(r_lista3.json()) > 0)

        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        r_lista_depois = requests.get('http://localhost:5000/professores')
        r_lista2_depois = requests.get('http://localhost:5000/turmas')
        r_lista3_depois = requests.get('http://localhost:5000/alunos')
        
        self.assertEqual(len(r_lista_depois.json()),0)
        self.assertEqual(len(r_lista2_depois.json()),0)
        self.assertEqual(len(r_lista3_depois.json()),0)

    # ---- Testa se o DELETE da rota /alunos deleta o aluno do id selecionado ---- #
    def test_004_deleta_alunos(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        
        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Adicionando alunos ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Fábio",
            "class_id": 1, 
            "born_date": "2004-09-18", 
            "first_grade": 2, 
            "second_grade": 4
            })
        requests.post('http://localhost:5000/alunos',json={
            "name": "Luiz",
            "class_id": 1, 
            "born_date": "2006-06-25", 
            "first_grade": 5, 
            "second_grade": 7
            })
        requests.post('http://localhost:5000/alunos',json={
            "name": "Kaio",
            "class_id": 1, 
            "born_date": "2006-04-10", 
            "first_grade": 5, 
            "second_grade": 9
            })
        
        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()
        
        self.assertEqual(len(lista_retornada),3)
        
        requests.delete('http://localhost:5000/alunos/2')
        
        r_lista2 = requests.get('http://localhost:5000/alunos')
        lista_retornada2 = r_lista2.json()
        
        self.assertEqual(len(lista_retornada2),2) 

        acheiFabio = False
        acheiKaio = False
        for aluno in lista_retornada:
            if aluno['name'] == 'Fábio':
                acheiFabio=True
            if aluno['name'] == 'Kaio':
                acheiKaio=True
        if not acheiFabio or not acheiKaio:
            self.fail("Você pode ter deletado o aluno errado!")

        requests.delete('http://localhost:5000/alunos/1')

        r_lista3 = requests.get('http://localhost:5000/alunos')
        lista_retornada3 = r_lista3.json()
        
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['name'] == 'Kaio':
            pass
        else:
            self.fail("Você pode ter deletado o aluno errado!")

    # ---- Testa se o PUT da rota /alunos atualiza o aluno do id selecionado ---- #
    def test_005_edita_alunos(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Adicionando alunos ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Diego",
            "class_id": 1, 
            "born_date": "2002-06-28", 
            "first_grade": 10, 
            "second_grade": 9
            })
        requests.post('http://localhost:5000/alunos',json={
            "name": "Bruna",
            "class_id": 1, 
            "born_date": "2006-01-30", 
            "first_grade": 2,
            "second_grade": 9
            })
        
        r_antes = requests.get('http://localhost:5000/alunos/2')
        
        self.assertEqual(r_antes.json()['name'],'Bruna')

        requests.put('http://localhost:5000/alunos/2', json={
            "name": "Brunasser",
            "class_id": 1, 
            "born_date": "2006-01-30", 
            "first_grade": 2,
            "second_grade": 9
            })
        
        r_depois = requests.get('http://localhost:5000/alunos/2')
        
        self.assertEqual(r_depois.json()['name'],'Brunasser')
        self.assertEqual(r_depois.json()['age'],19)

    # ---- Testa se o GET retorna todos os alunos ---- #
    def test_006_retorna_todos_alunos(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Adicionando alunos ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Fábio",
            "class_id": 1, 
            "born_date": "2004-09-18", 
            "first_grade": 2, 
            "second_grade": 4
            })
        requests.post('http://localhost:5000/alunos',json={
            "name": "Kaio",
            "class_id": 1, 
            "born_date": "2006-04-10", 
            "first_grade": 5, 
            "second_grade": 9
            })
        
        acheiFabio = False
        acheiKaio = False

        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()

        for aluno in lista_retornada:
            if aluno['name'] == 'Fábio':
                acheiFabio=True
            if aluno['name'] == 'Kaio':
                acheiKaio=True
        if not acheiFabio or not acheiKaio:
            self.fail("Não retornou todos os alunos")

        self.assertEqual(len(lista_retornada),2)

    # ---- Testa se as rotas em que precisa passar um id retorna o erro falando que não existe o id selecionado ---- #
    def test_007_id_inexistente_alunos(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Adicionando aluno ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Fábio",
            "class_id": 1,
            "born_date": "2004-09-18",
            "first_grade": 10, 
            "second_grade": 9
            })

        # ---- Rota PUT ---- #
        r = requests.put('http://localhost:5000/alunos/30',json={
            "name": "Fábio",
            "class_id": 1, 
            "born_date": "2004-09-18", 
            "first_grade": 2, 
            "second_grade": 4
            })

        self.assertEqual(r.json()['Error'],'O aluno que você quer atualizar não foi encontrado.')

        # ---- Rota GET ---- #
        r = requests.get('http://localhost:5000/alunos/50')
        
        self.assertEqual(r.json()['Error'],'O aluno não foi encontrado.')

        # ---- Rota DELETE ---- #
        r = requests.delete('http://localhost:5000/alunos/50')
        
        self.assertEqual(r.json()['Error'],'O aluno que você quer deletar não foi encontrado.')

    # ---- Testa se o PUT e o POST retornam o erro que as chaves não podem tem valores vazios ---- #
    def test_008_atualiza_ou_adiciona_aluno_com_valores_vazios(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Adicionando aluno ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Diego",
            "class_id": 1, 
            "born_date": "2002-06-28", 
            "first_grade": 10, 
            "second_grade": 9
            })

        # ---- Chave name com valor vazio ---- #
        r = requests.put('http://localhost:5000/alunos/1',json={
            "name": "",
            "class_id": 1, 
            "born_date": "2002-06-28", 
            "first_grade": 10, 
            "second_grade": 9
            })
        
        self.assertEqual(r.json()['Error'],'As chaves não podem estar vazias.')

        # ---- Chave born_date com valor vazio ---- #
        r = requests.post('http://localhost:5000/alunos',json={
            "name": "Fábio",
            "class_id": 1, 
            "born_date": "", 
            "first_grade": 10, 
            "second_grade": 9
            })
        
        self.assertEqual(r.json()['Error'],'As chaves não podem estar vazias.')

    # ---- Testa se o PUT e o POST retornam o erro que está faltando alguma chave no request ---- #
    def test_009_atualiza_ou_adiciona_aluno_sem_alguma_chave(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Adicionando aluno ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Diego",
            "class_id": 1, 
            "born_date": "2002-06-28", 
            "first_grade": 10, 
            "second_grade": 9
            })
        
        # ---- PUT sem a chave class_id ---- #
        r = requests.put('http://localhost:5000/alunos/1',json={
            "name": "Fábio",
            "born_date": "2002-06-28", 
            "first_grade": 10, 
            "second_grade": 9
            })
        
        self.assertEqual(r.json()['Error'],'Você não passou alguma chave.')
        
        # ---- POST sem a chave first_grade ---- #
        r = requests.post('http://localhost:5000/alunos',json={
            "name": "Luiz",
            "class_id": 1, 
            "born_date": "2006-06-25", 
            "second_grade": 7
            })
        
        self.assertEqual(r.json()['Error'],'Você não passou alguma chave.')

    # ---- Teste para ver se retorna o erro que o id da classe passada não existe ---- #
    def test_010_atualiza_ou_adiciona_aluno_com_classe_inexistente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Adicionando aluno ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Fábio",
            "class_id": 1, 
            "born_date": "2004-09-18",
            "first_grade": 2, 
            "second_grade": 4
            })
        
        r = requests.put('http://localhost:5000/alunos/1',json={
            "name": "Fábio",
            "class_id": 60,
            "born_date": "2002-06-28", 
            "first_grade": 10, 
            "second_grade": 9
            })
        
        self.assertEqual(r.json()['Error'],'O Id da classe não existe.')

        r = requests.post('http://localhost:5000/alunos',json={
            "name": "Diego",
            "class_id": 50, 
            "born_date": "2002-06-28", 
            "first_grade": 10, 
            "second_grade": 9
            })
        
        self.assertEqual(r.json()['Error'],'O Id da classe não existe.')

    # ---- Testa se o POST da rota /professores está adicionando os professores ---- #
    def test_011_adiciona_professores(self):
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        requests.post('http://localhost:5000/professores',json={
            "name": "Odair",
            "age": 26,
            "subject": "DevOps",
            "info": "Usa óculos"
            })
        
        r_lista = requests.get('http://localhost:5000/professores')
        lista_retornada = r_lista.json()

        achei_caio = False
        achei_odair = False
        for professor in lista_retornada:
            if professor['name'] == 'Caio':
                achei_caio = True
            if professor['name'] == 'Odair':
                achei_odair = True
        
        if not achei_caio:
            self.fail('Professor Caio não apareceu na lista de professores')
        if not achei_odair:
            self.fail('Professor Odair não apareceu na lista de professores')
            
    # ---- Testa se o GET da rota /professores devolve o professor do id selecionado ---- #
    def test_012_professor_por_id(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        requests.post('http://localhost:5000/professores',json={
            "name": "Odair",
            "age": 26,
            "subject": "DevOps",
            "info": "Usa óculos"
            })

        resposta = requests.get('http://localhost:5000/professores/2')
        dict_retornado = resposta.json()
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('name',dict_retornado)
        
        self.assertEqual(dict_retornado['name'],'Odair')

    # ---- Testa se o DELETE da rota /professores deleta o professor do id selecionado ---- #
    def test_013_deleta_professores(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        requests.post('http://localhost:5000/professores',json={
            "name": "Odair",
            "age": 26,
            "subject": "DevOps",
            "info": "Usa óculos"
            })
        requests.post('http://localhost:5000/professores',json={
            "name": "Vitor",
            "age": 26,
            "subject": "Banco de Dados",
            "info": "Bombado"
            })
        
        r_lista = requests.get('http://localhost:5000/professores')
        lista_retornada = r_lista.json()
        
        self.assertEqual(len(lista_retornada),3)
        
        requests.delete('http://localhost:5000/professores/2')
        
        r_lista2 = requests.get('http://localhost:5000/professores')
        lista_retornada2 = r_lista2.json()
        
        self.assertEqual(len(lista_retornada2),2) 

        acheiCaio = False
        acheiVitor = False
        for professor in lista_retornada:
            if professor['name'] == 'Caio':
                acheiCaio=True
            if professor['name'] == 'Vitor':
                acheiVitor=True
        if not acheiCaio or not acheiVitor:
            self.fail("Você pode ter deletado o professor errado!")

        requests.delete('http://localhost:5000/professores/1')

        r_lista3 = requests.get('http://localhost:5000/professores')
        lista_retornada3 = r_lista3.json()
        
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['name'] == 'Vitor':
            pass
        else:
            self.fail("Você pode ter deletado o professor errado!")

    # ---- Testa se o PUT da rota /professores atualiza o professor do id selecionado ---- #
    def test_014_edita_professores(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        requests.post('http://localhost:5000/professores',json={
            "name": "Odair",
            "age": 26,
            "subject": "DevOps",
            "info": "Usa óculos"
            })
        
        r_antes = requests.get('http://localhost:5000/professores/2')
        
        self.assertEqual(r_antes.json()['name'],'Odair')

        requests.put('http://localhost:5000/professores/2', json={
            "name": "Vitor",
            "age": 32,
            "subject": "Banco de Dados",
            "info": "Bombado"
            })
        
        r_depois = requests.get('http://localhost:5000/professores/2')
        
        self.assertEqual(r_depois.json()['name'],'Vitor')
        self.assertEqual(r_depois.json()['age'],32)

    # ---- Testa se o GET retorna todos os professores ---- #
    def test_015_retorna_todos_professores(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        requests.post('http://localhost:5000/professores',json={
            "name": "Odair",
            "age": 26,
            "subject": "DevOps",
            "info": "Usa óculos"
            })
  
        acheiCaio = False
        acheiOdair = False

        r_lista = requests.get('http://localhost:5000/professores')
        lista_retornada = r_lista.json()

        for professor in lista_retornada:
            if professor['name'] == 'Caio':
                acheiCaio=True
            if professor['name'] == 'Odair':
                acheiOdair=True
        if not acheiCaio or not acheiOdair:
            self.fail("Não retornou todos os professores")

        self.assertEqual(len(lista_retornada),2)

    # ---- Testa se as rotas em que precisa passar um id retorna o erro falando que não existe o id selecionado ---- #
    def test_016_id_inexistente_professores(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Rota PUT ---- #
        r = requests.put('http://localhost:5000/professores/30',json={
            "name": "Odair",
            "age": 26,
            "subject": "DevOps",
            "info": "Usa óculos"
            })

        self.assertEqual(r.json()['Error'],'O professor que você quer atualizar não foi encontrado.')

        # ---- Rota GET ---- #
        r = requests.get('http://localhost:5000/professores/50')
        
        self.assertEqual(r.json()['Error'],'O professor não foi encontrado.')

        # ---- Rota DELETE ---- #
        r = requests.delete('http://localhost:5000/professores/50')
        
        self.assertEqual(r.json()['Error'],'O professor que você quer deletar não foi encontrado.')

    # ---- Testa se o PUT e o POST retornam o erro que as chaves não podem tem valores vazios ---- #
    def test_017_atualiza_ou_adiciona_professor_com_valores_vazios(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })

        # ---- Chave name com valor vazio ---- #
        r = requests.put('http://localhost:5000/professores/1',json={
            "name": "",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        self.assertEqual(r.json()['Error'],'As chaves não podem estar vazias.')

        # ---- Chave subject com valor vazio ---- #
        r = requests.post('http://localhost:5000/professores',json={
            "name": "Odair",
            "age": 26,
            "subject": "",
            "info": "Usa óculos"
            })
        
        self.assertEqual(r.json()['Error'],'As chaves não podem estar vazias.')

    # ---- Testa se o PUT e o POST retornam o erro que está faltando alguma chave no request ---- #
    def test_018_atualiza_ou_adiciona_professor_sem_alguma_chave(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        
        # ---- PUT sem a chave info ---- #
        r = requests.put('http://localhost:5000/professores/1',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços"
            })
        
        self.assertEqual(r.json()['Error'],'Você não passou alguma chave.')
        
        # ---- POST sem a chave age ---- #
        r = requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        self.assertEqual(r.json()['Error'],'Você não passou alguma chave.')

    # ---- Testa se o POST da rota /turmas está adicionando as turmas ---- #
    def test_019_adiciona_turmas(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turmas ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        requests.post('http://localhost:5000/turmas',json={
            "name": "DevOps",
            "professor_id": 1,
            "active": True
            })
        
        
        r_lista = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista.json()

        achei_api = False
        achei_devops = False
        for turma in lista_retornada:
            if turma['name'] == 'API e Microserviços':
                achei_api = True
            if turma['name'] == 'DevOps':
                achei_devops = True
        
        if not achei_api:
            self.fail('Turma API e Microserviços não apareceu na lista de turmas')
        if not achei_devops:
            self.fail('Turma DevOps não apareceu na lista de turmas')
            
    # ---- Testa se o GET da rota /turmas devolve a turma do id selecionado ---- #
    def test_020_turma_por_id(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turmas ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        requests.post('http://localhost:5000/turmas',json={
            "name": "DevOps",
            "professor_id": 1,
            "active": True
            })

        resposta = requests.get('http://localhost:5000/turmas/2')
        dict_retornado = resposta.json()
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('name',dict_retornado)
        
        self.assertEqual(dict_retornado['name'],'DevOps')

    # ---- Testa se o DELETE da rota /turmas deleta a turma do id selecionado ---- #
    def test_021_deleta_turmas(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        
        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turmas ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        requests.post('http://localhost:5000/turmas',json={
            "name": "DevOps",
            "professor_id": 1,
            "active": True
            })
        requests.post('http://localhost:5000/turmas',json={
            "name": "Banco de Dados",
            "professor_id": 1,
            "active": True
            })
        
        r_lista = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista.json()
        
        self.assertEqual(len(lista_retornada),3)
        
        requests.delete('http://localhost:5000/turmas/2')
        
        r_lista2 = requests.get('http://localhost:5000/turmas')
        lista_retornada2 = r_lista2.json()
        
        self.assertEqual(len(lista_retornada2),2) 

        acheiApi = False
        acheiBD = False
        for turma in lista_retornada:
            if turma['name'] == 'API e Microserviços':
                acheiApi=True
            if turma['name'] == 'Banco de Dados':
                acheiBD=True
        if not acheiApi or not acheiBD:
            self.fail("Você pode ter deletado a turma errada!")

        requests.delete('http://localhost:5000/turmas/1')

        r_lista3 = requests.get('http://localhost:5000/turmas')
        lista_retornada3 = r_lista3.json()
        
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['name'] == 'Banco de Dados':
            pass
        else:
            self.fail("Você pode ter deletado a turma errada!")

    # ---- Testa se o PUT da rota /turmas atualiza a turma do id selecionado ---- #
    def test_022_edita_turmas(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turmas ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        requests.post('http://localhost:5000/turmas',json={
            "name": "DevOps",
            "professor_id": 1,
            "active": True
            })
        
        r_antes = requests.get('http://localhost:5000/turmas/2')
        
        self.assertEqual(r_antes.json()['name'],'DevOps')

        requests.put('http://localhost:5000/turmas/2', json={
            "name": "Banco de Dados",
            "professor_id": 1,
            "active": True
            })
        
        r_depois = requests.get('http://localhost:5000/turmas/2')
        
        self.assertEqual(r_depois.json()['name'],'Banco de Dados')

    # ---- Testa se o GET retorna todas as turmas ---- #
    def test_023_retorna_todas_turmas(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turmas ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        requests.post('http://localhost:5000/turmas',json={
            "name": "DevOps",
            "professor_id": 1,
            "active": True
            })
  
        acheiApi = False
        acheiDevOps = False

        r_lista = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista.json()

        for turma in lista_retornada:
            if turma['name'] == 'API e Microserviços':
                acheiApi=True
            if turma['name'] == 'DevOps':
                acheiDevOps=True
        if not acheiApi or not acheiDevOps:
            self.fail("Não retornou todas as turmas")

        self.assertEqual(len(lista_retornada),2)

    # ---- Testa se as rotas em que precisa passar um id retorna o erro falando que não existe o id selecionado ---- #
    def test_024_id_inexistente_turmas(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        
        # ---- Rota PUT ---- #
        r = requests.put('http://localhost:5000/turmas/30',json={
            "name": "DevOps",
            "professor_id": 1,
            "active": True
            })

        self.assertEqual(r.json()['Error'],'A turma que você quer atualizar não foi encontrada.')

        # ---- Rota GET ---- #
        r = requests.get('http://localhost:5000/turmas/50')
        
        self.assertEqual(r.json()['Error'],'A turma não foi encontrada.')

        # ---- Rota DELETE ---- #
        r = requests.delete('http://localhost:5000/turmas/50')
        
        self.assertEqual(r.json()['Error'],'A turma que você quer deletar não foi encontrada.')

    # ---- Testa se o PUT e o POST retornam o erro que as chaves não podem tem valores vazios ---- #
    def test_025_atualiza_ou_adiciona_turma_com_valores_vazios(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        # ---- Chave name com valor vazio ---- #
        r = requests.put('http://localhost:5000/turmas/1',json={
            "name": "",
            "professor_id": 1,
            "active": True
            })
        
        self.assertEqual(r.json()['Error'],'As chaves não podem estar vazias.')

        # ---- Chave name com valor vazio ---- #
        r = requests.post('http://localhost:5000/turmas',json={
            "name": "",
            "professor_id": 1,
            "active": True
            })
        
        self.assertEqual(r.json()['Error'],'As chaves não podem estar vazias.')

    # ---- Testa se o PUT e o POST retornam o erro que está faltando alguma chave no request ---- #
    def test_026_atualiza_ou_adiciona_turma_sem_alguma_chave(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        
        # ---- PUT sem a chave professor_id ---- #
        r = requests.put('http://localhost:5000/turmas/1',json={
            "name": "API e Microserviços",
            "active": True
            })
        
        self.assertEqual(r.json()['Error'],'Você não passou alguma chave.')
        
        # ---- POST sem a chave active ---- #
        r = requests.post('http://localhost:5000/turmas',json={
            "name": "API e Microserviços",
            "professor_id": 1
            })
        
        self.assertEqual(r.json()['Error'],'Você não passou alguma chave.')

    # ---- Teste para ver se retorna o erro que o id do professor passado não existe ---- #
    def test_027_atualiza_ou_adiciona_turma_com_professor_inexistente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })

        r = requests.put('http://localhost:5000/turmas/1',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 20,
            "active": True
            })
        
        self.assertEqual(r.json()['Error'],'O Id do professor não existe.')

        r = requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 50,
            "active": True
            })
        
        self.assertEqual(r.json()['Error'],'O Id do professor não existe.')

    # ---- Teste para ver se o método calculate_age da classe Student está calculando a idade de forma correta ---- #
    def test_028_calculo_idade_do_aluno(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        
        # ---- Adicionando aluno ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Fábio",
            "class_id": 1, 
            "born_date": "2004-09-18", 
            "first_grade": 2, 
            "second_grade": 4
            })
        
        r = requests.get('http://localhost:5000/alunos/1')
        
        self.assertEqual(r.json()['age'],20)

    # ---- Teste para ver se o erro de data de nascimento em formato errado é disparado ---- #
    def test_029_data_de_nascimento_em_formato_errado(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        
        # ---- Adicionando aluno ---- #
        r = requests.post('http://localhost:5000/alunos',json={
            "name": "Fábio",
            "class_id": 1, 
            "born_date": "18/09/2004", 
            "first_grade": 2, 
            "second_grade": 4
            })
        
        self.assertEqual(r.json()['Error'],'A data está escrita de forma errada, o certo é yyyy-mm-dd.')

    # ---- Teste para ver se a média final está sendo calculada corretamante ---- #
    def test_030_calculo_de_media_final(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        # ---- Adicionando professor ---- #
        requests.post('http://localhost:5000/professores',json={
            "name": "Caio",
            "age": 26,
            "subject": "API e Microserviços",
            "info": "Tem tatuagem"
            })
        
        # ---- Adicionando turma ---- #
        requests.post('http://localhost:5000/turmas',json={
            "name": "Desenvolvimento de API e Microserviços",
            "professor_id": 1,
            "active": True
            })
        
        # ---- Adicionando aluno ---- #
        requests.post('http://localhost:5000/alunos',json={
            "name": "Fábio",
            "class_id": 1, 
            "born_date": "2004-09-18", 
            "first_grade": 7.5, 
            "second_grade": 4.5
            })
        
        r = requests.get('http://localhost:5000/alunos/1')
        
        self.assertEqual(r.json()['final_average'],6)

    # ---- Testes de integração ---- #

    # ---- SetUp ---- #
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    # ---- Teste para ver se o professor está sendo criado corretamente no banco de dados ---- #
    def test_031_criacao_professor_no_bd(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        professor = Professor('Caio', 26, 'API e Microserviços', 'Tem tatuagem')
        db.session.add(professor)
        db.session.commit()

        r = Professor.query.first()
        self.assertEqual(r.name,'Caio')
        self.assertEqual(r.subject,'API e Microserviços')

    # ---- Teste para ver se a turma está sendo criada corretamente no banco de dados ---- #
    def test_032_criacao_turma_no_bd(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        professor = Professor('Caio', 26, 'API e Microserviços', 'Tem tatuagem')
        db.session.add(professor)
        db.session.commit()

        classroom = Classroom('Desenvolvimento de API e Microserviços', 1, True)
        db.session.add(classroom)
        db.session.commit()

        r = Classroom.query.first()
        self.assertEqual(r.name,'Desenvolvimento de API e Microserviços')
        self.assertEqual(r.active,True)

    # ---- Teste para ver se o aluno está sendo criado corretamente no banco de dados ---- #
    def test_033_criacao_aluno_no_bd(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        professor = Professor('Caio', 26, 'API e Microserviços', 'Tem tatuagem')
        db.session.add(professor)
        db.session.commit()

        classroom = Classroom('Desenvolvimento de API e Microserviços', 1, True)
        db.session.add(classroom)
        db.session.commit()

        student = Student('Diego', 1, '2002-06-28', 8, 6)
        db.session.add(student)
        db.session.commit()

        r = Student.query.first()
        self.assertEqual(r.name,'Diego')
        self.assertEqual(r.age,22)
        self.assertEqual(r.final_average,7)

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)

if __name__ == '__main__':
    runTests()