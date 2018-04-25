var paused;
var game;

var scl = 20;
var w = 400;
var h = 600;

var shapes = {0: [[1,1,0],
                  [0,1,1],
                  [0,0,0]],
              1: [[0,1,1],
                  [1,1,0],
                  [0,0,0]],
              2: [[1,0,0],
                  [1,1,1],
                  [0,0,0]],
              3: [[0,0,1],
                  [1,1,1],
                  [0,0,0]],
              4: [[0,1,0],
                  [1,1,1],
                  [0,0,0]],
              5: [[1,1],
                  [1,1]],
              6: [[1,1,1,1],
                  [0,0,0,0],
                  [0,0,0,0],
                  [0,0,0,0]]};

var colours = {0: [0,100,0],
               1: [255,0,0],
               2: [0,0,255],
               3: [255,140,0],
               4: [139,0,139],
               5: [255,255,0],
               6: [0,255,255]
              }


function setup(){
  createCanvas(w, h);
  frameRate(8);
  game = new Game();
  paused = false;
}

function draw(){
  background(200);
  game.update();
  game.checkRow();
  game.show();
  controls();
}

function controls(){
  if(keyIsDown(LEFT_ARROW)){
    game.shape.update(-1, 0, game.board);
  }else if(keyIsDown(RIGHT_ARROW)){
    game.shape.update(1, 0, game.board);    
  }else if(keyIsDown(DOWN_ARROW)){
    game.shape.update(0, 1, game.board);
  }
}

function keyPressed(){
  if(key == ' '){
    if(paused){
      paused = false;
      loop();
    }else{
      paused = true;
      noLoop();
    }
  }
  if(keyCode == 38){
    game.shape.rotate();
  }
}
