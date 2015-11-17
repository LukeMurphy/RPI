import random
import sys


I = 0
lastI = 1
msg = ["Oh Infinite beatitude of existence me ",
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
"Me me me I mine mine mine is "
"Me wonderful me that I am "
] 


def soliloquy(override = False,arg = "") :
    global I, lastI, msg

    print("called ...")
    msgTxt = ""
    length = len(msg)
    if(length > 1) :
        if(random.random() > .9 or override) :
                I = int(random.random() * length)

                while (I == lastI):
                        I = int(random.random() * length)
                msgTxt  =  msg[I]
        if(arg != "") : msgTxt = arg    
        sys.stdout.write(msgTxt)
        sys.stdout.flush()
        #print(msg[I]),
        lastI = I