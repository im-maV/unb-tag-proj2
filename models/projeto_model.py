class Projeto:
    """
    Representa um projeto disponível para alocação de alunos.

    Deve armazenar: código identificador, número de vagas,
    e a lista de alunos candidatos (preenchida
    posteriormente pelo graph_builder).
    """
    def __init__(self, cod, num_vagas, nota_min):
        self.cod = cod
        self.num_vagas = num_vagas
        self.nota_min = nota_min
        self.ranking_alunos: list[str] = []
    def __repr__(self):
        return f"Projeto(cod='{self.cod}', num_vagas={self.num_vagas}, nota_min={self.nota_min}"
