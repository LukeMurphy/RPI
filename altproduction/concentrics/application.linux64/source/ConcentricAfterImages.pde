//------------------------------//

PShader Scrunchie;
boolean frameMoved = false;
int setupSet = 1;

//------------------------------//
String mode = "run";

PFont f;
int rows = 4;
int cols = 4;

int cellWidth = 64;
int cellHeight = 32;

//------------------------------//
void setup() {
  size(340, 340, P2D);
  noStroke();

  f = createFont("SourceCodePro-Regular.ttf", 12);
  textFont(f);

  if (mode == "diagnostics" ) {
    rows = floor(height/cellHeight) + 1;
    cols = floor(width/cellWidth) + 1;
  } else {
    Scrunchie = loadShader("basic.glsl");
    Scrunchie.set("resolution", float(width), float(height));   
    //Scrunchie.set("lineScale", 10.0);

    Scrunchie.set("rTimeMult", 2.0);
    Scrunchie.set("gTimeMult", 20.0);
    Scrunchie.set("bTimeMult", 2.0);

    Scrunchie.set("distortionScale", .52);
    Scrunchie.set("brightness", .65);
  }
}

void draw() {
  background(10, 0, 10);

  if (mode  == "diagnostics") {
    fill(10, 0, 10);
    rect(0, 0, width, height);

    for (int r=0; r<rows; r++) {
      stroke(0, 100, 10);
      line(0, r*cellHeight, width, r*cellHeight);

      for (int c=0; c<cols; c++) {
        stroke(0, 100, 100);
        line(c*cellWidth, 0, c*cellWidth, height);
        fill(200, 0, 0);
        text((str(c*cellWidth) + " " + str((r-1)*cellHeight)), c*cellWidth + 5, r*cellHeight - 15);
        noStroke();
        fill(0, 0, 250);
        ellipse(c*cellWidth + 5, r*cellHeight - 27, 4, 4);
      }
    }
  } else {
    background(20, 0, 170);
    Scrunchie.set("time", millis() / 1000.0);
    shader(Scrunchie);  
    //rect(0, 0, 250, 320); 
    if (setupSet == 1 ) {
      if (!frameMoved) {
        surface.setLocation(100, 100);
        frameMoved = true;
      }
      rect(0, 0, 248, 200);
      rect(248, 120, 24, 24);
    }

    if (setupSet == 2) {
      if (!frameMoved) {
        surface.setLocation(2580, 120);
        frameMoved = true;
      }
      rect(40, 10, 260, 220);
    }
  }
}
