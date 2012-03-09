from os.path import join, isfile

from config import get_conf_filepath
from debug import log

HS_FILE = get_conf_filepath('hiscores')
SCORE_LIMIT = 20

if not isfile(HS_FILE):
    with open(HS_FILE, 'a') as f:
        pass

def _reverse_enum(seq):
    # Using range for this is "bad practice" but enumerate won't give the
    # desired functionality.
    for i in range(len(seq), 0, -1):
        yield i-1, seq[i-1]

def _from_file(fileobj):
    scores = []
    for line in fileobj:
        name, score = line.split(',')
        scores.append((name, int(score)))
    return scores
        
def _insert_score(name, score, scores):
    # NB: This returns the player's position in the high scores (start from 1),
    #     not the position in the scores list (start from 0).
    for posn, (_name, _score) in _reverse_enum(scores):
        if score <= _score:
            scores.insert(posn+1, (name, score))
            return posn + 2
    scores.insert(0, (name, score))
    return 1

def _to_file(scores, fileobj):
    fileobj.writelines('{},{}\n'.format(*i) for i in scores)

def get_scores():
    with open(HS_FILE, 'r') as f:
        return _from_file(f)

def print_scores():
    scores = get_scores()
    for p, s in enumerate(scores):
        name, score = s
        print('\t'.join((str(p+1), name, str(score))))
    exit(0)
        

def add_score(name, score):
    """Takes name and score as arguments.
    Reads scorelist from file, updates it with given name and score, and
    returns tuple containing updated scorelist and player's position in it."""
    scores = get_scores()
    if not score:
        return scores, None
    posn = _insert_score(name, score, scores)
    if len(scores) > SCORE_LIMIT:
        scores = scores[:SCORE_LIMIT]
    with open(HS_FILE, 'w') as f:
        _to_file(scores, f)
    return scores, posn
