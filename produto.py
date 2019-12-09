from pymongo import MongoClient
from flask import Flask, render_template, request


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


@app.route('/')
def index():    

    lista = []

    documents = collection.find()
    
    for document in documents:

        p = Produto(str(document['nome']), str(document['quantidade']), str(document['valor']), str(document['_id']))
        
        lista.append(p)            
    
    return render_template('lista.html', titulo='produtos', produtos=lista)

@app.route('/novo')
def novo():

    lista = []

    documents = collection.find()
    
    for document in documents:
        p = Produto(str(document['nome']), str(document['quantidade']), str(document['valor']), str(document['_id']))
        
        lista.append(p)

    return render_template('novo.html', titulo='Novo Produto', produtos=lista)


@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    quantidade = request. form['quantidade']
    valor = request. form['valor']
    #produto = Produto(nome, quantidade, valor, str(id))
    #lista.append(produto)

    prod = {"nome": nome, "quantidade": quantidade, "valor": valor }

    collection.insert_one(prod)

    lista = []

    documents = collection.find()
    
    for document in documents:
        p = Produto(str(document['nome']), str(document['quantidade']), str(document['valor']), str(document['_id']))
        
        lista.append(p)




    return render_template('novo.html', titulo='Produto', produtos=lista)

#------------------------EDITAR-----------------------------------
@app.route('/editar/<id>')
def editar(id):

    print("ID para ser atualizado: " + id)
    
    p = collection.find_one({"_id":id})

    produto = Produto(str(p['nome']), str(p['quantidade']), str(p['valor']), str(p['_id']))


    return render_template('editar.html', titulo='Editando Produto', produto=produto )


@app.route('/atualizar', methods=['POST',])
def atualizar():
  pass
#---------------------------------------------

@app.route('/deletar')
def deletar(id):

    print('aki01...')

    collection.delete_one(id)

    return render_template('novo.html', titulo='Produto', produtos=lista) 




@app.route('/limpar')
def limpar():

    print('aki01...')

    return render_template('lista.html', titulo='produtos', produtos=lista) 



app.run(debug=True)
