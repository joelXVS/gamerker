import pygame
import sys
import random
import math
from enum import Enum

# Inicializar pygame
pygame.init()

# Constantes
ANCHO, ALTO = 1000, 700
TAMANO_CASILLA = 40
FILAS, COLUMNAS = 20, 10  # Esto nos da 200 casillas
MARGEN_TABLERO = 50
ANCHO_TABLERO = COLUMNAS * TAMANO_CASILLA
ALTO_TABLERO = FILAS * TAMANO_CASILLA

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL_CLARO = (173, 216, 230)
VERDE_CLARO = (144, 238, 144)
ROSA_CLARO = (255, 182, 193)
AMARILLO_CLARO = (255, 255, 224)

# Colores de jugadores
COLORES_JUGADORES = [
    (255, 0, 0),     # Rojo
    (0, 0, 255),     # Azul
    (0, 255, 0),     # Verde
    (255, 165, 0)    # Naranja
]

# Estados del juego
class EstadoJuego(Enum):
    MENU_PRINCIPAL = 0
    SELECCION_JUGADORES = 1
    JUEGO = 2
    FINAL = 3

# Configurar la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Serpientes y Escaleras")
reloj = pygame.time.Clock()

# Clase Jugador
class Jugador:
    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.posicion = 1  # Todos comienzan en la casilla 1
        self.es_pc = False
    
    def mover(self, pasos):
        nueva_posicion = self.posicion + pasos
        if nueva_posicion <= 200:  # No se puede pasar de 200
            self.posicion = nueva_posicion
        return self.posicion

    def dibujar(self, superficie):
        # Convertir posición a coordenadas en el tablero
        fila, columna = posicion_a_coordenadas(self.posicion)
        x = MARGEN_TABLERO + columna * TAMANO_CASILLA + TAMANO_CASILLA // 2
        y = ALTO - MARGEN_TABLERO - fila * TAMANO_CASILLA - TAMANO_CASILLA // 2
        
        # Desplazamiento para múltiples jugadores en la misma casilla
        desplazamiento = self.id * 5
        
        # Dibujar ficha del jugador
        pygame.draw.circle(superficie, self.color, (x + desplazamiento, y - desplazamiento), 10)

