StringDict initConfig;
StringDict config;

PShape bg;
PGraphics canvas;
PGraphics animationCanvas;

PFont fnt;
boolean moved = false;
int windowXPos = 0;
int windowYPos = 0;

int windowWidth = 100;
int windowHeight = 100;
int canvaswidth = 100;
int canvasheight = 100;
int animationCanvaswidth = 100;
int animationCanvasheight = 100;
int centerX = 0;
int centerY = 0;
int cutups = 0;

float canvasRotation = 0.0;

float brightness = 1.0;
float bgbrightness = 1.0;

float driftToCenter = 1000;
float deltaFactor = 1.0;
float deltaDirection = .1;
float drawPartProbability = 1.0;
float orientationFlipProb = 0.0;


float widthRandomness = 0.0;
float heightRandomness = 0.0;

int xOffset = 0;
int yOffset = 0;

int numberOfParts = 0;

// 0 is linear, 1 is radial
int motionType = 0;
int xOffCanvasBuffer = 0;
int yOffCanvasBuffer = 0;

ArrayList<Part> parts;
Dither ditherer;
float ditherLevels = 1.0;

int vDistance = 1;
int hDistance = 1;
int rowsLeftOff = 0;

float changeColorProb = 0.0;
float randomColorProb = 0.0;
boolean doDrawGrid = false;
color gridLineColor;
color gridTextColor;

float[] bgcolors_hsv;
float[] gridLineColors_hsv;
float[] gridTextColors_hsv;
float[] partColors_hsv;
float[] fixedColors_hsv;
float[] partStrokeColors_hsv;
float[] rndclrs_hsv = {0.0, 360.0, 0.0, 255.0, 0.0, 255.0, 20.0};


color bgcolor;
int bgAlpha = 0;
ColorTransition ct;

// Single color for all parts
ColorTransition allPartsct;
Boolean uniformColor;
Boolean multipleOrigins = false;

PImage realImage;
boolean useImageSprites  = false;


/*

 *********************
 *    -----------    *
 *   |   oooooooooooooooooooooooooooo
 *   |   o      |    *              o 
 *   |   o      |    *              o
 *   |   o      |    *              o
 *   |   oooooooooooooooooooooooooooo ANIMATION CANVAS
 *   |          |    *
 *   |          |    *
 *   |          |    *
 *   |          |    *
 *   |          |    *
 *   |          |    *
 *    ----------- CANVAS 
 *                   *
 *                   *
 ********************* WINDOW
 
 
 
 
 
 
 */


void settings() {

    /*************************************************/
    //  PARSE CONFIG FILE  
    /*************************************************/

    initConfig = ConfigParse("base-config.cfg");
    String configFileToLoad = initConfig.get("configFile");

    println("Using config file: ", configFileToLoad);

    config = ConfigParse(configFileToLoad);

    String[] temp;
    temp = config.get("p.fixedColors_hsv").split(",");
    fixedColors_hsv = ParseColorStringHSV(temp);

    temp = config.get("bgcolors_hsv").split(",");
    bgcolors_hsv = ParseColorStringHSV(temp);

    temp = config.get("gridLineColors_hsv").split(",");
    gridLineColors_hsv = ParseColorStringHSV(temp);

    temp = config.get("gridTextColors_hsv").split(",");
    gridTextColors_hsv = ParseColorStringHSV(temp);

    bgAlpha = parseInt(bgcolors_hsv[6]);

    temp = config.get("rndclrs_hsv").split(",");
    rndclrs_hsv = ParseColorStringHSV(temp);


    String[] gridLineColors = config.get("gridLineColor").split(",");
    gridLineColor = ParseColorString(gridLineColors);

    String[] gridTextColors = config.get("gridTextColor").split(",");
    gridTextColor = ParseColorString(gridTextColors);

    brightness = parseFloat(config.get("brightness"));
    bgbrightness = parseFloat(config.get("bgbrightness"));

    windowWidth = parseInt(config.get("windowWidth"));
    windowHeight = parseInt(config.get("windowHeight"));   

    canvaswidth = parseInt(config.get("canvaswidth"));
    canvasheight = parseInt(config.get("canvasheight"));    

    animationCanvaswidth = parseInt(config.get("animationCanvaswidth"));
    animationCanvasheight = parseInt(config.get("animationCanvasheight"));

    canvasRotation = parseFloat(config.get("canvasRotation"));

    doDrawGrid = parseBoolean(config.get("drawGrid"));

    windowXPos = parseInt( config.get("windowXPos"));
    windowYPos = parseInt( config.get("windowYPos"));

    xOffset = parseInt( config.get("xOffset"));
    yOffset = parseInt( config.get("yOffset"));
    centerX = parseInt( config.get("p.centerX"));
    centerY = parseInt( config.get("p.centerY"));

    xOffCanvasBuffer = parseInt( config.get("p.xOffCanvasBuffer"));
    yOffCanvasBuffer = parseInt( config.get("p.yOffCanvasBuffer"));

    cutups = parseInt( config.get("cutups"));

    motionType = parseInt( config.get("p.motionType"));

    ditherer = new Dither();
    ditherer.x0 = parseInt(config.get("ditherer.x0"));
    ditherer.x1 = parseInt(config.get("ditherer.x1"));
    ditherer.y0 = parseInt(config.get("ditherer.y0"));
    ditherer.y1 = parseInt(config.get("ditherer.y1"));
    ditherer.levels = parseInt(config.get("ditherer.levels"));

    size(windowWidth, windowHeight);
}


