"""Modelo Aluno para candidatos no sistema de alocação SPA."""


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

    def tem_mais_preferencias(self) -> bool:
        """Retorna True se ainda houver projetos não propostos na lista."""
        return self.prox_preferencia < len(self.preferencia)

    def proxima_preferencia(self) -> str | None:
        """Retorna o próximo projeto a ser proposto ou None se não houver mais."""
        if self.tem_mais_preferencias():
            return self.preferencia[self.prox_preferencia]
        return None

    def __repr__(self):
        return f"Aluno(cod='{self.cod}', projetos={self.preferencia}, nota={self.nota})"
