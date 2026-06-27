import networkx as nx
from spa.augmenting_path import find_augmenting_path, augment_matching

class Aluno:
    def __init__(self, matricula):
        self.matricula = matricula
    def __repr__(self):
        return f"Aluno({self.matricula})"

class Projeto:
    def __init__(self, codigo, num_vagas):
        self.codigo = codigo
        self.num_vagas = num_vagas
    def __repr__(self):
        return f"Proj({self.codigo})"

class MatchingState:
    def __init__(self, matching, allocated_projects):
        self.matching = matching
        self.allocated_projects = allocated_projects

    def is_matched(self, aluno, projeto) -> bool:
        return self.matching.get(aluno) == projeto

    def has_capacity(self, projeto) -> bool:
        current_students = self.allocated_projects.get(projeto, [])
        return len(current_students) < projeto.num_vagas


def executar_teste():
    print("--- INICIANDO TESTE DE CAMINHO AUMENTADO ---\n")

    # 1. Cria os nós
    a1 = Aluno("A1")
    a2 = Aluno("A2")
    p1 = Projeto("P1", num_vagas=1)
    p2 = Projeto("P2", num_vagas=1)

    # 2. Cria o Grafo Bipartido
    G = nx.Graph()
    G.add_nodes_from([a1, a2], bipartite=0)
    G.add_nodes_from([p1, p2], bipartite=1)
    
    # A1 quer P1
    # A2 quer P1 e P2
    G.add_edges_from([(a1, p1), (a2, p1), (a2, p2)])

    # 3. Forçando um Estado Inicial "Ruim"
    # A2 roubou a vaga do P1. A1 está livre. P2 está livre.
    matching_inicial = {a2: p1}
    projetos_alocados = {p1: [a2], p2: []}
    
    estado = MatchingState(matching_inicial, projetos_alocados)

    print(f"Estado Inicial: A1 está livre. P1 tem o {estado.allocated_projects[p1]}")

    # 4. Buscando o Caminho Aumentado a partir do Aluno 1
    print("\nBuscando caminho para A1...")
    caminho = find_augmenting_path(a1, G, estado)

    if caminho:
        print(f"Caminho encontrado: {caminho}")
        
        # 5. Aplicando a augmentação
        augment_matching(caminho, estado)
        
        print("\n--- ESTADO APÓS AUGMENTAÇÃO ---")
        print(f"Matching final: {estado.matching}")
        print(f"Alunos no P1: {estado.matching[p1]}")
        print(f"Alunos no P2: {estado.matching[p2]}")
        print("Sucesso! A1 conseguiu o P1 e o A2 foi remanejado para o P2.")
    else:
        print("Nenhum caminho encontrado (Algo deu errado na lógica).")
