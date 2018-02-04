'''Painter and paintable manager'''

class Paintable:
    '''Object that has some representation on screen and thus can be painted'''
    z = 0

    def paint(self, context ):
        pass

    def show(self):
        Painter.add_paintable( self )

    def hide(self):
        Painter.remove_paintable( self )

class Painter:
    '''Manages paintable objects and paints them to screen'''
    #shouldFilterPaintables : bool = False
    paintables = []
    shouldSortPaintables = False

    @classmethod
    def add_paintable( cls, p : Paintable ):
        if p is None or p in cls.paintables: return
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
            cls.paintables.sort( reverse=True, key=lambda p: p.z)
            cls.shouldSortPaintables = False
        for p in cls.paintables:
            p.paint( context )
