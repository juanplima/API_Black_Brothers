from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Inicializa o Flask
app = Flask(__name__)

# Configura o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u794777727_BlackBrothers:blackjP157@srv1526.hstgr.io:3306/u794777727_BlackBrotherBD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa os objetos do SQLAlchemy e Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Importar as rotas depois da inicialização do app, db e ma
from routes import *

# Roda o app
if __name__ == '__main__':
    app.run(debug=True)

