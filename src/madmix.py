'''Mad Mix Game'''

from entity import EntityManager
from sound import Sound
from graphics import Graphics, Sprite, Text
from util import smoothstep
from entity import Entity
import resources
# __pragma__('skip')
from stubs import window, console
# __pragma__('noskip')

def madmix_go():
    console.log( '* * * Mad Mix Game * * *' )
    Sound.init()
    Graphics.init()
    Graphics.load('intro', 'fonts')
    console.log( 'Iniciando mainLoop...' )
    EntityManager.add_entity( Main() )
    window.requestAnimationFrame( main_loop )

def main_loop( timestamp : float ):
    try:
        Graphics.setup_context()
        EntityManager.run_frame( timestamp )
        Graphics.render()
        window.requestAnimationFrame( main_loop )
    except:
        Sound.stop()
        raise

class SpriteTitulo(Sprite):
    time = 0
    DURACION = 480

    def __init__(self, imagen, x0, y0, x1, y1):
        super().__init__(imagen, x0, y0)
        self.x0, self.y0 = x0, y0
        self.x1, self.y1 = x1, y1

    def think(self, deltaTime):
        self.time += deltaTime
        if self.time < self.DURACION:
            f = self.time / self.DURACION
            self.x = smoothstep( self.x0, self.x1, f )
            self.y = smoothstep( self.y0, self.y1, f )
        else:
            self.x = self.x1
            self.y = self.y1

class Menu(Entity):
    lista = [ 'JUGAR', 'RECORDS', 'OPCIONES', 'AYUDA', 'CREDITOS' ]
    textos = []

    def __init__(self):
        for i in range(len(self.lista)):
            x = 155 - len(self.lista[i]) * 8 / 2
            self.textos[i] = Text( x, Graphics.height / 2 + i * 16, self.lista[i] )


class Main(Sprite):
    z = 100
    opacity = 0
    _time = 0
    _flash = 0
    _flashing = False
    _proc = None

    def __init__(self):
        super().__init__(None)
        self._proc = self.proc()

    def paint(self, ctx):
        if self._flashing:
            ctx.save()
            ctx.fillStyle = 'white'
            ctx.fillRect( 0, 0, Graphics.width, Graphics.height )
            ctx.restore()
            self._flashing = False
        else:
            super().paint(ctx)

    def think(self, deltaTime):
        self._time += deltaTime
        next(self._proc)

    def proc(self):
        console.log('[Main] Iniciando...')
        while not resources.all_loaded():
            yield
        console.log('[Main] Todo cargado!')
        resources.get_dom('music').play()
        self.image = resources.get_dom('intro','splash')
        self._time = 0
        while self._time < 1000:
            self.opacity = self._time / 1000
            yield
        self.opacity = 1
        while self._time < 3895 - 480:
            yield
        EntityManager.add_entity( SpriteTitulo( resources.get_dom('intro','mad'), 320, 100, 70, 5 ) );
        while self._time < 4375 - 480:
            yield
        self._flashing = True
        EntityManager.add_entity( SpriteTitulo( resources.get_dom('intro','mix'), -68, 100, 170, 5 ) );
        while self._time < 4855 - 480:
            yield
        self._flashing = True
        EntityManager.add_entity( SpriteTitulo( resources.get_dom('intro','game'), 105, 205, 105, 30 ) );
        while self._time < 4855:
            yield
        self._flashing = True
        flash = 4855
        while self._time < 6500:
            while self._time - flash < 480:
                yield
            self._flashing = True
            flash += 480
        while self._time < 7000:
            self.opacity = 1 - ((self._time - 6500) / 500 * 0.7)
            yield
        self.opacity = 0.3
        EntityManager.add_entity( Menu() )
        while True: yield
