function createBoard(){
  var board = Array(h/scl);
  for(var i = 0; i < board.length; i++){
    board[i] = Array(w/scl);
  }
  for(var i = 0; i < board.length; i++){
    for(var j = 0; j < board[i].length; j++){
      board[i][j] = new Cell(i, j);
    }
  }
  return board;
}

function Game(){
  this.board = createBoard();
  this.shape = new Shape();

  //updates the tetris piece
  this.update = function(){
    if(!this.shape.b){
      this.shape.update(0, 1, this.board);
    }else{
      this.add2board();
      this.shape = new Shape();
    }
  }

  //displays both stationary and moving pieces
  this.show = function(){
    this.shape.show();
    for(var i = 0; i < this.board.length; i++){
      for(var j = 0; j < this.board[i].length; j++){
        this.board[i][j].show()
      }
    }
  }

  //changes the values of cells in the array 
  this.swap = function(i1, i2){
    for(var j = 0; j < this.board[i1].length; j++){
      var temp = this.board[i1][j];
      this.board[i1][j] = this.board[i2][j];
      this.board[i2][j] = temp; 
    }
    this.switch(i1, i2);
  }
  this.switch = function(i1, i2){
    for(var j = 0; j < this.board[i1].length; j++){
      this.board[i1][j].swap(i1);
      this.board[i2][j].swap(i2);
    }
  }

  //clears any full rows
  this.clearRow = function(i){
    for(var j = 0; j < this.board[i].length; j++){
      this.board[i][j].reset();
    }
  }

  //sums the values in a row
  this.sumRow = function(i, s){
    var counter = 0;
    for(var j = 0; j < this.board[i].length; j++){
      if(this.board[i][j].s){
        counter ++;
      }
    }
    return counter == s;
  }

  //responsible for checking if any rows have been filled
  this.checkRow = function(){
    var fullRows = [];
    for(var i = 0; i < this.board.length; i++){
      if(this.sumRow(i, this.board[i].length)){
        fullRows.push(i);
      }
    }
    if(fullRows.length > 0){
      for(var f = 0; f < fullRows.length; f++){
        this.clearRow(fullRows[f]);
        for(var i = fullRows[f]; i > 1; i--){
          this.swap(i, i-1);
        }
      }
    }
  }

  //covert a stationary tetris piece to cells on the games board
  this.add2board = function(){
    var squares = this.shape.squares();
    for(var i = 0; i < squares.length; i++){
      var square = squares[i]
      this.board[square[0]][square[1]].colour(this.shape.c);
    }
  }

}