'''
------------------------------------------------
To Operate, this needs this in main() at start of piece

# -------------------------------------------------------- #

    from modules.manager_coordinator import CoordinationManager

# -------------------------------------------------------- #

    config.pieceId = workConfig.getint("particles", "pieceId", fallback=0)
    config.numberOfPiecesBeingManaged = workConfig.getint("particles", "numberOfPiecesBeingManaged", fallback=0)
    mngrSetupCoordination(config)


# -------------------------------------------------------- #

def mngrSetupCoordination(config) :
    _CM = CoordinationManager(config)
    _CM.pieceId = config.pieceId
    _CM.numberOfActivePieces = config.numberOfPiecesBeingManaged
    _CM.initiateListeners()
    # overrides what is called
    _CM.mngrAction = mngrAction
    _CM.mngrLocalAction = mngrLocalAction
    # _CM.stateFlags = {"lines":"raw"}
    config.coordinationManager = _CM

where mngrAction and mngrLocalAction are set to handle the local change and what
to do with the other pieces
------------------------------------------------
mngrAction is what is called when the manager state has changed and the piece is
responding to that change

def mngrAction():
    _CM: CoordinationManager
    _CM = config.coordinationManager
    # _CM.numberOfActivePieces = 4

    # for k,v in _CM.stateFlags.items() :
    #     pieceLogger(f"[piece-{config.pieceId}]: {k} = {v}", 2)

    for k,v in _CM.shareddict.get_all().items() :
        if k == "all" :
            [code here .......]
------------------------------------------------
mngrLocalAction is the triggering function and has to call:

# send signal to common dict that this piece has changed and what has changed
def mngrLocalAction(_x,_y) :
    # action when this piece changes - i.e. broadcast to others
    _CM: CoordinationManager
    _CM = config.coordinationManager
    if _CM.usingManagerComms :
        # ----------------------------------------------------------- #
        # will set all the other pieces to p[pieceId]Change = False but set this one to True
        # also sets the stateFlag to the stateFlagChange value eg "bg":"rnd"
        config.coordinationManager.coordinateChanges({optional new k/v pair})
        [then do things]


to let the other pieces know what is going on....
------------------------------------------------
This has to be put in the runWork or looping function to poll the manager state:

    config.coordinationManager.checkTime()

------------------------------------------------
'''
from logging import config
from multiprocessing.managers import BaseManager
from modules.configuration import pieceLogger
from modules.holder_director import Director


class PieceManager(BaseManager):
    pass

class CoordinationManager:

    config = None
    pieceId = 0
    usingManagerComms = False
    stateFlags = {}
    slotRate = 0.95
    numberOfActivePieces = 4

    def __init__(self, config):
        self.config = config


    def initiateListeners(self):
        self.usingManagerComms = True
        self.config.noWindowChrome = True

        # managing speed of checking the managed shared dicts
        self.commsController = Director(self.config)
        self.commsController.slotRate = self.slotRate
        
        try:
            PieceManager.register('sharedlist', exposed=['get_all', 'append', 'clear'])
            PieceManager.register('shareddict', exposed=['get_all', 'set', 'get', 'clear'])
            PieceManager.register('sharedData', exposed=['publicAction'])

            self.m = PieceManager(address=('127.0.0.1', 50000), authkey=b'LEDDELI49')
            self.m.connect()
            self.sharedlist = self.m.sharedlist()
            self.shareddict = self.m.shareddict()
            self.sharedData = self.m.sharedData()
        except Exception as e:
            pieceLogger(f"[piece-{self.pieceId} init] : {e}",1)
            self.usingManagerComms = False
            self.config.noWindowChrome = False


    def coordinateChanges(self, **kwargs):
            for key, argValue in kwargs.items():
                pieceLogger(f"{key}: {argValue}", 0, False, f"[piece-{self.pieceId} broadcast] : ")
                '''
                # set all the other piece values to p[n]-changed = False
                # then set the calling piece p[n]-changed = True
                # indicates the latest piece to have changed or had a triggering event
                ''' 
            try:
                for i in range(1,self.numberOfActivePieces+1) :
                    self.shareddict.set(f"p{i}-changed", False)
                    if self.pieceId == i :
                        if key  == "all" :
                            self.shareddict.set(f"{key}", argValue)
                        else :
                            self.shareddict.set(f"p{i}-{key}", argValue)
                        self.shareddict.set(f"p{i}-changed", True)
                        self.shareddict.set("lines","raw")
                for flag, value in self.stateFlags.items():
                    self.shareddict.set(flag, value)
            except Exception as e:
                pieceLogger(f"[piece-{self.pieceId} broadcast] : {e}",1)


    def checkList(self):
        _ref  = self.pieceId
        result = self.sharedlist.get_all()
        state = self.shareddict.get_all()

        # pieceLogger(state, 0, False, f"[piece-{self.pieceId}] checklist: ")

        # check if the shared dict has both, one of the flags to look for and 
        # has a p[n]-changed key/value
        # for flag,value in self.stateFlags.items():
        #     if flag in state and f"p{_ref}-changed" in state :
        #         # if the value of the shared k:v pair matches what is in the dict 
        #         # then call on the piece to respond
        #         if state[flag] == value and state[f"p{_ref}-changed"] == False:
        #             self.mngrAction()
        #             self.shareddict.set(f"p{_ref}-changed",True)

        # This version does not check against a list of stateFlags,
        # just calls the local mngrAction and lets it decide what to do
        if f"p{_ref}-changed" in state :
            # if the value of the shared k:v pair matches what is in the dict 
            # then call on the piece to respond
            if state[f"p{_ref}-changed"] == False:
                self.mngrAction()
                self.shareddict.set(f"p{_ref}-changed",True)


    def checkTime(self):
        if self.usingManagerComms:
            self.commsController.checkTime()
            if self.commsController.advance:
                self.checkList()


    # override these in the piece handle what happens
    def mngrAction(self, **kwargs):
        pieceLogger("[mngrAction] hello - no override?")
        pass


    def mngrLocalAction(self, **kwargs):
        pieceLogger("[mngrLocalAction] hello - no override?")
        pass

    
