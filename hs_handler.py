from os.path import join, isfile

from config import CONF_DIR

HS_FILE = join(CONF_DIR, 'hiscores')

class HighScoreHandler:
    
    def __init__(self):
        if isfile(HS_FILE):
            self.parse(HS_FILE)
        else:
            self.scores = []
    
    def parse(self, hs_file):
        with open(hs_file, 'r') as f:
            scores = []
            for line in f:
                name, score = line.split(',')
                scores.append((name, int(score)))
            self.scores = scores
    
    def add_score(self, name, score, sort=True):
        # TODO: Write an algorithm to find whereabouts in list new score will
        # be places, and return that number.
        # If we limit the number of entries and the new score doesn't make the
        # list, return None.
        self.scores.append([name, score])
        if sort:
            self.scores.sort(key=lambda x: x[1], reverse=True)
    
    def write(self, hs_file=HS_FILE):
        with open(hs_file, 'w') as f:
            f.writelines('{},{}\n'.format(*i) for i in self.scores)