void setup() {
    surface.setTitle("cascade");
    //smooth();
    frameRate(60);
    //background(20, 100, 20, 100);

    /*************************************************
     	 Creates the visible canvas and the animation canvas
     	 They may be the same size of not depending on setup
     	 *************************************************/

    canvas = createGraphics(canvaswidth, canvasheight);
    animationCanvas = createGraphics(animationCanvaswidth, animationCanvasheight);

    fnt = createFont("SourceCodePro-Regular.ttf", 11);
    textFont(fnt);

    String[] temp;

    temp = config.get("p.partColors_hsv").split(",");
    partColors_hsv = ParseColorStringHSV(temp);

    temp = config.get("p.partStrokeColors_hsv").split(",");
    partStrokeColors_hsv = ParseColorStringHSV(temp);

    uniformColor = parseBoolean(config.get("p.uniformColor"));
    println("Using uniformcolor: ", uniformColor);

    multipleOrigins = parseBoolean(config.get("p.multipleOrigins"));
    println("Using multipleOrigins: ", multipleOrigins);

    useImageSprites = parseBoolean(config.get("p.useImageSprites"));
    println("Using multipleOrigins: ", useImageSprites);

    if (uniformColor == true) {
        allPartsct = new ColorTransition();
        allPartsct.alpha = int(fixedColors_hsv[6]);
        allPartsct.brightness = bgbrightness;
        allPartsct.startColor = color(0, 0, 200, int(fixedColors_hsv[6]));
        allPartsct.endColor = color(200, 0, 0, int(fixedColors_hsv[6]));

        allPartsct.doNewTansition = true;
        allPartsct.steps = 20;
        allPartsct.rndStepMin = 300;
        allPartsct.rndStepMax = 900;
        allPartsct.partColors_hsv = fixedColors_hsv;
        allPartsct.setupColorTransition();
    }

    drawPartProbability = parseFloat(config.get("p.drawPartProbability"));
    driftToCenter = parseFloat(config.get("p.driftToCenter"));
    deltaFactor = parseFloat( config.get("p.deltaFactor"));
    deltaDirection = parseFloat( config.get("p.deltaDirection"));
    numberOfParts = parseInt( config.get("p.numberOfParts"));
    vDistance = parseInt( config.get("p.vDistance"));
    hDistance = parseInt( config.get("p.hDistance"));
    rowsLeftOff = parseInt( config.get("p.rowsLeftOff"));
    changeColorProb = parseFloat(config.get("p.changeColorProb"));
    randomColorProb = parseFloat(config.get("p.randomColorProb"));
    orientationFlipProb = parseFloat(config.get("p.orientationFlipProb"));

    String realImageSource = (config.get("realImageSource"));
    realImage = loadImage(realImageSource);

    widthRandomness = parseFloat(config.get("p.widthRandomness"));
    heightRandomness = parseFloat(config.get("p.heightRandomness"));

    buildPatterns();
}

