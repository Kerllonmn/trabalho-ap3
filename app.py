from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Inicializa o Flask e configura o banco de dados SQLite
#cd "C:\Users\Kerllon\TRABALHO AP3"
#..\venv\Scripts\activate
#python app.py

app = Flask(__name__)
# O arquivo do banco vai se chamar 'cobrancas.db' e vai sumir na raiz do projeto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cobrancas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desativa um recurso que consome muita memória e não vamos usar
db = SQLAlchemy(app)

# MODELO DE DADOS: Define como as cobranças vão ser armazenadas no banco de dados

class Cobranca(db.Model):
    # Definindo as colunas da tabela
    id = db.Column(db.Integer, primary_key=True) # O ID é gerado automático (1, 2, 3...)
    cliente = db.Column(db.String(100), nullable=False) # Texto de até 100 caracteres, não aceita vazio
    valor = db.Column(db.Float, nullable=False) # Números quebrados (dinheiro)
    vencimento = db.Column(db.String(10), nullable=False) # Salvando a data como texto puro (ex: 2026-06-01)
    status = db.Column(db.String(20), default='Pendente') # Se ninguém falar nada, começa como 'Pendente'
    forma_pagamento = db.Column(db.String(20), nullable=False, default='Pix') # Começa como Pix por padrão

    # Funçãozinha massa para transformar o objeto do banco em um dicionário Python (ajuda a virar JSON depois)
    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.cliente,
            "valor": self.valor,
            "vencimento": self.vencimento,
            "status": self.status,
            "forma_pagamento": self.forma_pagamento
        }


# ROTAS DE PÁGINA (SÓ TRABALHAM COM HTML)


# Rota da página inicial (quando o usuário só digita o endereço do site)
# O render_template vai procurar o arquivo 'index.html' dentro da pasta 'templates' e mostrar ele na tela

@app.route('/')
def pagina_inicial():
    return render_template('index.html') # Vai buscar o arquivo index.html na pasta /templates

# Rota para abrir o dashboard
@app.route('/dashboard')
def pagina_dashboard():
    return render_template('dashboard.html')

# LUGAR ONDE FICA A API (SÓ TRABALHA COM DADOS, SEM HTML)
# Essas rotas são chamadas pelo JavaScript do frontend para criar, ler, atualizar ou deletar cobranças no banco de dados

# GET: Pega todas as cobranças salvas para mostrar na tela

@app.route('/api/cobrancas', methods=['GET'])
def listar_cobrancas():
    # Vai no banco e faz um "SELECT * FROM cobranca"
    cobrancas = db.session.query(Cobranca).all()
    # Converte cada cobrança da lista para dicionário e joga tudo na tela em formato JSON
    return jsonify([c.to_dict() for c in cobrancas]), 200

# POST: Recebe dados do frontend e cria uma cobrança nova no banco
@app.route('/api/cobrancas', methods=['POST'])
def criar_cobranca():
    dados = request.json # Pega o pacote de dados enviado pelo JavaScript
    
    # Monta a nova cobrança usando o que veio do formulário
    nova_cobranca = Cobranca(
        cliente=dados['cliente'],
        valor=float(dados['valor']), # Garante que o valor vai ser tratado como número flutuante
        vencimento=dados['vencimento'],
        forma_pagamento=dados['forma_pagamento']
    )
    
    db.session.add(nova_cobranca) # Prepara para salvar
    db.session.commit() # Salva de verdade no arquivo .db
    return jsonify(nova_cobranca.to_dict()), 201 # Retorna o que foi criado com status 201 (Criado)

# PUT: Atualiza alguma informação. Aqui serve para mudar o status (ex: de Pendente para Pago)
@app.route('/api/cobrancas/<int:id>', methods=['PUT'])
def atualizar_status(id):
    # Procura no banco a cobrança que tem exatamente o ID que veio na URL
    cobranca = db.session.get(Cobranca, id)
    
    # Se não achar nada, avisa o front que deu ruim (Erro 404)
    if not cobranca:
        return jsonify({"erro": "Cobrança não encontrada"}), 404
    
    dados = request.json
    if 'status' in dados:
        cobranca.status = dados['status'] # Troca o status antigo pelo novo que veio na requisição
    
    db.session.commit() # Salva a alteração no banco
    return jsonify(cobranca.to_dict()), 200

# DELETE: Apaga o registro do banco de dados para sempre
@app.route('/api/cobrancas/<int:id>', methods=['DELETE'])
def deletar_cobranca(id):
    cobranca = db.session.get(Cobranca, id)
    
    if not cobranca:
        return jsonify({"erro": "Cobrança não encontrada"}), 404
        
    db.session.delete(cobranca) # Prepara a exclusão
    db.session.commit() # Confirma a exclusão no banco
    return jsonify({"mensagem": "Cobrança deletada"}), 200

#INICIALIZAÇÃO DO BANCO DE DADOS
# O código abaixo é responsável por criar o arquivo do banco de dados e a tabela necessária para armazenar as cobranças, caso eles ainda não existam. Ele roda automaticamente quando o aplicativo é iniciado.


# Isso aqui garante que o arquivo de banco seja criado automaticamente caso ele não exista na primeira vez
with app.app_context():
    db.create_all()

# Liga o servidor se executarmos esse script diretamente pelo comando 'python app.py'
if __name__ == '__main__':
    # debug=True faz o servidor reiniciar sozinho sempre que você salvar uma alteração aqui no código
    app.run(debug=True)