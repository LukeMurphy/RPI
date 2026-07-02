'''
------------------------------------------------
To Operate, this needs this in main() at start of piece

    from modules.manager_coordinator import CoordinationManager

    #  ---------------------------------------------- #
    config.coordinationManager = CoordinationManager(config)
    config.coordinationManager.pieceId = config.pieceId
    config.coordinationManager.initiateListeners()
    # overrides what is called
    config.coordinationManager.mngrAction = mngrAction
    config.coordinationManager.mngrLocalAction = mngrLocalAction
    #  ---------------------------------------------- #

where mngrAction and mngrLocalAction are set to handle the local change and what
to do with the other pieces
------------------------------------------------
mngrAction is what is called when the manager state has changed and the piece is
responding to that change
------------------------------------------------
mngrLocalAction is the triggering function and has to call:

    if config.coordinationManager.usingManagerComms :
        # will set all the other pieces to p[pieceId]Change = False but set this one to True
        # also sets the stateFlag to the stateFlagChange value eg "bg":"rnd"
        config.coordinationManager.coordinateChanges()
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
    stateFlag = "bg"
    stateFlagChange = "rnd"
    slotRate = 0.95

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

            self.m = PieceManager(address=('127.0.0.1', 50000), authkey=b'secret')
            self.m.connect()
            self.sharedlist = self.m.sharedlist()
            self.shareddict = self.m.shareddict()
            self.sharedData = self.m.sharedData()
        except Exception as e:
            pieceLogger(e,1)
            self.usingManagerComms = False
            self.config.noWindowChrome = False


    def coordinateChanges(self):
            # self.config.sharedData.publicAction()
            try:
                self.shareddict.set("p1Change", False)
                self.shareddict.set("p2Change", False)
                self.shareddict.set("p3Change", False)
                self.shareddict.set("p4Change", False)

                if self.pieceId == 1 : 
                    self.shareddict.set("p1Change", True)
                if self.pieceId == 2 : 
                    self.shareddict.set("p2Change", True)
                if self.pieceId == 3 : 
                    self.shareddict.set("p3Change", True)
                if self.pieceId == 4 : 
                    self.shareddict.set("p4Change", True)

                self.shareddict.set(self.stateFlag, self.stateFlagChange)
            except Exception as e:
                pieceLogger(e,1)


    def checkList(self):
        _ref  = self.pieceId
        result = self.sharedlist.get_all()
        state = self.shareddict.get_all()

        # pieceLogger(f"state: {state}")

        if self.stateFlag in state and f"p{_ref}Change" in state :
            if state[self.stateFlag] == self.stateFlagChange and state[f"p{_ref}Change"] == False:
                self.mngrAction()
                self.shareddict.set(f"p{_ref}Change",True)
        # if random.random() < .001 :
        #     ChangeBG()


    def checkTime(self):
        if self.usingManagerComms:
            self.commsController.checkTime()
            if self.commsController.advance:
                self.checkList()


    # override these in the piece handle what happens
    def mngrAction(self):
        pieceLogger("[mngrAction] hello - no override?")
        pass


    def mngrLocalAction(self):
        pieceLogger("[mngrLocalAction] hello - no override?")
        pass

    
