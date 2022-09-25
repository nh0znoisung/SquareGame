from atexit import register
from locals import *

class __Config(object):
    
    # This is essentially the API
    DEFAULT = {'highscores': [], 
               'fullscreen': False,
               'sound': True,
               'turbo': False}
    
    MAX_NAME_LEN = 10
    
    def __init__(self):
        
        self.__dict__['_data'] = self.DEFAULT
        file = open('highscore.txt', 'r')
        Lines = file.readlines()
        for i in Lines:
            a = i[:i.index(":")]
            b = i[i.index(" ")+1:]
            self.highscores.append((a, int(b)))
        self.highscores.sort(key=lambda x:-x[1])
        self.highscores = self.highscores[:HIGHSCORES_AMOUNT]

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
        
        name = "Anonymous" if name=="" else name[:self.MAX_NAME_LEN]
        
        self.highscores.append((name, score))
        file = open('highscore.txt', 'a')
        file.writelines(name + ": " + str(score) + "\n")
        file.close()
        # Sort the list
        self.highscores.sort(key=lambda a: -a[1])
        # Truncate to HIGHSCORES_AMOUNT items
        del self.highscores[HIGHSCORES_AMOUNT:]

        
conf = __Config()
