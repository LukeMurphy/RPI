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

public class ConcentricAfterImages extends PApplet {

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
public void setup() {
  
  noStroke();

  f = createFont("SourceCodePro-Regular.ttf", 12);
  textFont(f);

  if (mode == "diagnostics" ) {
    rows = floor(height/cellHeight) + 1;
    cols = floor(width/cellWidth) + 1;
  } else {
    Scrunchie = loadShader("basic.glsl");
    Scrunchie.set("resolution", PApplet.parseFloat(width), PApplet.parseFloat(height));   
    //Scrunchie.set("lineScale", 10.0);

    Scrunchie.set("rTimeMult", 2.0f);
    Scrunchie.set("gTimeMult", 20.0f);
    Scrunchie.set("bTimeMult", 2.0f);

    Scrunchie.set("distortionScale", .52f);
    Scrunchie.set("brightness", .65f);
  }
}

public void draw() {
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

    Scrunchie.set("time", millis() / 1000.0f);
    shader(Scrunchie);  
    //rect(0, 0, 250, 320); 
    if (setupSet == 1 ) {
      if (!frameMoved) {
        surface.setLocation(40, 40);
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
  public void settings() {  size(340, 340, P2D); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "ConcentricAfterImages" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
