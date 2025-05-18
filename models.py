
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PessoaDesaparecida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(10))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    data_desaparecimento = db.Column(db.String(10))
    descricao = db.Column(db.Text)
    contato = db.Column(db.String(200))
    arquivos = db.relationship('Arquivo', backref='pessoa', lazy=True)

class Arquivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10))  # foto, video, audio
    caminho = db.Column(db.String(200))
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa_desaparecida.id'), nullable=False)
