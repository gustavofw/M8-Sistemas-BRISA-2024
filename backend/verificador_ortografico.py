from spellchecker import SpellChecker

spell = SpellChecker(language='pt')  # Especifica o idioma como português

print("Para sair, pressione Enter sem inserir uma palavra!")
while True:
    word = input('Insira uma palavra para verificar a ortografia: ')
    if word == '':  # Para sair do loop se a entrada for vazia
        break
    word = word.lower()

    if word in spell:
        print("'{}' está escrita corretamente!".format(word)) # Reconhece caso a palavra tenha sido escrita da forma correta
    else:
        correta = spell.correction(word)
        print("A melhor ortografia para '{}' é '{}'".format(word, correta)) # Reconhece a melhor possivel correção para palavra errada.

        print("Se isso não for suficiente, aqui estão todas as palavras candidatas possíveis:")
        print(spell.candidates(word)) # Lista possibilidades de correção para a palavra.
        print("Essa é a palavra correta:", correta) # Variável "correta" recebe o valor com a palavra corrigida. 