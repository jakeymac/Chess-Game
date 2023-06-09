import tkinter as tk
from game_piece import *
from board import *
import tkinter.messagebox as tk_mb

columns = "abcdefgh"

#I CAN DO IMAGES, LET'S DO IMAGES ON TOP OF THE BUTTONS FOR EACH PIECE

#######################
#Could update the chess piece class to have position updated and 
#then use the class variable to chec k for possible moves
######################

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess")
        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=1,column=0)

        self.current_turn = "White"
        self.playerInCheck = None

        self.currentButtonSelected = None
        
        #List to hold all buttons and corresponding pieces
        self.board = Board()

        for row in range(0,8):
            new_row_label = tk.Label(self.board_frame,text=f"{row+1}")
            new_row_label.grid(row=row,column=0)
            column_num = 1
            for column in range(0,8):
                new_square = tk.Button(self.board_frame,command= lambda coord=[row,column]: self.game_action(coord),highlightbackground="#37d3ff",highlightthickness=0)
                new_square.grid(row=row,column=column_num)
                
                self.board.setButton([row,column],new_square)

                column_label = tk.Label(self.board_frame,text=columns[column])
                column_label.grid(row=9,column=column_num)

                column_num += 1

        self.turn_label = tk.Label(self.root,text="White's Turn")
        self.update_label = tk.Label(self.root)
        self.turn_label.grid(row=2,column=0)
        self.update_label.grid(row=3,column=0)

        self.start_game()

        self.root.mainloop()

    def setCurrentButtonSelected(self,coords):
        if coords:
            self.currentButtonSelected = coords
            #Add selected look to button
            self.board.selectedButton(coords)
        else:
            if self.currentButtonSelected:
                #Deselect
                self.board.deselectedButton(self.currentButtonSelected)
                self.currentButtonSelected = None
    def changeTurn(self):
        if self.current_turn == "White":
            self.current_turn = "Black"
        else:
            self.current_turn = "White"

        self.turn_label.config(text=f"{self.current_turn}'s Turn")


    def start_game(self):
        self.whites_turn = True
        self.piece_name_list = [["r","n","b","q","k","b","n","r"],
                                ["R","N","B","Q","K","B","N","R"]]
        
        piece_type_dict = {"p": Pawn,
                           "r": Rook,
                           "n": Knight,
                           "b": Bishop,
                           "q": Queen,
                           "k": King}
        
        #Begin by placing on black's row
        row = 0
        for player in self.piece_name_list:
            
            for index in range(0,8):
                newPiece = piece_type_dict.get(player[index].lower())(player[index],[row,index])
                self.board.setPiece([row,index],newPiece)
                self.board.updateButton([row,index],newPiece.getPieceChar())

            #placing on white's row
            row = 7

        #Add black and white pawns
        for column in range(8):
            self.board.setPiece([1,column],Pawn("p",[1,column]))
            self.board.updateButton([1,column],"p")

            self.board.setPiece([6,column],Pawn("P",[6,column]))
            self.board.updateButton([6,column],"P")
    

        #Assign Rooks
        self.board.blackKing.assign_rooks([self.board.getPiece([0,0]),self.board.getPiece([0,7])])
        self.board.whiteKing.assign_rooks([self.board.getPiece([7,0]),self.board.getPiece([7,7])])

    def attemptMove(self,origin,destination):
        #Add support for castling, for making sure check doesn't work. If in check, the need to cover up the king
        originalRow = origin[0]
        originalColumn = origin[1]
        newRow = destination[0]
        newColumn = destination[1]

        if destination in self.board.getAllPossibleMoves([originalRow,originalColumn]):
            self.board.movePiece(origin,destination)

            self.changeTurn()
        #Check if white is in check

        for color in ["White","Black"]:
            inCheck = self.checkForCheck(color)
            if inCheck:
                self.update_label.config(text=f"{color} is in check")
                self.playerInCheck = color
                if self.checkForCheckMate():
                    tk_mb.showinfo(message="HI THERE, CHECK MATE GOVNA")
                return
            else:
                self.update_label.config(text="")
                self.playerInCheck = None

    def updateHighlightedButton(self):
        if self.currentButtonSelected:
            pass
        
    def game_action(self,button_coord):
        """Function to handle all button presses\n
        button_coord: list - the set of coordinates corresponding to the button that the user has pressed"""


        #STILL HAS BUG FOR CHECK/CHECKMATE. BUTTON DISSAPEARS AFTER UNCHECKING, THEN RECHECKING 
        #SHOULD ALSO CHECK IF CHECK MATE WORKS IN THAT CASE. IT'S WORKING OTHERWISE
        
        
        
        """if button_coord == [5,6] and self.board.getPieceName(self.currentButtonSelected) == "q":
            print("hi")
            pass"""

        #If the user clicks the same piece they've already selected 
        #This deselects the piece
        if self.currentButtonSelected == button_coord:
            self.setCurrentButtonSelected(None)
        else:  
            if self.currentButtonSelected:
                castled = False
                #Support for castling
                #Start by checking for the black king
                #MAKE SURE TO CHECK FRO NO CHECK/CHECKMATE
                if self.board.getPieceName(self.currentButtonSelected) == "k":
                    #Could make this a method ie: self.board.hasBlackKingMoved/hasKingMoved(color)
                    if not self.board.blackKing.get_has_moved():
                        #Original king's position
                        originalPosition = self.currentButtonSelected

                        #left from black's perspective
                        leftCastleTarget = [originalPosition[0],originalPosition[1] + 2] 
                        leftBishopPosition = [originalPosition[0],originalPosition[1] + 1]
                        
                        #Right from black's perspective
                        queenPosition = [originalPosition[0],originalPosition[1] - 1]
                        rightBishopPosition = [originalPosition[0],originalPosition[1] - 2]
                        rightCastleTarget = [originalPosition[0],originalPosition[1] - 3]
                        
                        
                        
                        blackLeftRook = self.board.blackKing.getLeftRook()
                        blackRightRook = self.board.blackKing.getRightRook()

                        if button_coord == leftCastleTarget:
                            self.setCurrentButtonSelected(None)
                            if not blackLeftRook.get_has_moved():
                                if self.board.isEmpty(leftCastleTarget) and self.board.isEmpty(leftBishopPosition):
    
                                    #Check if the move is legal
                                    self.board.movePiece(originalPosition,leftCastleTarget)
                                    if self.testExperimentBoard(blackLeftRook,leftBishopPosition):
                                        self.board.movePiece(blackLeftRook.getPosition(),leftBishopPosition)
    
                                        castled = True
                                    else:
                                        self.board.movePiece(leftCastleTarget,originalPosition)

                        elif button_coord == rightCastleTarget:
                            self.setCurrentButtonSelected(None)
                            if not blackRightRook.get_has_moved():
                                if self.board.isEmpty(rightCastleTarget) and self.board.isEmpty(queenPosition) and self.board.isEmpty(rightBishopPosition):
                                    self.board.movePiece(originalPosition, rightCastleTarget)
                                    if self.testExperimentBoard(blackRightRook,rightBishopPosition):
                                        self.board.movePiece(rightBishopPosition,blackRightRook.getPosition())
                                        
                                        castled = True
                                    else:
                                        self.board.movePiece(rightCastleTarget, originalPosition)

                                #Will need to move pieces before eperimenting board, since it's two pieces moving.
                #Check for white king
                elif self.board.getPieceName(self.currentButtonSelected) == "K":
                    if not self.board.whiteKing.get_has_moved():
                        #Original king's position
                        originalPosition = self.currentButtonSelected

                        #right from white's perspective
                        rightCastleTarget = [originalPosition[0],originalPosition[1] + 2]
                        rightBishopPosition = [originalPosition[0],originalPosition[1] + 1]

                        #left from white's perspective
                        queenPosition = [originalPosition[0],originalPosition[1] - 1]
                        leftBishopPosition = [originalPosition[0],originalPosition[1] - 2]
                        leftCastleTarget = [originalPosition[0],originalPosition[1] - 3]

                        whiteLeftRook = self.board.whiteKing.getLeftRook()
                        whiteRightRook = self.board.whiteKing.getRightRook()
                        
                        if button_coord == leftCastleTarget:
                            self.setCurrentButtonSelected(None)
                            if not whiteLeftRook.get_has_moved():
                                if self.board.isEmpty(queenPosition) and self.board.isEmpty(leftCastleTarget) and self.board.isEmpty(leftBishopPosition):
                                    
                                    #Check if the movie is legal
                                    self.board.movePiece(originalPosition,leftCastleTarget)
                                    if self.testExperimentBoard(whiteLeftRook,leftBishopPosition):
                                        self.board.movePiece(whiteLeftRook.getPosition(),leftBishopPosition)
                                        
                                        castled = True
                                    
                                    else:
                                        self.board.movePiece(leftCastleTarget,originalPosition)

                        elif button_coord == rightCastleTarget:
                            self.setCurrentButtonSelected(None)
                            if not whiteRightRook.get_has_moved():
                                if self.board.isEmpty(rightCastleTarget) and self.board.isEmpty(rightBishopPosition):
                                    self.board.movePiece(originalPosition,rightCastleTarget)
                                    if self.testExperimentBoard(whiteRightRook,rightBishopPosition):
                                        self.board.movePiece(whiteRightRook.getPosition(),rightBishopPosition)
                                        
                                        castled = True
                                    
                                    else:
                                        self.board.movePIece(rightCastleTarget,originalPosition)

                if castled:
                    self.changeTurn()

                    if self.playerInCheck:
                        self.update_label.config(text="")
                        self.playerInCheck = None
                        
                    else:
                        if self.checkForCheck(self.current_turn):
                            self.playerInCheck = self.current_turn
                            if self.checkForCheckMate():
                                play_again = tk_mb.askquestion(title="Game Over",message="Would you like to play again?")
                                if play_again:
                                    self.start_game()
                                else:
                                    self.root.destroy()
                            else:
                                #Update the label telling the user that a player is in check
                                self.update_label.config(text=f"{self.playerInCheck} is in check")

                    #No need to do anything else for this move, just exit the function
                    return
                
                if button_coord in self.board.getAllPossibleMoves(self.currentButtonSelected):
                    if self.board.isEmpty(button_coord) or self.board.getColor(button_coord) != self.current_turn:
                        if self.testExperimentBoard(self.board.getPiece(self.currentButtonSelected),button_coord):
                            self.board.movePiece(self.currentButtonSelected,button_coord)
                    
                            
                            self.changeTurn()

                            if self.playerInCheck:
                                self.update_label.config(text="")
                                self.playerInCheck = None
                                
                            else:
                                if self.checkForCheck(self.current_turn):
                                    self.playerInCheck = self.current_turn
                                    if self.checkForCheckMate():
                                        tk_mb.showinfo(message="CHECK MATE GOVNA")
                                    else:
                                        self.update_label.config(text=f"{self.playerInCheck} is in check")

                self.setCurrentButtonSelected(None)
           
            else:
                if not self.board.isEmpty(button_coord):
                    if self.board.getColor(button_coord) == self.current_turn:
                        self.setCurrentButtonSelected(button_coord)

            
    def testExperimentBoard(self,piece,testMove):
        """This function will make an experimental move to see if the move will get a player out of check\n
        Returns true if the move gets the player out of check, false if not"""
        startPosition = piece.getPosition()
       
        pieceAtTarget = self.board.getPiece(testMove)
        
        #CHANGE MOVE PIECE LATER TO ONLY MOVE THE PIECES ON THE BOARD NOT THE BUTTONS, ETC. 
        #WILL MAKE THE CODE MORE EFFICIENT
        self.board.movePiece(startPosition,testMove)
        self.board.displayBoard()
        #Check for check returns true if the king is in check. 
        #This funciton wants to see if this move is legal for a player to make 
        # to not leave their own king in check
        result = not self.checkForCheck(piece.getColor())
        self.board.movePiece(testMove,startPosition)
        self.board.setPiece(testMove,pieceAtTarget)
        self.board.displayBoard()

        return result

    
        """
        originalPosition = piece.getPosition()
        pieceAtTestMove = self.board.getPiece(testMove)

        self.board.setPiece(testMove,piece)
        self.board.setPiece(originalPosition,None)
        print("Experimental")
        self.board.displayBoard()
        if self.playerInCheck:
            result = not self.checkForCheck(self.playerInCheck)
        else:
            result = not self.checkForCheck(piece.getColor())
    

        #PIECES ARE NOT BEING REPLACEDDDD

        self.board.setPiece(testMove,pieceAtTestMove)
        self.board.setPiece(originalPosition,piece)
        print("After:")
        self.board.displayBoard()
        return result"""

    def checkForCheckMate(self):
        #Muat test all piece's capability to block the checkmate
        #Find all pieces of the color of the king in check. 
        #Get their possible moves.
        #Try those moves on board
        #Check each piece of other color to see if they can still attack the king with that move
        
        for row in self.board.board:
            for space in row:
                if space.piece != None:
                    if space.piece.getColor() == self.playerInCheck:
                        for move in space.piece.getPossibleMoves(self.board):
                            if self.board.getPiece(move) == None or self.board.getColor(move) != self.playerInCheck:
                                if self.testExperimentBoard(space.piece,move):
                                    return False
                            
        return True
                        

    def checkForCheck(self,kingColor):
        """This function will be used throughout other functions to see if a king is in check or \n 
        check mate(has to be in check, then check all possible moves for an uncheck)\n
        Returns True if the king is in check, False if not"""
        #This function could be changed to check in game_action to check if 
        # there have been more than 3 turns
        king = self.board.getKing(kingColor)

        opposite_dict = {"White":"Black","Black":"White"}
        targetingColor = opposite_dict.get(kingColor)
        for row in self.board.board:
            for space in row:
                if space.piece != None:
                    if space.piece.getColor() == targetingColor:
                        if king.getPosition() in space.getPossibleMoves():
                            return True
                    
        return False

#Get things running
main = Main()