# Clase Tablero
class Tablero:
    def __init__(self):
        self.serpientes = {}  # Dict de cabeza -> cola
        self.escaleras = {}   # Dict de inicio -> fin
        self.generar_serpientes_escaleras()
    
    def generar_serpientes_escaleras(self):
        # Generar escaleras (10 escaleras)
        for _ in range(10):
            inicio = random.randint(1, 180)  # No muy cerca del final
            fin = random.randint(inicio + 10, min(199, inicio + 50))  # Asegurar que suban
            self.escaleras[inicio] = fin
        
        # Generar serpientes (10 serpientes)
        for _ in range(10):
            cabeza = random.randint(20, 199)  # No muy cerca del inicio
            cola = random.randint(max(1, cabeza - 50), cabeza - 5)  # Asegurar que bajen
            self.serpientes[cabeza] = cola
    
    def verificar_casilla(self, posicion):
        if posicion in self.escaleras:
            return self.escaleras[posicion]
        elif posicion in self.serpientes:
            return self.serpientes[posicion]
        return posicion
    
    def dibujar(self, superficie):
        # Dibujar fondo del tablero
        pygame.draw.rect(superficie, BLANCO, 
                        (MARGEN_TABLERO, MARGEN_TABLERO, 
                         ANCHO_TABLERO, ALTO_TABLERO))
        
        # Dibujar casillas
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                # Alternar colores para las casillas
                if (fila + columna) % 2 == 0:
                    color = AZUL_CLARO
                else:
                    color = VERDE_CLARO
                
                x = MARGEN_TABLERO + columna * TAMANO_CASILLA
                y = MARGEN_TABLERO + fila * TAMANO_CASILLA
                
                pygame.draw.rect(superficie, color, 
                                (x, y, TAMANO_CASILLA, TAMANO_CASILLA))
                
                # Calcular número de casilla
                if fila % 2 == 0:  # Filas pares (0, 2, 4...), de izquierda a derecha
                    num_casilla = (FILAS - fila - 1) * COLUMNAS + columna + 1
                else:  # Filas impares (1, 3, 5...), de derecha a izquierda
                    num_casilla = (FILAS - fila) * COLUMNAS - columna
                
                # Dibujar número de casilla
                fuente = pygame.font.SysFont(None, 20)
                texto = fuente.render(str(num_casilla), True, NEGRO)
                superficie.blit(texto, (x + 5, y + 5))
        
        # Dibujar serpientes
        for cabeza, cola in self.serpientes.items():
            inicio_fila, inicio_col = posicion_a_coordenadas(cabeza)
            fin_fila, fin_col = posicion_a_coordenadas(cola)
            
            x1 = MARGEN_TABLERO + inicio_col * TAMANO_CASILLA + TAMANO_CASILLA // 2
            y1 = MARGEN_TABLERO + inicio_fila * TAMANO_CASILLA + TAMANO_CASILLA // 2
            x2 = MARGEN_TABLERO + fin_col * TAMANO_CASILLA + TAMANO_CASILLA // 2
            y2 = MARGEN_TABLERO + fin_fila * TAMANO_CASILLA + TAMANO_CASILLA // 2
            
            pygame.draw.line(superficie, (255, 0, 0), (x1, y1), (x2, y2), 3)
            pygame.draw.circle(superficie, (255, 0, 0), (x1, y1), 5)  # Cabeza
            pygame.draw.circle(superficie, (150, 0, 0), (x2, y2), 5)  # Cola
        
        # Dibujar escaleras
        for inicio, fin in self.escaleras.items():
            inicio_fila, inicio_col = posicion_a_coordenadas(inicio)
            fin_fila, fin_col = posicion_a_coordenadas(fin)
            
            x1 = MARGEN_TABLERO + inicio_col * TAMANO_CASILLA + TAMANO_CASILLA // 2
            y1 = MARGEN_TABLERO + inicio_fila * TAMANO_CASILLA + TAMANO_CASILLA // 2
            x2 = MARGEN_TABLERO + fin_col * TAMANO_CASILLA + TAMANO_CASILLA // 2
            y2 = MARGEN_TABLERO + fin_fila * TAMANO_CASILLA + TAMANO_CASILLA // 2
            
            pygame.draw.line(superficie, (0, 128, 0), (x1, y1), (x2, y2), 3)
            pygame.draw.circle(superficie, (0, 128, 0), (x1, y1), 5)  # Inicio
            pygame.draw.circle(superficie, (0, 200, 0), (x2, y2), 5)  # Fin

