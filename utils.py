import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'ssl_ca': os.getenv('SSL_CA_PATH'),
}

def conectar_banco():
    return mysql.connector.connect(**config)

def listar_imoveis():
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis")
    resultados = cur.fetchall()
    cur.close()
    conn.close()

    imoveis = []
    for imovel in resultados:
        imoveis.append({
            "id": imovel[0],
            "logradouro": imovel[1],
            "tipo_logradouro": imovel[2],
            "bairro": imovel[3],
            "cidade": imovel[4],
            "cep": imovel[5],
            "tipo": imovel[6],
            "valor": imovel[7],
            "data_aquisicao": imovel[8]
        })
    return imoveis