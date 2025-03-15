Primeiros passos para utilizar a API: 

Faça a instalação das seguintes bibliotecas:

pip install flask 
pip install request
pip install SQLAlchemy
pip install Marshmallow

2- Copie e cole o código em seu repositório. 
3- Abra o terminal do VSCode, e rode o seguinte comando: python app.py
4- Após isso, verifique se a conexão com o Flask foi estabelecida. 

Realização de testes:

1- Faça o download do POSTMAN
2- Crie sua conta e logue 
3- Vai em NEW e depoist HTTP
4- Selecione POST e digite o URL gerado pela sua Flask e adicione /nome-da-tabela, por exemplo http://134.0.0.1:4000/estado 
5- Realize a criação de uma instancia: {
    "ID_Estado": 4,
    "Nome": "Manaus"
}
6- Verifique o LOG e depois o SQL.


