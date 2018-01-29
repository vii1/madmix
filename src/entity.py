'''Gestor de entidades'''

from enum import Enum

class Status( Enum ):
	'''Estado de una entidad'''
	NEW = 0
	AWAKE = 1
	FROZEN = 2
	DEAD = 3

class Entity:
	'''Una entidad es un objeto que "piensa" en cada frame'''
	priority : int = 0
	status : Status = Status.NEW

	def Think( self, deltaTime ):
		pass

	def Kill( self ):
		self.status = Status.DEAD
		EntityManager.shouldFilterEntities = True

	def Freeze( self ):
		if self.status != Status.DEAD:
			self.status = Status.FROZEN

	def Unfreeze( self ):
		if self.status == Status.FROZEN:
			self.status = Status.AWAKE


class EntityManager:
	'''EntityManager gestiona la lista de entidades, procesa las señales y las ejecuta en orden de prioridad'''
	shouldFilterEntities : bool = False
	entities : list = []
	shouldSortEntities : bool = False
	lastTime : float = 0

	def AddEntity( ent : Entity ):
		if ent is None: return
		EntityManager.entities.append( ent )
		EntityManager.shouldSortEntities = True

	def RunFrame( timestamp : float ):
		self = EntityManager
		if self.lastTime == 0:
			self.lastTime = timestamp
		if self.shouldSortEntities:
			# Ejecutamos las entidades de mayor a menor prioridad
			self.entities.sort( reverse=True, key=lambda e: e.priority )
			self.shouldSortEntities = False
		ents = self.entities[:]
		deltaTime = timestamp - self.lastTime
		for e in ents:
			if e.status == Status.AWAKE:
				e.Think( deltaTime )
		if self.shouldFilterEntities:
			self.entities = [ e for e in self.entities if e.status != Status.DEAD ]
			self.shouldFilterEntities = False
		for e in self.entities:
			if e.status == Status.NEW:
				e.status = Status.AWAKE
		self.lastTime = timestamp
