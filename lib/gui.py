### Author: Dustin Hu
### Date: 04-06-2014
### Purpose: To be the GUI for the domino game

from dominogame import DominoError
import dominogame
import hand
import time
import random
import tkMessageBox
import os
from Tkinter import *

class App(object):
    ### Author: Dustin Hu
    ### Date: 04-06-2014
    ### Purpose: To contain the app of the dominogame

    ### Fields:
    ####### root: The Tk() on which everything rests
    ####### menubar: The menubar of the program
    ####### filemenu: THe filemun of the program
    ####### canvas: The canvas on which everything will be drawn
    ####### game: The dominogame instance of the game
    ####### TCanvas: Table's canvas
    ####### currX: The current X of the table
    ####### currY: The current Y of the table
    ####### domNum: The domino number to flip
    ####### domValue: THe value of the domino
    ####### btnStart: STart button
    ####### dirVar: The direction in which the player wishes to move
    ####### dirGroup: THe frame for directino
    ####### btnPlayerTurn: The player's turn button
    ####### btnEndTurn: The end turn button
    ####### vcmd: Validation comand
    ####### clickedDomino: The domino that the player clicked on
    ####### playable: Whetehr or not the player can play
    ####### played: wehtehr or not a move has been done. If this reaches a threshold, it will end in a tie.
    ####### btnReset: Resets the game
    
    ### Methods:
    ####### resetGame: Resets the game
    ####### endTie: Ends a tiegame/stalemate
    ####### showScoe: Shows the score
    ####### saveScore: Saves scores 
    ####### getCoords: Gets the coordinates of the mouse
    ####### genCoords: Generates the coordinates for the dominoes
    ####### getAbout: Gets the about
    ####### getHelp: Gets the help
    ####### checkPlayable: Checks whether or not the player can play
    ####### validate: Validates input
    ####### endGame: Ends the game
    ####### cpuPlay: Runs the computer's turn
    ####### playerTurn: Runs the players turn
    ####### initFrame: Initializes the frames
    ####### flip: Flips the domino at i
    ####### initInput: Initialzes the input boxes
    ####### updateTable: Updates the canvas of the table
    ####### startGame: Starts the game
    ####### initButtons: Intializes the buttons
    ####### initLabels: Intializes the labels 
    ####### initTable: Initalizes the table 
    ####### initGame: Initalizes the game itself.
    ####### initCanvas: Initalizes the canvas
    ####### initRoot: Initalizes the root
    ####### __init__: Initalizes the thing

    def resetGame(self):
        ### Author: DUstin Hu
        ### DAte: 15-06-2014
        ### Purpose: To reset the game
        ### Input: None
        ### Output: None
        self.canvas.delete(ALL)
        self.initGame()
        

    def endTie(self):
        ### Author: DUstin Hu
        ### Date: 15-06-2014
        ### Purpose: To end a stalement
        ### Input: None
        ### Output: None
        tkMessageBox.showinfo("Tie Game", "The game is a tie!")
        self.playable = False
        self.btnEndTurn.config(state = DISABLED)
        self.btnPlayerTurn.config(state = DISABLED)
        self.btnReset.config(state = NORMAL)


    def showScore(self):
        ### Author: Dustin hu
        ### Date: 15-06-2014
        ### Purpose: To show the score 
        ### Input: None
        ### Output: Non
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            path = path.split("/")
            path = path[1:-1]
            data = ""
            for part in path:
                data = data + "/" + part
            data = data + "/save/info.txt"
            indata = open(data, "r")
            info = [int(line) for line in indata]
            indata.close()

        
            cpu1 = "CPU1: "  + str(info[0])
            cpu2 = "CPU2: " + str(info[1])
            cpu3 = "CPU3: " + str(info[2])
            player = "Player: " + str(info[3])
            scores = sorted([cpu1, cpu2, cpu3, player], key = lambda word: int(word.split()[-1]), reverse = True)
            strOut = ""

            for i in xrange(1, len(scores) + 1):
                strOut = strOut + str(i) + ". " + scores[i - 1] + "\n"
        

            tkMessageBox.showinfo("Score", strOut)

        except IndexError:
            path = os.path.dirname(os.path.abspath(__file__))
            path = path.split("/")
            path = path[1:-1]
            data = ""
            for part in path:
                data = data + "/" + part
            data = data + "/save/info.txt"
            indata = open(data, "w")
            output = "0\n0\n0\n0\n"
            indata.write(output)
            indata.close()
            self.showScore()
            
            
        
        

    def saveScore(self, winner, score):
        ### Author: Dustin Hu
        ### DAte: 14-06-2014
        ### Purpose: Saves the score to the scorefile
        ### Input: None
        ### Output: None
        
        path = os.path.dirname(os.path.abspath(__file__))
        path = path.split("/")
        path = path[1:-1]
        data = ""
        for part in path:
            data = data + "/" + part
        data = data + "/save/info.txt"
        indata = open(data, "r")
        info = [str(line) for line in indata]
        indata.close()

        info[winner] = str(str(int(info[winner]) + score) + "\n")
        strOutput = ""
        for line in info:
            strOutput = strOutput + line

        output = open(data, "w")
        output.write(strOutput)
        output.close()

        

    def clickMove(self, event):
        ### Author: DUstin Hu
        ### DAte: 13-06-2014
        ### Purpose: To allow the player to click and move
        ### Input: None
        ### Output: None
        
        if event.y >= 10 and event.y <= 60:
            self.clickedDomino = self.getCoords(event)

        
        leftEnd = int(self.game.table.getEnds()[0])
        rightEnd = int(self.game.table.getEnds()[1])



        domino = int(self.game.pHand.dominoes[self.clickedDomino - 1].returnValue())



        rightDom = self.game.table.getCurrRight(600)
        direction = str(rightDom[-1])
        #### This istop right hand corner of the current domino
        rightDom = (int(rightDom[0]) + 60, int(rightDom[1]))

        

        if self.playable == True:
            if int(event.x) >= 100 and int(event.x) <= 160 and int(event.y) >= 130 and int(event.y) <= 160:
                try:
                    if domino % 10 == leftEnd:
                        self.game.playerTurn(position = True, index = self.clickedDomino - 1, placement = "L")
                        self.updateTable()
                        self.playable = False
                        self.btnPlayerTurn.config(state = DISABLED)
                    
                    elif domino // 10 == leftEnd:
                        self.flip(self.clickedDomino -1 )
                        self.game.playerTurn(position = True, index = self.clickedDomino - 1, placement = "L")
                        self.updateTable()
                        self.playable = False
                        self.btnPlayerTurn.config(state = DISABLED)
                except DominoError:
                    tkMessageBox.showinfo("Invalid move", "THat is an invalid move!")
                    
            else:
                if direction == "R":
                    if int(event.x) >= int(rightDom[0]- 90) and int(event.x) <= int(rightDom[0]) and int(event.y) >= int(rightDom[1]) and int(event.y) <= int(rightDom[1] + 30):
                        try:
                            if domino // 10 == rightEnd:
                                self.game.playerTurn(position = True, index = self.clickedDomino -1, placement = "R")
                                self.updateTable()
                                self.playable = False
                                self.btnPlayerTurn.config(state = DISABLED)

                            elif domino % 10 == rightEnd:
                                self.flip(self.clickedDomino -1 )
                                self.game.playerTurn(position = True, index = self.clickedDomino -1, placement = "R")
                                self.updateTable()
                                self.playable = False
                                self.btnPlayerTurn.config(state = DISABLED)
                        except DominoError:
                            tkMessageBox.showinfo("Invalid move", "THat is an invalid move!")
                            
                elif direction == "DR":
                    if int(event.x) >= int(rightDom[0] - 60) and int(event.x) <= int(rightDom[0] + 60) and int(event.y) >= int(rightDom[1] - 30) and int(event.y) <= int(rightDom[1] + 90):
                        try:
                            if domino // 10 == rightEnd:
                                self.game.playerTurn(position = True, index = self.clickedDomino -1 , placement = "R")
                                self.updateTable()
                                self.playable = False
                                self.btnPlayerTurn.config(state = DISABLED)

                            elif domino % 10 == rightEnd:
                                self.flip(self.clickedDomino -1)
                                self.game.playerTurn(position = True, index = self.clickedDomino -1 , placement = "R")
                                self.updateTable()
                                self.playable = False
                                self.btnPlayerTurn.config(state = DISABLED)
                        except DominoError:
                            tkMessageBox.showinfo("Invalid move", "THat is an invalid move!")
                                
                    #### Move towards the left
                elif direction == "L":
                    if int(event.x) >= int(rightDom[0] - 60) and int(event.x) <= int(rightDom[0] + 60) and int(event.y) >= int(rightDom[1]) and int(event.y) <= int(rightDom[1] + 60):
                        try:
                            if domino // 10 == rightEnd:
                                self.game.playerTurn(position = True, index = self.clickedDomino -1 , placement = "R")
                                self.updateTable()
                                self.playable = False
                                self.btnPlayerTurn.config(state = DISABLED)

                            elif domino % 10 == rightEnd:
                                self.flip(self.clickedDomino - 1)
                                self.game.playerTurn(position = True, index = self.clickedDomino - 1, placement = "R")
                                self.updateTable()
                                self.playable = False
                                self.btnPlayerTurn.config(state = DISABLED)
                        except DominoError:
                            tkMessageBox.showinfo("Invalid move", "THat is an invalid move!")

                elif direction == "DL":
                    if int(event.x) >= int(rightDom[0] - 120) and int(event.x) <= int(rightDom[0] + 120) and int(event.y) >= int(rightDom[1] - 60) and int(event.y) <= int(rightDom[1] + 60):
                        try:
                            if domino // 10 == rightEnd:
                                self.game.playerTurn(position = True, index = self.clickedDomino -1, placement = "R")
                                self.updateTable()
                                self.playable = False
                                self.btnPlayerTurn.config(state = DISABLED)

                            elif domino % 10 == rightEnd:
                                self.flip(self.clickedDomino -1 )
                                self.game.playerTurn(position = True, index = self.clickedDomino -1 , placement = "R")
                                self.updateTable()
                                self.playable = False
                                self.btnPlayerTurn.config(state = DISABLED)
                        except DominoError:
                            tkMessageBox.showinfo("Invalid move", "THat is an invalid move!")
                                
                                                                                                                               
                        
        if len(self.game.pHand.dominoes) == 0:
            self.endGame("Player", self.game.calcScore(self.game.c1Hand, self.game.c2Hand, self.game.c3Hand))
        

        
    def getCoords(self, event):
        ### Author: Dustin Hu
        ### DAte: 13-06-2014
        ### Purpose: To get the coordinates at which the user clicks
        ### Input: THe coordiantes from the player
        ### Output: None
        possibleMoves = self.genCoords()
        domino = -1
        #### THis goes thorugh possible moves and cehcks whetehr or not event.x is between them
        for i in xrange(0, len(possibleMoves)):
            moves = possibleMoves[i]
            minX = int(moves[0])
            maxX = int(moves[1])
            if int(event.x) >= minX and int(event.x) <= maxX:
                domino = i
        return domino

        

    def genCoords(self):
        ### Author: Dustin Hu
        ### Date: 13-06-2014
        ### Purpose: To generate a lit of coordinates for the drag and drop
        ### Input: None
        ### Output: None
        topLeft = 65
        bottomRight = 95
        clickCoords = []
        for i in xrange(0, len(self.game.pHand.dominoes) + 1):
            clickCoords.append((topLeft, bottomRight))
            topLeft = topLeft + 35
            bottomRight = bottomRight + 35
        return clickCoords
        
        

    def getAbout(self):
        ### Author: DUstin Hu
        ### DAte: 13-06-2014
        ### Purpoes: To get the About information
        ### Input: None
        ### Output: None
        tkMessageBox.showinfo("About", "Author: Dustin Hu\nDate:08-06-2014 to 15-06-2014\nTeacher: Don Smith")

    def getHelp(self):
        ### Author: DUstin Hu
        ### DAet: 13-06-2014
        ### Purpose: To get help
        ### Input: None
        ### Output: None
        tkMessageBox.showinfo("Help", "Hit the start game button to start the game.\nType in the domino number that you wish to play, counting from 0 at the far left of your hand and select which end of the chain you want to play it on (If the chain has turned, the lower one is the right). Hit the play button to play it, and the End Turn button to end your turn. However, if it's possible for you to play a domino, the End Turn button will not be enabled until you've played a card!\nAlternatively, you can click on the domino that you wish to play and where to play it to play it.")


    def checkPlayable(self):
        ### AUthor: Dustin Hu
        ### Date: 13-06-2014
        ### Purpose: To cehck if the user has any playable dominoes
        ### Input: None
        ### Output: None

        playable = []
        leftEnd = int(self.game.table.getEnds()[0])
        rightEnd = int(self.game.table.getEnds()[1])
        
        for domino in self.game.pHand.dominoes:
            dom = int(domino.value)

            if dom % 10 == rightEnd:
                playable.append((domino, "R"))
            elif dom // 10 == leftEnd:
                playable.append((domino, "L"))

        if len(playable) != 0:
            self.btnPlayerTurn.config(state = NORMAL)
        else:
            self.cpuPlay()

    
    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        words = ""
        for i in xrange(0, len(self.game.pHand.dominoes) ):
            words = words + str(i)
                        
        if text in words:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False


        
    def endGame(self, playerName, score):
        ### AUthor: DUstin Hu
        ### DAte: 11-06-2014
        ### Input: Name of player that own
        ### Output: None
        tkMessageBox.showinfo("Game Over!", "Congratulations, %s won, with a score of %i!" %( playerName, score))
        self.playable = False
        player = 0
        if playerName == "Computer 1":
            player = 0
        elif playerName == "Computer 2":
            player = 1
        elif playerName == "Computer 3":
            player = 2
        elif playerName == "Player":
            player = 3

        self.saveScore(player, score)
        self.btnReset.config(state = NORMAL)
        self.playable = False
        self.played = 0
        self.btnEndTurn.config(state = DISABLED)
        self.btnPlayerTurn.config(state = DISABLED)
        

    def cpuPlay(self):
        ### Author: DUstin hu
        ### DAte: 11-08-2014
        ### Purpose: To allow the computer to play
        ### Input: None
        ### Output: None
        
        done = False
        oriLength = len(self.game.c1Hand.dominoes)
        self.btnEndTurn.config(state = DISABLED)
        self.game.cpuTurn(self.game.c1Hand)
        newLength = len(self.game.c1Hand.dominoes)
        if oriLength == newLength:
            self.played = self.played + 1
        else:
            self.played = 0


