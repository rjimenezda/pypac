#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame, time

def cargar_imagen(archivo, transparencia = False):
    """ Cargamos una imagen y cogemos el color key en 0, 0 """
    try:
        imagen = pygame.image.load(archivo)
    except pygame.error, message:
        raise SystemExit, message
    imagen = imagen.convert()
    if transparencia:
        color = imagen.get_at((0, 0))
        imagen.set_colorkey(color, pygame.RLEACCEL)
    return imagen
    
class Ghost(pygame.sprite.Sprite):
    """ Clase que maneja un fantasma cualquiera """
    def __init__(self, x = 0, y = 0):
        """ Constructor """
        # LLamamos al constructor de la clase de la que heredamos
        pygame.sprite.Sprite.__init__(self)
        
        # Estados para la IA
        self.estado = 'buscando'
        #self.estado = 'siguiendo'
        #self.estado = 'huyendo'
        #self.estado = 'volviendo'
        
        # Imágenes
        self._normal = list()
        self._huyendo = list()
        self._volviendo = list()

        self.load_imgs()
        
        self.parpadeo = False
        self.idx_deb = 0
        
        # Definimos una velocidad
        self.speed = 5
        
        # El fantasma no se mueve al crearse
        self.next_move = (0, 0)
        
        # El índice de la imagen normal
        self.idx_img = 0
        self.idx_img_huye = 0
        
        # La orientación
        self.orient = 0
        
        # Definimos la imagen inicial
        self.image = self._normal[self.orient][self.idx_img]
        
        # Definimos la posición, en principio la de la imagen
        self.rect = self.image.get_rect()
        
        # La alteramos si se pasa por parámetros
        self.rect = pygame.rect.Rect((x, y) , self.rect.bottomright)
        
        self.movimientos = [[4, 30], [1, 30], [3, 30], [2, 30]]
        
        self.temp_counter = 0
        
    def lolaso_padre(self):
        print 'YIEJAJAJAJ'
        
    def load_imgs(self):
        """ Creamos un vector con las imágenes del sprite """
        self._normal = list()
        print 'To be re-written'
        
    def stop(self):
        """ Detiene al fantasma """
        self.next_move = (0, 0)
    
    def left(self):
        """ El fantasma se mueve hacia la izquierda """
        self.next_move = (- self.speed, 0)
        self.orient = 0
        
    def right(self):
        """ El fantasma se mueve hacia la derecha """
        self.next_move = (self.speed, 0)
        self.orient = 1
        
    def down(self):
        """ El fantasma se mueve hacia abajo """
        self.next_move = (0, self.speed)
        self.orient = 2
        
    def up(self):
        """ El fantasma se mueve hacia arriba """
        self.next_move = (0, - self.speed)
        self.orient = 3
        
    def debilitar(self):
        """ Nos comemos una píldora gorda """
        self.estado = 'huyendo'
    
    def parpadear(self):
        """ Hacemos que parpadee el fantasma """
        self.parpadeo = True
    
    def habilitar(self):
        """ Se pasa el tiempo de la píldora gorda"""
        self.parpadeo = False
        self.estado = 'buscando'
        
    def comer(self):
        """ Nos comemos un fantasma """
        self.estado = 'volviendo'
        
    def ia(self):
        """ Define cómo se mueve el fantasma """
        try:
            t_a = self.movimientos[self.temp_counter]
            if t_a[1] != 0:
                if t_a[0] == 1:
                    self.right()
                    t_a[1] -= 1
                elif t_a[0] == 2:
                    self.left()
                    t_a[1] -= 1
                elif t_a[0] == 3:
                    self.up()
                    t_a[1] -= 1
                elif t_a[0] == 4:
                    self.down()
                    t_a[1] -= 1
            else:
                self.temp_counter += 1
        except IndexError:
            self.temp_counter = 0
            self.movimientos =  [[4, 30], [1, 30], [3, 30], [2, 30]]
    
    def update(self):
        """ """
        self.ia()
        
        if self.estado == 'buscando' or self.estado == 'persiguiendo':        
            # Si no está parado
            if self.next_move != (0, 0):
                # Miramos qué imagen hay que dibujar la siguiente
                if self.idx_img == 0:
                    self.idx_img += 1
                elif self.idx_img == 1:
                    self.idx_img -= 1
                
                # Asignamos esa imagen
                self.image = self._normal[self.orient][self.idx_img]
        elif self.estado == 'huyendo':
            
            if not self.parpadeo:
                if self.idx_deb == 0:
                    self.idx_deb = 2
                elif self.idx_deb == 2:
                    self.idx_deb = 0
            elif self.parpadeo:
                if self.idx_deb == 3:
                    self.idx_deb = 0
                else:
                    self.idx_deb += 1
            
            self.image = self._huyendo[self.idx_deb]
        elif self.estado == 'volviendo':
            self.image = self._volviendo[self.orient]
        
        # Movemos lo que haga falta
        self.rect = self.rect.move(self.next_move)
        
