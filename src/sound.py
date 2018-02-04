'''Sound and music management'''

from resources import resources, MultiFileRes, FileRes
# __pragma__('skip')
from stubs import window, console, Audio, __new__
# __pragma__('noskip')

# load_music_resource
def load_music_resource( music: MultiFileRes ):
    music.dom = __new__( Audio() )
    music.dom.loop = True
    music.dom.volume = Sound._music_volume
    music.dom.addEventListener( 'canplay', music.on_loaded, True )
    if music.dom.canPlayType( 'audio/ogg' ):
        music.dom.src = music.files['ogg']
    else:
        music.dom.src = music.files['mp3']
    return music

# load_sfx_resource
def load_sfx_resource( sfx: FileRes ):
    sfx.dom = __new__( Audio() )
    sfx.dom.volume = Sound._sfx_volume
    sfx.dom.addEventListener( 'canplay', sfx.on_loaded, True )
    sfx.dom.src = sfx.file
    return sfx

class Sound:
    context = None
    disabled = False

    @classmethod
    def init( cls ):
        console.log( '[sound] init' )
        cls._music_volume = 0.5
        cls._sfx_volume = 0.5
        AudioContext = window.AudioContext or window.webkitAudioContext
        if not AudioContext:
            console.log( '[sound] ERROR: No AudioContext API detected. Disabling sound.' )
            cls.disabled = True
            return
        cls.context = __new__( window.AudioContext() )
        load_music_resource( resources['music'] )
        for sfx in resources['sfx'].values():
            load_sfx_resource( sfx )

    @classmethod
    def set_volume( cls, music = None, sfx = None ):
        if cls.disabled: return
        if music is float:
            cls._music_volume = min( max( music, 0.0 ), 1.0 )
            resources['music'].dom.volume = cls._music_volume
        if sfx is float:
            cls._sfx_volume = min( max( sfx, 0.0 ), 1.0 )
            for sfx in resources['sfx'].values():
                sfx.dom.volume = cls._sfx_volume

    @classmethod
    def stop( cls ):
        if cls.disabled: return
        resources['music'].dom.pause()
        for sfx in resources['sfx'].values():
            sfx.dom.pause()
