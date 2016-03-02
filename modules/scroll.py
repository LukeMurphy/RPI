import time
import random
import ImageFont
import textwrap
import math

########################
#scroll speed and steps per cycle
scrollSpeed = 0.0006
stroopSpeed = 0.0001
steps = 2
stroopSteps = 2

fontSize = 14
vOffset  = -1
opticalOpposites = True
countLimit = 6
count = 0

# fcu present will start with the opposite
paintColor = "GREEN"

r=g=b=0

def changeColor( rnd = False) :
        global r,g,b,config
        if (rnd == False) :
                if(r == int(255* config.brightness)) :
                        r = 0
                        g = int(255* config.brightness)
                        b = 0
                else :
                        g = 0
                        r = int(255* config.brightness)
                        b = 0
        else :
                r = int(random.uniform(0,255) * config.brightness)
                g = int(random.uniform(0,255) * config.brightness)
                b = int(random.uniform(0,255) * config.brightness)

def scrollMessage( arg, clrChange = False, adjustLenth = False, direction = "Left") :   
        global config, scrollSpeed, stroopSpeed, steps, fontSize, vOffset  
        changeColor(clrChange)

        # draw the meassage to get its size
        font = config.ImageFont.truetype(config.path  + '/fonts/freefont/FreeSerifBold.ttf',fontSize)
        tempImage = config.Image.new("RGBA", (1200,196))
        draw  = config.ImageDraw.Draw(tempImage)
        pixLen = draw.textsize(arg, font = font)
        # For some reason textsize is not getting full height !
        fontHeight = int(pixLen[1] * 1.3)

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
                config.render(scrollImage, xOffset, n, pixLen[0], fontHeight)
                time.sleep(scrollSpeed)

        elif(direction == "Top") :
                imageHeight = pixLen[0]

                print (pixLen, imageHeight, fontHeight)

                scrollImage = config.Image.new("RGBA", (imageHeight, imageHeight))
                draw  = config.ImageDraw.Draw(scrollImage)
                draw.text((0,0),arg,(r,g,b),font=font)
                #scrollImage = scrollImage.rotate(-90)
                #scrollImage.load()
                #print(scrollImage.size)

                xOffset =int(random.random()*(config.screenWidth - fontHeight))

                for n in range(0,pixLen[0] + config.screenHeight):
                    config.render(scrollImage, xOffset, -n + pixLen[0] , 0,0)
                    time.sleep(.012)


        else :
            scrollImage = config.Image.new("RGBA", (pixLen[0],fontHeight))
            draw  = config.ImageDraw.Draw(scrollImage)
            iid = scrollImage.im.id
            draw.text((0,0),arg,(r,g,b),font=font)

            start = 0
            end = scrollImage.size[0]
            start = -config.screenWidth
            if(direction == "Right") : 
                start = -end
                end = config.screenWidth


            for n in range(start,end, steps):
                if(direction == "Left") :
                        config.render(scrollImage, -n, vOffset, pixLen[0], fontHeight, False)
                        config.actions.drawBlanks()
                else :
                        config.actions.drawBlanks()
                        config.render(scrollImage, n, vOffset, pixLen[0], fontHeight, False)
                        if(random.random() > 0.9998) :
                                        config.actions.glitch()
                                        break
                time.sleep(scrollSpeed)

def present(arg, clr = (250,150,150), duration = 1, repeat = -1) :
        global config, scrollSpeed, steps, fontSize, vOffset, countLimit, count
        global r,g,b, paintColor
        
        vFactor = 1.5

        try:
            #changeColor(False)
            if (paintColor == "RED") : 
                paintColor = "GREEN"
            else :
                paintColor =  "RED"
            #clr = tuple(int(a*config.brightness) for a in (clr))
            paintColorRGB = config.subtractiveColors(paintColor)

            fSize = int(config.screenHeight * vFactor)
     
            # draw the message to get its size - not very accurate for height tho...
            font = ImageFont.truetype(config.path + '/fonts/freefont/FreeSansBold.ttf', fSize)
            pixLen = config.draw.textsize(arg, font = font)

            # make a new image with the right size
            scrollImage = config.Image.new("RGBA", (pixLen[0], pixLen[1] + 20))
            draw = config.ImageDraw.Draw(scrollImage)
            xoffRange = 1
            yOffRange = 2

            # Draw the 'shadow' - either the 'optical ' RGB opposite or the RBY paint 'opposite/compliment'
            if(random.random() > .5) :
                draw.text((-xoffRange, yOffRange), arg,config.colorCompliment(paintColorRGB), font=font)
            else:
                draw.text((-xoffRange, yOffRange), arg,config.colorComplimentRBY(paintColor), font=font)

            # Draw the actual text    
            draw.text((0,0 ), arg, paintColorRGB, font=font)

            # Scale the image to fit the full set of panels (using a rough formula for font offset)
            scaledSize = (config.screenWidth , int( vFactor * float(config.screenHeight * pixLen[1]) / fSize) + 8) 
            #scaledSize = (config.screenWidth , config.screenHeight) 
            scrollImage = scrollImage.resize(scaledSize)

            vOffset = -scaledSize[1]/8
            config.render(scrollImage, 0, vOffset + 4, config.screenWidth, config.screenHeight - vOffset)
            config.actions.drawBlanks()

            time.sleep(duration)

            if(count <= countLimit) :
                count +=1
                # if countLimit = 0 then assume go on forever ...
                if(countLimit == 0) : count = 0

                if(repeat == -1) : present(arg, paintColorRGB,  duration, repeat)
                if(repeat > 0 ) :  present(arg, paintColorRGB,  duration, repeat - 1)
                if(repeat == 0) : pass
    
               
            #else : 
                #pass
                #exit()

        except KeyboardInterrupt:
            #print "Stopping"
            exit()     

