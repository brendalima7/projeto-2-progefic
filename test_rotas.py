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