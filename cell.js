function Cell(i, j){
  this.i = i;
  this.j = j;
  this.c = null;
  this.s = false;

  this.reset = function(){
    this.c = null;
    this.s = false;
  }

  this.swap = function(i){
    this.i = i
  }

  this.colour = function(c){
    this.c = c;
    this.s = true;
  }  

  this.show = function(){
    if(this.s){
      stroke(0);
      fill(this.c);
      rect(this.j * scl, this.i * scl, scl, scl);
    } 
  }
}

function Shape(){
  this.i = 0;
  this.j = 4 * scl;
  this.b = false;

  this.v = int(random(0, 7))
  this.shape = shapes[this.v];
  this.c = colours[this.v];

  //displays the piece
  this.show = function(){
    stroke(0);
    fill(this.c);
    for(var i = 0; i < this.shape.length; i++){
      for(var j = 0; j < this.shape[i].length; j++){
        if(this.shape[i][j] == 1){
          rect(this.j +  j * scl, this.i + i * scl, scl, scl);
        }
      }
    }
  }

  //updates the piece
  this.update = function(x, y, board){
    this.lower(y, board);
    this.turn(x, board);
  }

  //function for rotating the tetris pieces array
  this.rotate = function(){
    matrix = this.shape.reverse();
    for (var i = 0; i < matrix.length; i++) {
      for (var j = 0; j < i; j++) {
        var temp = matrix[i][j];
        matrix[i][j] = matrix[j][i];
        matrix[j][i] = temp;
      }
    }
    this.shape = matrix;
  }
  //function for the pieces movement in the y coordinate
  this.lower = function(y, board){
    if(this.bottom() < h && !this.floor(0, y, board)){
      this.i += y * scl;
    }else{
      this.b = true;
    }
  }

  //function for the pieces movement in the x coordinate
  this.turn = function(x, board){
    if(this.left() + x*scl >= 0 && this.right() + x*scl <= w){
      if(this.i < h){
        if(!this.floor(x, 0, board)){
          this.j += x * scl;
        }
      }
    }
  }

  //return the y coordinate of the lowest point of the tetris piece
  this.bottom = function(){
    var bottom = 0;
    for(var i = 0; i < this.shape.length; i++){
      for(var j = 0; j < this.shape[i].length; j++){
        if(this.shape[i][j] == 1 && i > bottom){
          bottom = i;
        }
      }
    }
    return this.i + bottom * scl + scl;
  }

  //return the x coordinate of the furthest point to the left of the tetris piece
  this.left = function(){
    var left = 100;
    for(var i = 0; i < this.shape.length; i++){
      for(var j = 0; j < this.shape[i].length; j++){
        if(this.shape[i][j] == 1 && j < left){
          left = j;
        }
      }
    }
    return this.j + left * scl;
  }

  //return the x coordinate of the furthest point to the right of the tetris piece
  this.right = function(){
    var right = 0;
    for(var i = 0; i < this.shape.length; i++){
      for(var j = 0; j < this.shape[i].length; j++){
        if(this.shape[i][j] == 1 && j > right){
          right = j;
        }
      }
    }
    return this.j + right * scl + scl;
  }


  //checks for collisions against stations pieces (cells) on the games board array
  this.checkCollision = function(i, j, board){
    return board[i/scl][j/scl].s;
  }

  //returns if the piece has been stopped by another pieces on the game board array
  this.floor = function(x, y, board){
    for(var i = 0; i < this.shape.length; i++){
      for(var j = 0; j < this.shape[i].length; j++){
        if(this.shape[i][j] == 1){
          if(this.checkCollision(this.i + (i*scl) + y*scl, this.j + (j*scl) + x*scl, board)){
            return true;
          }
        }
      }
    }
    return false;
  }

  //returns positions of each point in the tetris piece so it can be added to the board
  this.squares = function(){
    var squares = [];
    for(var i = 0; i < this.shape.length; i++){
      for(var j = 0; j < this.shape[i].length; j++){
        if(this.shape[i][j] == 1){
          squares.push([this.i/scl + i, this.j/scl + j]);
        }
      }
    }
    return squares;
  }
}
