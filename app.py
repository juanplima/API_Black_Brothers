from flask import Flask
from flask_cors import CORS
from extensions import db 
from routes import register_routes

app = Flask(__name__)
CORS(app)

# Configurações do seu banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u794777727_BlackBrothers1:senhanovaBD157@193.203.175.99/u794777727_BlackBrotherBD'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True
}

# Inicializando o SQLAlchemy com a aplicação Flask
db.init_app(app)

# Registrando as rotas
register_routes(app, db)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

