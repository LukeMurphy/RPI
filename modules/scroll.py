import time
import random
import ImageFont
import textwrap
import math

########################
#scroll speed and steps per cycle
scrollSpeed = .0011
steps = 6
fontSize = 14
vOffset  = -1

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
        global config, scrollSpeed, steps, fontSize, vOffset
            
        changeColor(clrChange)

        # draw the meassage to get its size
        font = config.ImageFont.truetype(config.path  + '/fonts/freefont/FreeSerifBold.ttf',fontSize)
        tempImage = config.Image.new("RGBA", (1200,128))
        draw  = config.ImageDraw.Draw(tempImage)
        pixLen = draw.textsize(arg, font = font)
        

        # make a new image with the right size
        config.renderImage = config.Image.new("RGBA", (config.actualScreenWidth , config.screenHeight))
        scrollImage = config.Image.new("RGBA", pixLen)
        draw  = config.ImageDraw.Draw(scrollImage)
        iid = scrollImage.im.id


        if(direction == "Bottom") :
            # The new image is going to be vertically stacked letters so will be
            # roughly as tall as it is long when written out horizontally
            # get average letter width

            letterHeight = pixLen[1] * 5/7
            imageHeight = len(arg) * letterHeight

            scrollImage = config.Image.new("RGBA", (pixLen[1], imageHeight))
            draw  = config.ImageDraw.Draw(scrollImage)
            iid = scrollImage.im.id
            chars = list(arg)
            count = 0
            xOffset = -int(config.screenWidth/2 * random.random()) + 10
            vOffset  = -1

            for letter in chars :
                draw.text((2,count * letterHeight),letter,(r,g,b),font=font)
                count += 1

            end = scrollImage.size[1]
            start = -64
            
            for n in range(start,end):
                #fix  config.matrix.SetImage(config.id,xOffset,-n)
                config.render(scrollImage, xOffset, n, pixLen[0], pixLen[1])
                time.sleep(scrollSpeed)

        elif(direction == "Top") :
                imageHeight = pixLen[0]

                print (pixLen, imageHeight)

                scrollImage = config.Image.new("RGBA", (imageHeight, pixLen[1]))
                draw  = config.ImageDraw.Draw(scrollImage)
                draw.text((0,0),arg,(r,g,b),font=font)
                scrollImage = scrollImage.rotate(-90)
                scrollImage.load()
                xOffset =int(random.random()*(config.screenWidth - pixLen[1]))

                for n in range(0,pixLen[0] + config.screenHeight):
                    config.render(scrollImage, xOffset, -n + pixLen[0] , 0,0)
                    time.sleep(.012)


        else :
            scrollImage = config.Image.new("RGBA", pixLen)
            draw  = config.ImageDraw.Draw(scrollImage)
            iid = scrollImage.im.id
            draw.text((0,0),arg,(r,g,b),font=font)

            start = 0
            end = scrollImage.size[0]
            start = -128
            if(direction == "Right") : 
                start = -end
                end = 128

            

            for n in range(start,end):
                try :
                    if(direction == "Left") :
                            config.render(scrollImage, -n, vOffset,pixLen[0], pixLen[1], False)
                            config.actions.drawBlanks()
                    else :
                            config.actions.drawBlanks()
                            config.render(scrollImage, n, vOffset,pixLen[0], pixLen[1], False)
                            if(random.random() > 0.9998) :
                                            config.actions.glitch()
                                            break
                except KeyboardInterrupt:
                            #print "Stopping"
                            break

                time.sleep(scrollSpeed)

def stroop( arg, clr, direction = "Left") :

        global r,g,b
        #matrix.Clear()
        speed = .018
        font = ImageFont.truetype(config.path + '/fonts/freefont/FreeSansBold.ttf',30)
        font2 = ImageFont.truetype(config.path + '/fonts/freefont/FreeSansBold.ttf',30)
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

