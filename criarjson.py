import json

# Definindo a estrutura dos dados com descrição e link para cada palavra-chave
dados_iniciais = {
    "setores": {
        "compras": {
            "exportação-NFE": {
                "descricao": "Para mais informações sobre exportação NFE, visite:",
                "link": "https://www.sitegoverno.gov.br/exportacao-nfe"
            },
            "importação": {
                "descricao": "Veja detalhes sobre o processo de importação em:",
                "link": "https://www.sitegoverno.gov.br/importacao"
            },
            "cotação": {
                "descricao": "Informações sobre cotação podem ser encontradas aqui:",
                "link": "https://www.siteempresa.com.br/cotacao"
            }
        },
        "estoque": {
            "inventário": {
                "descricao": "Dicas para gerenciar seu inventário:",
                "link": "https://www.siteempresa.com.br/inventario"
            },
            "reposição": {
                "descricao": "Procedimentos de reposição de estoque:",
                "link": "https://www.siteempresa.com.br/reposicao"
            },
            "logística": {
                "descricao": "Logística e gestão:",
                "link": "https://www.siteempresa.com.br/logistica"
            }
        }
    }
}

# Caminho do arquivo JSON
caminho_do_arquivo = 'palavraschaves.json'

# Criando e salvando os dados no arquivo JSON
with open(caminho_do_arquivo, 'w') as arquivo:
    json.dump(dados_iniciais, arquivo, indent=4)

print(f"Arquivo {caminho_do_arquivo} criado com sucesso com os dados iniciais.")
