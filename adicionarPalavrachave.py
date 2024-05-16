import json

def carregar_palavras_chaves():
    with open('palavraschaves.json', 'r') as arquivo:
        return json.load(arquivo)

def salvar_palavras_chaves(dados):
    with open('palavraschaves.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

dados = carregar_palavras_chaves()

dados['setores']['compras']['novas-compras'] = {
    "descricao": "Descrição para novas compras",
    "link": "https://www.sitecompras.com.br/novas-compras"
}

salvar_palavras_chaves(dados)