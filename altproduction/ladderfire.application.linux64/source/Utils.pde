void drawGrid() {
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

color ParseColorString(String[] colorStr) {
    int[] colorVals = new int[4];
    int i = 0;
    for (String c : colorStr) {
        colorVals[i] = (parseInt(trim(c)));
        i++;
    }
    return color(colorVals[0], colorVals[1], colorVals[2], colorVals[3]);
}

float[] ParseColorStringHSV(String[] colorStr) {
    float[] colorVals = new float[7];
    int i = 0;
    for (String c : colorStr) {
        colorVals[i] = (parseFloat(trim(c)));
        i++;
    }
    return colorVals;
}

color randomHSBA(float[] ranges, float alpha, float brightness) {
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

    color clr = HSVToRGB(h, s, v, a);
    return clr;
}


color randomRGBA(boolean gs, int alpha, float brightness) {
    int r = int(random(0, 255) * brightness);
    int g = int(random(0, 255) * brightness);
    int b = int(random(0, 255) * brightness);
    int a = int(random(10, 255));

    if (alpha != -1) a = alpha;

    if (gs) g=b=r;

    color clr = color(r, g, b, a);
    return clr;
}



color HSVToRGB(float h, float s, float v, float a) {

    float c = v * s / 255.0;
    float huex = h / 60.0;
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

StringDict ConfigParse(String configFile) {

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
