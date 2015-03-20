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
		entityManager.shouldFilterEntities = true;
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

var entityManager = new (function() {
	this.shouldFilterEntities = false;
	var entities = [];
	var shouldSortEntities = false;
	var lastTime = 0;
	this.AddEntity = function( ent ) {
		if( !ent ) return;
		entities.push( ent );
		shouldSortEntities = true;
	};
	this.RunFrame = function( timestamp ) {
		if( lastTime == 0 ) {
			lastTime = timestamp;
		}
		if( shouldSortEntities ) {
			entities.sort( function(a,b) { return a.priority < b.priority } );
			shouldSortEntities = false;
		}
		var ents = entities.slice();
		var deltaTime = timestamp - lastTime;
		ents.map( function( ent ) {
			if( ent.status == STATUS.AWAKE ) {
				ent.Think( deltaTime );
			}
		});
		if( this.shouldFilterEntities ) {
			entities = entities.filter( function( ent ) {
				return ent.status != STATUS.DEAD;
			});
			shouldFilterEntities = false;
		}
		entities.map( function( ent ) {
			if( ent.status == STATUS.NEW ) {
				ent.status = STATUS.AWAKE;
			}
		});
		lastTime = timestamp;
	};
})();

var painter = new (function() {
	this.shouldFilterPaintables = false;
	var paintables = [];
	var shouldSortPaintables = false;
	this.AddPaintable = function( p ) {
		if( !p ) return;
		paintables.push( p );
		shouldSortPaintables = true;
	};
	this.Paint = function( context ) {
		if( this.shouldFilterPaintables ) {
			paintables = paintables.filter( function( p ) {
				return p.status == null || p.status != STATUS.DEAD;
			});
		}
		if( shouldSortPaintables ) {
			paintables.sort( function(a,b) { return a.z < b.z } );
			shouldSortPaintables = false;
		}
		for( var i = 0; i < paintables.length; ++i ) {
			paintables[i].Paint( context );
		}
	};
})();

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
	height: 200,
	clear: true
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
	entityManager.AddEntity( new Main() );
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
	if( graphics.clear ) {
		graphics.context.clearRect( 0, 0, graphics.width, graphics.height );
	}
	entityManager.RunFrame( timestamp );
	painter.Paint( graphics.context );
	window.requestAnimationFrame( mainLoop );
}

function Sprite( image, x, y ) {
	this.super = Entity;
	this.super();
	this.x = x || 0;
	this.y = y || 0;
	this.image = image;
	this.opacity = 1;
	this.painter = painter;
	this.z = 0;
	painter.AddPaintable( this );	
	this.Paint = function( ctx ) {
		if( !this.image ) return;
		ctx.save();
		ctx.globalAlpha = this.opacity;
		ctx.drawImage( this.image, this.x, this.y );
		ctx.restore();
	}
	var super_Kill = this.Kill;
	this.Kill = function() {
		super_Kill();
		painter.shouldFilterPaintables = true;
	}
}

function Main() {
	console.log("Creando entidad Main()...")
	this.super = Sprite;
	this.super();
	this.z = 100;
	this.opacity = 0;
	var time = 0;
	var estado = 0;
	var flash = 0;
	var flashing = false;
	this.Paint = function( ctx ) {
		ctx.save();
		if( flashing ) {
			ctx.fillStyle = 'white';
			ctx.fillRect( 0, 0, graphics.width, graphics.height );
			flashing = false;
		} else if( this.image ) {
			ctx.globalAlpha = this.opacity;
			ctx.drawImage( this.image, 0, 0 );
		}
		ctx.restore();
	};
	this.Think = function( deltaTime ) {
		if( estado > 0 ) {
			time += deltaTime;
		}
		switch( estado ) {
			case 0:
				if( loaded && res.intro.splash.loaded ) {
					sound.musica.audio.play();
					this.image = res.intro.splash.image;
					estado = 1;
				}
				break;
			case 1:
				if( time < 1000 ) {
					this.opacity = time / 1000;
				} else {
					this.opacity = 1;
				}
				if( time >= 3895 - 480 ) {
					entityManager.AddEntity( new SpriteTitulo( res.intro.mad.image, 320, 100, 70, 5 ) );
					estado = 2;
				}
				break;
			case 2:
				if( time >= 4375 - 480 ) {
					flashing = true;
					entityManager.AddEntity( new SpriteTitulo( res.intro.mix.image, -68, 100, 170, 5 ) );
					estado = 3;
				}
				break;
			case 3:
				if( time >= 4855 - 480 ) {
					flashing = true;
					entityManager.AddEntity( new SpriteTitulo( res.intro.game.image, 105, 205, 105, 30 ) );					
					estado = 4;
				}
				break;
			case 4:
				if( time >= 4855 ) {
					flashing = true;
					estado = 5;
					flash = 4855;
				}
				break;
			case 5:
				if( time >= 7000 ) {
					this.opacity = 0.3;
				} else if( time >= 6500 ) {
					this.opacity = 1 - ((time - 6500) / 500 * 0.7);
				} else if( time - flash >= 480 ) {
					flashing = true;
					//this.opacity = 0;
					flash += 480;
				}
				break;
		}
	}
}

function smoothstep( edge0, edge1, x ) {
	x = Math.min( Math.max( x, 0.0 ), 1.0 ); 
    return edge0 + (edge1-edge0) * (x*x*x*(x*(x*6 - 15) + 10));
}

function SpriteTitulo( imagen, x0, y0, x1, y1 ) {
	this.super = Sprite;
	this.super( imagen, x0, y0 );
	var time = 0;
	var DURACION = 480;
	this.Think = function( deltaTime ) {
		time += deltaTime;
		if( time <= DURACION ) {
			var f = time / DURACION;
			this.x = smoothstep( x0, x1, f );
			this.y = smoothstep( y0, y1, f );
		} else {
			this.x = x1;
			this.y = y1;
		}
	}
}

function Menu() {
	this.super = Entity;
	this.super();

}