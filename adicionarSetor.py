import json

def carregar_palavras_chaves():
    with open('palavraschaves.json', 'r') as arquivo:
        return json.load(arquivo)

def salvar_palavras_chaves(dados):
    with open('palavraschaves.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

dados = carregar_palavras_chaves()

novo_setor = 'financeiro'
if novo_setor not in dados['setores']:
    dados['setores'][novo_setor] = {
        'pagamentos': {
            "descricao": "Descrição para pagamentos",
            "link": "https://www.sitefinanceiro.com.br/pagamentos"
        },
        'recebimentos': {
            "descricao": "Descrição para recebimentos",
            "link": "https://www.sitefinanceiro.com.br/recebimentos"
        },
        'balanço': {
            "descricao": "Descrição para balanço",
            "link": "https://www.sitefinanceiro.com.br/balanco"
        }
    }
    salvar_palavras_chaves(dados)
    print(f"Setor '{novo_setor}' adicionado com sucesso.")
else:
    print(f"Setor '{novo_setor}' já existe.")

    salvar_palavras_chaves(dados)