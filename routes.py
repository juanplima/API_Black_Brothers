from flask import request, jsonify
from app import app, db
from models import *

# Função para criar CRUD genérico
def create_crud_routes(model, model_name):
    # Nome único para os endpoints
    get_all_endpoint = f'get_all_{model_name}'
    get_one_endpoint = f'get_one_{model_name}'
    create_endpoint = f'create_{model_name}'
    update_endpoint = f'update_{model_name}'
    delete_endpoint = f'delete_{model_name}'

    # Rota para buscar todos os registros
    @app.route(f'/{model_name}', methods=['GET'], endpoint=get_all_endpoint)
    def get_all_records():
        data = model.query.all()
        return jsonify([{k: v for k, v in vars(item).items() if k != '_sa_instance_state'} for item in data])

    # Rota para buscar um registro por ID
    @app.route(f'/{model_name}/<int:id>', methods=['GET'], endpoint=get_one_endpoint)
    def get_one_record(id):
        item = model.query.get(id)
        if item:
            return jsonify({k: v for k, v in vars(item).items() if k != '_sa_instance_state'})
        return jsonify({'error': f'{model_name} com ID {id} não encontrado'}), 404

    # Rota para adicionar um novo registro
    @app.route(f'/{model_name}', methods=['POST'], endpoint=create_endpoint)
    def create_record():
        data = request.get_json()
        try:
            new_item = model(**data)
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'success': f'{model_name} criado com sucesso', 'id': new_item.id}), 201
        except Exception as e:
            return jsonify({'error': f'Erro ao criar {model_name}', 'details': str(e)}), 400

    # Rota para atualizar um registro
    @app.route(f'/{model_name}/<int:id>', methods=['PUT'], endpoint=update_endpoint)
    def update_record(id):
        item = model.query.get(id)
        if not item:
            return jsonify({'error': f'{model_name} com ID {id} não encontrado'}), 404
        data = request.get_json()
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify({'success': f'{model_name} atualizado com sucesso'})

    # Rota para deletar um registro
    @app.route(f'/{model_name}/<int:id>', methods=['DELETE'], endpoint=delete_endpoint)
    def delete_record(id):
        item = model.query.get(id)
        if not item:
            return jsonify({'error': f'{model_name} com ID {id} não encontrado'}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': f'{model_name} deletado com sucesso'})

# Criando rotas para todas as tabelas
for model_class in [Estado, Cidade, Bairro, CEP, TipoEndereco, Endereco, Academia, TipoTelefone, 
                    Pessoa, Telefone, Usuario, Cargo, Empregado, Dieta, Treino, TipoPagamento, 
                    TipoPlano, Plano, Aluno, MenuPrincipal, Comunidade, TipoFeedbacks, Feedbacks]:
    create_crud_routes(model_class, model_class.__name__.lower())
