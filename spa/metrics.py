"""
spa.metrics
===========
Calcula métricas derivadas do emparelhamento final: índice de preferência
por projeto, e a matriz/tabela final de classificações cruzadas
"""


def compute_preference_index(project, state, graph) -> float:
    """
    Calcula o índice de preferência agregado de um projeto, resumindo quão
    bem ele foi atendido em termos da posição de preferência média dos
    alunos que nele foram alocados.
    """
    pass


def compute_all_preference_indices(state, graph) -> dict:
    """
    Calcula o índice de preferência para todos os projetos do grafo,
    retornando um dicionário {codigo_projeto: indice}.
    """
    pass


def student_rank_in_project_list(student, project, graph) -> int:
    """
    Retorna a classificação do aluno na lista de candidatos do projeto
    (ex: 3º melhor entre os candidatos, ordenado por nota agregada).
    """
    pass


def project_rank_in_student_list(student, project, graph) -> int:
    """
    Retorna a classificação do projeto na lista de preferências do aluno
    (1ª, 2ª ou 3ª escolha).
    """
    pass


def build_final_matching_matrix(state, graph):
    """
    Monta a tabela final (pandas DataFrame) com colunas: Aluno, Projeto
    Emparelhado, Classificação do Aluno na lista do Projeto, Classificação
    do Projeto na lista do Aluno — incluindo alunos não emparelhados, se
    houver, conforme exemplo do enunciado.
    """
    pass