# Clase Juego
class Juego:
    def __init__(self):
        self.estado = EstadoJuego.MENU_PRINCIPAL
        self.tablero = Tablero()
        self.jugadores = []
        self.jugador_actual = 0
        self.valor_dado = 0
        self.lanzando_dado = False
        self.tiempo_lanzamiento = 0
        self.ganador = None
        self.num_jugadores = 0
        self.incluir_pc = False
    
    def iniciar_juego(self, num_jugadores, incluir_pc=False):
        self.jugadores = []
        self.num_jugadores = num_jugadores
        self.incluir_pc = incluir_pc
        
        # Crear jugadores
        for i in range(num_jugadores):
            self.jugadores.append(Jugador(i, COLORES_JUGADORES[i]))
        
        # Si se incluye PC, reemplazar el último jugador
        if incluir_pc:
            self.jugadores[-1].es_pc = True
        
        self.jugador_actual = 0
        self.estado = EstadoJuego.JUEGO
        self.tablero = Tablero()  # Generar nuevo tablero
    
    def lanzar_dado(self):
        if not self.lanzando_dado:
            self.lanzando_dado = True
            self.tiempo_lanzamiento = pygame.time.get_ticks()
    
    def actualizar_lanzamiento(self):
        if self.lanzando_dado:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_lanzamiento > 1000:  # 1 segundo de animación
                self.valor_dado = random.randint(1, 6)
                self.lanzando_dado = False
                
                # Mover jugador
                jugador = self.jugadores[self.jugador_actual]
                nueva_posicion = jugador.mover(self.valor_dado)
                
                # Verificar si cayó en serpiente o escalera
                nueva_posicion = self.tablero.verificar_casilla(nueva_posicion)
                jugador.posicion = nueva_posicion
                
                # Verificar si hay un ganador
                if nueva_posicion == 200:
                    self.ganador = jugador
                    self.estado = EstadoJuego.FINAL
                else:
                    # Pasar al siguiente jugador
                    self.jugador_actual = (self.jugador_actual + 1) % len(self.jugadores)
                    
                    # Si el siguiente jugador es PC, lanzar automáticamente
                    if self.jugadores[self.jugador_actual].es_pc:
                        self.lanzar_dado()
    
    def dibujar(self):
        ventana.fill(GRIS)
        
        if self.estado == EstadoJuego.MENU_PRINCIPAL:
            self.dibujar_menu_principal()
        elif self.estado == EstadoJuego.SELECCION_JUGADORES:
            self.dibujar_seleccion_jugadores()
        elif self.estado == EstadoJuego.JUEGO:
            self.dibujar_juego()
        elif self.estado == EstadoJuego.FINAL:
            self.dibujar_final()
    
    def dibujar_menu_principal(self):
        # Dibujar título
        fuente_titulo = pygame.font.SysFont(None, 72)
        texto_titulo = fuente_titulo.render("Serpientes y Escaleras", True, NEGRO)
        ventana.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 150))
        
        # Dibujar botón de inicio
        pygame.draw.rect(ventana, VERDE_CLARO, (ANCHO // 2 - 100, 300, 200, 50))
        fuente_boton = pygame.font.SysFont(None, 36)
        texto_boton = fuente_boton.render("Comenzar", True, NEGRO)
        ventana.blit(texto_boton, (ANCHO // 2 - texto_boton.get_width() // 2, 310))
    
    def dibujar_seleccion_jugadores(self):
        # Dibujar título
        fuente_titulo = pygame.font.SysFont(None, 48)
        texto_titulo = fuente_titulo.render("Selecciona Jugadores", True, NEGRO)
        ventana.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 100))
        
        opciones = ["1 Jugador vs PC", "2 Jugadores", "3 Jugadores", "4 Jugadores"]
        
        for i, opcion in enumerate(opciones):
            y = 200 + i * 70
            pygame.draw.rect(ventana, AZUL_CLARO, (ANCHO // 2 - 150, y, 300, 50))
            fuente_opcion = pygame.font.SysFont(None, 36)
            texto_opcion = fuente_opcion.render(opcion, True, NEGRO)
            ventana.blit(texto_opcion, (ANCHO // 2 - texto_opcion.get_width() // 2, y + 10))
    
    def dibujar_juego(self):
        # Dibujar tablero
        self.tablero.dibujar(ventana)
        
        # Dibujar jugadores
        for jugador in self.jugadores:
            jugador.dibujar(ventana)
        
        # Dibujar información del turno y dado
        fuente_info = pygame.font.SysFont(None, 36)
        texto_turno = fuente_info.render(f"Turno: Jugador {self.jugador_actual + 1}", True, self.jugadores[self.jugador_actual].color)
        ventana.blit(texto_turno, (ANCHO - 250, 50))
        
        # Dibujar dado
        pygame.draw.rect(ventana, BLANCO, (ANCHO - 200, 100, 100, 100))
        if self.lanzando_dado:
            valor_mostrado = random.randint(1, 6)
        else:
            valor_mostrado = self.valor_dado if self.valor_dado > 0 else "?"
        
        texto_dado = fuente_info.render(str(valor_mostrado), True, NEGRO)
        ventana.blit(texto_dado, (ANCHO - 150, 130))
        
        # Dibujar botón de lanzar dado
        if not self.lanzando_dado and not self.jugadores[self.jugador_actual].es_pc:
            pygame.draw.rect(ventana, VERDE_CLARO, (ANCHO - 200, 220, 100, 50))
            fuente_boton = pygame.font.SysFont(None, 24)
            texto_boton = fuente_boton.render("Lanzar", True, NEGRO)
            ventana.blit(texto_boton, (ANCHO - 170, 235))
    
    def dibujar_final(self):
        ventana.fill(ROSA_CLARO)
        
        # Dibujar mensaje de ganador
        fuente_titulo = pygame.font.SysFont(None, 72)
        texto_titulo = fuente_titulo.render(f"¡Jugador {self.ganador.id + 1} Gana!", True, self.ganador.color)
        ventana.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 150))
        
        # Dibujar botón de volver al menú
        pygame.draw.rect(ventana, VERDE_CLARO, (ANCHO // 2 - 150, 300, 300, 50))
        fuente_boton = pygame.font.SysFont(None, 36)
        texto_boton = fuente_boton.render("Volver al Menú", True, NEGRO)
        ventana.blit(texto_boton, (ANCHO // 2 - texto_boton.get_width() // 2, 310))
        
        # Dibujar botón de jugar de nuevo
        pygame.draw.rect(ventana, AZUL_CLARO, (ANCHO // 2 - 150, 370, 300, 50))
        texto_boton = fuente_boton.render("Jugar de Nuevo", True, NEGRO)
        ventana.blit(texto_boton, (ANCHO // 2 - texto_boton.get_width() // 2, 380))

    def manejar_eventos(self, evento):
        if evento.type == pygame.QUIT:
            return False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()
            
            if self.estado == EstadoJuego.MENU_PRINCIPAL:
                # Verificar clic en botón de inicio
                if ANCHO // 2 - 100 <= pos_mouse[0] <= ANCHO // 2 + 100 and 300 <= pos_mouse[1] <= 350:
                    self.estado = EstadoJuego.SELECCION_JUGADORES
            
            elif self.estado == EstadoJuego.SELECCION_JUGADORES:
                # Verificar clic en opciones de jugadores
                for i in range(4):
                    y = 200 + i * 70
                    if ANCHO // 2 - 150 <= pos_mouse[0] <= ANCHO // 2 + 150 and y <= pos_mouse[1] <= y + 50:
                        if i == 0:  # 1 Jugador vs PC
                            self.iniciar_juego(2, True)
                        else:  # 2, 3 o 4 Jugadores
                            self.iniciar_juego(i + 1)
            
            elif self.estado == EstadoJuego.JUEGO:
                # Verificar clic en botón de lanzar dado
                if not self.lanzando_dado and not self.jugadores[self.jugador_actual].es_pc:
                    if ANCHO - 200 <= pos_mouse[0] <= ANCHO - 100 and 220 <= pos_mouse[1] <= 270:
                        self.lanzar_dado()
            
            elif self.estado == EstadoJuego.FINAL:
                # Verificar clic en botón de volver al menú
                if ANCHO // 2 - 150 <= pos_mouse[0] <= ANCHO // 2 + 150 and 300 <= pos_mouse[1] <= 350:
                    self.estado = EstadoJuego.MENU_PRINCIPAL
                
                # Verificar clic en botón de jugar de nuevo
                if ANCHO // 2 - 150 <= pos_mouse[0] <= ANCHO // 2 + 150 and 370 <= pos_mouse[1] <= 420:
                    self.iniciar_juego(self.num_jugadores, self.incluir_pc)
        
        return True

# Función para convertir posición (1-200) a coordenadas (fila, columna)
def posicion_a_coordenadas(posicion):
    posicion -= 1  # Ajustar a índice 0
    fila = FILAS - 1 - (posicion // COLUMNAS)
    
    if (FILAS - 1 - fila) % 2 == 0:  # Filas pares (desde abajo)
        columna = posicion % COLUMNAS
    else:  # Filas impares (desde abajo)
        columna = COLUMNAS - 1 - (posicion % COLUMNAS)
    
    return fila, columna

# Función principal
def main():
    juego = Juego()
    ejecutando = True
    
    while ejecutando:
        for evento in pygame.event.get():
            ejecutando = juego.manejar_eventos(evento)
        
        # Actualizar lógica del juego
        if juego.estado == EstadoJuego.JUEGO:
            juego.actualizar_lanzamiento()
        
        # Dibujar
        juego.dibujar()
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()