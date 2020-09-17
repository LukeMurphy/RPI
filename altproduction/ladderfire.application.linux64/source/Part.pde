// A class to describe a Polygon (with a PShape)

class Part {

    PGraphics pg;
    PShape s;
    float x, y;
    float speed;
    float speedRangeMin = .5;
    float speedRange = 5.0;
    float rotationSpeed;
    float rotation = 0.0;
    float fixedRotation = 0.0;
    float rotationRange = .01;
    float deltaFactor = 1.0;

    float angle = 0.0;
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
    float distanceFromCenterThreshold = 25.0;

    boolean uniformColor = false;
    boolean contracting = true;
    boolean doAlternateDirection = false;

    ColorTransition ct;
    ColorTransition ctbg;
    ColorTransition strokeColor;


    boolean colorChanged = false;

    float centerX = 0.0;
    float centerY = 0.0;

    PImage unitImage;
    PImage unitDisplayImage;


    Part(PGraphics _pg) {
        pg = _pg;
    }


    void setUp() {


        speed = random(speedRangeMin, speedRange);

        if (random(0, 1) > .5 && doAlternateDirection == true) {
            speed *= -1.0;
        }
        rotationSpeed = random(-rotationRange, rotationRange);
        int selection = int(random(3)); 

        selection = 1;
        makeSquare();

        imageSprite();



        if (motionType == 1) {

            angle = random(0, TWO_PI);
            rotation = angle;

            if (random(0, 1) > orientationFlipProb) {
                orientationAngle = HALF_PI;
            } else {
                orientationAngle = 0.0;
            }
        }
    }


    void imageSprite() {
        if(random(0,1) > .85) {
            if(random(0,1) > .5) {
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



    void makeSquare() {
        s = createShape(RECT, 0, 0, baseHeight, baseSize);
        s.setFill(ct.currentColor);
        s.setStroke(strokeColor.currentColor);
        polygonType = 1;
    }



    void radialMotion() {
        float delta = (canvaswidth/2 - x);
        float drift = delta/driftToCenter * deltaFactor;


        // segment length
        // point 1 is origin

        x = centerX + radialPosition * cos(angle);
        y = centerY + radialPosition * sin(angle);

        radialPosition += speed;


        if (y > canvasheight + yOffCanvasBuffer || y < 0.0 - yOffCanvasBuffer || x > canvaswidth + xOffCanvasBuffer || x < 0 - xOffCanvasBuffer) {
            y = centerY;
            x = centerX;
            radialPosition = 0.0;

            // I could also reset the angle, size etc
            // but by not doing it, it gives a more repetitive feel
            // as if the whole thing is some king of gif loop


            //setUp();
            //angle = random(0, TWO_PI);
            //rotation = angle;
            //speed = random(speedRangeMin, speedRange);
        }
    }

    void linearMotion() {
        float delta = (canvaswidth/2 - x);
        float drift = delta/driftToCenter * deltaFactor;

        if (abs(delta) < .55) {
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
    void move() {
        if (motionType == 0) {
            linearMotion();
        } else if (motionType == 1) {
            radialMotion();
        }
    }


    // Draw the object
    void display() {

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
