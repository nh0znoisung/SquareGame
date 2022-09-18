from locals import *

class __Config(object):
    
    # This is essentially the API
    DEFAULT = {'highscores': [], 
               'fullscreen': False,
               'sound': True}
    
    MAX_NAME_LEN = 25
    
    def __init__(self):
        
        self.__dict__['_data'] = self.DEFAULT
    
    def __getattr__(self, name):
        try:
            return self.__dict__['_data'][name]
        except KeyError as e:
            raise AttributeError(e)
        
    def __setattr__(self, name, value):
        
        if name in self.__dict__['_data']:
            self.__dict__['_data'][name] = value
        else:
            raise AttributeError(name)
        
    def __delattr__(self, name):
        raise AttributeError(name)
        
    def is_highscore(self, score):
        '''Will this score make it in to the high score list?'''
        
        if len(self.highscores) < HIGHSCORES_AMOUNT:
            return True
        
        return score > self.highscores[-1][1]
    
    def register_highscore(self, name, score):
        '''Register a highscore'''
        
        name = name[:self.MAX_NAME_LEN]
        
        self.highscores.append((name, score))
        # Sort the list
        self.highscores.sort(key=lambda a: -a[1])
        # Truncate to HIGHSCORES_AMOUNT items
        del self.highscores[HIGHSCORES_AMOUNT:]

        
conf = __Config()
