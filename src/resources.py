'''Resources management'''

# __pragma__('skip')
from stubs import console
# __pragma__('noskip')

_managed_resources = []

def all_loaded():
    return all(x.loaded for x in _managed_resources)

def get_dom(*args):
    r = resources
    for x in args:
        r = r[x]
    return r.dom

class Res:
    '''Resource (abstract)'''
    dom = None
    loaded = False

    def __init__(self):
        _managed_resources.append(self)

    def on_loaded( self ):
        self.loaded = True


class FileRes( Res ):
    '''File resource'''

    def __init__( self, file: str ):
        super().__init__()
        self.file = file

    def on_loaded( self ):
        super().on_loaded()
        console.log( '[resource] Loaded: ' + self.file )


class MultiFileRes( Res ):
    '''File with multiple files associated so the browser will choose one (whichever is compatible)'''

    def __init__( self, files: dict ):
        super().__init__()
        self.files = files

    def on_loaded( self ):
        super().on_loaded()
        console.log( '[resource] Loaded: ' + str( self.files ) )

resources = {
    'intro': {
        'splash': FileRes( 'graficos/splash.png' ),
        'mad': FileRes( 'graficos/mad.png' ),
        'mix': FileRes( 'graficos/mix.png' ),
        'game': FileRes( 'graficos/game.png' ),
    },
    'fonts': {
        'font': FileRes( 'graficos/caracteres.png' ),
    },
    'music': MultiFileRes( {
        'ogg': 'sonidos/madmix.ogg',
        'mp3': 'sonidos/madmix.mp3',
    } ),
    'sfx': {
        'ready': FileRes( 'sonidos/ready.wav' ),
        'chomp': FileRes( 'sonidos/chomp.wav' ),
        'death': FileRes( 'sonidos/death.wav' ),
        'ding': FileRes( 'sonidos/ding.wav' ),
        'gogogo': FileRes( 'sonidos/gogogo.wav' ),
        'ladybug': FileRes( 'sonidos/ladybug.wav' ),
        'stomp': FileRes( 'sonidos/stomp.wav' ),
    }
}
