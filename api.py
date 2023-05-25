from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))

    def __init__(self, nome):
        self.nome = nome


@app.route('/users', methods=['POST'])
def criar_user():
    nome = request.json['nome']
    user = User(nome)
    db.session.add(user)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário criado com sucesso!'})


@app.route('/users', methods=['GET'])
def listar_users():
    users = User.query.all()
    resultado = []
    for user in users:
        resultado.append({'id': user.id, 'nome': user.nome})
    return jsonify(resultado)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(threaded=True)
