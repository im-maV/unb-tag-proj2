class Aluno:
    """
    Representa um aluno candidato.

    Deve armazenar: matrícula, lista de preferências de projetos em ordem
    (até 3), e nota agregada (3, 4 ou 5).
    """
    def __init__(self, cod: str, projetos: list[str], nota: str):
        self.cod = cod
        self.preferencia = projetos
        self.nota = nota
        self.prox_preferencia = 0
    def __repr__(self):
        return f"Aluno(cod='{self.cod}', projetos={self.projetos}, nota={self.nota}"