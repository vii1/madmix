"use strict";

var STATUS = {
	NEW: 0,
	AWAKE: 1,
	FROZEN: 2,
	DEAD: 3
};

var opciones = {
	smooth: false,
	musicvol: 0.5,
	fxvol: 1
}

function Entity() {
	this.priority = 0;
	this.status = STATUS.NEW;
	this.Think = function( deltaTime ) {};
	this.Kill = function() {
		this.status = STATUS.DEAD;
	};
	this.Freeze = function() {
		if( this.status != STATUS.DEAD ) {
			this.status = STATUS.FROZEN;
		}
	};
	this.Unfreeze = function() {
		if( this.status == STATUS.FROZEN ) {
			this.status = STATUS.AWAKE;
		}
	}
	return this;
}

var entityManager = {
	entities: [],
	shouldSortEntities: false,
	lastTime: 0,
	addEntity: function( ent ) {
		if( !ent ) return;
		this.entities.push( ent );
		this.shouldSortEntities = true;
	},
	runFrame: function( timestamp ) {
		if( this.lastTime == 0 ) {
			this.lastTime = timestamp;
		}
		if( this.shouldSortEntities ) {
			this.entities.sort( function(a,b) { return a.priority < b.priority } );
			this.shouldSortEntities = false;
		}
		var ents = this.entities.slice();
		var deltaTime = timestamp - this.lastTime;
		ents.map( function( ent ) {
			if( ent.status == STATUS.AWAKE ) {
				ent.Think( deltaTime );
			}
		});
		this.entities = this.entities.filter( function( ent ) {
			return ent.status != STATUS.DEAD;
		})
		this.entities.map( function( ent ) {
			if( ent.status == STATUS.NEW ) {
				ent.status = STATUS.AWAKE;
			}
		});
		this.lastTime = timestamp;
	}
};

var res = {
	intro: {
		splash: { file: 'graficos/splash.png' },
		mad: { file: 'graficos/mad.png' },
		mix: { file: 'graficos/mix.png' },
		game: { file: 'graficos/game.png' }
	}
}

var graphics = {
	canvas: null,
	context: null,
	width: 320,
	height: 200
};

var sound = {
	musica: {
		ogg: 'sonidos/madmix.ogg',
		mp3: 'sonidos/madmix.mp3'
	},
	fx: {
		ready: { file: 'sonidos/ready.wav' },
		chomp: { file: 'sonidos/chomp.wav' },
		death: { file: 'sonidos/death.wav' },
		ding: { file: 'sonidos/ding.wav' },
		gogogo: { file: 'sonidos/gogogo.wav' },
		ladybug: { file: 'sonidos/ladybug.wav' },
		stomp: { file: 'sonidos/stomp.wav' }
	},
	ctx: new (window.AudioContext || window.webkitAudioContext)()
	/*stop: function() {
		for(i=0; i<this.elements.length; i++) {
			this.elements[i].pause();
			this.elements[i].currentTime = 0;
		}
	}*/
};

var loaded = false;

function madmix_go() {
	console.log("* * * Mad Mix Game * * *");
	//cargando = document.getElementById('cargando');
	//presentacion = document.getElementById('presentacion');
	graphics.canvas = document.getElementById('canvas');
	console.log("Cargando recursos...");
	var mus = new Audio();
	mus.loop = true;
	mus.volume = opciones.musicvol;
	mus.addEventListener( 'canplay', function() {
		loaded = true;
		mus.play();
	}, true);
	if( mus.canPlayType( 'audio/ogg' ) ) {
		mus.src = sound.musica.ogg;
	} else {
		mus.src = sound.musica.mp3;
	}
	sound.musica.audio = mus;
	for( var i in sound.fx ) {
		var fx = sound.fx[i];
		fx.audio = new Audio();
		fx.audio.volume = opciones.fxvol;
		fx.audio.src = fx.file;
	}
	for(var i in res) {
		var group = res[i];
		for(var j in group) {
			var elem = group[j];
			elem.image = new Image();
			elem.loaded = false;
			elem.image.addEventListener( "load", ( function(e) {
				return function() {
					e.loaded = true;
				};
			})(elem));
			elem.image.src = elem.file;
		}
	}
	console.log("Iniciando mainLoop...")
	entityManager.addEntity( new Main() );
	window.requestAnimationFrame( mainLoop );
}

