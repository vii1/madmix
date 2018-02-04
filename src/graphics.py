'''Graphics and rendering management'''

from resources import resources
from painter import Painter
# __pragma__('skip')
from stubs import document, Image, console, __new__
# __pragma__('noskip')

def disableSmooth( context ):
    context.mozImageSmoothingEnabled = False
    context.webkitImageSmoothingEnabled = False
    context.msImageSmoothingEnabled = False
    context.imageSmoothingEnabled = False

class Graphics:
    canvas = None
    context = None
    width = 320
    height = 200
    clear = True
    smooth = False

    def init():
        console.log('[graphics] init')
        Graphics.canvas = document.getElementById( 'canvas' )

    def load( *args ):
        for groupname in args:
            group = resources[groupname]
            for i,img in group:
                img.dom = __new__( Image() )
                img.dom.addEventListener( 'load', img.on_loaded )
                img.dom.src = img.file

    @classmethod
    def setup_context(cls):
        cls.context = cls.canvas.getContext( '2d' )
        if not cls.smooth:
            disableSmooth( cls.context )
        # TODO: Respetar relación de aspecto( necesario para fullscreen)
        cls.context.setTransform(cls.canvas.width / cls.width, 0, 0, cls.canvas.height / cls.height, 0, 0)
        if cls.clear:
            cls.context.clearRect( 0, 0, cls.width, cls.height )

    @classmethod
    def render(cls):
        Painter.Paint( cls.context )
