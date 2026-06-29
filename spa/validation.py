"""
spa.validation
==============
Funções de validação e checagem de corretude do emparelhamento final.
    - matching : List[Tuple[Aluno, Projeto]]
    - O projeto não tem lista de preferência explícita; seu critério de
      preferência entre alunos é a nota (maior nota = mais preferido).
    - Par bloqueante (a, p): aluno 'a' e projeto 'p' não emparelhados entre
      si, tal que 'a' prefere 'p' ao seu atual (ou está livre) e 'p'
      aceitaria 'a' (nota >= nota_min E tem vaga ou preferiria 'a' a algum
      aluno já alocado).
"""

from models.aluno_model import Aluno
from models.projeto_model import Projeto
import networkx as nx

# Helper
def _build_indexes(
    matching: list[tuple[Aluno, Projeto]]
) -> tuple[dict[str, Projeto], dict[str, list[Aluno]]]:
    """
    Constroi dois índices a partir do matching:
        aluno_to_projeto : cod_aluno  -> Projeto (ou ausente se livre)
        projeto_to_alunos: cod_projeto -> List[Aluno]
    """
    aluno_to_projeto: dict[str, Projeto] = {}
    projeto_to_alunos: dict[str, list[Aluno]] = {}

    for aluno, projeto in matching:
        aluno_to_projeto[aluno.cod] = projeto
        projeto_to_alunos.setdefault(projeto.cod, []).append(aluno)

    return aluno_to_projeto, projeto_to_alunos


def _aluno_prefere(aluno: Aluno, projeto: Projeto, atual: Projeto | None) -> bool:
    """
    Retorna True se 'aluno' prefere 'projeto' ao seu projeto atual.
    Preferência é dada pela posição em aluno.preferencia (índice menor = mais preferido).
    Se o aluno está livre (atual=None), qualquer projeto na lista é preferível.
    """
    if projeto.cod not in aluno.preferencia:
        return False
    if atual is None:
        return True
    if atual.cod not in aluno.preferencia:
        # está alocado num projeto fora da lista — qualquer preferência é melhor
        return True
    return aluno.preferencia.index(projeto.cod) < aluno.preferencia.index(atual.cod)


def _projeto_prefere_aluno(
    projeto: Projeto,
    candidato: Aluno,
    alocados: list[Aluno],
) -> bool:
    """
    Retorna True se 'projeto' aceitaria 'candidato':
        - candidato atende nota_min, E
        - projeto tem vaga livre OU candidato tem nota maior que o pior alocado.
    """
    if candidato.nota < projeto.nota_min:
        return False
    if len(alocados) < projeto.num_vagas:
        return True
    pior = min(alocados, key=lambda a: a.nota)
    return candidato.nota > pior.nota


# Funcoes públicas
def find_blocking_pairs(
    matching: list[tuple[Aluno, Projeto]],
    graph: nx.Graph,
) -> list[tuple[Aluno, Projeto]]:
    """
    Procura por pares bloqueantes no emparelhamento:
    um aluno e um projeto que, mesmo não emparelhados entre si, prefeririam
    mutuamente trocar de situação.

    Retorna a lista de pares (Aluno, Projeto) bloqueantes
    (vazia se o emparelhamento é estável).
    """
    aluno_to_projeto, projeto_to_alunos = _build_indexes(matching)
    blocking: list[tuple[Aluno, Projeto]] = []

    for aluno in {a for a, _ in matching} | {
        node for node in graph.nodes if isinstance(node, Aluno)
    }:
        atual = aluno_to_projeto.get(aluno.cod)  # None se livre

        for projeto in graph.neighbors(aluno):
            # Ignora o projeto ao qual já está emparelhado
            if atual is not None and atual.cod == projeto.cod:
                continue

            alocados = projeto_to_alunos.get(projeto.cod, [])

            if _aluno_prefere(aluno, projeto, atual) and \
               _projeto_prefere_aluno(projeto, aluno, alocados):
                blocking.append((aluno, projeto))

    return blocking



def is_stable_matching(
    matching: list[tuple[Aluno, Projeto]],
    graph: nx.Graph,
) -> bool:
    """
    Roda todas as checagens e retorna True se o emparelhamento é válido e
    estável, False caso contrário. Imprime um resumo das violações encontradas.
    """
    blocking      = find_blocking_pairs(matching, graph)
    if blocking:
        print(f"[INSTÁVEL] {len(blocking)} par(es) bloqueante(s) encontrado(s):")
        for aluno, projeto in blocking:
            print(f"  Aluno {aluno.cod} (nota={aluno.nota}) <-> Projeto {projeto.cod} (nota_min={projeto.nota_min})")


    stable = not blocking
    print("[OK] Emparelhamento estável e válido." if stable else "[FALHA] Emparelhamento inválido.")
    return stable
