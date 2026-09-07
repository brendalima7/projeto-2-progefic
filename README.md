# Projeto 2 - Programação Eficaz

### Aluno: Brenda de Oliveira Lima

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![MySQL](https://img.shields.io/badge/mysql-%234479A1.svg?style=flat&logo=mysql&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=flat&logo=postman&logoColor=white)
![uv](https://img.shields.io/badge/uv-de5fe9?style=flat&logo=uv&logoColor=white)
![SQL](https://img.shields.io/badge/sql-%2300758F.svg?style=flat&logo=sqlite&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=flat&logo=github&logoColor=white)


# Setup
 
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install pytest flask
```
 
Rodar os testes:
 
```powershell
py -m pytest
```
 
# Notas de TDD / pytest
 
## Ordem certa
1. Escreve o teste (falha, porque nada existe ainda)
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
