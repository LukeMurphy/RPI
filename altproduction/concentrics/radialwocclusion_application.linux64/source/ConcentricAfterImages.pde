
PShader Scrunchie;
PImage img;

boolean frameMoved = false;

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
int setupSet = 5;

//------------------------------//
void setup() {

	size(580, 340, P2D);
	noStroke();

	img = loadImage("still-1.png");

	f = createFont("SourceCodePro-Regular.ttf", 12);
	textFont(f);

	if (mode == "diagnostics" ) {
		rows = floor(height/cellHeight) + 1;
		cols = floor(width/cellWidth) + 1;
	} else {
		// Set shader parameters
		Scrunchie = loadShader("basic.glsl");
		Scrunchie.set("resolution", float(width), float(height));	 
		//Scrunchie.set("lineScale", 10.0);

		Scrunchie.set("rTimeMult", 2.0);
		Scrunchie.set("gTimeMult", 10.0);
		Scrunchie.set("bTimeMult", 2.0);
		Scrunchie.set("distortionScale", .52);
		Scrunchie.set("brightness", .65);
		Scrunchie.set("tTimeMult", 1000.0);
		Scrunchie.set("shaderFunction", 0);
		Scrunchie.set("positionX", 255);
		Scrunchie.set("positionY", 180);

		if (setupSet == -1) {
			Scrunchie.set("rTimeMult", 5.0);
			Scrunchie.set("gTimeMult", 5.3);
			Scrunchie.set("bTimeMult", 1.5);
			Scrunchie.set("tTimeMult", 1000.0);
			Scrunchie.set("distortionScale", .1);
			Scrunchie.set("brightness", .85);
			Scrunchie.set("shaderFunction", 0);	
		}

		if (setupSet == 5) {
			Scrunchie.set("rTimeMult", 50.0);
			Scrunchie.set("gTimeMult", 52.3);
			Scrunchie.set("bTimeMult", 155.5);
			Scrunchie.set("tTimeMult", 5000.0);
			Scrunchie.set("distortionScale", .001);
			Scrunchie.set("brightness", .85);
			Scrunchie.set("shaderFunction", 2);	
		}

		if (setupSet == 0) {
			Scrunchie.set("rTimeMult", 50.0);
			Scrunchie.set("gTimeMult", 52.3);
			Scrunchie.set("bTimeMult", 155.5);
			Scrunchie.set("tTimeMult", 5000.0);
			Scrunchie.set("distortionScale", .001);
			Scrunchie.set("brightness", .85);
			Scrunchie.set("shaderFunction", 1);	
		}

		// P!0 tower 4 - slender
		if (setupSet == 4) {
			bg = color(50, 50, 60);
			//bg = color(120,120,30);
			rMax = 1.;
			gMax = 1.;
			bMax = 1.;
			Scrunchie.set("mono", 0);
			Scrunchie.set("min", -.40);
			Scrunchie.set("brightness", .5);	
			Scrunchie.set("distortionScale", .952);
		}

		// Arc test
		if (setupSet == 3) {
			bg = color(50, 50, 60);
			bg = color(100, 0, 80);
			//bg = color(120,120,30);
			rMax = 1.;
			gMax = 2.;
			bMax = 1.;
			Scrunchie.set("mono", 0);
			Scrunchie.set("min", .01);
			Scrunchie.set("brightness", .65);	
			Scrunchie.set("distortionScale", .952);

			blockHeight = 32;
			blockWidth = 62;
			xSpeed = .8;
			numBlocks = 90;
			blocks = new Block[numBlocks];
		}


		Scrunchie.set("rMax", rMax);
		Scrunchie.set("gMax", gMax);
		Scrunchie.set("bMax", bMax);


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

	if (mode	== "diagnostics") {
		fill(10, 0, 10);
		rect(0, 0, width, height);

		if (!frameMoved) {
			surface.setLocation(2660, 236);
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
				surface.setLocation(2580, 120);
				frameMoved = true;
			}
			rect(40, 10, 260, 220);
			image(img, 0, 0);
		}

		if (setupSet == 3) {
			if (!frameMoved) {
				surface.setLocation(2660, 234);
				//surface.setLocation(266, 120);
				frameMoved = true;
			}
			drawAndMove();
		}

		if (setupSet == 4) {
			if (!frameMoved) {
				surface.setLocation(2660, 234);
				//surface.setLocation(266, 120);
				frameMoved = true;
			}
			drawSimple();
		}
	}

	Scrunchie.set("time", millis() / 1000.0);
	shader(Scrunchie);	
	//rect(0, 0, 250, 320); 
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
