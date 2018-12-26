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


PShader Scrunchie;

public void setup() {
  
  noStroke();
 
  Scrunchie = loadShader("basic.glsl");
  Scrunchie.set("resolution", PApplet.parseFloat(width), PApplet.parseFloat(height));   
  Scrunchie.set("lineScale", 10.0f);
  
  Scrunchie.set("rTimeMult", 2.0f);
  Scrunchie.set("gTimeMult", 20.0f);
  Scrunchie.set("bTimeMult", 2.0f);
  
  Scrunchie.set("distortionScale", .52f);
  Scrunchie.set("brightness", .65f);
}

public void draw() {
  background(10,0,100);
  Scrunchie.set("time", millis() / 1000.0f);
  shader(Scrunchie);  
  //rect(0, 0, 250, 320); 
 
  rect(0,0,248,200);
  
  rect(248,120,24,24);

}
  public void settings() {  size(340, 340, P2D); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "--present", "--window-color=#666666", "--hide-stop", "ConcentricAfterImages" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
