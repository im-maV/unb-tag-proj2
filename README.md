# Projeto 2 — Alocação Aluno-Projeto (SPA)

**CIC0199 - Teoria e Aplicação de Grafos, Turma A, 2026/1 — Prof. Díbio**
**Integrantes:**

- Daniel Florencio Hollenbach — 241020859
- Mateus Valério — 190035161
- Maylla Krislainy — 190043873

---

## Variação do Algoritmo Utilizada

A implementação segue a variação **SPA-Student** descrita em Abraham, Irving e Manlove (2007), com uma adaptação por mérito:

- As propostas partem dos **alunos**, em ordem crescente de matrícula (execução determinística)
- Cada aluno propõe sequencialmente aos projetos em sua lista de preferência
- Um projeto **aceita** o aluno se ele atende à nota mínima exigida e há vaga disponível
- Se o projeto está **cheio** mas o candidato tem nota estritamente maior que o pior alocado, o pior é **expulso** e volta à fila de livres _(substituição por mérito)_
- O algoritmo termina quando não há mais alunos livres com propostas pendentes

Após o emparelhamento estável inicial (M₀), são realizadas **10 iterações de melhoria** por caminhos M-aumentantes, que tentam alocar os alunos que ficaram livres na primeira fase. Essa segunda fase maximiza a cardinalidade do matching, mas não preserva a estabilidade.

---

## Estrutura do Projeto

```
UNB-TAG-PROJ2/
│
├── data/
│   └── entradaProj2.26TAG.txt   # Arquivo de entrada com projetos e alunos
│
├── docs/
│   ├── artigo_spa.pdf            # Abraham, Irving & Manlove (2007)
│   ├── especificacao.pdf         # Especificação do projeto
│   ├── prompts_ai.md             # Registro dos prompts utilizados com LLM
│   └── Relatório Final.pdf       # Relatório entregue
│
├── models/                       # Classes Aluno e Projeto
│
├── output/                       # Saídas geradas pelo notebook
│   ├── iteracao_0.png            # Grafo pós-GS (matching inicial M₀)
│   ├── iteracao_1.png            # Grafo após 1ª iteração de melhoria
│   ├── ...
│   ├── iteracao_10.png           # Grafo após 10ª iteração
│   ├── preference_index.png      # Gráfico de índice de preferência por projeto
│   └── matching_matrix.csv       # Matriz de emparelhamento final completa
│
├── spa/                          # Pacote principal com toda a lógica do algoritmo
│
├── tests/                        # Testes automatizados
│
├── main.py                       # Ponto de entrada alternativo (linha de comando)
├── notebook.ipynb                # Notebook principal — execução e visualizações
└── requirements.txt              # Dependências do projeto
```

---

## Como Executar

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Abra e execute o notebook:
   ```bash
   jupyter notebook notebook.ipynb
   ```

As saídas (grafos, gráfico de preferência e matriz CSV) serão geradas automaticamente na pasta `output/`.

---

## Referências

- Abraham, D.J.; Irving, R.W.; Manlove, D.F. _Two algorithms for the Student-Project Allocation problem_. Journal of Discrete Algorithms, v. 5, n. 1, p. 73–90, 2007.
- Gale, D.; Shapley, L.S. College admissions and the stability of marriage. _American Mathematical Monthly_, v. 69, n. 1, p. 9–15, 1962.
