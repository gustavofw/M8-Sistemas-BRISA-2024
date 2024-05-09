import spacy
from spacy.symbols import NOUN
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
nlp = spacy.load("pt_core_news_lg")

@app.route('/process_user_input', methods=['POST'])
def process_user_input():
    input_text = request.json.get('text', '')
    response = process_user_input_helper(input_text)
    return jsonify({'response': response})

def process_user_input_helper(input_text):
    doc = nlp(input_text.lower())  # Convertendo a entrada para minúsculas
    
    # Palavras-chave relacionadas a compra e exportação de NFe
    keywords_compra = ["comprar", "compra"]
    keywords_export_nfe = ["exportação", "nfe", "nota", "fiscal", "eletrônica", "compras"]
    
    # Lista de tokens similares a "comprar"
    tokens_similares_compra = []
    for token in doc:
        if token.lemma_ == "comprar":
            tokens_similares_compra.append(token)
        else:
            similar_tokens = [t for t in nlp.vocab if t.has_vector and t.is_lower and t.is_alpha and any(s.lower() in keywords_compra for s in [t.text.lower()])]
            tokens_similares_compra.extend(similar_tokens)

    # Verifica se contém palavras-chave relacionadas a compra e exportação NFe
    compra_achou = any(token in keywords_compra for token in tokens_similares_compra)
    export_nfe_achou = any(word in input_text.lower() for word in keywords_export_nfe) 

    if compra_achou and not export_nfe_achou:
        return "Você mencionou compra. Talvez queira saber mais sobre a exportação de NFe? Posso ajudar com isso!"
    elif export_nfe_achou:
        return "Aqui está um link para ajudar com a exportação da NFe: https://www.nfe.fazenda.gov.br/portal/principal.aspx"
    else:
        return "Não identifiquei sua dúvida sobre compras ou NFe. Pode especificar mais?"

if __name__ == '__main__':
    app.run(debug=True)
