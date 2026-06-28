"""
spa.parser
==========
Responsável por ler o arquivo de entrada (entradaProj2.26TAG.txt) e converter
seu conteúdo em estruturas de dados Python prontas para uso pelo restante do
pipeline

"""

import re
from models.aluno_model import Aluno
from models.projeto_model import Projeto


def parse_input_file(filepath: str):
    """
    Lê o arquivo de entrada bruto e retorna duas listas: projetos e alunos.

    Deve identificar e separar as duas seções do arquivo (projetos e alunos),
    instanciando objetos Projeto e Aluno para cada linha.
    """
    l_projetos = []
    l_alunos = []
    proj_regex = re.compile(r"\((P\d+),\s*(\d+),\s*(\d+)\)")
    alunos_regex = re.compile(
        r"\((A\d+)\)\s*:\s*\(\s*((?:P\d+)(?:\s*,\s*P\d+)*)\s*\)\s*\((\d+)\)"
    )

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            match = proj_regex.search(line)
            if match:
                cod, num_vagas, nota_min = match.groups()
                l_projetos.append(
                    {"cod": cod, "num_vagas": int(num_vagas), "nota_min": int(nota_min)}
                )
                continue
            match = alunos_regex.search(line)
            if match:
                cod, projetos, nota = match.groups()
                l_alunos.append(
                    {
                        "cod": cod,
                        "projetos": [p.strip() for p in projetos.split(",")],
                        "nota": int(nota),
                    }
                )

    projetos = [Projeto(**p) for p in l_projetos]
    alunos = [Aluno(**a) for a in l_alunos]

    return projetos, alunos


def validate_parsed_data(projetos: list, alunos: list) -> None:
    """
    Valida a integridade dos dados extraídos pelo parser.

    Checa: matrículas duplicadas, projetos referenciados nas preferências
    que não existem na lista de projetos, notas fora do intervalo [3, 5],
    e preferências vazias ou com mais de 3 itens.

    Inconsistências são logadas como warnings sem interromper o pipeline.
    """
    proj_validos = {p.cod for p in projetos}
    cods_alunos = [a.cod for a in alunos]

    # Matrículas duplicadas
    duplicatas = {c for c in cods_alunos if cods_alunos.count(c) > 1}
    if duplicatas:
        print(f"[AVISO] Alunos com matrícula duplicada: {duplicatas}")

    for aluno in alunos:
        # Projetos inexistentes nas preferências
        invalidos = [p for p in aluno.preferencia if p not in proj_validos]
        if invalidos:
            print(f"[AVISO] {aluno.cod} referencia projetos inexistentes: {invalidos}")

        # Preferências duplicadas
        if len(aluno.preferencia) != len(set(aluno.preferencia)):
            print(
                f"[AVISO] {aluno.cod} tem preferências duplicadas: {aluno.preferencia}"
            )

        # Nota fora do intervalo
        if aluno.nota not in (3, 4, 5):
            print(f"[AVISO] {aluno.cod} tem nota inválida: {aluno.nota}")

        # Número de preferências
        if len(aluno.preferencia) == 0:
            print(f"[AVISO] {aluno.cod} sem preferências")
        elif len(aluno.preferencia) > 3:
            print(
                f"[AVISO] {aluno.cod} tem mais de 3 preferências: {aluno.preferencia}"
            )

    print("=" * 60)
