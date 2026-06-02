# 📊 Sistema de Cobranças & Dashboard Financeiro

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

> Trabalho prático desenvolvido para a avaliação da **AP3** da faculdade. Um sistema web completo para gerenciamento de clientes, controle de cobranças e análise financeira de inadimplência em tempo real.

---

##  Funcionalidades

* **Cadastro de Cobranças:** Interface fluida para inserção de novos registros.
* **Cards Informativos:** Visualização rápida do faturamento (Total Geral, Pago, Inadimplentes e A Cobrar).
* **Tabela Dinâmica:** Listagem automática com foco crítico em clientes inadimplentes (em atraso).
* **Modo Escuro:** Alternância de tema (Claro/Escuro) para melhor usabilidade visual.
* **API JSON:** Integração assíncrona usando `Fetch API` no JavaScript para atualizar dados sem recarregar a página.

---

##  Tecnologias Utilizadas

O ecossistema do projeto foi construído utilizando:
* **Backend:** Python com o micro-framework Flask
* **Banco de Dados:** SQLite (persistência local via Flask-SQLAlchemy)
* **Frontend:** HTML5, CSS3 (Variáveis nativas para o Dark Mode) e JavaScript Moderno (Async/Await)

---

##  Como Rodar o Projeto Localmente

Siga os passos abaixo no terminal para executar a aplicação na sua máquina:

```bash
# 1. Entre na pasta do projeto
cd "TRABALHO AP3"

# 2. Ative o ambiente virtual (Windows)
..\venv\Scripts\activate

# 3. Execute a aplicação Flask
python app.py
