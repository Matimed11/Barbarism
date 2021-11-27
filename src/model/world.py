from lib.abstract_data_types import Matrix
from lib.chunk import Chunk
from lib.position import Position
from random import choice
from src.model import Cell
from lib.abstract_data_types.graph import Graph


class World:
    """ Class that represents the physical space where 
        are all the characters and buildings of the game
    """

    def __init__(self, order = 100):
        self.order = order
        self.positions: Matrix = self._generate_positions(order)
        self.chunks: Matrix = self._generate_chunks(25, order, self.positions)
        self.entities = Graph() # {Position -- Object}
        self.cells = dict() # {Position: Cell}
        self._generate_cells(self.positions)


    def get_position(self, position_index) -> (Chunk,Position):
        """ Returns the chunk and position 
            object that match with the given position index.
        """
        
        position = self.positions.get_element(position_index)
        length = Chunk.get_length()

        chunk_index = (position_index[0] // (length[0]), position_index[1] // (length[1]))
        chunk = self.chunks.get_element(chunk_index)

        if not chunk.has(position): raise KeyError()

        return (chunk, position)


    def get_biomes(self):
        """ Return a dict of biomes with Positions
            as keys based on self.cells.
        """
        
        raise NotImplementedError


    def get_adjacent_chunks(self, chunk) -> list:
        """ Returns the list of Chunk objects 
            adjacent to the one given by parameter.
        """

        return self.chunks.get_adjacencies(self.chunks.index(chunk))


    def get_adjacent_positions(self, position) -> list:
        """ Returns the list of Position objects 
            adjacent to the one given by parameter.
        """

        return self.positions.get_adjacencies(self.positions.index(position))


    def create_route(self, origin, destination):
        """ Given two Position returns the fastest way
            to get from the origin to the destination point.
        """

        raise NotImplementedError


    def get_limit(self) -> Position:
        """ Returns the last Position in the world.
        """

        index = self.positions.get_last_index()
        return self.positions.get_element(index)


    def _generate_positions(self, order):
        """ Generates a Matrix of Position type objects 
            based on the given size (order).
        """

        return Matrix(Position.create_collection((0,0), (order -1 ,order -1)))


    def add_entity(self, position, entity):
        self.entities.add_edge((position, entity))


    def get_entities(self, positions: list):
        entities = dict()
        entities |= {
            position: list(self.entities.get_adjacencies(position))[0]
            for position in positions
            if self.entities.has_node(position)
            }
            
        return entities


    def get_entity_position(self, entity):
        return list(self.entities.get_adjacencies(entity))[0]


    def get_charactor_nation(self, position):
        for nation in self.nations:
            if nation.has_charactor(position):
                return nation


    def _generate_chunks(self, min_size:int, order, positions):
        """ Returns a Matrix of Chunk objects based on a given size 
            (the minimum number of cells that can fit in a Chunk).
        """

        size = min_size
        while True:
            if not (order%size):
                break
            size +=1

        splited_positions = positions.split(order/size)

        return Matrix([[Chunk(positions, (y,x)) for x, positions in enumerate(row)]
            for y, row in enumerate(splited_positions.iter_rows())])


    def _generate_cells(self, positions):
        """ Receives a Matrix of Position type objects and
            generate a dict of Cell type objects with a position as key.
        """
        
            
        self.cells |= {position: Cell(friction = 1) for position in positions}


    def get_random_point(self) -> (Chunk, Position):
        """ Returns a Chunk and a Position on that 
            chunk where to place a charactor.
        """

        # In the future a more complex spawn method will be implemented.
        chunk = self.chunks.random()
        return (chunk, chunk.get_random_position())