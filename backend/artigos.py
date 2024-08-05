from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

def carregar_palavras_chaves():
    with open('palavraschaves.json', 'r') as arquivo:
        return json.load(arquivo)

def salvar_palavras_chaves(dados):
    with open('palavraschaves.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

@app.route('/')
def index():
    return render_template('interfaceadd.html')

@app.route('/add', methods=['POST'])
def add_article():
    dados = carregar_palavras_chaves()
    
    setor = request.form['setor']
    artigo = request.form['artigo']
    descricao = request.form['descricao']
    link = request.form['link']
    
    if setor not in dados['setores']:
        dados['setores'][setor] = {}

    dados['setores'][setor][artigo] = {
        "descricao": descricao,
        "link": link
    }
    
    salvar_palavras_chaves(dados)
    
    return jsonify({"message": "Artigo adicionado com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)