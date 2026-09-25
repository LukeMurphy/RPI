import random
import settings_pieces as psets

if psets.MODES[psets.MODE] == "fixed" :
    __import__(psets.PIECES[psets.PIECE])
if psets.MODES[psets.MODE] == "random" or "random_w_restart":
    _c = random.choice(psets.PIECES)
    __import__(_c)
if psets.MODES[psets.MODE] == "remote" :
    import timer_coord
    timer_coord.getPieceToPlay()
    __import__(timer_coord.pieceToPlay)
