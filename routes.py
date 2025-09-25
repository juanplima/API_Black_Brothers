# routes.py (com a nova rota de debug)

from flask import Blueprint, request, jsonify
from extensions import db
from models import *
from sqlalchemy.exc import IntegrityError
from datetime import datetime

routes = Blueprint('routes', __name__)

def register_routes(app, db):
    app.register_blueprint(routes)

# ... (todas as suas outras rotas, como generic_crud, login, get_alunos_com_detalhes, etc., continuam aqui)
def generic_crud(model):
    model_name = model.__tablename__

    @routes.route(f"/{model_name}", methods=["GET"])
    def get_all(model=model):
        query = model.query
        for key, value in request.args.items():
            if hasattr(model, key):
                attr = getattr(model, key)
                try: value = int(value)
                except ValueError: pass
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
        fields = [c.key for c in model.__table__.columns]
        filtered_data = {k: v for k, v in data.items() if k in fields}
        record = model(**filtered_data)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    create.__name__ = f"create_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["PUT"])
    def update(id, model=model):
        data = request.json
        record = model.query.get_or_404(id)
        for key, value in data.items():
            if hasattr(record, key):
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

@routes.route("/alunos/detalhes", methods=["GET"])
def get_alunos_com_detalhes():
    resultados = db.session.query(Aluno, Pessoa, Tipo_Plano).join(Usuario, Aluno.FK_Usuario_ID == Usuario.ID_Usuario).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).join(Plano, Aluno.FK_Planos_ID == Plano.ID_Planos).join(Tipo_Plano, Plano.FK_TipoPlano_ID == Tipo_Plano.ID_TipoPlanos).all()
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

@routes.route("/alunos/from-user", methods=["POST"])
def promover_usuario_a_aluno():
    data = request.json
    required_fields = ['usuarioId', 'planoId']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "ID do usuário e do plano são obrigatórios"}), 400
    try:
        novo_plano = Plano(FK_TipoPlano_ID=data['planoId'], FK_Usuario_ID=data['usuarioId'])
        db.session.add(novo_plano)
        db.session.flush()
        novo_aluno = Aluno(FK_Usuario_ID=data['usuarioId'], FK_Planos_ID=novo_plano.ID_Planos, altura=data.get('altura'), peso=data.get('peso'))
        db.session.add(novo_aluno)
        db.session.commit()
        return jsonify({"message": "Usuário promovido a aluno com sucesso!", "matricula": novo_aluno.Matricula}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Este usuário já é um aluno."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500

@routes.route("/usuarios/nao-alunos", methods=["GET"])
def get_usuarios_nao_alunos():
    try:
        subquery = db.session.query(Aluno.FK_Usuario_ID).subquery()
        resultados = db.session.query(Usuario, Pessoa).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).filter(Usuario.ID_Usuario.notin_(subquery)).all()
        lista_de_usuarios = [{"ID_Usuario": usuario.ID_Usuario, "Nome": pessoa.Nome, "Email": pessoa.Email, "Login": usuario.Login} for usuario, pessoa in resultados]
        return jsonify(lista_de_usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/usuarios/nao-funcionarios", methods=["GET"])
def get_usuarios_nao_funcionarios():
    try:
        subquery = db.session.query(Empregado.FK_Usuario_ID).subquery()
        resultados = db.session.query(Usuario, Pessoa).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).filter(Usuario.ID_Usuario.notin_(subquery)).all()
        lista_de_usuarios = [{"ID_Usuario": usuario.ID_Usuario, "Nome": pessoa.Nome, "Email": pessoa.Email, "Login": usuario.Login} for usuario, pessoa in resultados]
        return jsonify(lista_de_usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/empregados/from-user", methods=["POST"])
def promover_usuario_a_empregado():
    data = request.json
    required_fields = ['usuarioId', 'cargoId', 'salario', 'cargaHoraria']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Campos obrigatórios faltando."}), 400
    try:
        novo_empregado = Empregado(FK_Usuario_ID=data['usuarioId'], FK_Cargo_ID=data['cargoId'], Salario=data['salario'], Carga_Horaria=data['cargaHoraria'], Descricao=data.get('descricao'))
        db.session.add(novo_empregado)
        db.session.commit()
        return jsonify({"message": "Usuário promovido a funcionário com sucesso!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Este usuário já é um funcionário."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500

@routes.route("/Tipo_Plano", methods=["GET"])
def get_planos_com_detalhes():
    planos_detalhados = Tipo_Plano.query.all()
    return jsonify([plano.to_dict() for plano in planos_detalhados])

@routes.route("/usuarios/detalhes", methods=["GET"])
def get_usuarios_com_detalhes():
    resultados = db.session.query(Usuario, Pessoa).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).all()
    lista_de_usuarios = []
    for usuario, pessoa in resultados:
        usuario_data = usuario.to_dict()
        usuario_data['Nome'] = pessoa.Nome
        usuario_data['Email'] = pessoa.Email
        usuario_data['CPF'] = pessoa.CPF
        lista_de_usuarios.append(usuario_data)
    return jsonify(lista_de_usuarios)

@routes.route("/treinos/detalhes", methods=["GET"])
def get_treinos_com_detalhes():
    resultados = db.session.query(Treino, Pessoa).join(Empregado, Treino.FK_Empregado_ID == Empregado.ID_Empregado).join(Usuario, Empregado.FK_Usuario_ID == Usuario.ID_Usuario).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).all()
    lista_de_treinos = []
    for treino, pessoa in resultados:
        treino_data = treino.to_dict()
        treino_data['Nome_Instrutor'] = pessoa.Nome 
        lista_de_treinos.append(treino_data)
    return jsonify(lista_de_treinos)

@routes.route("/empregados/detalhes", methods=["GET"])
def get_empregados_com_detalhes():
    resultados = db.session.query(Empregado, Pessoa).join(Usuario, Empregado.FK_Usuario_ID == Usuario.ID_Usuario).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).all()
    lista_de_empregados = []
    for empregado, pessoa in resultados:
        empregado_data = empregado.to_dict()
        empregado_data['Nome'] = pessoa.Nome
        lista_de_empregados.append(empregado_data)
    return jsonify(lista_de_empregados)


# <<< NOVIDADE AQUI: ROTA DE DEBUG PARA VER A ESTRUTURA DA TABELA >>>
@routes.route("/debug/table/<table_name>", methods=["GET"])
def debug_table_structure(table_name):
    try:
        # Este comando executa um SQL "cru" para descrever a tabela
        # Usamos db.text para segurança contra SQL Injection
        from sqlalchemy import text
        result_proxy = db.session.execute(text(f"DESCRIBE `{table_name}`"))
        
        columns = [row[0] for row in result_proxy] # O nome da coluna é o primeiro item da linha
        
        return jsonify({
            "table_name": table_name,
            "columns_found": columns
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Registra todas as rotas CRUD para os modelos genéricos
models_list = [
    Estado, Cidade, Bairro, CEP, Tipo_Endereco, Endereco, Academia,
    Tipo_Telefone, Pessoa, Telefone, Usuario, Cargo, Empregado, Dieta,
    Tipo_Pagamento, Plano, Tipo_Plano, Aluno, Menu_Principal,
    Comunidade, Feedbacks, Tipo_Feedbacks, Treino
]

for m in models_list:
    generic_crud(m)