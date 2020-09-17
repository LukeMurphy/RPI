import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class Player extends PApplet {

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

float canvasRotation = 0.0f;

float brightness = 1.0f;
float bgbrightness = 1.0f;

float driftToCenter = 1000;
float deltaFactor = 1.0f;
float deltaDirection = .1f;
float drawPartProbability = 1.0f;
float orientationFlipProb = 0.0f;


float widthRandomness = 0.0f;
float heightRandomness = 0.0f;

int xOffset = 0;
int yOffset = 0;

int numberOfParts = 0;

// 0 is linear, 1 is radial
int motionType = 0;
int xOffCanvasBuffer = 0;
int yOffCanvasBuffer = 0;

ArrayList<Part> parts;
Dither ditherer;
float ditherLevels = 1.0f;

int vDistance = 1;
int hDistance = 1;
int rowsLeftOff = 0;

float changeColorProb = 0.0f;
float randomColorProb = 0.0f;
boolean doDrawGrid = false;
int gridLineColor;
int gridTextColor;

float[] bgcolors_hsv;
float[] gridLineColors_hsv;
float[] gridTextColors_hsv;
float[] partColors_hsv;
float[] fixedColors_hsv;
float[] partStrokeColors_hsv;
float[] rndclrs_hsv = {0.0f, 360.0f, 0.0f, 255.0f, 0.0f, 255.0f, 20.0f};


int bgcolor;
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


public void settings() {

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


public void setup() {
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
        allPartsct.alpha = PApplet.parseInt(fixedColors_hsv[6]);
        allPartsct.brightness = bgbrightness;
        allPartsct.startColor = color(0, 0, 200, PApplet.parseInt(fixedColors_hsv[6]));
        allPartsct.endColor = color(200, 0, 0, PApplet.parseInt(fixedColors_hsv[6]));

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

public void buildPatterns() {
    // Make an ArrayList
    parts = new ArrayList<Part>();
    deltaFactor = 1.0f;
    int baseSize = parseInt(config.get("p.baseSize"));
    int baseHeight = parseInt(config.get("p.baseHeight"));
    int stagger = parseInt(config.get("p.stagger"));
    int staggerAmount = 0;

    int numberOfRows = PApplet.parseInt(animationCanvasheight/baseHeight) - rowsLeftOff + 1;
    int numberOfCols = PApplet.parseInt(animationCanvaswidth/baseSize);

    println("Number of rows:", numberOfRows);
    println("Number of cols:", numberOfCols);

    if (motionType == 1) {
        numberOfCols = PApplet.parseInt(numberOfParts/2);
        numberOfRows = PApplet.parseInt(numberOfParts/2);
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

                if (random(0, 1) > .5f && motionType ==1 && multipleOrigins == true) {
                    p.centerX = canvaswidth + xOffCanvasBuffer - 1;
                }
                if (random(0, 1) > .5f && motionType ==1 && multipleOrigins == true) {
                    p.centerY = centerY + random(0, canvasheight);
                }

                p.baseSize = PApplet.parseInt(random(baseSize, baseSize + widthRandomness * baseSize));
                p.baseHeight = PApplet.parseInt(random(baseHeight, baseHeight + heightRandomness * baseHeight));
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
                    p.ct.alpha = PApplet.parseInt(partColors_hsv[6]);
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
                p.strokeColor.alpha = PApplet.parseInt(partStrokeColors_hsv[6]);
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


public void draw() {

    int fixedBgColor = color(10, 0, 100, 100);

    ct.transitionStep();
    background(ct.currentColor);
    //background(fixedBgColor);

    if (!moved) { 
        surface.setLocation(windowXPos, windowYPos);
        moved = true;
    }

    if (random(0, 100) > 99.0f) {

        //deltaFactor += deltaDirection;

        if (random(0, 100) > 99.0f) {
            //deltaFactor = -random(.5, 2);
        }

        if (deltaFactor > 2 || deltaFactor < 0.0f) {
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

    if (canvasRotation != 0.0f) {
        //pushMatrix();
        //translate(0,0);
        scale(-1.0f, 1.0f);
        rotate(canvasRotation/180.0f * PI);
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
                translate(PApplet.parseInt(p.x),PApplet.parseInt(p.y));
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
                translate(PApplet.parseInt(p.x),PApplet.parseInt(p.y));
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
class ColorTransition {

    int startColor;
    int endColor;
    int currentColor;
    int steps = 100;
    float stepCount = 0.0f;
    float hDiff;
    float sDiff;
    float rDiff;
    float gDiff;
    float bDiff;
    float aDiff;

    FloatList startClrs;
    FloatList endClrs;
    FloatList currentClrs;

    boolean transitionDone = false;
    boolean doNewTansition = false;

    float brightness = 1.0f;
    int alpha = 0;
    int rndStepMin = 10;
    int rndStepMax = 100;



    float[] partColors_hsv;


    ColorTransition() {
        //print("ColorTransition Init");
    }


    public FloatList getColorArray(int clr) {

        int a = (clr >> 24) & 0xFF;
        int r = (clr >> 16) & 0xFF;
        int g = (clr >> 8) & 0xFF;
        int b = clr & 0xFF;

        FloatList l = new FloatList();
        l.append(PApplet.parseFloat(r));
        l.append(PApplet.parseFloat(g));
        l.append(PApplet.parseFloat(b));
        l.append(PApplet.parseFloat(a));

        return l;
    }


    public void setupColorTransition() {

        startClrs = 	getColorArray(startColor);
        endClrs = 		getColorArray(endColor);
        currentColor = 	startColor;
        currentClrs = 	getColorArray(currentColor);

        rDiff =  -(startClrs.get(0))/steps + (endClrs.get(0))/steps;
        gDiff =  -(startClrs.get(1))/steps + (endClrs.get(1))/steps;
        bDiff =  -(startClrs.get(2))/steps + (endClrs.get(2))/steps;
        aDiff =  -(startClrs.get(3))/steps + (endClrs.get(3))/steps;

        transitionDone = false;
        stepCount = 0.0f;

        //println(currentClrs);
    }



    public void transitionStep() {

        if (transitionDone == false ) {

            stepCount +=1;
            currentClrs.set(0, startClrs.get(0) + stepCount * rDiff);
            currentClrs.set(1, startClrs.get(1) + stepCount * gDiff);
            currentClrs.set(2, startClrs.get(2) + stepCount * bDiff);
            currentClrs.set(3, startClrs.get(3) + stepCount * aDiff);

            currentColor = color(
                PApplet.parseInt(currentClrs.get(0)), 
                PApplet.parseInt(currentClrs.get(1)), 
                PApplet.parseInt(currentClrs.get(2)), 
                PApplet.parseInt(currentClrs.get(3))   );

            if (stepCount > steps) {
                transitionDone = true;
                //endColor = randomRGBA(true);
                //startColor = currentColor;
                //setupColorTransition();
            }
        }

        if (transitionDone == true && doNewTansition == true) {
            startColor = currentColor;
            endColor = randomHSBA(partColors_hsv, alpha, brightness);
            steps = PApplet.parseInt(random(rndStepMin,rndStepMax));
            setupColorTransition() ;
            //println("new tansition",partColors_hsv, alpha, brightness );
        }
    }
}
class Dither {

    int levels = 1;
    int x0 = 1;
    int x1 = 1;
    int y0 = 1;
    int y1 = 1;

public void Dither() {

}

public PImage dither(PImage source) {
    float lNorm = 255.f/levels;

    // FS Kernal
    float d1 = 7.f / 16.f;
    float d2 = 3.f / 16.f;
    float d3 = 5.f / 16.f;
    float d4 = 1.f / 16.f;

    int c, nc, lc, rc;
    float r, g, b;
    float nr, ng, nb;
    float er, eg, eb;
    float lr, lg, lb;
    int x = 0, y = 0;

    // Ordered Dithering Implementation
    for (y = y0; y < y1; y++) {
        for (x = x0; x <= x1; x++) {
            // Retrieve current RGB value
            c = source.get(x, y);
            r = (c >> 16) & 0xFF;
            g = (c >> 8) & 0xFF;
            b = c & 0xFF;

            // Normalize and scale to number of levels
            // basically a cheap but crappy form of color quantization
            nr = round((r/255) * levels) * lNorm;
            ng = round((g/255) * levels) * lNorm;
            nb = round((b/255) * levels) * lNorm;

            // Set the current pixel
            nc = color(nr, ng, nb);
            source.set(x, y, nc);

            // Quantization Error
            er = r-nr;
            eg = g-ng;
            eb = b-nb;

            // Apply the kernel
            // +1, 0
            lc = source.get(x + 1, y);
            lr = (lc >> 16 & 0xFF) + d1 * er;
            lg = (lc >> 8 & 0xFF) + d1 * eg;
            lb = (lc & 0xFF) + d1 * eb;
            source.set(x + 1, y, color(lr, lg, lb));

            // -1, +1
            lc = source.get(x - 1, y + 1);
            lr = (lc >> 16 & 0xFF) + (d2*er);
            lg = (lc >> 8 & 0xFF) + (d2*eg);
            lb = (lc & 0xFF) + (d2*eb);
            source.set(x - 1, y + 1, color(lr, lg, lb));

            // 0, +1
            lc = source.get(x, y + 1);
            lr = (lc >> 16 & 0xFF) + (d3*er);
            lg = (lc >> 8 & 0xFF) + (d3*eg);
            lb = (lc & 0xFF) + (d3*eb);
            source.set(x, y + 1, color(lr, lg, lb));

            // +1, +1
            lc = source.get(x+1, y+1);
            lr = (lc >> 16 & 0xFF) + (d4*er);
            lg = (lc >> 8 & 0xFF) + (d4*eg);
            lb = (lc & 0xFF) + (d4*eb);
            source.set(x+1, y+1, color(lr, lg, lb));
        }
    }
     return source;
}
}
// A class to describe a Polygon (with a PShape)

class Part {

    PGraphics pg;
    PShape s;
    float x, y;
    float speed;
    float speedRangeMin = .5f;
    float speedRange = 5.0f;
    float rotationSpeed;
    float rotation = 0.0f;
    float fixedRotation = 0.0f;
    float rotationRange = .01f;
    float deltaFactor = 1.0f;

    float angle = 0.0f;
    int motionType = 0;

    int polygonType;
    int baseSize = 20;
    int baseHeight = 20;
    int height = 20;
    float radialPosition = 0;
    float orientationAngle = 0;
    float orientationFlipProb = 0;

    int xOffset = 30;
    int yOffset = 30;

    boolean doRotate = true;
    boolean doDrift = true;
    boolean randomX = true;

    int canvaswidth = 192;
    int canvasheight = 256;

    int xOffCanvasBuffer = 0;
    int yOffCanvasBuffer = 0;

    float driftToCenter = 1000;
    float distanceFromCenterThreshold = 25.0f;

    boolean uniformColor = false;
    boolean contracting = true;
    boolean doAlternateDirection = false;

    ColorTransition ct;
    ColorTransition ctbg;
    ColorTransition strokeColor;


    boolean colorChanged = false;

    float centerX = 0.0f;
    float centerY = 0.0f;

    PImage unitImage;
    PImage unitDisplayImage;


    Part(PGraphics _pg) {
        pg = _pg;
    }


    public void setUp() {


        speed = random(speedRangeMin, speedRange);

        if (random(0, 1) > .5f && doAlternateDirection == true) {
            speed *= -1.0f;
        }
        rotationSpeed = random(-rotationRange, rotationRange);
        int selection = PApplet.parseInt(random(3)); 

        selection = 1;
        makeSquare();

        imageSprite();



        if (motionType == 1) {

            angle = random(0, TWO_PI);
            rotation = angle;

            if (random(0, 1) > orientationFlipProb) {
                orientationAngle = HALF_PI;
            } else {
                orientationAngle = 0.0f;
            }
        }
    }


    public void imageSprite() {
        if(random(0,1) > .85f) {
            if(random(0,1) > .5f) {
                unitDisplayImage = loadImage("gun-23.png");
            } else {
                unitDisplayImage = loadImage("shell-in.png");

            }
        } else {
            unitDisplayImage = loadImage("smaller-blank.png");   

        }
        unitImage = unitDisplayImage.copy();
        int newSize = round(random(5,40));
        unitImage.resize(newSize,newSize);
    }



    public void makeSquare() {
        s = createShape(RECT, 0, 0, baseHeight, baseSize);
        s.setFill(ct.currentColor);
        s.setStroke(strokeColor.currentColor);
        polygonType = 1;
    }



    public void radialMotion() {
        float delta = (canvaswidth/2 - x);
        float drift = delta/driftToCenter * deltaFactor;


        // segment length
        // point 1 is origin

        x = centerX + radialPosition * cos(angle);
        y = centerY + radialPosition * sin(angle);

        radialPosition += speed;


        if (y > canvasheight + yOffCanvasBuffer || y < 0.0f - yOffCanvasBuffer || x > canvaswidth + xOffCanvasBuffer || x < 0 - xOffCanvasBuffer) {
            y = centerY;
            x = centerX;
            radialPosition = 0.0f;

            // I could also reset the angle, size etc
            // but by not doing it, it gives a more repetitive feel
            // as if the whole thing is some king of gif loop


            //setUp();
            //angle = random(0, TWO_PI);
            //rotation = angle;
            //speed = random(speedRangeMin, speedRange);
        }
    }

    public void linearMotion() {
        float delta = (canvaswidth/2 - x);
        float drift = delta/driftToCenter * deltaFactor;

        if (abs(delta) < .55f) {
            //drift = 1/drift;
            contracting = false;
        }

        y+=speed;

        if (doRotate) {
            rotation += rotationSpeed;
        }

        if (doDrift) {
            if (contracting == true) {
                x += drift;
            } else {
                x -= drift;
            }
        }

        if (speed > 0 && y > canvasheight ) {
            y = -baseHeight;
        }


        if (speed < 0 && y < -baseHeight ) {
            y = canvasheight + baseHeight;
        }

        if (x > canvaswidth  || x < 0 -baseSize) {
            contracting = true;
        }
    }

    // Simple motion
    public void move() {
        if (motionType == 0) {
            linearMotion();
        } else if (motionType == 1) {
            radialMotion();
        }
    }


    // Draw the object
    public void display() {

        pg.pushMatrix();
        pg.translate(x + xOffset, y + yOffset);
        pg.translate(baseSize/2, baseHeight/2);
        pg.rotate(rotation + orientationAngle);
        pg.translate(-baseSize/2, -baseHeight/2);

        pg.noStroke();
        //pg.stroke(strokeColor.currentColor);
        pg.fill(ct.currentColor);
        pg.rect(0, 0, baseSize, baseHeight);

        //s.setFill(ct.currentColor);
        //shape(s);
        pg.popMatrix();
    }
}
public void drawGrid() {
    stroke(gridLineColor);

    int panelWidth = 64;
    int panelHeight = 32;

    textAlign(LEFT);
    fill(gridTextColor);
    for (int x =0; x < 10; x ++) {

        line(x * panelWidth, 0, x*panelWidth, height );
        line(x * panelWidth -1, 0, x*panelWidth -1, height );

        for (int y = 0; y < 10; y ++) {
            line(0, y*panelHeight, width, y*panelHeight );
            line(0, y*panelHeight-1, width, y*panelHeight-1 );

            int xn = x * panelWidth;
            int yn = y * panelHeight;

            if (x > 0) {
                xn += 1;
            }

            if (y > 1) {
                yn += 0;
            }         

            String str = nf(xn) +  "x" + nf(yn);

            text(str, x * panelWidth + 2, y*panelHeight -2);
        }
    }
    fill(0, 0, 0, 0);
}

public int ParseColorString(String[] colorStr) {
    int[] colorVals = new int[4];
    int i = 0;
    for (String c : colorStr) {
        colorVals[i] = (parseInt(trim(c)));
        i++;
    }
    return color(colorVals[0], colorVals[1], colorVals[2], colorVals[3]);
}

public float[] ParseColorStringHSV(String[] colorStr) {
    float[] colorVals = new float[7];
    int i = 0;
    for (String c : colorStr) {
        colorVals[i] = (parseFloat(trim(c)));
        i++;
    }
    return colorVals;
}

public int randomHSBA(float[] ranges, float alpha, float brightness) {
    float hMin = ranges[0];
    float hMax = ranges[1];
    float sMin = ranges[2];
    float sMax = ranges[3];
    float vMin = ranges[4];
    float vMax = ranges[5];
    float h = random(hMin, hMax);
    float s = random(sMin, sMax);
    float v = random(vMin * brightness, vMax * brightness);
    float a = random(0, 255);

    if (alpha != -1) a = alpha; 

    int clr = HSVToRGB(h, s, v, a);
    return clr;
}


public int randomRGBA(boolean gs, int alpha, float brightness) {
    int r = PApplet.parseInt(random(0, 255) * brightness);
    int g = PApplet.parseInt(random(0, 255) * brightness);
    int b = PApplet.parseInt(random(0, 255) * brightness);
    int a = PApplet.parseInt(random(10, 255));

    if (alpha != -1) a = alpha;

    if (gs) g=b=r;

    int clr = color(r, g, b, a);
    return clr;
}



public int HSVToRGB(float h, float s, float v, float a) {

    float c = v * s / 255.0f;
    float huex = h / 60.0f;
    float x = c * (1 - abs(huex % 2 - 1));


    float r1 = 0;
    float g1 = 0;
    float b1 = 0;

    if (huex <= 1 && huex >= 0) {
        r1 = c;
        g1 = x;
        b1 = 0;
    }
    if (huex <= 2 && huex >= 1) {
        r1 = x;
        g1 = c;
        b1 = 0;
    }
    if (huex <= 3 && huex >= 2) {
        r1 = 0;
        g1 = c;
        b1 = x;
    }
    if (huex <= 4 && huex >= 3) {
        r1 = 0;
        g1 = x;
        b1 = c;
    }
    if (huex <= 5 && huex >= 4) {
        r1 = x;
        g1 = 0;
        b1 = c;
    }
    if (huex <= 6 && huex >= 5) {
        r1 = c;
        g1 = 0;
        b1 = x;
    }
    float m = v - c;
    float red = r1 + m;
    float green  =  g1 + m;
    float blue = b1 + m;



    //println(huex, c, x);
    //println(round(red), round(green), round(blue), round(a));

    return color(round(red), round(green), round(blue), round(a));
}

public StringDict ConfigParse(String configFile) {

    StringDict config = new StringDict();
    /* CONFIG LOAD AND PARSE */
    String[] properties = loadStrings(configFile);
    for (String p : properties) {
        String prop, val;
        //println(p);
        

        // Setting up a rudimentary config parser
        Boolean ignoreLine = false;
        if(p.indexOf("---") == 0 || p.indexOf("#") == 0) {
            ignoreLine = true;
        }


        if (p.length()>1 && ignoreLine == false) {
            String[] line = p.split("=");
            prop = trim(line[0]);
            val = trim(line[1]);
            config.set(prop, val);
        }
    }

    return config;
}
    static public void main(String[] passedArgs) {
        String[] appletArgs = new String[] { "Player" };
        if (passedArgs != null) {
          PApplet.main(concat(appletArgs, passedArgs));
        } else {
          PApplet.main(appletArgs);
        }
    }
}
