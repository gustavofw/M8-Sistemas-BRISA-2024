import json
import spacy
from unidecode import unidecode

# Carrega o modelo de linguagem
nlp = spacy.load("pt_core_news_lg")

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
    artigos_normalizados = {
        normalizar_texto(artigo): (artigo, info['descricao'], info['link'])
        for setor, artigos in setores.items()
        for artigo, info in artigos.items()
    }

    # Verifica se alguma frase no texto corresponde a um setor ou artigo
    for setor_normalizado, setor_original in setores_normalizados.items():
        if setor_normalizado in texto_normalizado:
            resultados['setor'] = setor_original
            break

    for artigo_normalizado, (artigo, descricao, link) in artigos_normalizados.items():
        if artigo_normalizado in texto_normalizado:
            resultados['artigos'].append((artigo, descricao, link))

    return resultados

def responder_usuario():
    texto_usuario = input("Por favor, digite sua pergunta: ")  # Solicita entrada do usuário
    palavras_chaves = carregar_palavras_chaves()
    resultado = encontrar_palavra_chave(texto_usuario, palavras_chaves)

    if resultado['artigos']:
        respostas = [f"{nome}: {descricao} {link}" for nome, descricao, link in resultado['artigos']]
        return "\n".join(respostas)
    elif resultado['setor']:
        artigos = ', '.join(palavras_chaves['setores'][resultado['setor']].keys())
        return f"Você mencionou o setor '{resultado['setor']}'. Os tópicos relacionados incluem: {artigos}. Sobre qual você tem dúvidas?"
    else:
        return "Não consegui identificar sua necessidade. Você poderia especificar mais?"

def main():
    print("Iniciando o chatbot...")
    while True:
        resposta = responder_usuario()
        print(resposta)
        continuar = input("Deseja continuar? (sim/não): ")
        if continuar.lower() != 'sim':
            print("Encerrando o chatbot...")
            break

if __name__ == "__main__":
    main()
