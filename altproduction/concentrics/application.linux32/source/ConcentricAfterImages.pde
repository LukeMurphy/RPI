
PShader Scrunchie;

void setup() {
  size(340, 340, P2D);
  noStroke();
 
  Scrunchie = loadShader("basic.glsl");
  Scrunchie.set("resolution", float(width), float(height));   
  Scrunchie.set("lineScale", 10.0);
  
  Scrunchie.set("rTimeMult", 2.0);
  Scrunchie.set("gTimeMult", 20.0);
  Scrunchie.set("bTimeMult", 2.0);
  
  Scrunchie.set("distortionScale", .52);
  Scrunchie.set("brightness", .65);
}

void draw() {
  background(10,0,100);
  Scrunchie.set("time", millis() / 1000.0);
  shader(Scrunchie);  
  //rect(0, 0, 250, 320); 
 
  rect(0,0,248,200);
  
  rect(248,120,24,24);

}
