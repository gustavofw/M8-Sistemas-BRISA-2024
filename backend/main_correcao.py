from spellchecker import SpellChecker
import spacy

spell = SpellChecker(language='pt')  # Especifica o idioma como português
nlp = spacy.load("pt_core_news_lg")

def process_user_input(input_text):
    # Correção ortográfica
    palavras = input_text.split()
    corrigidas = []

    # Loop sobre cada palavra na frase
    for palavra in palavras:
        # Se a palavra estiver correta, adiciona à lista corrigida
        if palavra in spell:
            corrigidas.append(palavra)
        else:
            # Caso contrário, corrige a palavra e adiciona à lista corrigida
            corrigida = spell.correction(palavra)
            corrigidas.append(corrigida)

    # Une as palavras corrigidas em uma única frase
    frase_corrigida = ' '.join(corrigidas)

    # Exibe a frase corrigida
    print("Frase corrigida:", frase_corrigida)

    # Identificação da palavra "compra"
    doc = nlp(frase_corrigida.lower())  # Convertendo a frase corrigida para minúsculas
    compra_achou = any(token.lemma_ == "comprar" for token in doc) # Verifica se contém "compra" em qualquer forma 
    export_nfe_palavraschaves = ["exportação", "nfe", "nota", "fiscal", "eletrônica"] # Verifica se contém as palavras-chave relacionadas exportação NFe
    export_nfe_achou = any(word in input_text.lower() for word in export_nfe_palavraschaves) 

    if compra_achou:
        print("Você mencionou compra. Talvez queira saber mais sobre a exportação de NFe? Posso ajudar com isso!")
    elif export_nfe_achou:
        print("Aqui está um link para ajudar com a exportação da NFe: https://www.nfe.fazenda.gov.br/portal/principal.aspx")
    else:
        print("Não identifiquei sua dúvida sobre compras ou NFe. Pode especificar mais?")

# Loop para manter o chatbot rodando
while True:
    user_input = input("Qual a sua dúvida? ")
    if user_input.lower() == 'sair':
        print("Obrigado por usar o chatbot. Até mais!")
        break
    process_user_input(user_input)
