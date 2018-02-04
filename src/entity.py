'''Entity manager'''

class Status:
    '''Status of an entity'''
    # No usamos Enum porque parece que Transcrypt no lo soporta
    NEW = 0
    AWAKE = 1
    FROZEN = 2
    DEAD = 3

class Entity:
    '''An entity is an object that "thinks" every frame'''
    priority = 0
    status = Status.NEW

    def think( self, deltaTime ):
        pass

    def kill( self ):
        self.status = Status.DEAD
        EntityManager.shouldFilterEntities = True

    def freeze( self ):
        if self.status != Status.DEAD:
            self.status = Status.FROZEN

    def unfreeze( self ):
        if self.status == Status.FROZEN:
            self.status = Status.AWAKE


class EntityManager:
    '''EntityManager manages the entity list, processes signals and runs entities in priority order'''
    shouldFilterEntities = False
    entities = []
    shouldSortEntities = False
    lastTime = 0

    @classmethod
    def add_entity( cls, ent : Entity ):
        if ent is None or ent in cls.entities: return
        cls.entities.append( ent )
        cls.shouldSortEntities = True

    @classmethod
    def run_frame( cls, timestamp : float ):
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
                e.think( deltaTime )
        if cls.shouldFilterEntities:
            cls.entities = [ e for e in cls.entities if e.status != Status.DEAD ]
            cls.shouldFilterEntities = False
        for e in cls.entities:
            if e.status == Status.NEW:
                e.status = Status.AWAKE
        cls.lastTime = timestamp
