# -*- coding: utf-8 -*-
"""
Algoritmo KAFE KEAN con Ajustes Finos en R y DO, RL Optimizado, Isolation Forest y Visualización 3D
"""

# 📚 IMPORTAR BIBLIOTECAS
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import io, base64
from sklearn.ensemble import IsolationForest
import logging

# 🔕 Desactivar logs innecesarios
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

# 🔑 VARIABLES INICIALES
def get_estado_inicial():
    """Retorna los valores iniciales del estado"""
    return (5.0, 3.0, 2.0, 1.5, 0.8, 0.7)  # (B, H_p, C, AI, R, DO)

# Parámetros RL
alpha = 0.1  
gamma = 0.95  
epsilon = 0.5  
num_episodios = 1500  
acciones = ['Ajustar_B', 'Ajustar_H', 'Ajustar_C', 'Ajustar_AI', 'Ajustar_R', 'Ajustar_DO']

# 📊 FUNCIONES PRINCIPALES
def calcular_esfuerzo(B, H_p, C, AI, R, DO):
    """Calcula el esfuerzo optimizado."""
    return (B * H_p) * (C**2 * AI) * R * DO

def calcular_recompensa_con_DO(estado):
    """Calcula la recompensa basada en el estado."""
    B, H_p, C, AI, R, DO = estado
    E = calcular_esfuerzo(B, H_p, C, AI, R, DO)
    incertidumbre = abs(E - DO)
    estabilidad_R = (1 / (1 + abs(R - 0.8)))  
    recompensa = (E / 100) - (0.1 * incertidumbre) + (0.2 * estabilidad_R)
    return recompensa

def actualizar_estado(estado, accion):
    """Actualiza el estado en base a la acción tomada."""
    B, H_p, C, AI, R, DO = estado
    delta = random.uniform(-0.3, 0.3)
    if accion == 'Ajustar_B': B = max(0.1, B + delta)
    elif accion == 'Ajustar_H': H_p = max(0.1, H_p + delta)
    elif accion == 'Ajustar_C': C = max(0.1, C + delta)
    elif accion == 'Ajustar_AI': AI = max(0.1, AI + delta)
    elif accion == 'Ajustar_R': R = max(0.1, R + delta)
    elif accion == 'Ajustar_DO': DO = max(0.1, DO + delta)
    return (B, H_p, C, AI, R, DO)

# 🧠 Q-LEARNING
def ejecutar_q_learning(num_episodios=1500):
    """Ejecuta el algoritmo de Q-Learning."""
    B, H_p, C, AI, R, DO = get_estado_inicial()
    num_estados = 150
    Q = pd.DataFrame(np.zeros((num_estados, len(acciones))), columns=acciones)
    estado = (B, H_p, C, AI, R, DO)
    recompensas_totales = []

    for episodio in range(num_episodios):
        estado_idx = episodio % num_estados
        accion = random.choice(acciones) if random.uniform(0, 1) < epsilon else Q.loc[estado_idx].idxmax()
        nuevo_estado = actualizar_estado(estado, accion)

        recompensa = calcular_recompensa_con_DO(nuevo_estado)
        Q.loc[estado_idx, accion] = (1 - alpha) * Q.loc[estado_idx, accion] + alpha * (recompensa + gamma * Q.loc[estado_idx].max())

        recompensas_totales.append(recompensa)
        estado = nuevo_estado

    return Q, recompensas_totales, estado

# 📊 DETECCIÓN DE ANOMALÍAS
def detectar_anomalias():
    """Ejecuta la detección de anomalías con Isolation Forest."""
    B, H_p, C, AI, R, DO = get_estado_inicial()
    data = pd.DataFrame({
        'AI_VALUE': np.random.rand(300),
        'C_VALUE': np.random.rand(300),
        'R': np.random.rand(300),
        'DO': np.random.rand(300)
    })
    data['E'] = calcular_esfuerzo(B, H_p, data['C_VALUE'], data['AI_VALUE'], data['R'], data['DO'])

    modelo_anomalias = IsolationForest(n_estimators=150, contamination=0.03, random_state=42)
    data['DO_FLAG'] = modelo_anomalias.fit_predict(data[['DO', 'E']])
    return data

# 📈 VISUALIZACIÓN PARA WEB
def generar_grafico():
    """Genera un gráfico de convergencia de Q-Learning y lo devuelve como imagen base64."""
    _, recompensas_totales, _ = ejecutar_q_learning()
    
    fig, ax = plt.subplots()
    ax.plot(recompensas_totales)
    ax.set_title('Convergencia del Aprendizaje por Refuerzo')
    ax.set_xlabel('Episodios')
    ax.set_ylabel('Recompensa')
    ax.grid(True)

    # Convertir la imagen en base64 para mostrar en Django
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded_string = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    
    return encoded_string