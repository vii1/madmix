'''Painter and paintable manager'''

from entity import Entity

class Paintable(Entity):
    '''Entity that has some representation on screen and thus can be painted'''
    z : int = 0
    def paint( context ):
        pass

class Painter:
    '''Manages paintable objects and paints them to screen'''
    shouldFilterPaintables : bool = False
    paintables : list = []
    shouldSortPaintables : bool = False

    @classmethod
    def add_paintable( cls, p : Paintable ):
        if p is None: return
        cls.paintables.append( p )
        cls.shouldSortPaintables = True

    @classmethod
    def remove_paintable( cls, p : Paintable ):
        if p is None: return
        try:
            cls.paintables.remove( p )
        except ValueError:
            pass

    @classmethod
    def paint( cls, context ):
        #if cls.shouldFilterPaintables:
        #    cls.paintables = [ p for p in cls.paintables if p.status != Status.DEAD ]
        #    cls.shouldFilterPaintables = False
        if cls.shouldSortPaintables:
            cls.paintables.sort( reverse=False, key=lambda p: p.z)
            cls.shouldSortPaintables = False
        for p in cls.paintables:
            p.paint( context )
