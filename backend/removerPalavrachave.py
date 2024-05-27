import json

def carregar_palavras_chaves():
    with open('palavraschaves.json', 'r') as arquivo:
        return json.load(arquivo)

def salvar_palavras_chaves(dados):
    with open('palavraschaves.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

dados = carregar_palavras_chaves()

if 'importação' in dados['setores']['compras']:
    del dados['setores']['compras']['importação']

salvar_palavras_chaves(dados)