class ColorTransition {

    color startColor;
    color endColor;
    color currentColor;
    int steps = 100;
    float stepCount = 0.0;
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

    float brightness = 1.0;
    int alpha = 0;
    int rndStepMin = 10;
    int rndStepMax = 100;



    float[] partColors_hsv;


    ColorTransition() {
        //print("ColorTransition Init");
    }


    FloatList getColorArray(color clr) {

        int a = (clr >> 24) & 0xFF;
        int r = (clr >> 16) & 0xFF;
        int g = (clr >> 8) & 0xFF;
        int b = clr & 0xFF;

        FloatList l = new FloatList();
        l.append(float(r));
        l.append(float(g));
        l.append(float(b));
        l.append(float(a));

        return l;
    }


    void setupColorTransition() {

        startClrs = 	getColorArray(startColor);
        endClrs = 		getColorArray(endColor);
        currentColor = 	startColor;
        currentClrs = 	getColorArray(currentColor);

        rDiff =  -(startClrs.get(0))/steps + (endClrs.get(0))/steps;
        gDiff =  -(startClrs.get(1))/steps + (endClrs.get(1))/steps;
        bDiff =  -(startClrs.get(2))/steps + (endClrs.get(2))/steps;
        aDiff =  -(startClrs.get(3))/steps + (endClrs.get(3))/steps;

        transitionDone = false;
        stepCount = 0.0;

        //println(currentClrs);
    }



    void transitionStep() {

        if (transitionDone == false ) {

            stepCount +=1;
            currentClrs.set(0, startClrs.get(0) + stepCount * rDiff);
            currentClrs.set(1, startClrs.get(1) + stepCount * gDiff);
            currentClrs.set(2, startClrs.get(2) + stepCount * bDiff);
            currentClrs.set(3, startClrs.get(3) + stepCount * aDiff);

            currentColor = color(
                int(currentClrs.get(0)), 
                int(currentClrs.get(1)), 
                int(currentClrs.get(2)), 
                int(currentClrs.get(3))   );

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
            steps = int(random(rndStepMin,rndStepMax));
            setupColorTransition() ;
            //println("new tansition",partColors_hsv, alpha, brightness );
        }
    }
}
