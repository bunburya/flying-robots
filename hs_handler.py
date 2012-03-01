from os.path import join, isfile

from config import CONF_DIR
from debug import log

HS_FILE = join(CONF_DIR, 'hiscores')
SCORE_LIMIT = 20

if not isfile(HS_FILE):
    with open(HS_FILE, 'a') as f:
        pass

def _from_file(fileobj):
    scores = []
    for line in fileobj:
        name, score = line.split(',')
        scores.append((name, int(score)))
    return scores
        
def _insert_score(name, score, scores):
    # TODO: This should iterate through the scores in reverse and insert the
    # score when we find that it is lower than the current position in the list
    for posn, (_name, _score) in enumerate(scores):
        if score > _score:
            scores.insert(posn, (name, score))
            return posn + 1
    if len(scores) < SCORE_LIMIT:
        scores.append((name, score))
        return len(scores) + 1
    else:
        return None

def _to_file(scores, fileobj):
    fileobj.writelines('{},{}\n'.format(*i) for i in scores)

def get_scores():
    with open(HS_FILE, 'r') as f:
        return _from_file(f)

def add_score(name, score):
    """Takes name and score as arguments.
    Reads scorelist from file, updates it with given name and score, and
    returns tuple containing updated scorelist and player's position in it."""
    with open(HS_FILE, 'r+') as f:
        scores = _from_file(f)
        f.truncate(0)
        f.seek(0)
        posn = _insert_score(name, score, scores)
        _to_file(scores, f)
    return scores, posn
