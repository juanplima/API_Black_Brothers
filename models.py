from extensions import db

# Base para todos os modelos com método to_dict
class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Estado(BaseModel):
    __tablename__ = 'Estado'
    ID_Estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(200), nullable=False)

class Cidade(BaseModel):
    __tablename__ = 'Cidade'
    ID_Cidade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(200), nullable=False)
    FK_Estado_ID = db.Column(db.Integer, db.ForeignKey('Estado.ID_Estado'), nullable=False)

class Bairro(BaseModel):
    __tablename__ = 'Bairro'
    ID_Bairro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(2000), nullable=False)
    FK_Cidade_ID = db.Column(db.Integer, db.ForeignKey('Cidade.ID_Cidade'), nullable=False)

class CEP(BaseModel):
    __tablename__ = 'CEP'
    ID_CEP = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numeroCEP = db.Column(db.String(20), nullable=False)
    FK_Bairro_ID = db.Column(db.Integer, db.ForeignKey('Bairro.ID_Bairro'), nullable=False)

class Tipo_Endereco(BaseModel):
    __tablename__ = 'Tipo_Endereco'
    ID_Tipo_END = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descricao = db.Column(db.String(1000), nullable=False)

class Endereco(BaseModel):
    __tablename__ = 'Endereco'
    ID_Endereco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Logradouro = db.Column(db.String(100), nullable=False)
    Numero = db.Column(db.String(10), nullable=False)
    Complemento = db.Column(db.String(100))
    FK_CEP_ID = db.Column(db.Integer, db.ForeignKey('CEP.ID_CEP'), nullable=False)
    FK_Tipo_End = db.Column(db.Integer, db.ForeignKey('Tipo_Endereco.ID_Tipo_END'), nullable=False)

class Academia(BaseModel):
    __tablename__ = 'Academia'
    CNPJ = db.Column(db.String(14), primary_key=True)  # CNPJ sem máscara = 14 dígitos
    Nome = db.Column(db.String(100), nullable=False)
    FK_Endereco_ID = db.Column(db.Integer, db.ForeignKey('Endereco.ID_Endereco'), nullable=False)

class Tipo_Telefone(BaseModel):
    __tablename__ = 'Tipo_Telefone'
    ID_TipoTEL = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descricao = db.Column(db.String(100), nullable=False)

class Pessoa(BaseModel):
    __tablename__ = 'Pessoa'
    CPF = db.Column(db.String(11), primary_key=True)  # CPF sem máscara = 11 dígitos
    Nome = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    DtNasc = db.Column(db.Date, nullable=False)
    FK_Academia_ID = db.Column(db.String(14), db.ForeignKey('Academia.CNPJ'), nullable=False)

class Telefone(BaseModel):
    __tablename__ = 'Telefone'
    ID_Telefone = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Telefone01 = db.Column(db.String(11), nullable=False)
    Telefone02 = db.Column(db.String(11))
    FK_CPF = db.Column(db.String(11), db.ForeignKey('Pessoa.CPF'), nullable=False)
    FK_TipoTel_ID = db.Column(db.Integer, db.ForeignKey('Tipo_Telefone.ID_TipoTEL'), nullable=False)

class Usuario(BaseModel):
    __tablename__ = 'Usuario'
    ID_Usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Login = db.Column(db.String(250), nullable=False)
    Senha = db.Column(db.String(250), nullable=False)
    FK_Pessoa_ID = db.Column(db.String(11), db.ForeignKey('Pessoa.CPF'), nullable=False)

class Cargo(BaseModel):
    __tablename__ = 'Cargo'
    ID_Cargo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Cargo = db.Column(db.String(1000), nullable=False)
    Atuacao = db.Column(db.String(1000), nullable=False)

