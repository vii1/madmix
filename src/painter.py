'''Gestor de paintables y painter'''

from entity import Entity

class Paintable(Entity):
	z : int = 0
	def Paint( context ):
		pass

class Painter:
	shouldFilterPaintables : bool = False
	paintables : list = []
	shouldSortPaintables : bool = False

	def AddPaintable( p : Paintable ):
		if p is None: return
		Painter.paintables.append( p )
		Painter.shouldSortPaintables = True

	def RemovePaintable( p : Paintable ):
		if p is None: return
		try:
			Painter.paintables.remove( p )
		except ValueError:
			pass

	def Paint( context ):
		self = Painter
		#if self.shouldFilterPaintables:
		#	self.paintables = [ p for p in self.paintables if p.status != Status.DEAD ]
		#	self.shouldFilterPaintables = False
		if self.shouldSortPaintables:
			self.paintables.sort( reverse=False, key=lambda p: p.z)
			self.shouldSortPaintables = False
		for p in self.paintables:
			p.Paint( context )
