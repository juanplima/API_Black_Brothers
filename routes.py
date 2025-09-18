# routes.py (versão final com rotas compatíveis para web e mobile)

from flask import Blueprint, request, jsonify
from extensions import db
from models import *

routes = Blueprint('routes', __name__)

def register_routes(app, db):
    app.register_blueprint(routes)

# A função genérica continua a mesma, criando rotas para todos os modelos
def generic_crud(model):
    model_name = model.__tablename__

    @routes.route(f"/{model_name}", methods=["GET"])
    def get_all(model=model):
        query = model.query
        for key, value in request.args.items():
            if hasattr(model, key):
                attr = getattr(model, key)
                try:
                    value = int(value)
                except ValueError:
                    pass
                query = query.filter(attr == value)
        records = query.all()
        return jsonify([r.to_dict() for r in records])
    get_all.__name__ = f"get_all_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["GET"])
    def get_one(id, model=model):
        record = model.query.get_or_404(id)
        return jsonify(record.to_dict())
    get_one.__name__ = f"get_one_{model_name}"

    @routes.route(f"/{model_name}", methods=["POST"])
    def create(model=model):
        data = request.json
        record = model(**data)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    create.__name__ = f"create_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["PUT"])
    def update(id, model=model):
        data = request.json
        record = model.query.get_or_404(id)
        for key, value in data.items():
            setattr(record, key, value)
        db.session.commit()
        return jsonify(record.to_dict())
    update.__name__ = f"update_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["DELETE"])
    def delete(id, model=model):
        record = model.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        return '', 204
    delete.__name__ = f"delete_{model_name}"

@routes.route("/Usuario/login", methods=["POST"])
def login_usuario():
    data = request.json
    login = data.get("login")
    senha = data.get("senha")
    if not login or not senha:
        return jsonify({"error": "Campos 'login' e 'senha' são obrigatórios"}), 400
    usuario = Usuario.query.filter_by(Login=login, Senha=senha).first()
    if usuario:
        return jsonify(usuario.to_dict())
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404


# <<< ROTA ESPECIALIZADA E RENOMEADA PARA ALUNOS >>>
@routes.route("/alunos/detalhes", methods=["GET"])
def get_alunos_com_detalhes():
    resultados = db.session.query(
        Aluno, Pessoa, Tipo_Plano
    ).join(
        Usuario, Aluno.FK_Usuario_ID == Usuario.ID_Usuario
    ).join(
        Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF
    ).join(
        Plano, Aluno.FK_Planos_ID == Plano.ID_Planos
    ).join(
        Tipo_Plano, Plano.FK_TipoPlano_ID == Tipo_Plano.ID_TipoPlanos
    ).all()
    lista_de_alunos = []
    for aluno, pessoa, tipo_plano in resultados:
        aluno_data = aluno.to_dict()
        aluno_data['Nome'] = pessoa.Nome 
        aluno_data['Email'] = pessoa.Email
        aluno_data['CPF'] = pessoa.CPF
        aluno_data['Nome_Plano'] = tipo_plano.Nome
        aluno_data['Preco_Plano'] = float(tipo_plano.Preco)
        lista_de_alunos.append(aluno_data)
    return jsonify(lista_de_alunos)


# ROTA PARA OS PLANOS (não precisa renomear, pois não conflita)
@routes.route("/Tipo_Plano", methods=["GET"])
def get_planos_com_detalhes():
    planos_detalhados = Tipo_Plano.query.all()
    return jsonify([plano.to_dict() for plano in planos_detalhados])


# <<< ROTA ESPECIALIZADA E RENOMEADA PARA USUÁRIOS >>>
@routes.route("/usuarios/detalhes", methods=["GET"])
def get_usuarios_com_detalhes():
    resultados = db.session.query(
        Usuario, 
        Pessoa
    ).join(
        Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF
    ).all()

    lista_de_usuarios = []
    for usuario, pessoa in resultados:
        usuario_data = usuario.to_dict()
        usuario_data['Nome'] = pessoa.Nome
        usuario_data['Email'] = pessoa.Email
        usuario_data['CPF'] = pessoa.CPF
        lista_de_usuarios.append(usuario_data)
    return jsonify(lista_de_usuarios)


# Registra todas as rotas CRUD para os modelos genéricos
# <<< MUDANÇA FINAL: TODOS OS MODELOS ESTÃO NA LISTA NOVAMENTE >>>
models_list = [
    Estado, Cidade, Bairro, CEP, Tipo_Endereco, Endereco, Academia,
    Tipo_Telefone, Pessoa, Telefone, Usuario, Cargo, Empregado, Dieta,
    Treino, Tipo_Pagamento, Plano, Tipo_Plano, Aluno, Menu_Principal,
    Comunidade, Feedbacks, Tipo_Feedbacks
]

for m in models_list:
    generic_crud(m)