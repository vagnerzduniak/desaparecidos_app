
import os
from flask import Blueprint, request, jsonify
from models import db, PessoaDesaparecida, Arquivo
from utils import allowed_file
from config import UPLOAD_FOLDER

routes = Blueprint('routes', __name__)

@routes.route('/cadastro', methods=['POST'])
def cadastrar():
    data = request.form
    arquivos = request.files
    pessoa = PessoaDesaparecida(
        nome=data.get('nome'),
        idade=data.get('idade'),
        sexo=data.get('sexo'),
        cidade=data.get('cidade'),
        estado=data.get('estado'),
        data_desaparecimento=data.get('data_desaparecimento'),
        descricao=data.get('descricao'),
        contato=data.get('contato')
    )
    db.session.add(pessoa)
    db.session.commit()

    for tipo in ['foto', 'video', 'audio']:
        for file in request.files.getlist(tipo):
            if file and allowed_file(file.filename):
                filename = file.filename
                pasta = os.path.join(UPLOAD_FOLDER, tipo + 's')
                os.makedirs(pasta, exist_ok=True)
                caminho = os.path.join(pasta, filename)
                file.save(caminho)
                arquivo = Arquivo(tipo=tipo, caminho=caminho, pessoa_id=pessoa.id)
                db.session.add(arquivo)

    db.session.commit()
    return jsonify({'mensagem': 'Cadastro realizado com sucesso!'}), 201

@routes.route('/busca', methods=['GET'])
def buscar():
    nome = request.args.get('nome')
    cidade = request.args.get('cidade')
    estado = request.args.get('estado')

    query = PessoaDesaparecida.query
    if nome:
        query = query.filter(PessoaDesaparecida.nome.ilike(f"%{nome}%"))
    if cidade:
        query = query.filter_by(cidade=cidade)
    if estado:
        query = query.filter_by(estado=estado)

    resultados = []
    for pessoa in query.all():
        resultados.append({
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade,
            'sexo': pessoa.sexo,
            'cidade': pessoa.cidade,
            'estado': pessoa.estado,
            'data_desaparecimento': pessoa.data_desaparecimento,
        })

    return jsonify(resultados)

@routes.route('/pessoa/<int:id>', methods=['GET'])
def ver_pessoa(id):
    pessoa = PessoaDesaparecida.query.get_or_404(id)
    arquivos = [{'tipo': a.tipo, 'caminho': a.caminho} for a in pessoa.arquivos]
    return jsonify({
        'id': pessoa.id,
        'nome': pessoa.nome,
        'idade': pessoa.idade,
        'sexo': pessoa.sexo,
        'cidade': pessoa.cidade,
        'estado': pessoa.estado,
        'data_desaparecimento': pessoa.data_desaparecimento,
        'descricao': pessoa.descricao,
        'contato': pessoa.contato,
        'arquivos': arquivos
    })
