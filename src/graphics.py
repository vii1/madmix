'''Graphics and rendering management'''

from resources import resources
from painter import Painter, Paintable
from entity import Entity
# __pragma__('skip')
from stubs import document, Image, console, __new__
# __pragma__('noskip')

class Graphics:
    canvas = None
    context = None
    width = 320
    height = 200
    clear = True
    smooth = False

    def init():
        console.log( '[graphics] init' )
        Graphics.canvas = document.getElementById( 'canvas' )

    def load( *args ):
        for groupname in args:
            group = resources[groupname]
            for img in group.values():
                img.dom = __new__( Image() )
                img.dom.addEventListener( 'load', img.on_loaded )
                img.dom.src = img.file

    @classmethod
    def setup_context( cls ):
        cls.context = cls.canvas.getContext( '2d' )
        if not cls.smooth:
            cls.disable_smooth()
        # TODO: Respetar relación de aspecto( necesario para fullscreen)
        cls.context.setTransform( cls.canvas.width / cls.width, 0, 0, cls.canvas.height / cls.height, 0, 0 )
        if cls.clear:
            cls.context.clearRect( 0, 0, cls.width, cls.height )

    @classmethod
    def render( cls ):
        Painter.paint( cls.context )

    @classmethod
    def disable_smooth( cls ):
        cls.context.mozImageSmoothingEnabled = False
        cls.context.webkitImageSmoothingEnabled = False
        cls.context.msImageSmoothingEnabled = False
        cls.context.imageSmoothingEnabled = False

class Sprite( Entity, Paintable ):
    opacity = 1.0
    x = 0.0
    y = 0.0
    image = None

    def __init__( self, image, x = 0.0, y = 0.0 ):
        self.image = image
        self.x = x
        self.y = y
        Painter.add_paintable( self )

    def paint( self, ctx ):
        if self.image is None: return
        ctx.save()
        ctx.globalAlpha = self.opacity
        ctx.drawImage( self.image, self.x, self.y )
        ctx.restore()

    def kill( self ):
        super().kill()
        self.hide()

    def sleep(self):
        self.freeze()
        self.hide()

    def awake(self):
        self.unfreeze()
        self.show()

class Text( Paintable ):
    x = 0.0
    y = 0.0
    text = ''
    font = None

    def __init__( self, x = 0.0, y = 0.0, text = '' ):
        self.x = x
        self.y = y
        self.text = text
        self.z = -100
        self.font = resources['fonts']['font']
        Painter.add_paintable( self )

    def paint( self, ctx ):
        x = self.x
        for ch in self.text:
            #c = ch[0].encode()[0]
            c = ch.charCodeAt(0)
            # '!'..'Z'
            if(c >= 33 and c <= 90):
                c -= 32
                ctx.drawImage( self.font.dom,
                              (c % 8) * 10 + 2, (c >> 3) * 10 + 2,  # coordenadas origen
                              8, 8,                                 # tamaño origen
                              x, self.y,                            # coordenadas destino
                              8, 8 )                                # tamaño destino
            x += 8

