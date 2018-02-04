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

    def init():
        console.log( '[sound] init' )
        Sound._music_volume = 0.5
        Sound._sfx_volume = 0.5
        if 'AudioContext' in dir( window ):
            Sound.context = __new__( window.AudioContext() )
        elif 'webkitAudioContext' in dir( window ):
            Sound.context = __new__( window.webkitAudioContext() )
        else:
            console.log( '[sound] ERROR: No AudioContext API detected. Disabling sound.' )
            Sound.disabled = True
            return
        load_music_resource( resources['music'] )
        for i,sfx in resources['sfx']:
            load_sfx_resource( sfx )

    def set_volume( music = None, sfx = None ):
        if music is float:
            Sound._music_volume = min