class Blinky(Ghost):
    """ 
        Especialización del fantasma con el sprite y el comportamiento
        del fantasma rosa 'Blinky'
    """
    def __init__(self, x, y):
        """ """
        Ghost.__init__(self, x, y)
        
    def load_imgs(self):
        """ Cargamos imágenes para Blinky """
        # Imágenes normales
        self._normal.append([cargar_imagen('img/blinkyl1.png', True),
         cargar_imagen('img/blinkyl2.png', True)])
        self._normal.append([cargar_imagen('img/blinkyr1.png', True),
         cargar_imagen('img/blinkyr2.png', True)])
        self._normal.append([cargar_imagen('img/blinkyd1.png', True),
         cargar_imagen('img/blinkyd2.png', True)])
        self._normal.append([cargar_imagen('img/blinkyu1.png', True),
         cargar_imagen('img/blinkyu2.png', True)])
        
        # Imágenes huyendo / parpadeando
        self._huyendo.append(cargar_imagen('img/blue1.png', True))
        self._huyendo.append(cargar_imagen('img/gray1.png', True))
        self._huyendo.append(cargar_imagen('img/blue2.png', True))
        self._huyendo.append(cargar_imagen('img/gray2.png', True))
        
        # Imágenes volviendo
        self._volviendo.append(cargar_imagen('img/eyesl.png', True))
        self._volviendo.append(cargar_imagen('img/eyesr.png', True))
        self._volviendo.append(cargar_imagen('img/eyesd.png', True))
        self._volviendo.append(cargar_imagen('img/eyesu.png', True))

        
class Pinky(Ghost):
    """ 
        Especialización del fantasma con el sprite y el comportamiento
        del fantasma rosa 'Blinky'
    """
    def __init__(self, x, y):
        """ """
        Ghost.__init__(self, x, y)
        
    def load_imgs(self):
        """ Cargamos imágenes para Pinky """
        self._normal.append([cargar_imagen('img/pinkyl1.png', True),
         cargar_imagen('img/pinkyl2.png', True)])
        self._normal.append([cargar_imagen('img/pinkyr1.png', True),
         cargar_imagen('img/pinkyr2.png', True)])
        self._normal.append([cargar_imagen('img/pinkyd1.png', True),
         cargar_imagen('img/pinkyd2.png', True)])
        self._normal.append([cargar_imagen('img/pinkyu1.png', True),
         cargar_imagen('img/pinkyu2.png', True)])
        
        # Imágenes huyendo / parpadeando
        self._huyendo.append(cargar_imagen('img/blue1.png', True))
        self._huyendo.append(cargar_imagen('img/gray1.png', True))
        self._huyendo.append(cargar_imagen('img/blue2.png', True))
        self._huyendo.append(cargar_imagen('img/gray2.png', True))
        
        # Imágenes volviendo
        self._volviendo.append(cargar_imagen('img/eyesl.png', True))
        self._volviendo.append(cargar_imagen('img/eyesr.png', True))
        self._volviendo.append(cargar_imagen('img/eyesd.png', True))
        self._volviendo.append(cargar_imagen('img/eyesu.png', True))