#### Insert sleep        
        self.updateTable()
        if len(self.game.c1Hand.dominoes) == 0:
            self.endGame("Computer 1", self.game.calcScore(self.game.c2Hand, self.game.c3Hand, self.game.pHand))
            self.btnPlayerTurn.config(state = DISABLED)
            done = True

        if done == False:
            oriLength = len(self.game.c2Hand.dominoes)
            self.game.cpuTurn(self.game.c2Hand)
            newLength = len(self.game.c2Hand.dominoes)
            if oriLength == newLength:
                self.played = self.played + 1
            else:
                self.played = 0
                        
#### Insert sleep

            self.updateTable()
            if len(self.game.c2Hand.dominoes) == 0:
                self.endGame("Computer 2", self.game.calcScore(self.game.c1Hand, self.game.c3Hand, self.game.pHand))
                self.btnPlayerTurn.config(state = DISABLED)                
                done = True

                
        if done == False:
            oriLength = len(self.game.c3Hand.dominoes)
            self.game.cpuTurn(self.game.c3Hand)
            newLength = len(self.game.c3Hand.dominoes)
            if oriLength == newLength:
                self.played = self.played + 1
            else:
                self.played = 0
#### Insert sleep            
            self.updateTable()
            if len(self.game.c3Hand.dominoes) == 0:
                self.endGame("Computer 3", self.game.calcScore(self.game.c1Hand, self.game.c2Hand, self.game.pHand))
                self.btnPlayerTurn.config(state = DISABLED)

                
        if done == False:
            self.btnPlayerTurn.config(state = NORMAL)
            self.btnEndTurn.config(state = NORMAL)
            self.playable = True
            if self.played >= 4:
                self.endTie()
