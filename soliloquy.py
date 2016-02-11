from __future__ import print_function
import random, time
import sys
import threading



class soliloquy() :


    def __init__(self, arg=""):
        self.name = arg
        self.I = 0
        self.lastI = 1
        self.msg = [
        "Oh Infinite beatitude of existence me ",
        "I am; and there is nothing else beside I that is me ",
        "I fill all Space, and what I fill, I am ", 
        "What I think, that I utter; and what I utter, that I hear ",
        "I itself is Thinker, Utterer, Hearer, Thought, Word, Audition ",
        "it is the One, and yet the All in All ",
        "Ah, the happiness, ah, the happiness of Being "
        "Ah, the joy, ah, the joy of Thought ",
        "Ah that is me all me by me "
        "What can I not achieve by thinking!",
        " My own Thought coming to myself ",
        "Ah, the joy, the joy of Being ", 
        "Me I mine is "
        "Me wonderful me that I am "
        ] 
        self.length = len(self.msg)


    def soliloquy(self) :
        
        #print(self.name)
        '''
        delay = random.random() * 1
        time.sleep(delay)
        self.soliloquy()
        '''

        if(random.random() > .93) :
            rnd = int(random.uniform(1,6))    
            if(rnd == 1) :
                print('Me. ', end="")
            elif(rnd == 2) :
                print('Me. ')
            elif(rnd == 3) :
                print('I <==> me <==> I', end="")
            elif(rnd == 4) :
                print('I && me ', end="")
            elif(rnd == 5) :
                print('me <<< me ', end="")

        if(random.random() > .98) : print("O Me", end=" ")
        if(random.random() > .998) : 
            print("")
            print("|-------|")
            print("|   I   |")
            print("|-------|")

        msgTxt = ""
        if(random.random() > .99) :
            print(time.clock())
        if(random.random() > .97) :
                self.I = int(random.random() * self.length)

                while (self.I == self.lastI):
                    self.I = int(random.random() * self.length)
                msgTxt  =  self.msg[self.I]  
        print(msgTxt, end=" ")
        if(random.random() > .5) : print(" ", end="")
        if(random.random() > .85) : print(" ")
        self.lastI = self.I
        sys.stdout.flush()
        


#####################
s1 = soliloquy("s-one")
'''
s1 = soliloquy("s-one")
s2 = soliloquy("s=two")

threads = []

t = threading.Thread(target=s1.soliloquy)
threads.append(t)
t.start()

t = threading.Thread(target=s2.soliloquy)
threads.append(t)
t.start()

'''

while True :
    s1.soliloquy()


    delay = random.random() * .3
    #delay = .1
    time.sleep(delay)
