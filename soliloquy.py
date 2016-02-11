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

        self.drawings = []
        self.drawings.append("""
                                   `.-:/::::::::-..`                                                
                               `.:+o+/--/`      `..-:-`                                             
                           `.-:/+:.`                 .-:.                                           
                        `.:---:-`                      `-/.                                         
                       --.`-:.                           `::`                                       
                        `-:.                               ./.                 `                    
                       ./.                  ````            `/.                   .                 
                      ./             `:/`  -/:::/-`           +.                  .                 
                     `+             .+-:+`+-     -o           `o                                    
                     +`            .o`  +s.       s            o`                                   
                     +            `s`   `y`      :+            o`                                   
                    ./            +-     y/    `//            `o                                    
                    -:            y.  `.-/h/://:`             /.                                    
                    `+            -+///-.`-s`                :-                                     
                     +`                    s+/` .`          ::                                      
                     `+.                   /-.:/-          :-                                       
                       ::`                 `o            `/.                                        
                        `-:-                o`          -/`                                         
                           `::-`            ::       `-:.                                           
                              `-:--.`       `o   `.-:-`                                             
                                 ``.-----::::y////--.```                                            
                                  `.--:::----s-.....---:/::-                                        
                               .-::.``       /-           `-/:`                                     
                           `.-:-`            .+              ./:`                                   
                        `-::.`                s                ./:`                                 
                      `-:.`                   o`                 ./:                                
                    `::`                      /-                   -+`                              
                   ./.                        -/                    .+...`                          
                  ::                          `o                     `so.`                          
                `/.                            s                     /:/:                           
                /.                             s                    /:  :/                          
               :-                             `o                  `/-    /:                         
              `+                              `o                 .+.      o.                        
              :.                               s               `:/`       .o                        
              o                                s              ./-          +-                       
              :`                               o`           `/:`           .+                       
       .-.                                     /.          -/`              s                       
      .y:.                                     /-        `/:                +.                      
      s/                                       /.       `+.                 .+                      
      o+`                                      o`      -+`                   s                      
       :o:`                                    o      :/                     /-                     
         :+/`                                 -/     /:                      `s                     
           ./+:`                              +.    +-                        ::                    
              `://-`                          s    +:                          o`                   
                  .://-`                     `o   //                           .+                   
                      .:/:.                  -/  :+                             o.                  
                         `-//:.              /: /+                 `............:+..`               
                             `-//:.          o:++  ````....--..---..``           s `.-.             
                                ``://:-` ``..+s/-----....`````       -` `:::     y`   `-.           
                                  `..-:-:++/+y:         `  `y-  :+o +s+//.`o.   -h.     :`          
                       ``        ```-    ````:/-        / `os`.o+:h:yo/.   .o-../:      ..          
                   .....`          ::  `: ` //-s        o`o.o+///-.```      `-:.`       ..          
               `.-.``             `s`  `:.-.s/o-        :/. ``                         `-`          
             `--``             .. +o `::.``o/``                                       ..`           
             -.      `:+-:+o` `s++-+::`    s:                                      ``.`             
             :`    /++:y.` :+:+-.` ``      o/                                    `.``               
             .:     `  +-   `.`            :-                               ```.``                  
              .-.`     .o                                            `````````                      
                `.....``+`                                    ``````````                            
                    ``````....````                ````````````````                                  
                             ````...............`````````  """)


        self.drawings.append("""
            |-------|
            |   I   |
            |-------|
                    """)
        self.drawings.append("""
    000000000000000000000000000000000.0000.0000000000000000000000000000000000000000000000000
    0000000000000000000000000000000.00.....0000000000000000000000000000000000000000000
    00000000000000000000000000000  00000000000...0000000000000000000000000000000000000000
    000000000000000000000000000  .000000000000000  000000000000000000000000000000000000000
    00000000000000000000000000  000000000000000000  00000000000000000000000000000000000
    00000000000000000000000000  000000000000000000.00000000000000000000000000000000000000
    00000000000000000000000000  0000000000..00..00.00000000000000000000000000000000000000
    00000000000000000000000000  .000000....0.00000  0000000000000000000000000000000000000
    000000000000000000000000000   0000.0.00000000  0000000000000000000000000000000000000
    00000000000000000000000000000. 0000000000...000000000000000000000000000000000000000000
    0000000000000000000000000000000.....00.000000.00000000..0.000000000000000000000000000
    0000000000000000000000000000000000.0000...00.0000000000.0.....0000000000000000000000000
    000000000000000000000000000000000000.000000000000000000000000000000000000000000000
    0000000000000000000000000000000..000000000000000000000000000000..00000000000000000000000
    00000000000000000000000000000.000000000000000000000000000000000000..000000000000000000
    0000000000000000000000000000..0000000000000000000000000000000000000.0000000000000000
    00000000000000000000000000...0000000000000000000000000000000000000000000000000000000000
    00000000000000000000000000.000000000000000000000000000000000000000000000000000000000
    000000000000000000000000...000000000000000000000000000000000000000000000000000000000000
    00000000000000000000000.  000000000000000000000000000000000000000000000000000000000000
    00000000000000000000000..00000000000000000000000000000000000000000000000000000000000000
    000000000000000000000..00000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
 """)
        self.drawings.append(""" """)
        self.drawings.append(""" """)


    def soliloquy(self) :
        
        #print(self.name)
        '''
        delay = random.random() * 1
        time.sleep(delay)
        self.soliloquy()
        '''
        
        l1 = .9
        l2 = l1 + .02
        l3 = l1 + .04
        l4 = l1 + .06
        l5 = l1 + .08
        l6 = l1 + .09
        l7 = l1 + .096
        l8 = l1 + .098
        l9 = l1 + .0985

        # Print Self Shifters
        if(random.random() > l1) :
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

        if(random.random() > l3) : print("O Me", end=" ")
        if(random.random() > l8) : print(self)
        if(random.random() > l9) : print(time.clock())

        # Print a Self Drawing
        if(random.random() > l9) : 
            i = int(random.uniform(0,len(self.drawings)))
            print("I draw for me.")
            #print(self.drawings[i])
            for n in range(0,len(self.drawings[i])) :   
                print(self.drawings[i][n], end="")
                time.sleep(.002)

        msgTxt = ""
        
        ### Print from Soliloquy of The Point
        if(random.random() > l4) :
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