#            self.checkPlayable()

        

    def playerTurn(self):
        ### Author; Dustin Hu
        ### DAte: 10-08-2014
        ### Purpose: To call and setup the players turn
        ### Input: None
        ### Output: None
        oriLength = len(self.game.pHand)
        try:
            domino = int(self.game.pHand.dominoes[int(self.domValue.get())].returnValue())
        except IndexError:
            tkMessageBox.showinfo("Invalid value", "The value that you\'re entering is too large!")
            return
        leftEnd = int(self.game.table.getEnds()[0])
        rightEnd = int(self.game.table.getEnds()[1])
        direction = self.dirVar.get()
        
        try:
            # print domino // 10, leftEnd, domino // 10 == leftEnd
            # print domino % 10, leftEnd, domino % 10 == leftEnd
            # print domino // 10, rightEnd, domino // 10 == rightEnd
            # print domino % 10, rightEnd, domino % 10 == rightEnd
            # print direction, type(direction)
            # print direction == "L"
            # print direction == "R"

            if direction == "R":
                if domino // 10 == rightEnd:
                    self.game.playerTurn(position = True, index = int(self.domValue.get()), placement = "R")
                    self.updateTable()
                    self.btnPlayerTurn.config(state = DISABLED)
                    self.playable = False
                    self.btnEndTurn.config(state = NORMAL)
                elif domino % 10 == rightEnd:
                    self.flip(int(self.domValue.get()))
                    self.game.playerTurn(position = True, index = int(self.domValue.get()), placement = "R")
                    self.updateTable()
                    self.btnPlayerTurn.config(state = DISABLED)
                    self.playable = False
                    self.btnEndTurn.config(state = NORMAL)                    
            elif direction == "L":
                if domino // 10 == leftEnd:
                    self.flip(int(self.domValue.get()))
                    self.game.playerTurn(position = True, index = int(self.domValue.get()), placement = "L")
                    self.updateTable()
                    self.btnPlayerTurn.config(state = DISABLED)
                    self.playable = False
                    self.btnEndTurn.config(state = NORMAL)                    
                elif domino % 10 == leftEnd:
                    self.game.playerTurn(position = True, index = int(self.domValue.get()), placement = "L")
                    self.updateTable()
                    self.btnPlayerTurn.config(state = DISABLED)
                    self.playable = False
                    self.btnEndTurn.config(state = NORMAL)
                    
            if len(self.game.pHand.dominoes) == 0:
                self.endGame("Player", self.game.calcScore(self.game.c1Hand, self.game.c2Hand, self.game.c3Hand))

            self.domValue.set("0")

                
                    
        except DominoError:
            tkMessageBox.showinfo("Invalid move", "That is an invalid move!")

        newLength = len(self.game.pHand.dominoes)

        if newLength == oriLength:
            self.played = self.played + 1
        else:
            self.played = 0

        # print domino
        # print leftEnd
        # print rightEnd
        # print direction
        # if domino[0] == leftEnd and direction == 0:
        #     self.flip(int(self.domValue.get()))
        #     self.game.playerTurn(position = True, index = int(self.domValue.get()), placement = "L")
        #     self.updateTable()
            
        # elif domino[0] == leftEnd and direction == 1:
        #     tkMessageBox.showinfo("Error", "Wrong direction!")
            
        # elif domino[0] == rightEnd and direction == 0:
        #     tkMessageBox.showinfo("Error", "Wrong direction!")
            
        # elif domino[0] == rightEnd and direction == 1:
        #     self.game.playerTurn(position = True, index = int(self.domValue.get()), placement = "R")
        #     self.updateTable()

        # elif domino[1] == leftEnd and direction == 0:
        #     self.game.playerTurn(position = True, index = int(self.domValue.get()), placement = "L")
        #     self.updateTable()

        # elif domino[1] == leftEnd and direction == 1:
        #     tkMessageBox.showinfo("Error", "Wrong direction!")

        # elif domino[1] == rightEnd and direction == 0:
        #     tkMessageBox.showinfo("Error", "Wrong direction!")

        # elif domino[1] == rightEnd and direction == 1:
        #     self.flip(int(self.domValue.get()))
        #     self.game.playerTurn(position = True, index = int(self.domValue.get()), placement = "R")
        #     self.updateTable()
            
        # # self.game.playerTurn(position = True, index = int(self.domValue.get()), placement = self.dirVar.get())
        # # self.updateTable()

    def initFrame(self):
        ### Author: DUsitn hu
        ### Date: 10-06-2014
        ### Purpose: TO iintalize the frames and option buttons
        ### Input: None
        ### Output: None
        self.dirVar = StringVar()
        self.dirVar.set("L")
        self.dirGroup = LabelFrame(self.root, text = "Direction",
                                   padx = 5, pady = 5)
        self.dirGroup.place(x = 810, y = 100)
        Radiobutton(self.dirGroup, text = "Left", variable = self.dirVar, value = "L").grid(row = 0, sticky = W)
        Radiobutton(self.dirGroup, text = "Right", variable = self.dirVar, value = "R").grid(row = 1, sticky = W)
        

    def flip(self, i):
        ### Author: DUstin Hu
        ### DAte: 10-06-2014
        ### Purpose: To flip the domino at i.
        ### Input: i, an integer to flip at
        ### Output: None
