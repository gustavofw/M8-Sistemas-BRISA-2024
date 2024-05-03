from spellchecker import SpellChecker

spell = SpellChecker(language='pt')  # Especifica o idioma como português

word = input('Insira uma palavra para verificar a ortografia: ')
    
word = word.lower()

palavras = word.split()

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