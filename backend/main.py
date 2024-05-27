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

def carregar_palavras_chaves():
    with open('palavraschaves.json', 'r') as arquivo:
        return json.load(arquivo)

def normalizar_texto(texto):
    return unidecode(texto.lower())

def encontrar_palavra_chave(texto, palavras_chaves):
    texto_normalizado = normalizar_texto(texto)  # Normaliza o texto de entrada
    doc = nlp(texto_normalizado)
    setores = palavras_chaves['setores']
    resultados = {'setor': None, 'artigos': []}

    # Normaliza os nomes dos setores para comparação
    setores_normalizados = {normalizar_texto(setor): setor for setor in setores}
    artigos_normalizados = {}
    for setor, artigos in setores.items():
        for artigo, info in artigos.items():
            artigo_normalizado = normalizar_texto(artigo)
            artigos_normalizados[artigo_normalizado] = (artigo, info['descricao'], info['link'], setor)

    # Verifica se alguma frase no texto corresponde a um setor ou artigo
    for token in doc:
        token_text = token.text
        # Verifica setores
        for setor_normalizado, setor_original in setores_normalizados.items():
            if setor_normalizado in token_text:
                resultados['setor'] = setor_original
                break
        # Verifica artigos
        for artigo_normalizado, (artigo, descricao, link, setor) in artigos_normalizados.items():
            if artigo_normalizado in token_text:
                resultados['artigos'].append((artigo, descricao, link))

    # Se não encontrou nenhum artigo, tenta encontrar pelo menos o setor
    if not resultados['artigos'] and resultados['setor']:
        setor_artigos = setores[resultados['setor']]
        for artigo, info in setor_artigos.items():
            artigo_normalizado = normalizar_texto(artigo)
            if artigo_normalizado in texto_normalizado:
                resultados['artigos'].append((artigo, info['descricao'], info['link']))

    return resultados

@app.route('/process_user_input', methods=['POST'])
def process_user_input():
    data = request.json
    if not data or 'texto' not in data:
        return jsonify({'error': 'Nenhum texto fornecido'}), 400
    
    texto_usuario = data['texto']
    palavras_chaves = carregar_palavras_chaves()
    resultado = encontrar_palavra_chave(texto_usuario, palavras_chaves)

    if resultado['artigos']:
        respostas = [
            f"Artigo: {nome} <a href='{link}' target='_blank'>Clique aqui</a>"
            for nome, descricao, link in resultado['artigos']
        ]
        return jsonify({'respostas': respostas})
    elif resultado['setor']:
        artigos = ', '.join(palavras_chaves['setores'][resultado['setor']].keys())
        return jsonify({'mensagem': f"Você mencionou o setor '{resultado['setor']}'. Os tópicos relacionados incluem: {artigos}. Sobre qual você tem dúvidas?"})
    else:
        return jsonify({'mensagem': "Não consegui identificar sua necessidade. Você poderia especificar mais?"})

if __name__ == '__main__':
    app.run(debug=True)