#        print self.game.pHand.dominoes[int(i)]
        try:
            self.game.pHand.dominoes[int(i)].flip()
            self.updateTable()
        except (TypeError, ValueError, IndexError):
            pass
#            tkMessageBox.showinfo("Invalid Input", "Please enter a valid integer between 1 and %s" % str(len(self.game.pHand.dominoes)))
            


    def initInput(self):
        ### Author: Dustin Hu
        ### DAte: 10-06-2014
        ### Purpose: To initalize teh input boxes
        ### input: None
        # ### Output: None
        # self.domNum = StringVar()
        # self.domNum.set("0")

        self.domValue = StringVar()
        self.domValue.set(0)
        Entry(self.root, width = 2, textvariable = self.domValue, justify = RIGHT, validate = 'key', validatecommand = self.vcmd).place(x = 855, y = 75)
        
#        Entry(self.root, width = 2, textvariable = self.domNum, justify = RIGHT).place(x = 850, y= 250)
        
    def updateTable(self):
        ### Author: Dustin Hu
        ### Date: 09-06-2014
        ### Purpose: To update the game
        ### Input: None
        ### Output: None
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(100, 100, 600, 600, outline = "black", fill = "lawn green")
        self.game.pHand.displayHand(65, 10, self.canvas, orientation = "H" )
        self.game.c1Hand.displayHand(20, 65, self.canvas, orientation = "V", faceup = False)
        self.game.c2Hand.displayHand(650, 65, self.canvas, orientation = "V", faceup = False)
        self.game.c3Hand.displayHand(65, 650, self.canvas, orientation = "H", faceup = False)
        self.game.table.drawTable(600, self.canvas)

    def startGame(self):
        ### Author: Dustin Hu
        ### Date: 09-06-2014
        ### purpose: To start the game
        ### Input: None
        ### Output: None
        self.game.startGame()
        
        # if len(self.game.pHand.dominoes) == 6:
        #     self.cpuPlay()
            
        # elif len(self.game.c1Hand.dominoes) == 6:
        #     self.game.cpuTurn(self.game.c2Hand)
        #     ### Insert pause here
        #     self.updateTable()

        #     self.game.cpuTurn(self.game.c3Hand)
        #     ### Inesrt pause here
        #     self.updateTable()
            
        #     self.btnPlayerTurn.config(state = NORMAL)

        # elif len(self.game.c2Hand.dominoes) == 6:
        #     self.game.cpuTurn(self.game.c3Hand)
        #     self.updateTable()
        #     self.btnPlayerTurn.config(state = NORMAL)

        # elif len(self.game.c3Hand.dominoes) == 6:
        #     self.btnPlayerTurn.config(state = NORMAL)
            
            
        self.updateTable()
