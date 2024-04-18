import spacy

nlp = spacy.load("pt_core_news_lg")
with open ("./Artigo_Compras.txt") as f:
    text = f.read()
user = input("Qual a sua dúvida? ")
tokens = ["compras", "compra", "Compras", "Compra"]
for token in tokens:
    if token in user:
        doc = nlp(text)
        print(len(text))
        print(len(doc))
        for token in text[0:10]:
            print(token)
        for token in doc[:10]:
            print(token)
        for token in text.split()[:10]:
            print(token)
        for sent in doc.sents:
            print(sent)
        sentence1 = list(doc.sents)[2]
        print(sentence1)
        break
else:
    print("Nenhuma das palavras-chave foi encontrada na frase.") 