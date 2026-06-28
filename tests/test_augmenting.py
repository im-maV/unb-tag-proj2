"""
Teste de caminho M-aumentante.
 
Cenário:
    Alunos : A1 (nota 4), A2 (nota 5)
    Projetos: P1 (1 vaga, nota_min 3), P2 (1 vaga, nota_min 3)
 
    Preferências (grafo):
        A1 -> P1
        A2 -> P1, P2
 
    Estado inicial forçado (emparelhamento ruim):
        A2 está alocado em P1  →  matching = [(A2, P1)]
        A1 está livre          →  free_students = {"A1"}
        P2 está vazio
 
    Caminho aumentante esperado a partir de A1:
        A1 → P1 → A2 → P2
        (A1 entra em P1; A2 é deslocado para P2)
 
    Resultado esperado após augmentação:
        matching = [(A2, P2), (A1, P1)]   (tamanho 1 → 2, ou seja, +1)
"""



import networkx as nx
from spa.augmenting_path import augment_matching, find_augmenting_path
from models.matching_model import MatchingState
from models.aluno_model import Aluno
from models.projeto_model import Projeto



def executar_teste():
    print("--- INICIANDO TESTE DE CAMINHO AUMENTADO ---\n")

    # Aluno(cod, projetos_preferidos, nota)
    a1 = Aluno("A1", ["P1"], 4)
    a2 = Aluno("A2", ["P1", "P2"], 5)
 
    # Projeto(cod, num_vagas, nota_min)
    p1 = Projeto("P1", num_vagas=1, nota_min=3)
    p2 = Projeto("P2", num_vagas=1, nota_min=3)

    # 2. Cria o Grafo Bipartido
    G = nx.Graph()
    G.add_nodes_from([a1, a2], bipartite=0)   # lado dos alunos
    G.add_nodes_from([p1, p2], bipartite=1)   # lado dos projetos

    # A1 quer P1
    # A2 quer P1 e P2
    G.add_edges_from([(a1, p1), (a2, p1), (a2, p2)])


    # 3. Forçando um Estado Inicial "Ruim"
    # A2 roubou a vaga do P1. A1 está livre. P2 está livre.
    matching_inicial = [(a2, p1)]                   # List[Tuple[Aluno, Projeto]]
    proposed_edges   = []                           # sem histórico de propostas
    rejected_edges   = []                           # sem rejeições
    allocated_projects = {                          # Dict[str, List[Aluno]]
        p1.cod: [a2],
        p2.cod: [],
    }
    free_students = [a1]
    
    estado = MatchingState(
        matching_inicial, 
        proposed_edges, 
        rejected_edges, 
        allocated_projects, 
        free_students)
    tamanho_antes = len(estado.matching)

    print(f"Estado Inicial:")
    print(f"  matching      = {[(a.cod, p.cod) for a, p in estado.matching]}")
    print(f"  free_students = {estado.free_students}")
    print(f"  Tamanho do matching: {tamanho_antes}")

    # 4. Buscando o Caminho Aumentado a partir do Aluno 1
    print("\nBuscando caminho para A1...")
    caminho = find_augmenting_path(a1, G, estado)

    if caminho is None:
        print("FALHA: Nenhum caminho encontrado — algo deu errado na lógica.")
        return


    print(f"Caminho encontrado: {[n.cod for n in caminho]}")

    # 5. Aplicando a augmentação
    augment_matching(caminho, estado)
    estado.update_free_students([a1, a2])

    tamanho_depois = len(estado.matching)
    print("\n--- ESTADO APÓS AUGMENTAÇÃO ---")
    print(f"  matching      = {[(a.cod, p.cod) for a, p in estado.matching]}")
    print(f"  free_students = {estado.free_students}")
    print(f"  Tamanho do matching: {tamanho_depois}")

    # Verificações
    assert tamanho_depois == tamanho_antes + 1, (
        f"FALHA: o matching deveria crescer em 1 "
        f"(era {tamanho_antes}, ficou {tamanho_depois})"
    )

    alocados_p1 = estado.allocated_projects.get(p1.cod, [])
    alocados_p2 = estado.allocated_projects.get(p2.cod, [])
    
    assert any(a.cod == "A1" for a in alocados_p1), \
        "FALHA: A1 deveria estar alocado em P1 após augmentação."
    assert any(a.cod == "A2" for a in alocados_p2), \
        "FALHA: A2 deveria ter sido deslocado para P2."
    assert a1.cod not in estado.free_students, \
        "FALHA: A1 ainda consta como livre após ser alocado."
 
    print("\nSUCESSO: matching aumentou em +1, A1→P1 e A2→P2 conforme esperado.")



executar_teste()