from src.model.charactors import Charactor


class Aggressive(Charactor):
    """ Any person or entity that can fight.
    """
    
    def __init__(self, nation):
        super().__init__(nation)