class Pacman(pygame.sprite.Sprite):
    """ Clase que maneja el jugador del juego """
    def __init__(self, x = 0, y = 0):
        """ Constructor """
        # Llamada al constructor de la clase de la que hereda
        pygame.sprite.Sprite.__init__(self)
        
        # Está parado?
        self.parado = True
        # Velocidad del pacman
        self.speed = 5
        # Orientación 0 - 4
        self.orient = 0
        # Estado de la animación del sprite
        self.estado = 1
        # Vector de imagenes
        self.imgs = list()
        
        # Estado inicial de cada animación, boca cerrada
        zero = cargar_imagen('img/pzero.png', True)
        
        # Cargamos las imágenes
        self.imgs.append([zero, cargar_imagen('img/pl1.png', True),
                            cargar_imagen('img/pl2.png', True)])
        self.imgs.append([zero, cargar_imagen('img/pr1.png', True),
                            cargar_imagen('img/pr2.png', True)])
        self.imgs.append([zero, cargar_imagen('img/pd1.png', True),
                            cargar_imagen('img/pd2.png', True)])
        self.imgs.append([zero, cargar_imagen('img/pu1.png', True),
                            cargar_imagen('img/pu2.png', True)])
                            
        # Imagen del Sprite
        self.image = self.imgs[self.orient][self.estado]
        
        # Rectángulo del Sprite
        self.rect = self.image.get_rect()
        
        # Alteramos el rectángulo según el constructor
        self.rect = pygame.rect.Rect((x, y), self.rect.bottomright)
        
        # Vector de movimiento
        self.next_move = (0, 0)
        
    def update(self):
        """ Código de actualización del sprite """
        
        if self.next_move != (0, 0):
            if self.estado == 2:
                self.estado = 0
            else:
                self.estado += 1
            
            self.image = self.imgs[self.orient][self.estado]
            
            self.rect = self.rect.move(self.next_move)
        
    def stop(self):
        """ Paramos el pacman """
        self.next_move = (0, 0)
        
    def start(self):
        """ Arrancamos el pacman """
        if self.orient == 0:
            self.next_move = (-self.speed, 0)
        elif self.orient == 1:
            self.next_move = (self.speed, 0)
        elif self.orient == 2:
            self.next_move = (0, self.speed)
        elif self.orient == 3:
            self.next_move = (0, -self.speed)
        
    def left(self):
        """ Movemos el pacman a la izquierda """
        if self.orient != 0:
            self.orient = 0
            self.estado = 0
            self.next_move = (-self.speed, 0)
        
    def right(self):
        """ Movemos al pacman a la derecha """
        if self.orient != 1:
            self.orient = 1
            self.estado = 0
            self.next_move = (self.speed, 0)
        
    def down(self):
        """ Movemos el pacman hacia abajo """
        if self.orient != 2:
            self.orient = 2
            self.estado = 0
            self.next_move = (0, self.speed)
    
    def up(self):
        """ Movemos el pacman hacia arriba """
        if self.orient != 3:
            self.orient = 3
            self.estado = 0
            self.next_move = (0, -self.speed)
            
    def matar(self):
        """ Nos matan :sadface: """
        print 'NOoooooooooooooooooooooooo'