void buildPatterns() {
    // Make an ArrayList
    parts = new ArrayList<Part>();
    deltaFactor = 1.0;
    int baseSize = parseInt(config.get("p.baseSize"));
    int baseHeight = parseInt(config.get("p.baseHeight"));
    int stagger = parseInt(config.get("p.stagger"));
    int staggerAmount = 0;

    int numberOfRows = int(animationCanvasheight/baseHeight) - rowsLeftOff + 1;
    int numberOfCols = int(animationCanvaswidth/baseSize);

    println("Number of rows:", numberOfRows);
    println("Number of cols:", numberOfCols);

    if (motionType == 1) {
        numberOfCols = int(numberOfParts/2);
        numberOfRows = int(numberOfParts/2);
    }

    for (int col = 0; col < numberOfCols; col++) {
        for (int row = 0; row < numberOfRows; row++) {
            staggerAmount = 0;
            if (row % 2 > 0) staggerAmount = stagger;

            if (random(0, 1) < drawPartProbability) {
                //if (col%2 > 0 || staggerAmount == 0) {
                Part p = new Part(animationCanvas);  
                parts.add(p);
                p.motionType = motionType;
                p.orientationFlipProb = orientationFlipProb;
                p.baseSize = baseSize;

                p.centerX = centerX;
                p.centerY = centerY;

                p.xOffCanvasBuffer = xOffCanvasBuffer;
                p.yOffCanvasBuffer = yOffCanvasBuffer;

                if (random(0, 1) > .5 && motionType ==1 && multipleOrigins == true) {
                    p.centerX = canvaswidth + xOffCanvasBuffer - 1;
                }
                if (random(0, 1) > .5 && motionType ==1 && multipleOrigins == true) {
                    p.centerY = centerY + random(0, canvasheight);
                }

                p.baseSize = int(random(baseSize, baseSize + widthRandomness * baseSize));
                p.baseHeight = int(random(baseHeight, baseHeight + heightRandomness * baseHeight));
                p.speedRangeMin = parseFloat(config.get("p.speedRangeMin"));
                p.speedRange = parseFloat(config.get("p.speedRange"));
                p.canvaswidth = animationCanvaswidth;
                p.canvasheight = animationCanvasheight;
                p.driftToCenter = driftToCenter;
                p.deltaFactor = deltaFactor;
                p.rotationRange = parseFloat(config.get("p.rotationRange"));
                p.xOffset = xOffset;
                p.yOffset = yOffset;
                p.doRotate = parseBoolean(config.get("p.doRotate"));
                p.doDrift = parseBoolean(config.get("p.doDrift"));
                p.doAlternateDirection = parseBoolean(config.get("p.doAlternateDirection"));
                p.distanceFromCenterThreshold = parseFloat(config.get("p.distanceFromCenterThreshold"));
                p.uniformColor = uniformColor;
                p.fixedRotation =   random(-PI,PI);


                if (uniformColor == false) {
                    p.ct = new ColorTransition();
                    p.ct.partColors_hsv = partColors_hsv;
                    p.ct.alpha = int(partColors_hsv[6]);
                    p.ct.brightness = brightness;
                    p.ct.doNewTansition = true;
                    p.ct.steps = 10;
                    p.ct.rndStepMin = 500;
                    p.ct.rndStepMax = 900;
                    p.ct.setupColorTransition();
                } else {
                    p.ct = allPartsct;
                }

                p.strokeColor = new ColorTransition();
                p.strokeColor.alpha = int(partStrokeColors_hsv[6]);
                p.strokeColor.brightness = brightness;
                p.strokeColor.partColors_hsv = partStrokeColors_hsv;
                p.strokeColor.steps = 10;
                p.strokeColor.startColor = color(0, 0, 200, 1);
                p.strokeColor.endColor = color(200, 0, 0, 1 );
                p.strokeColor.doNewTansition = true;
                p.strokeColor.setupColorTransition();


                if (random(0, 1) <= randomColorProb) {
                    p.ct.partColors_hsv = rndclrs_hsv;
                }


                // DEBUG

                /*
                 if (row == 0) {
                 p.ct.startColor = color(0, 255, 0, 255);
                 p.ct.endColor = color(0, 255, 0, 255);
                 p.ct.doNewTansition = false;
                 p.ct.setupColorTransition();
                 }
                 
                 if (row == 1) {
                 p.ct.startColor = color(255, 0, 255, 255);
                 p.ct.endColor = color(255, 0, 255, 255);
                 p.ct.doNewTansition = false;
                 p.ct.setupColorTransition();
                 }
                 
                 if (row >= numberOfRows-1) {
                 p.ct.startColor = color(255, 0, 0, 255);
                 p.ct.endColor = color(255, 0, 0, 255);
                 p.ct.doNewTansition = false;
                 p.ct.setupColorTransition();
                 }
                 */


                p.setUp();

                p.x = col * p.baseSize + hDistance * col - staggerAmount;
                p.y = row * (p.baseHeight + vDistance);

                numberOfParts += 1;
                //}
            }
        }
    }


    println("numberOfParts: ", numberOfParts);

    for (int i = 0; i < numberOfParts; i++) {
        //smooth(1);
    }

    // THIS IS THE BACKGROUND COLOR CONTROLLER
    ct = new ColorTransition();
    ct.startColor = color(0, 0, 0, bgAlpha);
    ct.endColor = color(0, 0, 0, bgAlpha);
    ct.partColors_hsv = bgcolors_hsv;
    ct.doNewTansition = true;
    ct.alpha = bgAlpha;
    ct.brightness = bgbrightness;
    ct.steps = 10;
    ct.rndStepMin = 300;
    ct.rndStepMax = 900;
    ct.setupColorTransition();
}


