def PawnTester():
    pawn =  Pawn("P",[1,1])
    pawn2 = Pawn("p")

#NEED TO RENAME FUNCTIONS FOR NAME/PIECE IN ACCRODANCE TO THEIR EQUIVALENT IN BOARD.PY

class Chess_Piece:
    def __init__(self,piece,position):
        self.piece = piece
        self.name = self.getName()
        self.color = self.getColor()
        self.position = position

    def getPieceChar(self):
        return self.piece

    def getName(self):
        return f"{self.getColor()[0]} - {self.getPieceChar().lower()}"

    def getColor(self):
        if self.piece.islower():
            return "Black"
    
        return "White"
    
    def getPosition(self):
        return self.position
    
    def setPosition(self,position):
        self.position = position

#########
####################################################################################################
#Need to add support for double move forward for pawns, along with a passante, and castling. 
####################################################################################################
########


class Pawn(Chess_Piece):
    has_moved = False

    def set_has_moved(self):
        self.has_moved = True

    def get_has_moved(self):
        return self.has_moved
    
    def getPossibleMoves(self,board):
        """Checks for all possible moves
        board: an instance of the board list in order to check where pieces can be moved"""

        x = self.getPosition()[1]
        y = self.getPosition()[0]
        possibleMoves = []

        if self.getColor() == "Black":
            if board.isValidMove([y+1,x]):
                if board.isEmpty([y+1,x]):
                    possibleMoves.append([y+1,x])
                    if not self.has_moved:
                        if board.isValidMove([y+2,x]):
                            if board.isEmpty([y+2,x]):
                                possibleMoves.append([y+2,x])

            if board.isValidMove([y+1,x+1]):
                if not board.isEmpty([y+1,x+1]):
                    possibleMoves.append([y+1,x+1])
            
            if board.isValidMove([y+1,x-1]):
                if not board.isEmpty([y+1,x-1]):
                    possibleMoves.append([y+1,x-1])
            
            return possibleMoves

        else:
            if board.isValidMove([y-1,x]):
                if board.isEmpty([y-1,x]):
                    possibleMoves.append([y-1,x])
                    if not self.has_moved:
                        if board.isValidMove([y-2,x]):
                            if board.isEmpty([y-2,x]):
                                possibleMoves.append([y-2,x])

            if board.isValidMove([y-1,x+1]):
                if not board.isEmpty([y-1,x+1]):
                    possibleMoves.append([y-1,x+1])
            
            if board.isValidMove([y-1,x-1]):
                if not board.isEmpty([y-1,x-1]):
                    possibleMoves.append([y-1,x-1])
            
            return possibleMoves


