from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, flash, url_for

client = MongoClient('mongodb+srv://fabricio:admin123@cluster0-iehjg.mongodb.net/test?retryWrites=true&w=majority')

db = client['teste']

collection = db['produto']

app = Flask(__name__)

class Produto:
    def __init__(self, nome, quantidade, valor, id):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor


#produto1 = Produto('Produto Inicial 01', '10', '10,00', 0)
#produto2 = Produto('Produto Inicial 02', '10', '20,00', 0)
lista = []

def getProdutos():
    lista = []

    documents = collection.find()
    
    for document in documents:
        p = Produto(str(document['nome']), str(document['quantidade']), str(document['valor']), str(document['_id']))
        
        lista.append(p)

    return lista


@app.route('/')
def index():    

    return render_template('lista.html', titulo='Alterar/Deletar Produtos', produtos=getProdutos())


@app.route('/novo')
def novo():

    return render_template('novo.html', titulo='Cadastrar Produto', produtos=getProdutos())


@app.route('/criar', methods=['POST',])
def criar():
    
    if request.form['submit_button'] == 'acaoLimpar':        
        nome = ''
        quantidade = ''
        valor = ''
        return render_template('novo.html', titulo='Cadastrar Produto')  

    nome = request. form['nome']
    quantidade = request. form['quantidade']
    valor = request. form['valor']
    
    prod = {"nome": nome, "quantidade": quantidade, "valor": valor }

    collection.insert_one(prod)

    return render_template('novo.html', titulo='Cadastrar Produto', produtos=getProdutos())

#------------------------EDITAR-----------------------------------
@app.route('/editar/<id>')
def editar(id):

    #produto: Produto = collection.find_one(id)

    #gambiarra, pois não consegui buscar por id
    documents = collection.find()
    
    for document in documents:
        p = Produto(str(document['nome']), str(document['quantidade']), str(document['valor']), str(document['_id']))
        if p.id == str(id):
            produto = p
            break

    return render_template('editar.html', titulo='Editar Produto', produto=produto )


@app.route('/atualizar', methods=['POST',])
def atualizar():  
    
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    valor = request.form['valor']
    
    p = Produto(nome, quantidade, valor, id=request.form['id'])

    collection.update_one({ "_id": p.id}, {"name": p.nome}, {"quantidade": p.quantidade}, {"valor":p.valor})

    pass

    return redirect(url_for('index'))

#---------------------------------------------
@app.route('/deletar/<id>')
def deletar(id):

    documents = collection.find()
    
    for document in documents:
        p = Produto(str(document['nome']), str(document['quantidade']), str(document['valor']), str(document['_id']))
        if p.id == str(id):            
            break
    
    collection.delete_one({ "nome": p.nome })

    return render_template('lista.html', titulo='Alterar/Deletar Produtos', produtos=getProdutos())

#------------------------------------------------------------------------------------------------------------------

@app.route('/limpar', methods=['POST',])
def limpar():
    
    return render_template('lista.html', titulo='Produtos', produtos=lista) 

#-------------------------------------------------------------------------------------------------------------

@app.route('/home')
def home():
    
    return render_template('home.html', titulo='Seja Bem Vindo') 

#----------------------------------------------------------------------------

app.run(debug=True)