class Juego():
    """ Esta clase inicia todas las cosas de pygame """
    def __init__(self):
        """ Constructor duh """
        # Definimos algunos colores
        self.rojo = (255, 0, 0)
        self.blanco = (255, 255, 255)
        self.negro = (0, 0, 0)
        self.verde = (0, 255, 0)
        self.azul = (0, 0, 255)
        
        # Inicializaciones privadas
        self.__font()
        self.__display()
        self.__logic()
        self.__mixer()
        
        # Creamos algunos fantasmas y el pacman
        self.pacman = Pacman(400, 300)
        self.blinky = Blinky(300, 300)
        self.pinky = Pinky(100, 100)
        # Creamos un grupo de sprites
        self.g_ghosts = pygame.sprite.Group((self.blinky, self.pinky))
        self.g_pacman = pygame.sprite.GroupSingle((self.pacman))
        # Creamos un reloj de juego
        self.reloj = pygame.time.Clock()
        
        
    def bucle(self):
        """ Bucle de juego """
        
        while not self.terminado:
            self.reloj.tick(30)
            self.eventos()
            self.logica()
            self.dibujado()
        
    def dibujado(self):
        """ Aquí metemos lo que queremos que se vaya dibujando """
        
        if self.dondeestoy == 'intro':
            self.__dib_intro()
        elif self.dondeestoy == 'menu':
            self.__dib_menu()
        elif self.dondeestoy == 'juego':
            #self.__dib_juego()
            # Dibujado 
            self.pantalla.blit(self.sur_negro, (0, 0))
            self.g_ghosts.draw(self.pantalla)
            self.g_pacman.draw(self.pantalla)
            pygame.display.update()
        elif self.dondeestoy == 'creditos':
            self.__dib_cred()
        
        pygame.display.flip()
    
    def logica(self):
        """ Aquí se controlan colisiones, estados del juego etc..."""
        
        if self.dondeestoy == 'juego':
            # Actualizamos
            self.g_ghosts.update()
            self.g_pacman.update()
            fant_col = pygame.sprite.spritecollide(   self.pacman, 
                                                        self.g_ghosts, 
                                                        False, 
                                                        pygame.sprite.collide_circle_ratio(0.7))
            
            for fantasma in fant_col:
                if fantasma.estado == 'huyendo':
                    fantasma.comer()
                
                if fantasma.estado == 'buscando' or fantasma.estado == 'persiguiendo':
                    self.pacman.matar()

    def eventos(self):
        """ Aquí controlamos los eventos que nos lleguen """
        
        for evento in pygame.event.get():
            
            # Para poder salir del programa
            if evento.type == pygame.QUIT:
                self.terminado = True
                pygame.quit()
                exit()
            
            # Para saltarnos la intro...
            if self.dondeestoy == 'intro':
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.dondeestoy = 'menu'
                        
            # Estamos en el menú
            elif self.dondeestoy == 'menu':
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        if self.curpos != 1:
                            self.curpos -= 1
                    elif evento.key == pygame.K_DOWN:
                        if self.curpos != 3:
                            self.curpos += 1
                    elif evento.key == pygame.K_RETURN:
                        self.__menu_press()
                            
            # Aquí irán los controles del juego
            elif self.dondeestoy == 'juego':
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        self.pacman.up()
                        self.pacman.start()
                    elif evento.key == pygame.K_DOWN:
                        self.pacman.down()
                        self.pacman.start()
                    elif evento.key == pygame.K_LEFT:
                        self.pacman.left()
                        self.pacman.start()
                    elif evento.key == pygame.K_RIGHT:
                        self.pacman.right()
                        self.pacman.start()
                    elif evento.key == pygame.K_RETURN:
                        self.pinky.debilitar()
                        self.blinky.comer()
                    elif evento.key == pygame.K_1:
                        self.pinky.parpadear()
                    elif evento.key == pygame.K_2:
                        self.pinky.habilitar()
                        self.blinky.habilitar()
            # Aquí algo para salir de los créditos
            elif self.dondeestoy == 'creditos':
                pass

    def __menu_press(self):
        """ Esto se llama cuando se pulsa sobre una opción del menú"""
        if self.curpos == 1:
            self.dondeestoy = 'juego'
        elif self.curpos == 2:
            self.dondeestoy = 'creditos'
        elif self.curpos == 3:
            exit()
    
    def __dib_menu(self):
        """ Dibujamos menú """
                
        # Dibujamos las superficies para el menú
        self.pantalla.blit(self.sur_negro, (0, 0))
        self.pantalla.blit(self.sur_logo, self.menupos[0])
        self.pantalla.blit(self.sur_jugar, self.menupos[1])
        self.pantalla.blit(self.sur_creds, self.menupos[2])
        self.pantalla.blit(self.sur_salir, self.menupos[3])
        self.pantalla.blit(self.sur_cursor, 
                            (   self.menupos[self.curpos][0] - 35,
                                self.menupos[self.curpos][1]))

        
    def __dib_intro(self):
        """ Dibujamos la intro """
        self.sur_intro = cargar_imagen('./img/intro.png')
        self.pantalla.blit(self.sur_intro, (0, 0))
        pygame.display.flip()
        time.sleep(2)
        self.dondeestoy = 'menu'
        
    def __dib_juego(self):
        """ Dibujamos cositas del juego """
        #pygame.display.update()
        
    def __dib_cred(self):
        """ Dibujamos los créditos """
    
    def __logic(self):
        """ Método privado para cargar cosas de lógica del juego """
        self.terminado = False

        
        # Definimos las posiciones de los menús
        self.menupos = ((self.dim[0]/2 - self.sur_logo.get_width()/2, 30),
                        (self.dim[0]/2 - self.sur_jugar.get_width()/2, 250),
                        (self.dim[0]/2 - self.sur_creds.get_width()/2, 300),
                        (self.dim[0]/2 - self.sur_salir.get_width()/2, 350))
        
        # Posición del cursor del menú
        self.curpos = 1
        # Estado de la aplicación
        self.dondeestoy = 'menu'
    
    def __mixer(self):
        """ Método privado para cargar componentes de sonido """
        # Iniciamos el sub-sistema de sonido de pygame
        pygame.mixer.init()
        # Creamos una serie de canales
        self.snd_channel0 = pygame.mixer.Channel(0)
        self.snd_channel1 = pygame.mixer.Channel(1)
    
    def __display(self):
        """ Método privado para cargar componentes de imagen """
        
        # Definimos dimensiones de la pantalla
        self.disp_ancho = 800
        self.disp_alto = 600
        
        self.dim = (self.disp_ancho, self.disp_alto)
        
        # Creamos la pantalla 
        self.pantalla = pygame.display.set_mode(self.dim)
        
        # Le damos un nombre al display
        pygame.display.set_caption('PyPac')
        
        # Creamos una superficie negra con las dimensiones del display
        self.sur_negro = pygame.Surface(self.dim)
        self.sur_negro.fill(self.negro)
        
        # Cargamos imágenes interesantes
        self.sur_cursor = cargar_imagen('img/cursor.png', True)
        self.sur_logo = cargar_imagen('img/menupac.png', True)
        
        
    def __font(self):
        """ Método privado para cargar componentes de fuente """
        pygame.font.init()
        
        # Definimos un par de fuentes
        self.fuente_20 = pygame.font.SysFont('Monospace', 20, bold = True)
        self.fuente_60 = pygame.font.SysFont('Monospace', 60, bold = True)
        
        
        self.sur_jugar = self.fuente_20.render('Jugar', True, self.rojo)
        self.sur_creds = self.fuente_20.render(u'Créditos', True, self.azul)
        self.sur_salir = self.fuente_20.render('Salir', True, self.verde)
        
def main():
    """ Función principal, boilerplate """
    mi_juego = Juego()
    mi_juego.bucle()

if __name__ == '__main__':
    main()
