Sistema de Gerenciamento Escolar - API Principal (Alunos, Professores e Turmas)
Este repositório contém a API principal do sistema de gerenciamento escolar, responsável pelo cadastro e manutenção de alunos, professores e turmas. Esta API integra um ecossistema de microsserviços que inclui também os serviços de reserva de salas e atividades realizadas por professores.

Descrição da API
A API principal fornece endpoints RESTful para:

✅ Criar, listar, atualizar e deletar alunos

✅ Criar, listar, atualizar e deletar professores

✅ Criar, listar, atualizar e deletar turmas

🔄 Associar alunos a turmas e professores a turmas

Ela serve como núcleo do sistema, armazenando as entidades principais e fornecendo dados de base para os demais microsserviços.

Instruções de Execução com Docker
Pré-requisitos
Docker

Docker Compose

Como executar o projeto
Clone o repositório:
git clone https://github.com/KaioMungo/ProjetoFlask.git cd ProjetoFlask

Execute os serviços com Docker Compose:
docker-compose up --build

Acesse a API em:

http://localhost:5000


Endpoints disponíveis

/alunos (GET, POST)

/alunos/<id> (GET, PUT, DELETE)

/professores (GET, POST)

/professores/<id> (GET, PUT, DELETE)

/turmas (GET, POST)

/turmas/<id> (GET, PUT, DELETE)


Este sistema utiliza uma arquitetura baseada em:

1- Flask + Flask-SQLAlchemy: para a API principal e manipulação do banco de dados relacional

2- Blueprints: para modularização das rotas por entidade (alunos, professores, turmas)

3- Docker e Docker Compose: para ambiente isolado e reprodutível

4- SQLite/PostgreSQL: como banco de dados (dependendo do ambiente de desenvolvimento)

Estruturas de pastas
api-principal/ │ ├── aluno/ ├── instance/
├── professor/
├── reseta/
├── swagger/ ├── turma/
│ ├── Dockerfile ├── app.py ├── config.py ├── errors.py ├── README.md ├── render.yaml ├── requirements.txt └── tests.py

Integração com o ecossitemas de Microsserviços
O sistema foi desenvolvido com com uma arquitetura de microsserviços, cada um com a sua função e responsabilidades distintas:

1. API Principal (este repositório)
Responsável pelas entidades centrais: alunos, professores, turmas
Fornece dados de base para os outros serviços

2. API de Reserva de Salas
Gerencia reservas de salas para as turmas cadastradas na API principal
Comunicação feita via chamadas HTTP REST
Exemplo de interação: busca dados da turma por ID para associar à reserva

3. API de Atividades dos Professores
Armazena e exibe atividades realizadas pelos professores (ex: aulas, palestras, projetos)
Consome dados da API principal para obter detalhes do professor

Integração entre os serviços

1- Cada microsserviço possui seu próprio banco de dados

2- A comunicação ocorre através de requisições HTTP REST entre os serviços

3- Os serviços podem rodar em contêineres separados e se comunicar via Docker

Contatos
caso tenha duvidas ou sugestões, entre em contato com:

NOMES

Kaio Nogueira Mungo
Diego da Silva Criscuolo
Bruna Bispo Andreata
Luiz Henrique Barros Calazans
Fábio Luiz Garrote Ramaldes

EMAIL

kaio.mungo@aluno.faculdadeimpacta.com.br

diego.criscuolo@aluno.faculdadeimpacta.com.br

bruna.andreata@aluno.faculdadeimpacta.com.br

luiz.calazans@aluno.faculdadeimpacta.com.br

fabio.ramaldes@aluno.faculdadeimpacta.com.br

GITHUB

https://github.com/KaioMungo
https://github.com/Diego09cr
https://github.com/BrunaAndreata
https://github.com/LuizCalazans
https://github.com/FalgasDev

📜 Licença
Este projeto está licenciado sob os contatos acima.
