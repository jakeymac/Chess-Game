import tkinter as tk
from game_piece import *
columns = ["a","b","c","d","e","f","g","h"]

class Board:
    def __init__(self):
        self.board = []
        for row in range(8):
            self.board.append([])
            for column in range(8):
                self.board[row].append(Square(self))

        self.whiteKing = None
        self.blackKing= None

    def movePiece(self,origin,destination):
        originRow = origin[0]
        originColumn = origin[1]

        newRow = destination[0]
        newColumn = destination[1]

        self.updateButton([origin[0],origin[1]],"")
        self.setPiece([newRow,newColumn],self.getPiece([originRow,originColumn]))
        self.updateButton([newRow,newColumn],self.getPieceName([originRow,originColumn]))
        self.setPiece([originRow,originColumn],None)
        self.updatePiecePosition(destination,destination)

    def getHasMoved(self,position):
        if self.getPieceName(position).lower() in ["k","r"]: 
            return self.board[position[0]][position[1]].getHasMoved()

    def displayBoard(self):
        for row in self.board:
            row_string = ""
            for space in row:
                if space.piece != None:
                    row_string += space.getPieceName()
                else:
                    row_string += "0"

                row_string += " "

            print(row_string)

    def getKing(self,color):
        if color == "White":
            return self.whiteKing

        return self.blackKing
    
    def setKing(self,color,king):
        if color == "White":
            self.whiteKing = king
        
        else:
            self.blackKing = king

    def getColor(self,coordinates):
        return self.board[coordinates[0]][coordinates[1]].getColor()

    def setButton(self,coords,button):
        self.board[coords[0]][coords[1]].setButton(button)
    
    def updateButton(self,coords,text):
        self.board[coords[0]][coords[1]].button.config(text=text)

    def selectedButton(self,coords):
        self.board[coords[0]][coords[1]].button.config(highlightthickness = 1)

    def deselectedButton(self,coords):
        self.board[coords[0]][coords[1]].button.config(highlightthickness = 0)
    def getPiece(self,coords):
        return self.board[coords[0]][coords[1]].getPiece()
    
    def getPieceName(self,coords):
        return self.board[coords[0]][coords[1]].getPieceName()

    def setPiece(self,coords,piece):
        self.board[coords[0]][coords[1]].setPiece(piece)

    def isEmpty(self,position):
        return not self.board[position[0]][position[1]].hasPiece()
        
    def isValidMove(self,coordinate):
        #Check for kings?? Maybe set a class variable to hold the king's location
        if coordinate[0] > 7 or coordinate[0] < 0:
            return False
        if coordinate[1] > 7 or coordinate[1] < 0:
            return False
        
        return True
    
    def getAllPossibleMoves(self,coordinate):
        return self.board[coordinate[0]][coordinate[1]].getPossibleMoves()
    
    def updatePiecePosition(self,current,new):
        self.board[current[0]][current[1]].updatePosition(new)

class Square:
    def __init__(self,board):
        self.board = board
        self.button = None
        self.piece = None

    def setButton(self,button):
        self.button = button

    def setPiece(self,piece: Chess_Piece):
        if piece != None:

            if piece.getPieceChar().lower() == "k":
                self.board.setKing(piece.getColor(),piece)

        self.piece = piece

    def hasPiece(self):
        return self.piece != None

    def getPiece(self):
        return self.piece
    
    def getPieceName(self):
        return self.piece.getPieceChar()
    
    def getColor(self):
        return self.piece.getColor()
    
    def upateButtonText(self, text):
        self.button.config(text=text)

    def getPossibleMoves(self):
        return self.piece.getPossibleMoves(self.board)

    def updatePosition(self,position):
        self.piece.setPosition(position)