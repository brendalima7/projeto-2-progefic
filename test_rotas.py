import pytest
from unittest.mock import patch, MagicMock
from servidor import app  # e.g., arquivo api.py com app = Flask(__name__)
import utils

@pytest.fixture
def client():
    """Cria um cliente de teste para a API."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# ========================== TESTES - GET ========================================

# Teste listar todos os imóveis com todos os seus atributos;
@patch("utils.conectar_banco")
def test_GET_listar_imoveis_200(mock_conectar_banco, client):
    """GET /imoveis - lista com dados."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "Nicole Common", "Travessa", "Lake Danielle", "Judymouth", "85184", "casa em condominio", 488424, "2017-07-29"),
    ]

    mock_conectar_banco.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200
    assert response.get_json() == [{
        "id": 1,
        "logradouro": "Nicole Common", 
        "tipo_logradouro": "Travessa", 
        "bairro": "Lake Danielle", 
        "cidade": "Judymouth", 
        "cep": "85184", 
        "tipo": "casa em condominio", 
        "valor": 488424.0, 
        "data_aquisicao": "2017-07-29"
        },
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

# teste de listar imóveis com lista vazia
@patch("utils.conectar_banco")
def test_GET_listar_imoveis_vazios_200(mock_conectar_banco, client):
    """GET /imoveis - lista vazia."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    mock_conectar_banco.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200
    assert response.get_json() == []

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# Teste listar um imóvel específico pelo seu id com todos os seus atributos;
@patch("utils.conectar_banco")
def test_GET_listar_um_imovel_200(mock_conectar_banco, client):
    """GET /imoveis/<id> - imovel existe."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1, "Nicole Common", "Travessa", "Lake Danielle", "Judymouth", "85184", "casa em condominio", 488424, "2017-07-29")
    mock_conectar_banco.return_value = mock_conn

    response = client.get("/imoveis/1")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "logradouro": "Nicole Common", 
        "tipo_logradouro": "Travessa", 
        "bairro": "Lake Danielle", 
        "cidade": "Judymouth", 
        "cep": "85184", 
        "tipo": "casa em condominio", 
        "valor": 488424.0, 
        "data_aquisicao": "2017-07-29"
    }

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s",
        (1,),
    )
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

# Teste listar um movel não encontrado
@patch("utils.conectar_banco")
def test_GET_listar_um_imovel_not_found_404(mock_conectar_banco, client):
    """GET /imoveis/<id> - imóvel não existe."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None
    mock_conectar_banco.return_value = mock_conn

    response = client.get("/imoveis/999")

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imóvel não encontrado"}

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s",
        (999,),
    )
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# Teste adicionar um novo imóvel;
@patch("utils.conectar_banco")
def test_POST_criar_imovel_201(mock_conectar_banco, client):
    """POST /imoveis - cria imovel com sucesso."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simula ID gerado pelo banco
    mock_cursor.lastrowid = 1

    mock_conectar_banco.return_value = mock_conn

    payload = {
        "logradouro": "Nicole Common",
        "tipo_logradouro": "Travessa", 
        "bairro": "Lake Danielle", 
        "cidade": "Judymouth", 
        "cep": "85184", 
        "tipo": "casa em condominio", 
        "valor": 488424.0, 
        "data_aquisicao": "2017-07-29"
    }
    response = client.post("/imoveis", json=payload)

    assert response.status_code == 201
    assert response.get_json() == {"id": 1}

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ("Nicole Common", "Travessa", "Lake Danielle", "Judymouth", "85184", "casa em condominio", 488424, "2017-07-29"),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

# Teste erro ao criar um imovel
@patch("utils.conectar_banco")
def test_POST_criar_imovel_400(mock_conectar_banco, client):
    """POST /imovel - falta campo obrigatório -> 400. Não deve acessar o banco."""
    response = client.post("/imoveis", json={"logradouro": "Nicole Common"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_conectar_banco.assert_not_called()