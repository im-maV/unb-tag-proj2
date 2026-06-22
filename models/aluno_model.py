class Aluno:
    """
    Representa um aluno candidato.

    Deve armazenar: matrícula, lista de preferências de projetos em ordem
    (até 3), e nota agregada (3, 4 ou 5).
    """
    def __init__(self, cod: str, projetos: list[str], nota: str):
        self.cod = cod
        self.projetos = projetos
        self.nota = nota
        self.current_pref_index = 0 #Necessãrio ??
    def __repr__(self):
        return f"Aluno(cod='{self.cod}', projetos={self.projetos}, nota={self.nota}"