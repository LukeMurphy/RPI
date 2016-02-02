from __future__ import print_function
import random, time
import sys



class soliloquy() :


    def __init__(self):
        self.I = 0
        self.lastI = 1
        self.msg = ["Oh Infinite beatitude of existence me ",
        "I am; and there is nothing else beside I that is me ",
        "I fill all Space, and what I fill, I am ", 
        "What I think, that I utter; and what I utter, that I hear ",
        "I itself is Thinker, Utterer, Hearer, Thought, Word, Audition ",
        "it is the One, and yet the All in All ",
        "Ah, the happiness, ah, the happiness of Being "
        "Ah, the joy, ah, the joy of Thought ",
        "Ah that is me all me by me "
        "What can I not achieve by thinking! My own Thought coming to myself ",
        "Ah, the joy, the joy of Being ", 
        "Me I mine is "
        "Me wonderful me that I am "
        ] 
        self.length = len(self.msg)


    def soliloquy(self) :
        
        #print("me.")
        if(random.random() > .2) :
            rnd = int(random.uniform(1,4))
            
            if(rnd == 1) :
                print('Me. ', end="")
            elif(rnd == 2) :
                print('Me. ')
            elif(rnd == 3) :
                print('[I] ', end="")
        if(random.random() > .8) : print("O Me", end=" ")
      
        msgTxt = ""

        if(random.random() > .7) :
                self.I = int(random.random() * self.length)

                while (self.I == self.lastI):
                    self.I = int(random.random() * self.length)
                msgTxt  =  self.msg[self.I]  
        print(msgTxt, end=" ")
        if(random.random() > .5) : print(" ")
        self.lastI = self.I
        sys.stdout.flush()


#####################
s = soliloquy()

while True :
    s.soliloquy()
    delay = random.random() * 1
    time.sleep(delay)