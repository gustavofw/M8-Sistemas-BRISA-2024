import json
import pyodbc
import os


def ler_json(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


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


caminho_arquivo = os.path.join(os.path.dirname(__file__), 'palavraschaves.json')


data = ler_json(caminho_arquivo)


connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=BRISA;"
    "Trusted_Connection=yes;"
)


connection = pyodbc.connect(connection_string)
print("Conexão estabelecida com sucesso.")


atualizar_banco_dados(data, connection)


connection.close()
print("Conexão fechada com sucesso.")
