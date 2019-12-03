from pymongo import MongoClient
from flask import Flask, render_template, request


client = MongoClient('mongodb+srv://fabricio:admin123@cluster0-iehjg.mongodb.net/test?retryWrites=true&w=majority')

db = client['teste']

collection = db['produto']

app = Flask(__name__)


class Produto:
    def __init__(self, nome, quantidade, valor):
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor


produto1 = Produto('Produto Inicial 01', '10', '10,00')
produto2 = Produto('Produto Inicial 02', '10', '20,00')
lista = [produto1, produto2]


@app.route('/')
def index():
    return render_template('lista.html', titulo='produtos', produtos=lista)


@app.route('/deletar/<int:id>')
def deletar(id):
    
    collection.delete_one(id)
    return render_template('novo.html', titulo='Produto', produtos=lista)  


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Produto')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    quantidade = request. form['quantidade']
    valor = request. form['valor']
    produto = Produto(nome, quantidade, valor)
    lista.append(produto)

    prod = {"nome": nome, "quantidade": quantidade, "valor": valor }

    collection.insert_one(prod)

    return render_template('novo.html', titulo='Produto', produtos=lista)


app.run(debug=True)
