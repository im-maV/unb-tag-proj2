# Registro de Uso de IA Generativa

## Objetivo

Documentar as interações com modelos LLM utilizadas durante o desenvolvimento do projeto SPA

---

## Prompt 01 — Estruturação da Arquitetura

### Objetivo

Definir uma arquitetura modular para implementação do algoritmo SPA em Python.

### Prompt
Crie uma estrutura de projeto python para a especificação do projeto que visa propor uma implementação do problema SPA, segundo o artigo *Two algorithms for the student-project allocation problem. Journal of Discrete Algorithms, Abraham, D.J. and Irving, R.W. and Manlove*. Considere que o código será migrado para um notebook jupyter explicativo.
Considere inicialmente a seguinte estrutura:
```spa/
    - parser dos dados
    - visualização dos dados
    - gale_shapley
    - algorítimo caminhos aumentados
docs/
data/
arquivo_notebook
README.md
main.py <- entry point```
Não implemente nenhum códiga, mas forneça um docstring explicativa para cada função/classe


### Resultado Utilizado
... 

### Modificações Realizadas
Foram adicionados os arquivos requirements.txt e .gitignore

---


## Prompt 02 - Debugg-1
### Prompt
Verifique por inconsistências e erros no módulo gale_shapley.py. Indique quais erros e propostas de soluções, mas não altere o arquivo.

### Modificações Realizadas
Com base nas propostas geradas pelo modelo, foram feitas as seguintes correções/refatorações:
1. aluno expulso continua no matching
2. destruindo informação do número de vagas de projeto
3. Nota minima do projeto não verificada
4. aluno emparelhado duas vezes
5. Logica da estrutura de dados de emparelhados alterada
- Features
1. Verificação minimo alunos por projeto
2. Movido a logica do propose para fora do loop principal

