from dataclasses import dataclass


class ErroreSemantico(Exception):
    pass


@dataclass
class SimboloFunzione:
    nome: str
    tipi_parametri: list
    tipo_ritorno: str | None


class TabellaFunzioni:
    """Tabella globale: una voce per ogni funzione del programma."""

    def __init__(self):
        self._funzioni = {}

    def dichiara(self, simbolo):
        if simbolo.nome in self._funzioni:
            raise ErroreSemantico(
                f"funzione '{simbolo.nome}' dichiarata piu' volte"
            )
        self._funzioni[simbolo.nome] = simbolo

    def cerca(self, nome):
        return self._funzioni.get(nome)


class TabellaVariabili:
    """Scope di una funzione: parametri e variabili locali con il loro tipo."""

    def __init__(self):
        self._variabili = {}

    def dichiara(self, nome, tipo):
        if nome in self._variabili:
            raise ErroreSemantico(f"'{nome}' dichiarato piu' volte")
        self._variabili[nome] = tipo

    def cerca(self, nome):
        return self._variabili.get(nome)
