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


PShader PsychShader;
PImage img;

boolean frameMoved = false;
boolean productionExport = true;

float xPos = 0;
float yPos = 0;
int numBlocks = 80;
Block[] blocks = new Block[numBlocks];

float rMax = 1.0f;
float gMax = 1.3f;
float bMax = 1.0f;

int bg = color(20, 0, 60, 1);

int blockHeight = 60;
int blockWidth = 60;
int blockPosRange = 32;
float xSpeed = .8f;


//------------------------------//
PFont f;
int rows = 4;
int cols = 4;

int cellWidth = 64;
int cellHeight = 32;
//------------------------------//

String mode = "run";
// 4 ==> tall thin tower
// 3 ==> arc
// 2 ==> allover / x pile
// 5 ==> radial with occlusion
// 0 ==> user(s)
// 6 ==> all
int setupSet = 2;

//------------------------------//
public void setup() {

	
	noStroke();

	img = loadImage("still-1.png");

	f = createFont("SourceCodePro-Regular.ttf", 12);
	textFont(f);

	if (mode == "diagnostics" ) {
		rows = floor(height/cellHeight) + 1;
		cols = floor(width/cellWidth) + 1;
	} else {
		// Set shader parameters
		PsychShader = loadShader("basic.glsl");
		PsychShader.set("resolution", PApplet.parseFloat(width), PApplet.parseFloat(height));	 
		//PsychShader.set("lineScale", 10.0);

		PsychShader.set("rTimeMult", 2.0f);
		PsychShader.set("gTimeMult", 10.0f);
		PsychShader.set("bTimeMult", 2.0f);
		PsychShader.set("distortionScale", .52f);
		PsychShader.set("brightness", .65f);
		PsychShader.set("tTimeMult", 1000.0f);
		PsychShader.set("shaderFunction", 0);
		PsychShader.set("positionX", 255);
		PsychShader.set("positionY", 180);

	// CORNER ROUND SQUARE
		if (setupSet == 2) {
			PsychShader.set("rTimeMult",5.02f);
			PsychShader.set("gTimeMult",5.0f);
			PsychShader.set("bTimeMult",2.010f);

			// This affects the tone but adding to or dropping
			// each rgb chanel
			PsychShader.set("rFactor", 1.10f);
			PsychShader.set("gFactor", 1.0f);
			PsychShader.set("bFactor", 1.0f);


			PsychShader.set("rMin", .010f);
			PsychShader.set("gMin", .05f);
			PsychShader.set("bMin", .01f);

			PsychShader.set("distortionScale", .2f);
			PsychShader.set("brightness", .75f);
			PsychShader.set("tTimeMult", 1000.0f);
			PsychShader.set("shaderFunction", 0);
			PsychShader.set("positionX", 25);
			PsychShader.set("positionY", 180);
			bg = color(20, 0, 80, 1);

		}

		if (setupSet == 6) {
			PsychShader.set("positionX", 0);
			PsychShader.set("positionY", 0);
			PsychShader.set("rTimeMult", 5.0f);
			PsychShader.set("gTimeMult", 5.3f);
			PsychShader.set("bTimeMult", 1.5f);
			PsychShader.set("tTimeMult", 1000.0f);
			PsychShader.set("distortionScale", .1f);
			PsychShader.set("brightness", .85f);
			PsychShader.set("shaderFunction", 0);	
		}

		if (setupSet == -1) {
			PsychShader.set("rTimeMult", 5.0f);
			PsychShader.set("gTimeMult", 5.3f);
			PsychShader.set("bTimeMult", 1.5f);
			PsychShader.set("tTimeMult", 1000.0f);
			PsychShader.set("distortionScale", .1f);
			PsychShader.set("brightness", .85f);
			PsychShader.set("shaderFunction", 0);	
		}

		if (setupSet == 5) {
			PsychShader.set("rTimeMult", 50.0f);
			PsychShader.set("gTimeMult", 52.3f);
			PsychShader.set("bTimeMult", 155.5f);
			PsychShader.set("tTimeMult", 5000.0f);
			PsychShader.set("distortionScale", .001f);
			PsychShader.set("brightness", .85f);
			PsychShader.set("shaderFunction", 2);	
		}

		if (setupSet == 0) {
			PsychShader.set("rTimeMult", 50.0f);
			PsychShader.set("gTimeMult", 52.3f);
			PsychShader.set("bTimeMult", 155.5f);
			PsychShader.set("tTimeMult", 5000.0f);
			PsychShader.set("distortionScale", .001f);
			PsychShader.set("brightness", .85f);
			PsychShader.set("shaderFunction", 1);	
		}

		// P!0 tower 4 - slender
		if (setupSet == 4) {
			bg = color(50, 50, 60);
			//bg = color(120,120,30);
			rMax = 1.f;
			gMax = 1.f;
			bMax = 1.f;
			PsychShader.set("mono", 0);
			PsychShader.set("min", -.40f);
			PsychShader.set("brightness", .5f);	
			PsychShader.set("distortionScale", .952f);
		}

		// Arc test
		if (setupSet == 3) {
			bg = color(50, 50, 60);
			bg = color(5, 0, 18);
			//bg = color(120,120,30);
			rMax = 1.f;
			gMax = 2.f;
			bMax = 1.f;

			PsychShader.set("mono", 0);

			PsychShader.set("shaderFunction", 0);
			PsychShader.set("rTimeMult", 2.0f);
			PsychShader.set("gTimeMult", 1.0f);
			PsychShader.set("bTimeMult", 2.0f);
			PsychShader.set("distortionScale", .952f);
			PsychShader.set("brightness", .65f);	
			PsychShader.set("min", .01f);
			PsychShader.set("tTimeMult", 1000.0f);

			
			PsychShader.set("shaderFunction", 1);
			PsychShader.set("rTimeMult", 50.0f);
			PsychShader.set("gTimeMult", 52.3f);
			PsychShader.set("bTimeMult", 155.5f);
			PsychShader.set("distortionScale", .0005f);
			PsychShader.set("tTimeMult", 2000.0f);
			PsychShader.set("brightness", .65f);	


			PsychShader.set("positionX", 255);
			PsychShader.set("positionY", 180);


			blockHeight = 232;
			blockWidth = 262;
			xSpeed = .8f;
			numBlocks = 90;
			blocks = new Block[numBlocks];
		}


		PsychShader.set("rMax", rMax);
		PsychShader.set("gMax", gMax);
		PsychShader.set("bMax", bMax);


		// Generate moving blocks	
		for (int i = 0; i < numBlocks; i++) {
			Block b = new Block();
			b.setUpBlock();
			b.velocity.x = xSpeed;
			b.dims.y = blockHeight;
			b.blockHeight = blockHeight;
			b.blockWidth = blockWidth;
			b.blockPosRange = 32;
			b.position.y = random(blockPosRange);
			//blocks = (Block[])append(blocks, b);
			b.position.x = random(width);
			if (random(1) > .5f) {
				b.dirx = -1;
			}
			blocks[i] = b;
		}
	}
}