#        self.checkPlayable()
        self.btnStart.config(state = DISABLED)
        self.btnEndTurn.config(state = NORMAL)
        self.btnPlayerTurn.config(state = NORMAL)
        self.playable = True

    def cpuTurn(self, hand):
        self.game.cpuTurn(hand)
        time.sleep(random.randint(1, 6))
        self.updateTable()

    def initButtons(self):
        ### Author: Dustin Hu
        ### Date: 09-06-2014
        ### Purpose: To initalize the buttons
        ### Input: None
        ### Output: None
        self.btnReset = Button(self.root, text = "Reset Game", state = DISABLED, command = lambda:self.resetGame())
        self.btnReset.place(x = 750, y = 250)
        self.btnEndTurn = Button(self.root, text = "End turn", state = DISABLED, command = lambda:self.cpuPlay())#.place(x = 800, y = 200)
        self.btnEndTurn.place(x = 750, y = 200)
        self.btnStart = Button(self.root, text = "Start Game", command = lambda:self.startGame())
        self.btnStart.place(x = 750, y = 25)
        self.btnPlayerTurn = Button(self.root, text = "Play", state = DISABLED,  command = lambda:self.playerTurn())
        self.btnPlayerTurn.place(x = 750, y = 100)
#        Button(self.root, text = "Flip", command = lambda:self.flip(self.domNum.get()) ).place(x = 775, y = 100)
        #.(x = 775, y = 100)

        # #################### CREATE A PLAYER TURN BUTTON HERE AND THEN .place() IT IN STARTGAME.
        

        # Button(self.root, text = "CpuTurn 1", command = lambda:self.cpuTurn(self.game.c1Hand)).place(x = 100, y = 750)
        # Button(self.root, text = "CpuTurn 2", command = lambda:self.cpuTurn(self.game.c2Hand)).place(x = 200, y = 750)
        # Button(self.root, text = "CpuTurn 3", command = lambda:self.cpuTurn(self.game.c3Hand)).place(x = 300, y= 750)
        # Button(self.root, text = "PlayerTurn", command = lambda:self.cpuTurn(self.game.pHand)).place(x = 400, y= 750)

        
    def initLabels(self):
        ### AUthor: Dustin Hu
        ### DAte: 05-06-2014
        ### Purpsoe: To initalize the labels in this game
        ### Input: None
        ### Output: None
        Label(self.root, text = "Player", background = "green", fg = "yellow").place(x = 325, y = 75)
        Label(self.root, text = "CPU 1", background = "green", fg = "yellow").place(x = 25, y = 75)

        Label(self.root, text = "CPU 3", background = "green", fg = "yellow").place(x = 325, y = 610)
