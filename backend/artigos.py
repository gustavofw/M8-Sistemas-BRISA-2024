from flask import Flask, request, jsonify, render_template
import json
import os
import pyodbc

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

def conectar_banco():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=BRISA;"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(connection_string)

def carregar_palavras_chaves():
    with open('palavraschaves.json', 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def salvar_palavras_chaves(dados):
    with open('palavraschaves.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4)

def buscar_setores():
    connection = conectar_banco()
    cursor = connection.cursor()
    cursor.execute("SELECT SetorID, Setor FROM Setores")
    setores = cursor.fetchall()
    connection.close()
    return setores

def atualizar_banco_dados(data, conn):
    cursor = conn.cursor()
    for setor, artigos in data['setores'].items():
        print(f"Processando setor: {setor}")  
        try:
            cursor.execute("SELECT SetorID FROM Setores WHERE Setor = ?", (setor,))
            setor_id = cursor.fetchone()
            if setor_id:
                setor_id = setor_id[0]
            else:
                cursor.execute("INSERT INTO Setores (Setor) OUTPUT INSERTED.SetorID VALUES (?)", (setor,))
                setor_id = cursor.fetchone()[0]
                conn.commit()
            for artigo, info in artigos.items():
                descricao = info['descricao']
                link = info['link']
                print(f"Processando artigo: {artigo} com descricao: {descricao} e link: {link}")  
                try:
                    cursor.execute("SELECT ArtigoID FROM ArtigosDeSuporte WHERE Artigo = ? AND SetorID = ?", (artigo, setor_id))
                    artigo_id = cursor.fetchone()
                    if artigo_id:
                        cursor.execute("""
                            UPDATE ArtigosDeSuporte 
                            SET Descricao = ?, LinkPDF = ? 
                            WHERE ArtigoID = ?
                        """, (descricao, link, artigo_id[0]))
                    else:
                        cursor.execute("""
                            INSERT INTO ArtigosDeSuporte (Artigo, Descricao, LinkPDF, SetorID) 
                            VALUES (?, ?, ?, ?)
                        """, (artigo, descricao, link, setor_id))
                    conn.commit()
                except pyodbc.Error as e:
                    print(f"Erro ao atualizar/inserir artigo: {e}")
        except pyodbc.Error as e:
            print(f"Erro ao processar setor: {e}")

@app.route('/')
def index():
    setores = buscar_setores()
    return render_template('interfaceadd.html', setores=setores)

@app.route('/add', methods=['POST'])
def add_article():
    dados = carregar_palavras_chaves()
    
    setor_id = request.form['setor']
    artigo = request.form['artigo']
    descricao = request.form['descricao']
    link = request.form['link']
    
    setor_nome = None
    for setor in buscar_setores():
        if setor[0] == int(setor_id):
            setor_nome = setor[1]
            break
    
    if setor_nome is None:
        return jsonify({"message": "Setor não encontrado."}), 400

    if setor_nome not in dados['setores']:
        dados['setores'][setor_nome] = {}

    dados['setores'][setor_nome][artigo] = {
        "descricao": descricao,
        "link": link
    }
    
    salvar_palavras_chaves(dados)
    
    connection = conectar_banco()
    atualizar_banco_dados(dados, connection)
    connection.close()
    
    return render_template('interfaceadd.html')

@app.route('/setores', methods=['GET', 'POST'])
def add_setor():
    if request.method == 'POST':
        setor_nome = request.form['setor-nome']
        if not setor_nome:
            return jsonify({"message": "O nome do setor não pode estar em branco."}), 400
        
        connection = conectar_banco()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Setores (Setor) VALUES (?)", (setor_nome,))
        connection.commit()
        connection.close()
        
        return jsonify({"message": "Setor adicionado com sucesso!"})
    
    return render_template('adicionar_setor.html')

@app.route('/remover-setor', methods=['GET', 'POST'])
def remover_setor():
    if request.method == 'POST':
        setor_id = request.form['setor-id']
        connection = conectar_banco()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Setores WHERE SetorID = ?", (setor_id,))
        connection.commit()
        connection.close()
        
        return jsonify({"message": "Setor removido com sucesso!"})
    
    setores = buscar_setores()
    return render_template('remover_setor.html', setores=setores)

@app.route('/editar-setor', methods=['GET', 'POST'])
def editar_setor():
    if request.method == 'POST':
        setor_id = request.form['setor-id']
        novo_nome = request.form['novo-nome']
        
        if not novo_nome:
            return jsonify({"message": "O nome do setor não pode estar em branco."}), 400
        
        connection = conectar_banco()
        cursor = connection.cursor()
        cursor.execute("UPDATE Setores SET Setor = ? WHERE SetorID = ?", (novo_nome, setor_id))
        connection.commit()
        connection.close()
        
        return jsonify({"message": "Setor atualizado com sucesso!"})
    
    setores = buscar_setores()
    return render_template('editar_setor.html', setores=setores)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
