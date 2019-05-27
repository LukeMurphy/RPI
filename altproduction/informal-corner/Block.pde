class Block { //<>//
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
    acceleration = new PVector(.0, .0);
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