public void draw() {
	background(10, 0, 10);

	if (mode == "diagnostics") {
		fill(10, 0, 10);
		rect(0, 0, width, height);

		if (!frameMoved) {
			//surface.setLocation(2660, 236);
			surface.setLocation(2816, 204);
			surface.setLocation(2752, 204);
			surface.setLocation(2816, 204);
			frameMoved = true;
		}

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
		background(bg);

		if (setupSet == -1 ) {
			if (!frameMoved) {
				surface.setLocation(1800, 900);
				//surface.setLocation(2500, 234);
				frameMoved = true;
			}
			rect(0, 0, 580, 340);

		}
		if (setupSet == 5 ) {
			if (!frameMoved) {
				surface.setLocation(1800, 900);
				surface.setLocation(2500, 234);
				frameMoved = true;
			}
			//rect(0, 0, 580, 340);
			
			// top
			rect(188, 0, 198, 96);
			
			// left
			rect(188, 96, 58, 196);
			
			// right
			rect(295, 96, 95, 196);
			//ellipse(125,130,70,70);
		}

		if (setupSet == 0 ) {
			if (!frameMoved) {
				//surface.setLocation(1800, 900);
				surface.setLocation(2660, 234);
				frameMoved = true;
			}
			//rect(0, 0, 580, 340);
			rect(64, 160, 122, 260, 50,50,0,0);
			rect(194, 160, 252, 260, 50,50,0,0);
			ellipse(125,130,70,70);
		}

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
				//surface.setLocation(2580, 120);
				surface.setLocation(2814, 204);
				// Production values
				if (productionExport == true) {
					surface.setLocation(100, 100);
				}
				frameMoved = true;
			}
			//ellipse(0,0,270,270);
			//rect(0, 0, 100, 260);
			ellipse(0,0,190,870);
			//rect(0, 0, 100, 260);
			//rect(100, 130, 60, 78);
			//image(img, 0, 0);
			//drawAndMove();
		}

		if (setupSet == 3) {
			if (!frameMoved) {
				surface.setLocation(2752, 204);
				//surface.setLocation(266, 120);
				frameMoved = true;
			}
			drawAndMove();
		}

		if (setupSet == 6) {
			if (!frameMoved) {
				//surface.setLocation(2660, 234);
				surface.setLocation(2816, 204);
				frameMoved = true;
		  }
			rect(0, 0, 260, 260);
			//drawSimple();
		}

		if (setupSet == 4) {
			if (!frameMoved) {
				surface.setLocation(2660, 234);
				//surface.setLocation(266, 120);
				frameMoved = true;
			}
			drawSimple();
		}


	
	PsychShader.set("time", millis() / 1000.0f);
	shader(PsychShader);	
	//rect(0, 0, 250, 320); 

	}
}