class Queen(Chess_Piece):   
    def getDiagonalMoves(self,board):
        """Gets all possible moves moving diagonally 
        board: an instance of the board list in order to check where pieces can be moved"""
    
        x = self.getPosition()[1]
        y = self.getPosition()[0]
        possibleMoves = []
        
        #left up diagonal
        xChange = -1
        yChange = 1
        leftUpDiagonal = True
        while leftUpDiagonal:
            newPosition = [y+yChange,x+xChange]
            if board.isValidMove(newPosition):
                if not board.isEmpty(newPosition):
                    leftUpDiagonal = False

                possibleMoves.append(newPosition)
                xChange = xChange - 1
                yChange += 1

            else:
                leftUpDiagonal = False
                
        #right up diagonal
        xChange = 1
        yChange = 1
        rightUpDiagonal = True
        while rightUpDiagonal:
            newPosition = [y+yChange,x+xChange]
            if board.isValidMove(newPosition):
                if not board.isEmpty(newPosition):
                    rightUpDiagonal = False

                possibleMoves.append(newPosition)
                xChange += 1 
                yChange += 1

            else:
                rightUpDiagonal = False


        rightDownDiagonal = True
        #right down diagonal
        xChange = 1
        yChange = -1
        rightDownDiagonal = True
        while rightDownDiagonal:
            newPosition = [y+yChange,x+xChange]
            if board.isValidMove(newPosition):
                if not board.isEmpty(newPosition):
                    rightDownDiagonal = False

                possibleMoves.append(newPosition)
                xChange += 1
                yChange = yChange - 1

            else:
                rightDownDiagonal = False

        #left down diagonal
        xChange = -1
        yChange = -1
        leftDownDiagonal = True
        while leftDownDiagonal:
            newPosition = [y+yChange,x+xChange]
            if board.isValidMove(newPosition):
                if not board.isEmpty(newPosition):
                    leftDownDiagonal = False

                possibleMoves.append(newPosition)
                xChange = xChange - 1
                yChange = yChange - 1

            else:
                leftDownDiagonal = False


        return possibleMoves

    
    def getHorizontalVerticalMoves(self,board):
        """Checks for all possible moves moving horizontally and vertically
        board: an instance of the board list in order to check where pieces can be moved"""
        x = self.getPosition()[1]
        y = self.getPosition()[0]
        possibleMoves = []

        #to left    
        checkingLeft = True
        xChange = -1
        while checkingLeft:
            #update here to use newposition variable instead of x+xChange,y coordinates
            if board.isValidMove([y,x+xChange]):
                if not board.isEmpty([y,x+xChange]):
                    checkingLeft = False

                possibleMoves.append([y,x+xChange])
                xChange = xChange -1

            else:
                checkingLeft = False

        #up
        checkingUp = True
        yChange = -1
        while checkingUp:
            if board.isValidMove([y+yChange,x]):
                if not board.isEmpty([y+yChange,x]):
                    checkingUp = False
                
                possibleMoves.append([y+yChange,x])
                yChange = yChange - 1
            else:
                checkingUp = False

        #to right
        checkingRight = True
        xChange = 1
        while checkingRight:
            if board.isValidMove([y,x+xChange]):
                if not board.isEmpty([y,x+xChange]):
                    checkingRight = False
                possibleMoves.append([y,x+xChange])
                xChange += 1       
            else:
                checkingRight = False 

        #down
        checkingDown = True
        yChange = 1
        while checkingDown:
            if board.isValidMove([y+yChange,x]):
                if not board.isEmpty([y+yChange,x]):
                    checkingDown = False
                    
                possibleMoves.append([y+yChange,x])
                yChange = yChange + 1
            else:
                checkingDown = False
        
        return possibleMoves

    def getPossibleMoves(self,board):
        """Checks for all possible moves
        board: an instance of the board list in order to check where pieces can be moved"""
        return self.getDiagonalMoves(board) + self.getHorizontalVerticalMoves(board)

class Bishop(Queen):
    def getPossibleMoves(self,board):
        return self.getDiagonalMoves(board)
    
class Rook(Queen):
    has_moved = False

    def get_has_moved(self):
        return self.has_moved
    
    def set_has_moved(self):
        self.has_moved = True

    def getPossibleMoves(self,board):
        return self.getHorizontalVerticalMoves(board)
        
class Knight(Chess_Piece):
    def getPossibleMoves(self,board):
        """Checks for all possible moves
        board: an instance of the board list in order to check where pieces can be moved"""
        x = self.getPosition()[1]
        y = self.getPosition()[0]
        possibleMovesToCheck = [[2,-1],[2,1],[1,-2],[-1,-2],[-2,-1],[-2,1],[1,2],[-1,2]]
        possibleMoves = [] #List to return
        for move in possibleMovesToCheck:
            new_coords = [y+move[1],x+move[0]]
            if board.isValidMove(new_coords):
                possibleMoves.append(new_coords)
        return possibleMoves

        
class King(Pawn):
    has_moved = False

    def get_has_moved(self):
        return self.has_moved

    def set_has_moved(self):
        self.has_moved = True

    def assign_rooks(self,rooks):
        """Assign rooks to check in order to castle"""
        if self.getColor() == "Black":
            self.leftRook = rooks[1]
            self.rightRook = rooks[0]

        else:
            self.rightRook = rooks[1]
            self.leftRook = rooks[0]

    def getLeftRook(self):
        return self.leftRook

    def getRightRook(self):
        return self.rightRook

    def getPossibleMoves(self,board):
        # NEEDS SUPPORT FOR CASTLING
        """Checks for all possible moves
        board: an instance of the board list in order to check where pieces can be moved"""
        x = self.getPosition()[1]
        y = self.getPosition()[0]
        possibleMovesToCheck = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
        possibleMoves = []
        for move in possibleMovesToCheck:
            new_coords = [y+move[0],x+move[1]]
            if board.isValidMove(new_coords):
                possibleMoves.append(new_coords)

        return possibleMoves