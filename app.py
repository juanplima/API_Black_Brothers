from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Inicializa o Flask
app = Flask(__name__)

# Configura o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u794777727_BlackBrothers1:senhaTopBD157A$@srv1526.hstgr.io:3306/u794777727_BlackBrotherBD'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600  # Tempo de conexão
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa os objetos do SQLAlchemy e Marshmallow sem associá-los ao app ainda
db = SQLAlchemy()
ma = Marshmallow()

# Importa os modelos (antes de inicializar db)
from models import *

# Agora inicializa db e ma com o app
db.init_app(app)
ma.init_app(app)

# Importar as rotas depois da inicialização do app, db e ma
from routes import *

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Roda o app
if __name__ == '__main__':
    app.run(debug=True)