function disableSmooth( context ) {
	context.mozImageSmoothingEnabled = false;
	context.webkitImageSmoothingEnabled = false;
	context.msImageSmoothingEnabled = false;
	context.imageSmoothingEnabled = false;
}

function mainLoop( timestamp ) {
	graphics.context = graphics.canvas.getContext('2d');
	if( !opciones.smooth ) disableSmooth( graphics.context );
	graphics.context.setTransform( graphics.canvas.width / graphics.width, 0, 0, graphics.canvas.height / graphics.height, 0, 0 );
	entityManager.runFrame( timestamp );
	window.requestAnimationFrame( mainLoop );
}

function Main() {
	console.log("Creando entidad Main()...")
	this.super = Entity;
	this.super();
	var time = 0;
	var estado = 0;
	var flash = 0;
	this.Think = function( deltaTime ) {
		var g = graphics.context;
		time += deltaTime;
		g.clearRect( 0, 0, graphics.width, graphics.height );
		if( estado > 1 && estado < 5 ) {
			g.drawImage( res.intro.splash.image, 0, 0 );
		}
		switch( estado ) {
			case 0:
				if( loaded && res.intro.splash.loaded ) {
					estado = 1;
				} else {
					break;
				}
			case 1:
				if( time < 1000 ) {
					g.globalAlpha = time / 1000;
					g.drawImage( res.intro.splash.image, 0, 0 );
				} else {
					g.globalAlpha = 1.0;
					g.drawImage( res.intro.splash.image, 0, 0 );
				}
				if( time >= 3895 - 480 ) {
					entityManager.addEntity( new SpriteTitulo( res.intro.mad.image, 320, 100, 70, 5 ) );
					estado = 2;
				}
				break;
			case 2:
				if( time >= 4375 - 480 ) {
					g.fillStyle = 'white';
					g.fillRect( 0, 0, graphics.width, graphics.height );
					entityManager.addEntity( new SpriteTitulo( res.intro.mix.image, -68, 100, 170, 5 ) );
					estado = 3;
				}
				break;
			case 3:
				if( time >= 4855 - 480 ) {
					g.fillStyle = 'white';
					g.fillRect( 0, 0, graphics.width, graphics.height );
					entityManager.addEntity( new SpriteTitulo( res.intro.game.image, 105, 205, 105, 30 ) );					
					estado = 4;
				}
				break;
			case 4:
				if( time >= 4855 ) {
					g.fillStyle = 'white';
					g.fillRect( 0, 0, graphics.width, graphics.height );
					estado = 5;
					flash = 4855;
				}
				break;
			case 5:
				if( time >= 7000 ) {
					g.globalAlpha = 0.3;
				} else if( time >= 6500 ) {
					g.globalAlpha = 1 - ((time - 6500) / 500 * 0.7);
				} else if( time - flash >= 480 ) {
					g.fillStyle = 'white';
					g.fillRect( 0, 0, graphics.width, graphics.height );
					g.globalAlpha = 0;
					flash += 480;
				}
				g.drawImage( res.intro.splash.image, 0, 0 );
				g.globalAlpha = 1;
				break;
		}
	}
}

function smoothstep( edge0, edge1, x ) {
    // Scale, bias and saturate x to 0..1 range
    //x = Math.min( Math.max( (x - edge0)/(edge1 - edge0), 0.0 ), 1.0 ); 
	x = Math.min( Math.max( x, 0.0 ), 1.0 ); 
    // Evaluate polynomial
    //return x*x*(3 - 2*x);
    return edge0 + (edge1-edge0) * (x*x*x*(x*(x*6 - 15) + 10));
}

function SpriteTitulo( imagen, x0, y0, x1, y1 ) {
	this.super = Entity;
	this.super();
	var time = 0;
	var DURACION = 480;
	this.Think = function( deltaTime ) {
		time += deltaTime;
		var g = graphics.context;		
		if( time > DURACION ) {
			g.drawImage( imagen, x1, y1 );
			return;
		}
		var f = time / DURACION;
		//g.drawImage( imagen, x0 + (x1-x0) * f, y0 + (y1-y0) * f );
		g.drawImage( imagen, smoothstep( x0, x1, f ), smoothstep( y0, y1, f ) );
	}
}