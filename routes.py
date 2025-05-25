from flask import Blueprint, request, jsonify
from extensions import db
from models import *

routes = Blueprint('routes', __name__)

def register_routes(app, db):
    app.register_blueprint(routes)

def generic_crud(model):
    model_name = model.__tablename__

    @routes.route(f"/{model_name}", methods=["GET"])
    def get_all(model=model):
        query = model.query

        #Aplica filtros com base nos parâmetros de consulta, se nao tiver nenhum parâmetro, retorna todos os registros.
        for key, value in request.args.items():
            #hasattr verifica se o modelo tem o atributo e getattr retorna o objeto em si.
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
    print(">>> ENTROU NA ROTA DE LOGIN <<<")  # <-- log
    
    data = request.json
    login = data.get("login")
    senha = data.get("senha")

    print(f"Login recebido: {login}, Senha recebida: {senha}")

    if not login or not senha:
        return jsonify({"error": "Campos 'login' e 'senha' são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(Login=login, Senha=senha).first()

    if usuario:
        print(">>> USUÁRIO ENCONTRADO <<<")
        return jsonify(usuario.to_dict())
    else:
        print(">>> USUÁRIO NÃO ENCONTRADO <<<")
        return jsonify({"error": "Usuário não encontrado"}), 404


# Registra todas as rotas CRUD para os modelos
models_list = [
    Estado, Cidade, Bairro, CEP, Tipo_Endereco, Endereco, Academia,
    Tipo_Telefone, Pessoa, Telefone, Usuario, Cargo, Empregado, Dieta,
    Treino, Tipo_Pagamento, Plano, Tipo_Plano, Aluno, Menu_Principal,
    Comunidade, Feedbacks, Tipo_Feedbacks
]

for m in models_list:
    generic_crud(m)
