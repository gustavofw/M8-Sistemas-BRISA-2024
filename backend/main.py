import spacy
from spacy.symbols import NOUN
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import json
from unidecode import unidecode

app = Flask(__name__)
CORS(app)
nlp = spacy.load("pt_core_news_lg")

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)

# Variável global para rastrear tentativas erradas
tentativas_erradas = 0

def carregar_palavras_chaves():
    with open('palavraschaves.json', 'r') as arquivo:
        return json.load(arquivo)

def normalizar_texto(texto):
    return unidecode(texto.lower())

def encontrar_palavra_chave(texto, palavras_chaves):
    texto_normalizado = normalizar_texto(texto)
    doc = nlp(texto_normalizado)
    setores = palavras_chaves['setores']
    resultados = {'setor': None, 'artigos': []}

    setores_normalizados = {normalizar_texto(setor): setor for setor in setores}
    artigos_normalizados = {}
    for setor, artigos in setores.items():
        for artigo, info in artigos.items():
            artigo_normalizado = normalizar_texto(artigo)
            if artigo_normalizado not in artigos_normalizados:
                artigos_normalizados[artigo_normalizado] = []
            artigos_normalizados[artigo_normalizado].append((artigo, info['descricao'], info['link'], setor))

    for token in doc:
        token_text = token.text
        for setor_normalizado, setor_original in setores_normalizados.items():
            if setor_normalizado in token_text:
                resultados['setor'] = setor_original
                break

    for artigo_normalizado, infos in artigos_normalizados.items():
        if artigo_normalizado in texto_normalizado:
            for artigo, descricao, link, setor in infos:
                resultados['artigos'].append((artigo, descricao, link))
                if not resultados['setor']:
                    resultados['setor'] = setor

    return resultados

@app.route('/process_user_input', methods=['POST'])
def process_user_input():
    global tentativas_erradas

    data = request.json
    if not data or 'texto' not in data:
        return jsonify({'error': 'Nenhum texto fornecido'}), 400
    
    texto_usuario = data['texto']
    palavras_chaves = carregar_palavras_chaves()
    resultado = encontrar_palavra_chave(texto_usuario, palavras_chaves)

    if resultado['artigos']:
        tentativas_erradas = 0
        respostas = [
            {'nome': nome, 'link': link}
            for nome, descricao, link in resultado['artigos']
        ]
        return jsonify({
            'mensagem': "Você mencionou o artigo:",
            'artigos': respostas
        })
    elif resultado['setor']:
        tentativas_erradas = 0
        artigos = [{'nome': nome, 'link': info['link']}
                   for nome, info in palavras_chaves['setores'][resultado['setor']].items()]
        return jsonify({
            'mensagem': f"Você mencionou o setor '{resultado['setor']}'. Os tópicos relacionados incluem:",
            'setor': resultado['setor'],
            'artigos': artigos
        })
    else:
        tentativas_erradas += 1
        if tentativas_erradas >= 5:
            tentativas_erradas = 0
            return jsonify({
                'mensagem': 'Não consegui identificar sua necessidade. <a href="https://wa.me/55498005918503" target="_blank">Clique aqui</a> para uma conversa com nosso suporte humanizado.'
            })
        elif tentativas_erradas == 4:
            return jsonify({'mensagem': "Não consegui identificar sua necessidade. Você poderia especificar mais?"})
        elif tentativas_erradas >= 3:
            setores = [{'nome': nome} for nome in palavras_chaves['setores']]
            return jsonify({
                'mensagem': "Não consegui identificar sua necessidade. Aqui estão todos os setores disponíveis:",
                'setores': [resultado['nome'] for resultado in setores]
            })
        else:
            return jsonify({'mensagem': "Não consegui identificar sua necessidade. Você poderia especificar mais?"})
if __name__ == '__main__':
    app.run(debug=True)
