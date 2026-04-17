"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""

from entorno import Agente

import random
class MiAgente(Agente):
    """
    Tu agente de navegación.

    Implementa el método decidir() para que el agente
    llegue del punto A al punto B en el grid.
    """


    def __init__(self):
        super().__init__(nombre="Agente Inteligente Mejorado")

        # Memoria de celdas visitadas
        self.visitadas = set()

        # Para evitar ir y venir
        self.pos_anterior = None

    def al_iniciar(self):
        self.visitadas = set()
        self.pos_anterior = None

    def es_valido(self, percepcion, direccion):
        return percepcion[direccion] == 'libre' or percepcion[direccion] == 'meta'

    def decidir(self, percepcion):

        pos_actual = percepcion['posicion']
        self.visitadas.add(pos_actual)

        # 🎯 1. Si ve la meta, va directo SIEMPRE
        for direccion in self.ACCIONES:
            if percepcion[direccion] == 'meta':
                return direccion

        vert, horiz = percepcion['direccion_meta']

        # 🎯 2. PRIORIDAD FUERTE hacia la meta (80%)
        for dir in [vert, horiz]:
            if dir != 'ninguna' and self.es_valido(percepcion, dir):
                if random.random() < 0.8:
                    return dir

        # 🌍 3. Generar opciones válidas (sin duplicados)
        opciones = []
        for dir in self.ACCIONES:
            if self.es_valido(percepcion, dir):
                if dir not in opciones:
                    opciones.append(dir)

        # 🔄 4. Evitar retroceder si hay más opciones
        if self.pos_anterior:
            opciones_filtradas = []
            for dir in opciones:
                dr, dc = self.DELTAS[dir]
                nueva_pos = (pos_actual[0] + dr, pos_actual[1] + dc)

                if nueva_pos != self.pos_anterior:
                    opciones_filtradas.append(dir)

            if opciones_filtradas:
                opciones = opciones_filtradas

        # 🧠 5. Preferir no visitadas
        no_visitadas = []
        for dir in opciones:
            dr, dc = self.DELTAS[dir]
            nueva_pos = (pos_actual[0] + dr, pos_actual[1] + dc)

            if nueva_pos not in self.visitadas:
                no_visitadas.append(dir)

        # 🎯 6. Si solo hay una opción clara, tomarla
        if len(no_visitadas) == 1:
            decision = no_visitadas[0]

        # 🎲 7. Decisión con control de aleatoriedad
        elif no_visitadas:
            decision = random.choice(no_visitadas)

        elif opciones:
            decision = random.choice(opciones)

        else:
            decision = random.choice(self.ACCIONES)

        # Guardar posición anterior
        self.pos_anterior = pos_actual

        return decision
        # ╔══════════════════════════════════════╗
        # ║   ESCRIBE TU LÓGICA AQUÍ             ║
        # ╚══════════════════════════════════════╝

        # Ejemplo básico (bórralo y escribe tu propia lógica):
        #
        # vert, horiz = percepcion['direccion_meta']
        #
        # if percepcion[vert] == 'libre' or percepcion[vert] == 'meta':
        #     return vert
        # if percepcion[horiz] == 'libre' or percepcion[horiz] == 'meta':
        #     return horiz
        #
        # return 'abajo'
        print('Hola decidir')
        for direccion in self.ACCIONES:
            celda = percepcion[direccion]
            if celda == 'meta':
                return direccion
            if celda == 'libre':
                return direccion

        return 'abajo'  # ← Reemplazar con tu lógica