def stroop( arg, clr, direction = "Left") :

        global r,g,b,config, opticalOpposites, stroopSpeed, stroopSteps

        brightness = config.brightness
        brightness = random.random()

        clr = tuple(int(a*brightness) for a in (clr))

        # Setting 2 fonts - one for the main text and the other for its "border"... not really necessary
        font = ImageFont.truetype( '/home/pi/RPI/fonts/freefont/FreeSansBold.ttf',30)
        font2 = ImageFont.truetype('/home/pi/RPI/fonts/freefont/FreeSansBold.ttf',30)
        pixLen = config.draw.textsize(arg, font = font)

        dims = [pixLen[0],pixLen[1]]
        if(dims[1] < 32) : dims[1] = 34

        config.image = config.Image.new("RGBA", (dims[0],dims[1]))
        config.draw  = config.ImageDraw.Draw(config.image)
        config.id = config.image.im.id

        # Draw Background Color
        # Optical (RBY) or RGB opposites

        if(opticalOpposites) :
            if(arg == "RED") : bgColor = tuple(int(a*brightness) for a in ((255,0,0)))
            if(arg == "GREEN") : bgColor = tuple(int(a*brightness) for a in ((0,255,0)))
            if(arg == "BLUE") : bgColor = tuple(int(a*brightness) for a in ((0,0,255)))
            if(arg == "YELLOW") : bgColor = tuple(int(a*brightness) for a in ((255,255,0)))
            if(arg == "ORANGE") : bgColor = tuple(int(a*brightness) for a in ((255,125,0)))
            if(arg == "VIOLET") : bgColor = tuple(int(a*brightness) for a in ((200,0,255)))
        else:
             bgColor = config.colorCompliment(clr, brightness)

        config.draw.rectangle((0,0,config.image.size[0]+32, config.screenHeight), fill=bgColor)

        # Draw the text with "borders"
        config.draw.text((-1,-1),arg,(0,0,0),font=font2)
        config.draw.text((1,1),arg,(0,0,0),font=font2)
        config.draw.text((0,0),arg,clr,font=font)

        start = 0
        end = config.image.size[0]+32
        offset = int(random.uniform(1,config.screenWidth-20))

        if(direction == "Top" or direction == "Bottom") :
            config.image = config.Image.new("RGBA", (dims[1], dims[0]*2))
            config.draw  = config.ImageDraw.Draw(config.image)
            config.id = config.image.im.id
            chars = list(arg)
            count = 0

            # Generate vertical text
            for letter in chars :
                    # rough estimate to create vertical text
                    config.draw.text((2,count * int(dims[1] * 3/4)),letter,clr,font=font)
                    count += 1
            start = -end
            end = end - int(random.random() * config.screenHeight)

            # Scroll vertical text UP
            for n in range(start,end, int(stroopSteps)):
                    config.render(config.image, offset, -n, dims[1], dims[0]*2)
                    time.sleep(stroopSpeed)

        if(direction == "Left" or direction == "Right") :
            # Left Scroll
            start = 0
            end = config.screenWidth - int(random.uniform(0,config.image.size[0])) #+ config.image.size[0] 

            if(direction == "Right") :
                start = -end
                end = int(random.uniform(0,config.image.size[0]))

            
            #vOffset = -1
            vOffset = int(random.uniform(0,config.rows)) * 32

            for n in range(start, end, int(stroopSteps)):
                    if(direction == "Left") :
                            #config.matrix.SetImage(config.id, 0, -2)
                            #config.matrix.SetImage(config.id, config.screenWidth-n, -2)
                            config.render(config.image, config.screenWidth-n, vOffset, dims[0], dims[1])
                    else :
                            #config.matrix.SetImage(config.id, n, -2)
                            config.render(config.image, n, vOffset, dims[0], dims[1])
                    time.sleep(stroopSpeed)

