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


# VALIDAÇÃO DE CAMPOS OBRIGATORIOS
CAMPOS_OBRIGATORIOS = {"logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao"}

def validar_campos_faltantes(data):
    if data is None:
        return sorted(list(CAMPOS_OBRIGATORIOS))
    return sorted([campo for campo in CAMPOS_OBRIGATORIOS if campo not in data])

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

def buscar_imovel_por_id(id):
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
    imovel = cur.fetchone()
    cur.close()
    conn.close()

    if not imovel:
        return None

    return {
        "id": imovel[0],
        "logradouro": imovel[1],
        "tipo_logradouro": imovel[2],
        "bairro": imovel[3],
        "cidade": imovel[4],
        "cep": imovel[5],
        "tipo": imovel[6],
        "valor": imovel[7],
        "data_aquisicao": imovel[8]
    }

def criar_imovel(dados):
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (dados["logradouro"], dados["tipo_logradouro"], dados["bairro"], dados["cidade"], dados["cep"], dados["tipo"], dados["valor"], dados["data_aquisicao"]),
    )
    conn.commit()
    novo_id = cur.lastrowid
    cur.close()
    conn.close()
    return novo_id

def alterar_imovel(id, dados):
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        (dados["logradouro"], dados["tipo_logradouro"], dados["bairro"], dados["cidade"], dados["cep"], dados["tipo"], dados["valor"], dados["data_aquisicao"], id),
    )
    resultado = cur.rowcount
    # Dica de sintaxe e comportamento:
    # - .fetchone(): Método (ação que busca a linha, usa parênteses).
    # - .rowcount  : Atributo (contagem de linhas afetadas/retornadas, sem parênteses).
    conn.commit()
    cur.close()
    conn.close()

    return resultado

def deletar_imovel(id):

    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("DELETE FROM imoveis WHERE id = %s", (id,))
    resultado = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    return resultado