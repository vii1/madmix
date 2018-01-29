'''Mad Mix Game'''

from entity import EntityManager
from painter import Painter
# from org.transcrypt.stubs.browser import *

# __pragma__('skip')
window = console = document = Audio = 0
# __pragma__('noskip')

class Opciones:
	smooth = False
	musicvol = 0.5
	fxvol = 0.5

class FileRes:
	file : str
	obj = None
	loaded = False
	def __init__( self, file: str ):
		self.file = file

res = {
	'intro': {
		'splash': FileRes( 'graficos/splash.png' ),
		'mad': FileRes( 'graficos/mad.png' ),
		'mix': FileRes( 'graficos/mix.png' ),
		'game': FileRes( 'graficos/game.png' ),
	},
	'fonts': {
		'font': FileRes( 'graficos/caracteres.png' ),
	},
}

class Graphics:
	canvas = None
	context = None
	width = 320
	height = 200
	clear = True

class Sound:
	musica = {
		'ogg': 'sonidos/madmix.ogg',
		'mp3': 'sonidos/madmix.mp3',
	}
	musica_audio = None
	fx = {
		'ready': FileRes( 'sonidos/ready.wav' ),
		'chomp': FileRes( 'sonidos/chomp.wav' ),
		'death': FileRes( 'sonidos/death.wav' ),
		'ding': FileRes( 'sonidos/ding.wav' ),
		'gogogo': FileRes( 'sonidos/gogogo.wav' ),
		'ladybug': FileRes( 'sonidos/ladybug.wav' ),
		'stomp': FileRes( 'sonidos/stomp.wav' ),
	}
	ctx = None

if 'AudioContext' in dir( window ):
	Sound.ctx = __new__( window.AudioContext() )
else:
	Sound.ctx = __new__( window.webkitAudioContext() )

loaded = False

def madmix_go():
	console.log( '* * * Mad Mix Game * * *' )
	Graphics.canvas = document.getElementById( 'canvas' )
	console.log( 'Cargando recursos...' )
	mus = __new__( Audio() )
	mus.loop = True
	mus.volume = Opciones.musicvol
	def load_ended(): loaded = True
	mus.addEventListener( 'canplay', load_ended, True )
	if mus.canPlayType( 'audio/ogg' ):
		mus.src = Sound.musica['ogg']
	else:
		mus.src = Sound.musica['mp3']
	Sound.musica_audio = mus
	for i,fx in Sound.fx:
		audio = __new__( Audio() )
		audio.volume = Opciones.fxvol
		audio.src = fx.file
		fx.obj = audio
	for i,group in res:
		for j,elem in group:
			elem.obj = __new__( Image() )
			#elem.loaded = False
			def elemLoaded():
				elem.loaded = True
			elem.obj.addEventListener( 'load', elemLoaded )
			elem.obj.src = elem.file
	console.log( 'Iniciando mainLoop...' )
	EntityManager.AddEntity( Main() )
	window.requestAnimationFrame( mainLoop )

def disableSmooth( context ):
	context.mozImageSmoothingEnabled = False
	context.webkitImageSmoothingEnabled = False
	context.msImageSmoothingEnabled = False
	context.imageSmoothingEnabled = False

def mainLoop( timestamp : float ):
	Graphics.context = Graphics.canvas.getContext( '2d' )
	if not Opciones.smooth:
		disableSmooth( Graphics.context )
	# TODO: Respetar relación de aspecto( necesario para fullscreen)
	Graphics.context.setTransform(Graphics.canvas.width / Graphics.width, 0, 0, Graphics.canvas.height / Graphics.height, 0, 0)
	if Graphics.clear:
		Graphics.context.clearRect( 0, 0, Graphics.width, Graphics.height )
	EntityManager.RunFrame( timestamp )
	Painter.Paint( Graphics.context )
	window.requestAnimationFrame( mainLoop )
