"""
spa.parser
==========
Responsável por ler o arquivo de entrada (entradaProj2.26TAG.txt) e converter
seu conteúdo em estruturas de dados Python prontas para uso pelo restante do
pipeline

"""


class Projeto:
    """
    Representa um projeto disponível para alocação de alunos.

    Deve armazenar: código identificador, número mínimo de vagas (r_i),
    número máximo de vagas (v_i), e a lista de alunos candidatos (preenchida
    posteriormente pelo graph_builder).
    """
    pass


class Aluno:
    """
    Representa um aluno candidato.

    Deve armazenar: matrícula, lista de preferências de projetos em ordem
    (até 3), e nota agregada (3, 4 ou 5).
    """
    pass


def parse_input_file(filepath: str):
    """
    Lê o arquivo de entrada bruto e retorna duas listas: projetos e alunos.

    Deve identificar e separar as duas seções do arquivo (projetos e alunos),
    instanciando objetos Projeto e Aluno para cada linha.
    """
    pass


def validate_parsed_data(projetos: list, alunos: list) -> None:
    """
    Valida a integridade dos dados extraídos pelo parser.

    Deve checar: matrículas duplicadas, projetos referenciados nas
    preferências que não existem na lista de projetos, notas fora do
    intervalo [3, 5], e preferências vazias ou com mais de 3 itens.
    Levanta exceção descritiva em caso de inconsistência.
    """
    pass
