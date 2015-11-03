import time
import random
import ImageFont
import textwrap
import math

########################




r=g=b=0

def changeColor( rnd = False) :
        global r,g,b
        if (rnd == False) :
                if(r == 255) :
                        r = 0
                        g = 255
                        b = 0
                else :
                        g = 0
                        r = 255
                        b = 0
        else :
                r = int(random.uniform(0,255))
                g = int(random.uniform(0,255))
                b = int(random.uniform(0,255))


def scrollMessage( arg, clrChange = False, adjustLenth = False, direction = "Left") :	
        global config
        
        #matrix.Clear()
        
        changeColor(clrChange)
        font = config.ImageFont.truetype('/home/pi/rpi-rgb-led-matrix-master/fonts/freefont/FreeSerifBold.ttf',30)
        pixLen = config.draw.textsize(arg, font = font)
        #print (pixLen)

        config.image = config.Image.new("RGBA", pixLen)
        config.draw  = config.ImageDraw.Draw(config.image)
        config.id = config.image.im.id

        #message(arg, clrChange)
        config.draw.text((0,0),arg,(r,g,b),font=font)

        start = 0
        end = config.image.size[0]
        voffset  = -1
        xoffset = int(config.screenWidth/2 * random.random())
        if(direction == "Right") :
                        start = -end
                        end = 0

        if(direction == "Bottom") :
                        config.image = config.Image.new("RGBA", (pixLen[1],pixLen[0]*2))
                        config.draw  = config.ImageDraw.Draw(image)
                        config.id = config.image.im.id
                        chars = list(arg)
                        count = 0
                        for letter in chars :
                                        draw.text((2,count* pixLen[1] * 3/4),letter,(r,g,b),font=font)
                                        count += 1
                        start = -end
                        end = end

                        for n in range(start,end):
                                        config.matrix.SetImage(config.id,xoffset,-n)
                                        time.sleep(config.scrollSpeed)

        elif(direction == "Top") :
                        start = -end
                        end = 0

                        config.image = config.image.rotate(-90)
                        config.id = config.image.im.id

                        for n in range(start,end):
                                        config.matrix.SetImage(config.id,xoffset,n)
                                        config.actions.drawBlanks()
                                        time.sleep(config.scrollSpeed)

        else :

                        for n in range(start,end):
                                        try :
                                                if(direction == "Left") :
                                                                config.matrix.SetImage(config.id, -n, voffset)
                                                                config.actions.drawBlanks()
                                                else :
                                                                config.matrix.SetImage(config.id, n, voffset)
                                                                config.actions.drawBlanks()
                                                                if(random.random() > 0.9998) :
                                                                                config.actions.glitch()
                                                                                break
                                        except KeyboardInterrupt:
                                                        #print "Stopping"
                                                        break

                                        time.sleep(config.scrollSpeed)




def stroop( arg, clr, direction = "Left") :

        global r,g,b
        #matrix.Clear()
        speed = .018
        font = ImageFont.truetype('/home/pi/rpi-rgb-led-matrix-master/fonts/freefont/FreeSansBold.ttf',30)
        font2 = ImageFont.truetype('/home/pi/rpi-rgb-led-matrix-master/fonts/freefont/FreeSansBold.ttf',30)
        pixLen = config.draw.textsize(arg, font = font)

        config.image = config.Image.new("RGBA", pixLen)
        config.draw  = config.ImageDraw.Draw(config.image)
        config.id = config.image.im.id

        config.draw.rectangle((0,0,config.image.size[0]+32,config.screenHeight), fill="blue")
        config.draw.text((-1,-1),arg,(0,0,0),font=font2)
        config.draw.text((1,1),arg,(0,0,0),font=font2)
        config.draw.text((0,0),arg,clr,font=font)

        start = 0
        end = config.image.size[0]+32
        offset = int(random.uniform(1,config.screenWidth-20))

        if(direction == "Right") :
            start = -end
            end = 0

        if(direction == "Top") :
            config.image = config.Image.new("RGBA", (pixLen[1],pixLen[0]*2))
            config.draw  = config.ImageDraw.Draw(config.image)
            config.id = config.image.im.id
            chars = list(arg)
            count = 0
            for letter in chars :
                    config.draw.text((2,count* pixLen[1] * 3/4),letter,clr,font=font)
                    count += 1
            start = -end
            end = end

            for n in range(start,end):
                    config.matrix.SetImage(config.id,offset,-n)
                    time.sleep(0.01)

        else :
            # Left Scroll
            start = 0
            end = config.screenWidth + config.image.size[0]
            #matrix.Fill(0,0,255)
            for n in range(start,end):
                    if(direction == "Left") :

                            config.matrix.SetImage(config.id, 0, -2)
                            config.matrix.SetImage(config.id, config.screenWidth-n, -2)
                    else :
                            config.matrix.SetImage(config.id, n, -2)
                    time.sleep(0.01)

# ################################################### #

