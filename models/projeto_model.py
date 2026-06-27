"""Modelo Projeto para projetos disponíveis no sistema de alocação SPA."""

import bisect
from models.aluno_model import Aluno


class Projeto:
    """
    Representa um projeto disponível para alocação de alunos.

    Deve armazenar: código identificador, número de vagas,
    e a lista de alunos candidatos (preenchida
    posteriormente pelo graph_builder).
    """

    def __init__(self, cod: str, num_vagas: int, nota_min: int):
        self.cod = cod
        self.num_vagas = num_vagas
        self.nota_min = nota_min
        self.aluno_aceitos: list[Aluno] = []

    def tem_vaga(self) -> bool:
        """Retorna True se o projeto ainda tem vagas disponíveis."""
        return len(self.aluno_aceitos) < self.num_vagas

    def aceita_nota(self, nota: int) -> bool:
        """Retorna True se a nota atende ao requisito mínimo do projeto."""
        return nota >= self.nota_min

    def pior_aluno(self) -> Aluno | None:
        """Retorna o aluno de menor nota aceito ou None se vazio."""
        if not self.aluno_aceitos:
            return None
        return min(self.aluno_aceitos, key=lambda a: a.nota)

    def inserir_aluno(self, aluno: Aluno) -> None:
        """Insere aluno mantendo ordem decrescente de nota (melhor primeiro)."""
        notas = [-a.nota for a in self.aluno_aceitos]
        pos = bisect.bisect_right(notas, -aluno.nota)
        self.aluno_aceitos.insert(pos, aluno)

    def __repr__(self):
        return f"Projeto(cod='{self.cod}', num_vagas={self.num_vagas}, nota_min={self.nota_min})"
