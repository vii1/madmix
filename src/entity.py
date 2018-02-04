'''Entity manager'''

class Status:
    '''Status of an entity'''
    NEW = 0
    AWAKE = 1
    FROZEN = 2
    DEAD = 3

class Entity:
    '''An entity is an object that "thinks" every frame'''
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
    '''EntityManager manages the entity list, processes signals and runs entities in priority order'''
    shouldFilterEntities : bool = False
    entities : list = []
    shouldSortEntities : bool = False
    lastTime : float = 0

    @classmethod
    def AddEntity( cls, ent : Entity ):
        if ent is None: return
        cls.entities.append( ent )
        cls.shouldSortEntities = True

    @classmethod
    def RunFrame( cls, timestamp : float ):
        if cls.lastTime == 0:
            cls.lastTime = timestamp
        if cls.shouldSortEntities:
            # Ejecutamos las entidades de mayor a menor prioridad
            cls.entities.sort( reverse=True, key=lambda e: e.priority )
            cls.shouldSortEntities = False
        ents = cls.entities[:]
        deltaTime = timestamp - cls.lastTime
        for e in ents:
            if e.status == Status.AWAKE:
                e.Think( deltaTime )
        if cls.shouldFilterEntities:
            cls.entities = [ e for e in cls.entities if e.status != Status.DEAD ]
            cls.shouldFilterEntities = False
        for e in cls.entities:
            if e.status == Status.NEW:
                e.status = Status.AWAKE
        cls.lastTime = timestamp