class Empregado(BaseModel):
    __tablename__ = 'Empregado'
    ID_Empregado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Carga_Horaria = db.Column(db.Integer, nullable=False)
    Salario = db.Column(db.Numeric(10, 2), nullable=False)
    Descricao = db.Column(db.String(1000))
    FK_Usuario_ID = db.Column(db.Integer, db.ForeignKey('Usuario.ID_Usuario'), nullable=False)
    FK_Cargo_ID = db.Column(db.Integer, db.ForeignKey('Cargo.ID_Cargo'), nullable=False)

class Dieta(BaseModel):
    __tablename__ = 'Dieta'
    ID_Dieta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(200), nullable=False)
    Titulo_Refeicao = db.Column(db.String(1000), nullable=False)
    Descricao_Refeicao = db.Column(db.Text, nullable=False)
    FK_Empregado_ID = db.Column(db.Integer, db.ForeignKey('Empregado.ID_Empregado'), nullable=False)

# Em models.py
class Treino(BaseModel):
    __tablename__ = 'Treino'
    ID_Treino = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(1000), nullable=False)
    # Exercicio_Concluido = db.Column(db.Text, nullable=False)  comentado pq nao existe no banco
    # Video = db.Column(db.String(2400)) comentado pq nao existe no banco
    FK_Empregado_ID = db.Column(db.Integer, db.ForeignKey('Empregado.ID_Empregado'), nullable=True)

class Tipo_Pagamento(BaseModel):
    __tablename__ = 'Tipo_Pagamento'
    ID_Forma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descricao = db.Column(db.String(100), nullable=False)

class Tipo_Plano(BaseModel):
    __tablename__ = 'Tipo_Plano'
    ID_TipoPlanos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(1000), nullable=False)
    Preco = db.Column(db.Numeric(5, 2), nullable=False)
    Beneficios = db.Column(db.String(1000), nullable=False)

class Plano(BaseModel):
    __tablename__ = 'Plano'
    ID_Planos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FK_TipoPlano_ID = db.Column(db.Integer, db.ForeignKey('Tipo_Plano.ID_TipoPlanos'), nullable=False)
    FK_Usuario_ID = db.Column(db.Integer, db.ForeignKey('Usuario.ID_Usuario'), nullable=False)

class Aluno(BaseModel):
    __tablename__ = 'Aluno'
    Matricula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FK_Usuario_ID = db.Column(db.Integer, db.ForeignKey('Usuario.ID_Usuario'), nullable=False)
    FK_Planos_ID = db.Column(db.Integer, db.ForeignKey('Plano.ID_Planos'), nullable=False)
    altura = db.Column(db.Numeric(4, 2), nullable=True)
    peso = db.Column(db.Numeric(5, 2), nullable=True)

class Menu_Principal(BaseModel):
    __tablename__ = 'Menu_Principal'
    ID_Menu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Informacoes = db.Column(db.String(2000), nullable=False)
    Feedbacks = db.Column(db.String(2000))
    Titulo_Video = db.Column(db.String(2000))
    Videos = db.Column(db.String(2200))
    FK_Aluno_ID = db.Column(db.Integer, db.ForeignKey('Aluno.Matricula'), nullable=False)
    FK_Treino_ID = db.Column(db.Integer, db.ForeignKey('Treino.ID_Treino'), nullable=False)

class Comunidade(BaseModel):
    __tablename__ = 'Comunidade'
    ID_Comunidade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Informacoes = db.Column(db.String(2000))
    Feedbacks = db.Column(db.String(2000))
    Titulo_Video = db.Column(db.String(2000))
    Videos = db.Column(db.String(2200))

class Tipo_Feedbacks(BaseModel):
    __tablename__ = 'Tipo_Feedbacks'
    ID_TipoFeedbacks = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Topico = db.Column(db.String(2000), nullable=False)
    Descricao = db.Column(db.String(2200), nullable=False)

class Feedbacks(BaseModel):
    __tablename__ = 'Feedbacks'
    ID_Feedbacks = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FK_TipoFeedbacks_ID = db.Column(db.Integer, db.ForeignKey('Tipo_Feedbacks.ID_TipoFeedbacks'), nullable=False)
