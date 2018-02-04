'''Mad Mix Game'''

from entity import EntityManager
from sound import Sound
from graphics import Graphics
# __pragma__('skip')
from stubs import window, console
# __pragma__('noskip')

def madmix_go():
    console.log( '* * * Mad Mix Game * * *' )
    Sound.init()
    Graphics.init()
    Graphics.load('intro', 'fonts')
    console.log( 'Iniciando mainLoop...' )
    EntityManager.AddEntity( Main() )
    window.requestAnimationFrame( mainLoop )

def mainLoop( timestamp : float ):
    Graphics.setup_context()
    EntityManager.RunFrame( timestamp )
    Graphics.render()
    window.requestAnimationFrame( mainLoop )
