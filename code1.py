import pygame
import random
import sys
from pygame.locals import *

# Inicializar Pygame
pygame.init()
pygame.font.init()

# Constantes
ANCHO = 1000
ALTO = 700
FPS = 60
FONDO = (25, 25, 35)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
ROJO = (220, 60, 60)
VERDE = (60, 220, 80)
AZUL = (60, 100, 220)
AMARILLO = (220, 220, 60)
PURPURA = (180, 60, 220)
CYAN = (60, 220, 220)
NARANJA = (255, 165, 0)

# Colores para los jugadores
COLORES_JUGADORES = [ROJO, AZUL, VERDE, AMARILLO]

# Fuentes
FUENTE_GRANDE = pygame.font.SysFont("Arial", 48, bold=True)
FUENTE_MEDIANA = pygame.font.SysFont("Arial", 32, bold=True)
FUENTE_PEQUEÑA = pygame.font.SysFont("Arial", 20)

# Configuración de la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Serpientes y Escaleras")
reloj = pygame.time.Clock()

class Tablero:
    def __init__(self):
        self.casillas = 200
        self.filas = 20
        self.columnas = 10
        self.tam_casilla = 60
        self.margen_x = (ANCHO - self.columnas * self.tam_casilla) // 2
        self.margen_y = 50
        self.serpientes = {}
        self.escaleras = {}
        self.generar_serpientes_escaleras()
    
    def generar_serpientes_escaleras(self):
        # Generar serpientes (retrocesos)
        num_serpientes = 15
        for _ in range(num_serpientes):
            inicio = random.randint(30, self.casillas - 1)  # Evitar casillas muy bajas
            fin = random.randint(1, inicio - 20)  # Retroceso significativo
            self.serpientes[inicio] = fin
        
        # Generar escaleras (avances)
        num_escaleras = 15
        for _ in range(num_escaleras):
            inicio = random.randint(1, self.casillas - 30)  # Evitar casillas muy altas
            fin = random.randint(inicio + 20, min(inicio + 80, self.casillas - 1))  # Avance significativo
            # Evitar que una escalera termine donde empieza una serpiente
            if fin not in self.serpientes:
                self.escaleras[inicio] = fin
    
    def obtener_coordenadas_casilla(self, numero_casilla):
        if numero_casilla <= 0 or numero_casilla > self.casillas:
            return None
        
        # Ajustar a índice base 0
        numero_casilla -= 1
        
        # Calcular fila y columna (zigzag)
        fila = 19 - (numero_casilla // 10)
        col = numero_casilla % 10
        
        # En filas pares, invertir el orden de las columnas (zigzag)
        if fila % 2 == 1:
            col = 9 - col
            
        # Convertir a coordenadas en píxeles
        x = self.margen_x + col * self.tam_casilla + self.tam_casilla // 2
        y = self.margen_y + fila * self.tam_casilla + self.tam_casilla // 2
        
        return (x, y)
    
    def dibujar(self):
        for i in range(1, self.casillas + 1):
            # Determinar color de la casilla
            if i in self.serpientes:
                color_casilla = (220, 100, 100)  # Rojo claro para serpientes
            elif i in self.escaleras:
                color_casilla = (100, 220, 100)  # Verde claro para escaleras
            else:
                color_casilla = (220, 220, 220)  # Gris claro para normal
                
            # Calcular posición
            coord = self.obtener_coordenadas_casilla(i)
            if coord:
                x, y = coord
                
                # Dibujar casilla
                pygame.draw.rect(ventana, color_casilla, 
                                (x - self.tam_casilla//2, y - self.tam_casilla//2, 
                                 self.tam_casilla, self.tam_casilla))
                
                # Dibujar borde
                pygame.draw.rect(ventana, NEGRO, 
                                (x - self.tam_casilla//2, y - self.tam_casilla//2, 
                                 self.tam_casilla, self.tam_casilla), 1)
                
                # Dibujar número de casilla
                texto = FUENTE_PEQUEÑA.render(str(i), True, NEGRO)
                ventana.blit(texto, (x - texto.get_width()//2, y - texto.get_height()//2))
        
        # Dibujar serpientes y escaleras
        for inicio, fin in self.serpientes.items():
            inicio_coord = self.obtener_coordenadas_casilla(inicio)
            fin_coord = self.obtener_coordenadas_casilla(fin)
            if inicio_coord and fin_coord:
                # Dibujar línea con efecto serpentina
                pygame.draw.line(ventana, ROJO, inicio_coord, fin_coord, 4)
                # Dibujar cabeza de serpiente
                pygame.draw.circle(ventana, ROJO, fin_coord, 8)
        
        for inicio, fin in self.escaleras.items():
            inicio_coord = self.obtener_coordenadas_casilla(inicio)
            fin_coord = self.obtener_coordenadas_casilla(fin)
            if inicio_coord and fin_coord:
                # Dibujar línea de escalera
                pygame.draw.line(ventana, VERDE, inicio_coord, fin_coord, 4)
                # Dibujar tope de escalera
                pygame.draw.circle(ventana, VERDE, fin_coord, 8)

class Jugador:
    def __init__(self, id, es_bot=False, color=ROJO):
        self.id = id
        self.es_bot = es_bot
        self.posicion = 0
        self.color = color
        self.tamano = 15
        self.ganador = False
        
    def mover(self, pasos, tablero):
        nueva_posicion = self.posicion + pasos
        
        # Verificar si se pasa del final
        if nueva_posicion > tablero.casillas:
            return False
        
        self.posicion = nueva_posicion
        
        # Verificar si cayó en una serpiente
        if self.posicion in tablero.serpientes:
            self.posicion = tablero.serpientes[self.posicion]
            return "serpiente"
        
        # Verificar si cayó en una escalera
        if self.posicion in tablero.escaleras:
            self.posicion = tablero.escaleras[self.posicion]
            return "escalera"
        
        # Verificar si llegó a la meta
        if self.posicion == tablero.casillas:
            self.ganador = True
            return "ganador"
        
        return True
        
    def dibujar(self, tablero):
        if self.posicion > 0:
            coord = tablero.obtener_coordenadas_casilla(self.posicion)
            if coord:
                # Ajustar posición para múltiples jugadores en la misma casilla
                x, y = coord
                offset_x = (self.id % 2) * 20 - 10
                offset_y = (self.id // 2) * 20 - 10
                
                # Dibujar ficha
                pygame.draw.circle(ventana, self.color, (x + offset_x, y + offset_y), self.tamano)
                pygame.draw.circle(ventana, NEGRO, (x + offset_x, y + offset_y), self.tamano, 2)
                
                # Dibujar número del jugador
                texto = FUENTE_PEQUEÑA.render(str(self.id + 1), True, BLANCO)
                ventana.blit(texto, (x + offset_x - texto.get_width()//2, y + offset_y - texto.get_height()//2))

class Dado:
    def __init__(self):
        self.valor = 1
        self.lanzando = False
        self.contador_animacion = 0
        self.duracion_animacion = 20
        
    def lanzar(self):
        self.lanzando = True
        self.contador_animacion = 0
        
    def actualizar(self):
        if self.lanzando:
            self.contador_animacion += 1
            self.valor = random.randint(1, 6)
            
            if self.contador_animacion >= self.duracion_animacion:
                self.lanzando = False
                return True
        return False
    
    def dibujar(self, x, y, tamano=80):
        # Fondo del dado
        pygame.draw.rect(ventana, BLANCO, (x, y, tamano, tamano), border_radius=10)
        pygame.draw.rect(ventana, NEGRO, (x, y, tamano, tamano), 2, border_radius=10)
        
        # Puntos del dado según el valor
        punto_radio = tamano // 10
        if self.valor == 1:
            pygame.draw.circle(ventana, NEGRO, (x + tamano//2, y + tamano//2), punto_radio)
        elif self.valor == 2:
            pygame.draw.circle(ventana, NEGRO, (x + tamano//4, y + tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + 3*tamano//4, y + 3*tamano//4), punto_radio)
        elif self.valor == 3:
            pygame.draw.circle(ventana, NEGRO, (x + tamano//4, y + tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + tamano//2, y + tamano//2), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + 3*tamano//4, y + 3*tamano//4), punto_radio)
        elif self.valor == 4:
            pygame.draw.circle(ventana, NEGRO, (x + tamano//4, y + tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + 3*tamano//4, y + tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + tamano//4, y + 3*tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + 3*tamano//4, y + 3*tamano//4), punto_radio)
        elif self.valor == 5:
            pygame.draw.circle(ventana, NEGRO, (x + tamano//4, y + tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + 3*tamano//4, y + tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + tamano//2, y + tamano//2), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + tamano//4, y + 3*tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + 3*tamano//4, y + 3*tamano//4), punto_radio)
        elif self.valor == 6:
            pygame.draw.circle(ventana, NEGRO, (x + tamano//4, y + tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + 3*tamano//4, y + tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + tamano//4, y + tamano//2), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + 3*tamano//4, y + tamano//2), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + tamano//4, y + 3*tamano//4), punto_radio)
            pygame.draw.circle(ventana, NEGRO, (x + 3*tamano//4, y + 3*tamano//4), punto_radio)

class Juego:
    def __init__(self):
        self.estado = "menu_principal"
        self.tablero = Tablero()
        self.dado = Dado()
        self.jugadores = []
        self.turno_actual = 0
        self.contador_mensaje = 0
        self.mensaje = ""
        self.resultado_movimiento = None
        self.mostrar_resultados = False
        
    def iniciar_partida(self, num_jugadores, num_bots=0):
        self.jugadores = []
        total_jugadores = num_jugadores + num_bots
        
        # Crear jugadores humanos
        for i in range(num_jugadores):
            self.jugadores.append(Jugador(i, es_bot=False, color=COLORES_JUGADORES[i]))
        
        # Crear bots
        for i in range(num_bots):
            self.jugadores.append(Jugador(i + num_jugadores, es_bot=True, color=COLORES_JUGADORES[i + num_jugadores]))
        
        self.turno_actual = 0
        self.estado = "juego"
        self.mensaje = ""
        self.mostrar_resultados = False
        
    def procesar_evento(self, evento):
        if self.estado == "menu_principal":
            # Procesar eventos del menú principal
            if evento.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Verificar botones del menú
                if 350 <= x <= 650 and 200 <= y <= 250:
                    self.iniciar_partida(1, 1)  # Modo 1 jugador vs PC
                elif 350 <= x <= 650 and 280 <= y <= 330:
                    self.iniciar_partida(2, 0)  # Modo 2 jugadores
                elif 350 <= x <= 650 and 360 <= y <= 410:
                    self.iniciar_partida(3, 0)  # Modo 3 jugadores
                elif 350 <= x <= 650 and 440 <= y <= 490:
                    self.iniciar_partida(4, 0)  # Modo 4 jugadores
                elif 350 <= x <= 650 and 520 <= y <= 570:
                    pygame.quit()
                    sys.exit()
        
        elif self.estado == "juego":
            # Procesar eventos del juego
            if evento.type == MOUSEBUTTONDOWN:
                # Si es turno de un jugador humano y el dado no está en movimiento
                if (not self.jugadores[self.turno_actual].es_bot and 
                    not self.dado.lanzando and 
                    self.resultado_movimiento is None):
                    self.dado.lanzar()
        
        elif self.estado == "fin_partida":
            # Procesar eventos de fin de partida
            if evento.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Verificar botones
                if 300 <= x <= 500 and 450 <= y <= 500:
                    # Jugar de nuevo con mismos jugadores
                    self.iniciar_partida(sum(1 for j in self.jugadores if not j.es_bot), 
                                        sum(1 for j in self.jugadores if j.es_bot))
                elif 520 <= x <= 720 and 450 <= y <= 500:
                    # Volver al menú principal
                    self.estado = "menu_principal"
        
    def actualizar(self):
        if self.estado == "juego":
            jugador_actual = self.jugadores[self.turno_actual]
            
            # Procesar movimiento de bots
            if jugador_actual.es_bot and not self.dado.lanzando and self.resultado_movimiento is None:
                self.dado.lanzar()
            
            # Actualizar animación del dado
            if self.dado.lanzando:
                if self.dado.actualizar():
                    # El dado terminó de lanzarse
                    self.procesar_movimiento()
            
            # Manejar mensaje de resultado
            if self.resultado_movimiento is not None:
                self.contador_mensaje += 1
                if self.contador_mensaje > 60:  # Mostrar mensaje por 1 segundo
                    self.contador_mensaje = 0
                    self.resultado_movimiento = None
                    
                    # Verificar si hay un ganador
                    if jugador_actual.ganador:
                        self.mostrar_resultados = True
                        self.estado = "fin_partida"
                    else:
                        # Pasar al siguiente turno
                        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
    
    def procesar_movimiento(self):
        jugador_actual = self.jugadores[self.turno_actual]
        
        # Mover jugador según valor del dado
        resultado = jugador_actual.mover(self.dado.valor, self.tablero)
        
        # Mostrar mensaje según resultado
        if resultado == "serpiente":
            self.mensaje = f"¡Jugador {self.turno_actual + 1} cayó en una serpiente!"
        elif resultado == "escalera":
            self.mensaje = f"¡Jugador {self.turno_actual + 1} subió por una escalera!"
        elif resultado == "ganador":
            self.mensaje = f"¡Jugador {self.turno_actual + 1} ha ganado!"
        else:
            self.mensaje = f"Jugador {self.turno_actual + 1} avanzó {self.dado.valor} casillas"
        
        self.resultado_movimiento = resultado
    
    def dibujar_menu_principal(self):
        # Fondo
        ventana.fill(FONDO)
        
        # Título
        titulo = FUENTE_GRANDE.render("SERPIENTES Y ESCALERAS", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 80))
        
        # Botones
        self.dibujar_boton("1 Jugador vs PC", 350, 200, 300, 50, VERDE)
        self.dibujar_boton("2 Jugadores", 350, 280, 300, 50, AZUL)
        self.dibujar_boton("3 Jugadores", 350, 360, 300, 50, AMARILLO)
        self.dibujar_boton("4 Jugadores", 350, 440, 300, 50, ROJO)
        self.dibujar_boton("Salir", 350, 520, 300, 50, GRIS)
    
    def dibujar_juego(self):
        # Fondo
        ventana.fill(FONDO)
        
        # Dibujar tablero
        self.tablero.dibujar()
        
        # Dibujar jugadores
        for jugador in self.jugadores:
            jugador.dibujar(self.tablero)
        
        # Dibujar dado
        self.dado.dibujar(800, 100)
        
        # Información del turno
        jugador_actual = self.jugadores[self.turno_actual]
        texto_turno = FUENTE_MEDIANA.render(f"Turno: Jugador {self.turno_actual + 1}", True, jugador_actual.color)
        ventana.blit(texto_turno, (700, 200))
        
        # Información de posiciones
        y_pos = 250
        for i, jugador in enumerate(self.jugadores):
            texto = FUENTE_PEQUEÑA.render(f"Jugador {i+1}: Casilla {jugador.posicion}", True, jugador.color)
            ventana.blit(texto, (700, y_pos))
            y_pos += 30
        
        # Mostrar mensaje de resultado
        if self.resultado_movimiento is not None:
            pygame.draw.rect(ventana, (0, 0, 0, 180), (200, 300, 600, 80), border_radius=10)
            texto = FUENTE_MEDIANA.render(self.mensaje, True, BLANCO)
            ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 330))
        
        # Instrucciones
        if not jugador_actual.es_bot and not self.dado.lanzando and self.resultado_movimiento is None:
            texto = FUENTE_PEQUEÑA.render("Haz clic para lanzar el dado", True, BLANCO)
            ventana.blit(texto, (700, 400))
    
    def dibujar_fin_partida(self):
        # Fondo semi-transparente
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        ventana.blit(s, (0, 0))
        
        # Panel de resultados
        pygame.draw.rect(ventana, FONDO, (200, 150, 600, 400), border_radius=15)
        pygame.draw.rect(ventana, BLANCO, (200, 150, 600, 400), 3, border_radius=15)
        
        # Título
        ganador = next((j for j in self.jugadores if j.ganador), None)
        if ganador:
            texto = FUENTE_GRANDE.render(f"¡Jugador {ganador.id + 1} ha ganado!", True, ganador.color)
            ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 180))
        
        # Resultados
        y_pos = 250
        posiciones = sorted([(j.id, j.posicion) for j in self.jugadores], key=lambda x: x[1], reverse=True)
        for i, (id_jugador, posicion) in enumerate(posiciones):
            texto = FUENTE_MEDIANA.render(f"{i+1}. Jugador {id_jugador + 1}: Casilla {posicion}", True, self.jugadores[id_jugador].color)
            ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, y_pos))
            y_pos += 50
        
        # Botones
        self.dibujar_boton("Jugar de nuevo", 300, 450, 200, 50, VERDE)
        self.dibujar_boton("Menú principal", 520, 450, 200, 50, AZUL)
    
    def dibujar_boton(self, texto, x, y, ancho, alto, color):
        # Fondo del botón
        pygame.draw.rect(ventana, color, (x, y, ancho, alto), border_radius=10)
        pygame.draw.rect(ventana, NEGRO, (x, y, ancho, alto), 2, border_radius=10)
        
        # Texto del botón
        texto_render = FUENTE_PEQUEÑA.render(texto, True, NEGRO)
        ventana.blit(texto_render, (x + ancho//2 - texto_render.get_width()//2, 
                                y + alto//2 - texto_render.get_height()//2))
    
    def dibujar(self):
        if self.estado == "menu_principal":
            self.dibujar_menu_principal()
        elif self.estado == "juego":
            self.dibujar_juego()
            
            # Si se está mostrando el fin de partida
            if self.mostrar_resultados:
                self.dibujar_fin_partida()
        elif self.estado == "fin_partida":
            # Dibujar juego de fondo
            self.dibujar_juego()
            self.dibujar_fin_partida()

def main():
    juego = Juego()
    
    # Bucle principal
    ejecutando = True
    while ejecutando:
        # Eventos
        for evento in pygame.event.get():
            if evento.type == QUIT:
                ejecutando = False
            
            juego.procesar_evento(evento)
        
        # Actualizar
        juego.actualizar()
        
        # Dibujar
        juego.dibujar()
        
        pygame.display.flip()
        reloj.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()