#        Label(self.root, text = "CPU2", background = "green").place(x = 60, y = 300)
        Label(self.root, text = "CPU2", background = "green", fg = "yellow").place(x = 650, y = 75)


#        Label(self.root, text = "Flip Domino:").place(x = 725, y = 75)
        Label(self.root, text = "Domino to Play:").place(x = 750, y = 75)
    

    def initTable(self):
        ### Author: DUstin Hu
        ### Date: 05-06-2014
        ### Purpsoe: To initalize the table of the game
        ### Input: Nonep
        ### Output: None
        self.canvas.create_rectangle(100, 100, 600, 600, outline = "black", fill = "lawn green")
        # self.TCanvas = Canvas(self.root, width = 500, height = 500)
        # self.TCanvas.place(x= 100, y = 100)
        # self.TCanvas.config(background = "lawn green")

    def initGame(self):
        ### Author: Dustin Hu
        ### DAte: 05-06-2014
        ### Purpose: To setup the game itself, creates the dominogame, the hand, the table.
        ### Input: None
        ### Output: None
        self.game = dominogame.DominoGame()
        self.game.pHand.displayHand(65, 10, self.canvas, orientation = "H" )
        self.game.c1Hand.displayHand(20, 65, self.canvas, orientation = "V", faceup = False)
        self.game.c2Hand.displayHand(650, 65, self.canvas, orientation = "V", faceup = False)
        self.game.c3Hand.displayHand(65, 650, self.canvas, orientation = "H", faceup = False)
        self.initTable()
        self.playable = True 


    def initCanvas(self):
        ### Author: DUstin Hu
        ### Date: 04-06-2014
        ### Purpose: To initalize teh canvas
        ### Input: None
        ### Output: None
        self.canvas = Canvas(self.root, width = 725, height = 725)
        self.canvas.place(x = 0, y = 0)
        self.canvas.config(background = "green")
        self.initTable()
        self.canvas.bind("<Button-1>", self.clickMove)

        
    def initRoot(self):
        ### Author: Dustin Hu
        ### Date: 04-05-2014
        ### Purpose: To initalize the root of this game, along with the menu bar
        ### Input: None
        ### OUtput: None
        self.root = Tk()
        self.root.geometry("900x725")
        self.root.title("Dominoes")
        

        self.menubar = Menu(self.root)
        
        self.filemenu = Menu(self.menubar, tearoff = 0)
        self.filemenu.add_command(label = "Exit", command = lambda:self.root.destroy())

        self.menubar.add_cascade(label = "File", menu = self.filemenu)

        self.helpMenu = Menu(self.menubar, tearoff = 0)
        self.helpMenu.add_command(label = "Help", command = lambda:self.getHelp())
        self.helpMenu.add_command(label = "About", command = lambda:self.getAbout())
        self.helpMenu.add_command(label = "Scores", command = lambda:self.showScore())

        self.menubar.add_cascade(label = "Help", menu = self.helpMenu)


        self.root.config(menu = self.menubar)
        
    def __init__(self):
        ### Author: Dustin Hu
        ### DAte: 04-06-2014
        ### Purpose: To initalize the app of dominogame
        ### Input: None
        ### Output: None
        self.currX = 30
        self.currY = 30
        self.initRoot()
        self.vcmd = (self.root.register(self.validate),
                "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")

#        self.vcmd = (self.root.register(self.validate), "%d", "%i", "%P", "%S", "%v", "%V", "%W")
        self.initCanvas()
        # Keep initGame below initCanvas
        self.initGame()
        self.initLabels()
        self.initButtons()
        self.initInput()
        self.initFrame()
        self.played = 0
        self.playable = False
        self.clickedDomino = -1
#        Entry(self.root, width = 2, textvariable = self.domValue, justify = RIGHT, validate = 'key', validatecommand = vcmd).place(x = 850, y = 75)

        self.root.mainloop()

