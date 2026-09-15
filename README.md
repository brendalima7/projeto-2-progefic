# Projeto 2 - Programação Eficaz

### Aluno: Brenda de Oliveira Lima

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![MySQL](https://img.shields.io/badge/mysql-%234479A1.svg?style=flat&logo=mysql&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=flat&logo=postman&logoColor=white)
![SQL](https://img.shields.io/badge/sql-%2300758F.svg?style=flat&logo=sqlite&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=flat&logo=github&logoColor=white)

# Deploy

API hospedada na AWS EC2: http://18.207.155.72/imoveis

# Setup
 
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install pytest flask mysql-connector-python python-dotenv
```
 
Rodar os testes:
 
```powershell
py -m pytest
```

---

# Anotações pessoais de estudo

## Ordem certa
1. Escreve o teste 
2. Escreve o código mínimo pra passar
3. Refatora se precisar

## Testar exceção
```python
import pytest
 
with pytest.raises(ValueError):
    funcao(argumento_invalido)
```
- Usa o tipo certo (`ValueError`, `TypeError`, etc.), não `Exception` genérico, se o enunciado especificar.
- Cada chamada que deve lançar erro vai no seu próprio `with pytest.raises(...)`.

## Testar função com resultado aleatório
Uma única checagem pode passar "por sorte". Repete várias vezes:
```python
for _ in range(50):
    resultado = funcao_aleatoria()
    assert condicao(resultado)
```
 
## Organização
- Rota (`servidor.py`) só recebe requisição e devolve resposta — nunca tem SQL dentro.
- `utils.py` (ou `models.py`) guarda a lógica (SQL, validações, etc.) que a rota chama.

## Métodos HTTP
| Método | O que é | Pra que usar | Código de sucesso comum |
|---|---|---|---|
| GET | Busca/leitura de dado | Listar ou consultar recurso, sem alterar nada | 200 |
| POST | Criação | Criar um novo recurso | 201 |
| PUT | Atualização (substitui inteiro) | Atualizar um recurso existente por completo | 200 |
| PATCH | Atualização parcial | Atualizar só alguns campos de um recurso | 200 |
| DELETE | Remoção | Excluir um recurso existente | 200 ou 204 (sem corpo) |

## Códigos de status HTTP mais usados
| Código | Significado | Quando aparece |
|---|---|---|
| 200 | OK | Requisição deu certo, tem corpo de resposta |
| 201 | Created | Recurso criado com sucesso (comum em POST) |
| 204 | No Content | Deu certo, mas não tem corpo (comum em DELETE) |
| 400 | Bad Request | Requisição inválida (campo faltando, tipo inválido) |
| 404 | Not Found | Recurso não existe |
| 500 | Internal Server Error | Erro inesperado no servidor (não tratado no código) |

**200 vs 204:** 200 sempre vem com corpo (dados, mensagem). 204 é sucesso sem nada pra devolver — comum em DELETE, já que depois de apagar o recurso não sobra informação relevante pra mandar de volta. Nesse projeto optei por manter 200 com mensagem no DELETE, seguindo a estrutura dos projetos anteriores.