public void drawSimple() {
	//rect(0, 0, 448, 220);

	beginShape();
	vertex(20, 20);
	vertex(420, 20);
	vertex(420, 40);
	vertex(60, 40);
	vertex(60, 60);
	vertex(20, 60);
	endShape(CLOSE);
}


public void drawAndMove() {
		for (int i = 0; i < blocks.length; i++) {
		blocks[i].moveBlock();
		blocks[i].renderBlock();
	}
}
class Block {
  public PVector position, dims, velocity, acceleration;
  public int dirx = 1;
  public int diry = 1;
  public int blockHeight = 60;
  public int blockWidth = 60;
  public int blockPosRange = 32;

  Block() {
    
  }

  public void setUpBlock() {
    int w =  floor(random(blockWidth));
    int h =  floor(random(blockHeight));
    dims = new PVector(w, h);
    position = new PVector(0, random(blockPosRange));
    velocity = new PVector(random(5), 0); 
    acceleration = new PVector(.0f, .0f);
  }

  public void moveBlock() {
    //position.add(velocity);
    position.x += velocity.x * dirx;
    if (dirx  == 1) {
      if (position.x > width || position.y > height) {
        position.x = -dims.x;
        position.y = random(blockPosRange);
        //velocity.x = random(5);
        //velocity.y = 0.0;
      }
    } else {
      if (position.x < 0 - dims.x || position.y < 0 - dims.y) {
        position.x = width;
        position.y = random(blockPosRange);
        //velocity.x = random(5);
        //velocity.y = 0.0;
      }
    }

    velocity.add(acceleration);
  }

  public void renderBlock() {
    //ellipse(position.x, position.y, dims.x, dims.y);
    rect(position.x, position.y, dims.x, dims.y);
  }
}
  public void settings() { 	size(260, 260, P2D); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "ConcentricAfterImages" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
