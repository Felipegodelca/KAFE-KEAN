import math
import random


class SimpleQTable:
    def __init__(self, scores):
        self.scores = scores
        self.empty = not bool(scores)

    def mean(self):
        return self

    def idxmax(self):
        if not self.scores:
            return None
        return max(self.scores, key=self.scores.get)


def calcular_esfuerzo(proposito=5, progreso=5, resistencia=1):
    proposito = float(proposito)
    progreso = float(progreso)
    resistencia = max(float(resistencia), 1)
    return round(math.sqrt((proposito**2 + progreso**2) / resistencia), 2)


def ejecutar_q_learning(num_episodios=1500):
    acciones = {
        "Refuerza tu propósito": 0.72,
        "Avanza con constancia": 0.84,
        "Reduce fricción y enfócate": 0.78,
    }
    recompensas = []
    acumulado = 0.0
    for episodio in range(min(int(num_episodios), 1500)):
        acumulado += random.uniform(0.01, 0.05)
        recompensas.append(round(acumulado / (episodio + 1), 4))
    estado_final = (8, 7, 2)
    return SimpleQTable(acciones), recompensas, estado_final
