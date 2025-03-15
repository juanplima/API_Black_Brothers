from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Estado(db.Model):
    ID_Estado = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)

class Cidade(db.Model):
    ID_Cidade = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)
    FK_Estado_ID = db.Column(db.Integer, db.ForeignKey('estado.ID_Estado'), nullable=False)

class Bairro(db.Model):
    ID_Bairro = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(2000), nullable=False)
    FK_Cidade_ID = db.Column(db.Integer, db.ForeignKey('cidade.ID_Cidade'), nullable=False)

class CEP(db.Model):
    ID_CEP = db.Column(db.Integer, primary_key=True)
    numeroCEP = db.Column(db.String(20), nullable=False)
    FK_Bairro_ID = db.Column(db.Integer, db.ForeignKey('bairro.ID_Bairro'), nullable=False)

class TipoEndereco(db.Model):
    ID_Tipo_END = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(1000), nullable=False)

class Endereco(db.Model):
    ID_Endereco = db.Column(db.Integer, primary_key=True)
    Logradouro = db.Column(db.String(100), nullable=False)
    Numero = db.Column(db.String(10), nullable=False)
    Complemento = db.Column(db.String(100))
    FK_CEP_ID = db.Column(db.Integer, db.ForeignKey('cep.ID_CEP'), nullable=False)
    FK_Tipo_End = db.Column(db.Integer, db.ForeignKey('tipo_endereco.ID_Tipo_END'), nullable=False)

class Academia(db.Model):
    CNPJ = db.Column(db.BigInteger, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    FK_Endereco_ID = db.Column(db.Integer, db.ForeignKey('endereco.ID_Endereco'), nullable=False)

class TipoTelefone(db.Model):
    ID_TipoTEL = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(100), nullable=False)

class Pessoa(db.Model):
    CPF = db.Column(db.BigInteger, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    DtNasc = db.Column(db.Date, nullable=False)
    FK_Academia_ID = db.Column(db.BigInteger, db.ForeignKey('academia.CNPJ'), nullable=False)

class Telefone(db.Model):
    ID_Telefone = db.Column(db.Integer, primary_key=True)
    Telefone01 = db.Column(db.String(11), nullable=False)
    Telefone02 = db.Column(db.String(11))
    FK_CPF = db.Column(db.BigInteger, db.ForeignKey('pessoa.CPF'), nullable=False)
    FK_TipoTel_ID = db.Column(db.Integer, db.ForeignKey('tipo_telefone.ID_TipoTEL'), nullable=False)

class Usuario(db.Model):
    ID_Usuario = db.Column(db.Integer, primary_key=True)
    Login = db.Column(db.String(250), nullable=False)
    Senha = db.Column(db.String(250), nullable=False)
    FK_Pessoa_ID = db.Column(db.BigInteger, db.ForeignKey('pessoa.CPF'), nullable=False)

class Cargo(db.Model):
    ID_Cargo = db.Column(db.Integer, primary_key=True)
    Nome_Cargo = db.Column(db.String(1000), nullable=False)
    Atuacao = db.Column(db.String(1000), nullable=False)

class Empregado(db.Model):
    ID_Empregado = db.Column(db.Integer, primary_key=True)
    Carga_Horaria = db.Column(db.Integer, nullable=False)
    Salario = db.Column(db.Numeric(10, 2), nullable=False)
    Descricao = db.Column(db.String(1000))
    FK_Usuario_ID = db.Column(db.Integer, db.ForeignKey('usuario.ID_Usuario'), nullable=False)
    FK_Cargo_ID = db.Column(db.Integer, db.ForeignKey('cargo.ID_Cargo'), nullable=False)

class Dieta(db.Model):
    ID_Dieta = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)
    Titulo_Refeicao = db.Column(db.String(1000), nullable=False)
    Descricao_Refeicao = db.Column(db.Text, nullable=False)
    FK_Empregado_ID = db.Column(db.Integer, db.ForeignKey('empregado.ID_Empregado'), nullable=False)

class Treino(db.Model):
    ID_Treino = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(1000), nullable=False)
    Exercicio_Concluido = db.Column(db.Text, nullable=False)
    Video = db.Column(db.String(2400))
    FK_Empregado_ID = db.Column(db.Integer, db.ForeignKey('empregado.ID_Empregado'), nullable=False)

class TipoPagamento(db.Model):
    ID_Forma = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(100), nullable=False)

class TipoPlano(db.Model):
    ID_TipoPlanos = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(1000), nullable=False)
    Preco = db.Column(db.Numeric(5, 2), nullable=False)
    Beneficios = db.Column(db.String(1000), nullable=False)

class Plano(db.Model):
    ID_Planos = db.Column(db.Integer, primary_key=True)
    FK_TipoPlano_ID = db.Column(db.Integer, db.ForeignKey('tipo_plano.ID_TipoPlanos'), nullable=False)

class Aluno(db.Model):
    Matricula = db.Column(db.Integer, primary_key=True)
    FK_Usuario_ID = db.Column(db.Integer, db.ForeignKey('usuario.ID_Usuario'), nullable=False)
    FK_Planos_ID = db.Column(db.Integer, db.ForeignKey('plano.ID_Planos'), nullable=False)

class MenuPrincipal(db.Model):
    ID_Menu = db.Column(db.Integer, primary_key=True)
    Informacoes = db.Column(db.String(2000), nullable=False)
    Feedbacks = db.Column(db.String(2000))
    Titulo_Video = db.Column(db.String(2000))
    Videos = db.Column(db.String(2200))
    FK_Aluno_ID = db.Column(db.Integer, db.ForeignKey('aluno.Matricula'), nullable=False)
    FK_Treino_ID = db.Column(db.Integer, db.ForeignKey('treino.ID_Treino'), nullable=False)

class Comunidade(db.Model):
    ID_Comunidade = db.Column(db.Integer, primary_key=True)
    Informacoes = db.Column(db.String(2000))
    Feedbacks = db.Column(db.String(2000))
    Titulo_Video = db.Column(db.String(2000))
    Videos = db.Column(db.String(2200))

class TipoFeedbacks(db.Model):
    ID_TipoFeedbacks = db.Column(db.Integer, primary_key=True)
    Topico = db.Column(db.String(2000), nullable=False)
    Descricao = db.Column(db.String(2200), nullable=False)

class Feedbacks(db.Model):
    ID_Feedbacks = db.Column(db.Integer, primary_key=True)
    FK_TipoFeedbacks_ID = db.Column(db.Integer, db.ForeignKey('tipo_feedbacks.ID_TipoFeedbacks'), nullable=False)