void draw() {

    color fixedBgColor = color(10, 0, 100, 100);

    ct.transitionStep();
    background(ct.currentColor);
    //background(fixedBgColor);

    if (!moved) { 
        surface.setLocation(windowXPos, windowYPos);
        moved = true;
    }

    if (random(0, 100) > 99.0) {

        //deltaFactor += deltaDirection;

        if (random(0, 100) > 99.0) {
            //deltaFactor = -random(.5, 2);
        }

        if (deltaFactor > 2 || deltaFactor < 0.0) {
            //deltaDirection *= -1;
        }
    }

    animationCanvas.beginDraw();
    animationCanvas.noStroke();
    animationCanvas.fill(ct.currentColor);
    //animationCanvas.fill(fixedBgColor);
    animationCanvas.rect(0, 0, animationCanvaswidth, animationCanvasheight);


    if (uniformColor == true) {
        allPartsct.transitionStep();
    }


    for (Part p : parts) {
        p.display();
        p.move();
        p.driftToCenter = driftToCenter;
        p.deltaFactor = deltaFactor;

        if (uniformColor == false) {
            p.ct.transitionStep();
        }
        p.strokeColor.transitionStep();
    }

    animationCanvas.endDraw();
    animationCanvas.updatePixels();

    PImage render = ditherer.dither(animationCanvas.copy());

    //ditherLevels += .02;
    //ditherer.levels = round(ditherLevels);

    if (ditherer.levels > 16) {
        //ditherer.levels = 1;
        //ditherLevels = 2;
    }

    PImage crop0 = render.get(0, 0, animationCanvaswidth, animationCanvasheight);
    PImage crop1 = render.get(0, canvasheight * 0, animationCanvaswidth, canvasheight);
    PImage crop2 = render.get(0, canvasheight * 1, animationCanvaswidth, canvasheight );
    PImage crop3 = render.get(0, canvasheight * 2, animationCanvaswidth, canvasheight );
    PImage crop4 = render.get(0, canvasheight * 3, animationCanvaswidth, canvasheight );
    PImage crop5 = render.get(0, canvasheight * 4, animationCanvaswidth, canvasheight );
    PImage crop6 = render.get(0, canvasheight * 5, animationCanvaswidth, canvasheight );
    PImage cropDisturb = render.get(0, canvasheight * 5, animationCanvaswidth, 128 );

    if (canvasRotation != 0.0) {
        //pushMatrix();
        //translate(0,0);
        scale(-1.0, 1.0);
        rotate(canvasRotation/180.0 * PI);
        //popMatrix();
    }

    if (cutups == 0) {

        crop0.blend(realImage, 30, 0, 95, 245, 0, 0, 95, 245, ADD); 
        //crop0.blend(realImage, 0, 0, 35, 35, 0, 0, 35, 35, ADD); 

        image(ditherer.dither(crop0), 0, 0);

        if (useImageSprites) { 
            tint(100, 128);
            for (Part p : parts) {
                pushMatrix();
                translate(int(p.x),int(p.y));
                rotate(p.fixedRotation);
                image(p.unitImage, 0, 0 );
                popMatrix();
                g.removeCache(p.unitImage);
            }
            noTint();
        }

        g.removeCache(crop0);
    }


    if (cutups > 0) {

        crop1.blend(realImage, 30, 0, 89, 241, 0, 0, 89, 241, ADD); 

        if (useImageSprites) { 
            for (Part p : parts) {
                pushMatrix();
                translate(int(p.x),int(p.y));
                rotate(p.fixedRotation);
                tint(255, 126);
                image(p.unitImage, 0, 0 );
                popMatrix();
            }
        }

        image(ditherer.dither(crop1), 0, 0);
        g.removeCache(crop1);

        image(ditherer.dither(crop2), animationCanvaswidth*2, 0);
        g.removeCache(crop2); 

        pushMatrix();
        translate(animationCanvaswidth * 5, canvasheight);
        rotate(-HALF_PI*2);
        image(ditherer.dither(crop3), animationCanvaswidth*1, 0);
        g.removeCache(crop3); 
        popMatrix();

        pushMatrix();
        translate(animationCanvaswidth * 5, canvasheight);
        rotate(-HALF_PI*2);
        image(ditherer.dither(crop4), animationCanvaswidth*3, 0);
        g.removeCache(crop4);
        popMatrix();
    }



    if (doDrawGrid) {
        //gridLineColor = ct.currentColor;
        drawGrid();
    }
}
