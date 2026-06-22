"""
spa.parser
==========
Responsável por ler o arquivo de entrada (entradaProj2.26TAG.txt) e converter
seu conteúdo em estruturas de dados Python prontas para uso pelo restante do
pipeline

"""

import re
from models import Projeto, Aluno


def parse_input_file(filepath: str):
    """
    Lê o arquivo de entrada bruto e retorna duas listas: projetos e alunos.

    Deve identificar e separar as duas seções do arquivo (projetos e alunos),
    instanciando objetos Projeto e Aluno para cada linha.
    """
    l_projetos = []
    l_alunos = []
    proj_regex = re.compile(r'\((P\d{1,2}),\s*(\d+),\s*(\d+)\)')
    alunos_regex = re.compile(r'\((A\d{1,2})\)\s*:\s*\(\s*((?:P\d{1,2})(?:\s*,\s*P\d{1,2})*)\s*\)\s*\((\d+)\)')

    with open (filepath, "r") as file:
        for line in file:
            match = proj_regex.search(line)
            if match:
                cod, num_vagas, nota_min = match.groups()
                l_projetos.append({
                    "cod": cod,
                    "num_vagas": int(num_vagas),
                    "nota_min": int(nota_min)
                })
                continue
            match = alunos_regex.search(line)
            if match:
                cod, projetos, nota = match.groups()
                l_alunos.append({
                    "cod": cod,
                    "projetos": [
                        p.strip()
                        for p in projetos.split(",")],
                    "nota": int(nota)
                })

    projetos = [
        Projeto(**p)
        for p in l_projetos
    ]
    alunos = [
        Aluno(**a)
        for a in l_alunos
    ]

    return projetos, alunos



def validate_parsed_data(projetos: list, alunos: list) -> None:
    """
    Valida a integridade dos dados extraídos pelo parser.

    Deve checar: matrículas duplicadas, projetos referenciados nas
    preferências que não existem na lista de projetos, notas fora do
    intervalo [3, 5], e preferências vazias ou com mais de 3 itens.
    Levanta exceção descritiva em caso de inconsistência.
    """
    pass
