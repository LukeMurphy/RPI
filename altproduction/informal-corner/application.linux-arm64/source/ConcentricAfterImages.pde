
PShader PsychShader;
PImage img;

boolean frameMoved = false;
boolean productionExport = true;

float xPos = 0;
float yPos = 0;
int numBlocks = 80;
Block[] blocks = new Block[numBlocks];

float rMax = 1.0;
float gMax = 1.3;
float bMax = 1.0;

color bg = color(20, 0, 60, 1);

int blockHeight = 60;
int blockWidth = 60;
int blockPosRange = 32;
float xSpeed = .8;


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
void setup() {

	size(260, 260, P2D);
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
		PsychShader.set("resolution", float(width), float(height));	 
		//PsychShader.set("lineScale", 10.0);

		PsychShader.set("rTimeMult", 2.0);
		PsychShader.set("gTimeMult", 10.0);
		PsychShader.set("bTimeMult", 2.0);
		PsychShader.set("distortionScale", .52);
		PsychShader.set("brightness", .65);
		PsychShader.set("tTimeMult", 1000.0);
		PsychShader.set("shaderFunction", 0);
		PsychShader.set("positionX", 255);
		PsychShader.set("positionY", 180);

	// CORNER ROUND SQUARE
		if (setupSet == 2) {
			PsychShader.set("rTimeMult", .010);
			PsychShader.set("gTimeMult", .020);
			PsychShader.set("bTimeMult", .010);

			// This affects the tone but adding to or dropping
			// each rgb chanel
			PsychShader.set("rFactor", 1.0);
			PsychShader.set("gFactor", 1.0);
			PsychShader.set("bFactor", 1.0);


			PsychShader.set("rMin", .010);
			PsychShader.set("gMin", .01);
			PsychShader.set("bMin", .01);


			PsychShader.set("distortionScale", .62);
			PsychShader.set("brightness", .86);
			PsychShader.set("tTimeMult", 1000.0);
			PsychShader.set("shaderFunction", 0);
			PsychShader.set("positionX", 25);
			PsychShader.set("positionY", 180);
			bg = color(20, 0, 80, 1);


		}

		if (setupSet == 6) {
			PsychShader.set("positionX", 0);
			PsychShader.set("positionY", 0);
			PsychShader.set("rTimeMult", 5.0);
			PsychShader.set("gTimeMult", 5.3);
			PsychShader.set("bTimeMult", 1.5);
			PsychShader.set("tTimeMult", 1000.0);
			PsychShader.set("distortionScale", .1);
			PsychShader.set("brightness", .85);
			PsychShader.set("shaderFunction", 0);	
		}

		if (setupSet == -1) {
			PsychShader.set("rTimeMult", 5.0);
			PsychShader.set("gTimeMult", 5.3);
			PsychShader.set("bTimeMult", 1.5);
			PsychShader.set("tTimeMult", 1000.0);
			PsychShader.set("distortionScale", .1);
			PsychShader.set("brightness", .85);
			PsychShader.set("shaderFunction", 0);	
		}

		if (setupSet == 5) {
			PsychShader.set("rTimeMult", 50.0);
			PsychShader.set("gTimeMult", 52.3);
			PsychShader.set("bTimeMult", 155.5);
			PsychShader.set("tTimeMult", 5000.0);
			PsychShader.set("distortionScale", .001);
			PsychShader.set("brightness", .85);
			PsychShader.set("shaderFunction", 2);	
		}

		if (setupSet == 0) {
			PsychShader.set("rTimeMult", 50.0);
			PsychShader.set("gTimeMult", 52.3);
			PsychShader.set("bTimeMult", 155.5);
			PsychShader.set("tTimeMult", 5000.0);
			PsychShader.set("distortionScale", .001);
			PsychShader.set("brightness", .85);
			PsychShader.set("shaderFunction", 1);	
		}

		// P!0 tower 4 - slender
		if (setupSet == 4) {
			bg = color(50, 50, 60);
			//bg = color(120,120,30);
			rMax = 1.;
			gMax = 1.;
			bMax = 1.;
			PsychShader.set("mono", 0);
			PsychShader.set("min", -.40);
			PsychShader.set("brightness", .5);	
			PsychShader.set("distortionScale", .952);
		}

		// Arc test
		if (setupSet == 3) {
			bg = color(50, 50, 60);
			bg = color(5, 0, 18);
			//bg = color(120,120,30);
			rMax = 1.;
			gMax = 2.;
			bMax = 1.;

			PsychShader.set("mono", 0);

			PsychShader.set("shaderFunction", 0);
			PsychShader.set("rTimeMult", 2.0);
			PsychShader.set("gTimeMult", 1.0);
			PsychShader.set("bTimeMult", 2.0);
			PsychShader.set("distortionScale", .952);
			PsychShader.set("brightness", .65);	
			PsychShader.set("min", .01);
			PsychShader.set("tTimeMult", 1000.0);

			
			PsychShader.set("shaderFunction", 1);
			PsychShader.set("rTimeMult", 50.0);
			PsychShader.set("gTimeMult", 52.3);
			PsychShader.set("bTimeMult", 155.5);
			PsychShader.set("distortionScale", .0005);
			PsychShader.set("tTimeMult", 2000.0);
			PsychShader.set("brightness", .65);	


			PsychShader.set("positionX", 255);
			PsychShader.set("positionY", 180);


			blockHeight = 232;
			blockWidth = 262;
			xSpeed = .8;
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
			if (random(1) > .5) {
				b.dirx = -1;
			}
			blocks[i] = b;
		}
	}
}

void draw() {
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


	
	PsychShader.set("time", millis() / 1000.0);
	shader(PsychShader);	
	//rect(0, 0, 250, 320); 

	}
}

void drawSimple() {
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


void drawAndMove() {
		for (int i = 0; i < blocks.length; i++) {
		blocks[i].moveBlock();
		blocks[i].renderBlock();
	}
}
