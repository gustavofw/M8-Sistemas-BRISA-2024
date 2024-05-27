# M8-Sistemas-BRISA-2024
Projeto ChatBot M8 Sistemas
<div align="center">
<img src="https://m8sistemas.com.br/2021/wp-content/uploads/2023/05/logo_m8_sistemas-branca.png" widht="700px" />
</div>
Bibliotecas necessárias para o funcionamento do ChatBot:

- requests: Para fazer requisições HTTP, como consultas à API.
pip install requests

- Flask: Para criar o servidor web e definir rotas.
pip install Flask

- flask-cors: Para habilitar CORS no seu servidor Flask.
pip install flask-cors

- spacy: Para processamento de linguagem natural.
pip install spacy

- unidecode: Para normalização de texto, removendo acentuação.
pip install Unidecode

- spellchecker: Para correção ortográfica.
pip install pyspellchecker

Além disso, você também precisará dos modelos de linguagem do spaCy para o português:
python -m spacy download pt_core_news_lg