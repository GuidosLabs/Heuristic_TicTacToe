# TicTacToe.py
# Program that Learns to Play TicTacToe
# Designed by David Guidos, July 2017

# TODO: Find out why the cursor needs to be moved after the click and before the release to work
#       Probably relates to the window losing focus.

import json
import numpy
import os
#import pyaudio
import pygame
import sys
import time
import subprocess
from TTTBoard import Board
from TTTExperiences import Experiences

################################
#
#   A U D I O
#

## play audio file
#def playAudio(audioFilePathName):
#	global isRaspberryPi
#	if isRaspberryPi:
#		os.system("mplayer " + audioFilePathName)
#	else:
#		return_code = subprocess.call(["afplay", audioFilePathName])



################################
#
#   G A M E   E N G I N E   U I   R O U T I N E S
#

# initialize and start game engine
# returns the screen canvas
def startGameEngine():
	pygame.init( )
    
	# display title on canvas and clear the display
	size = (1000, 600)
	pygame.display.set_caption("Tic Tac Toe")
	screen = pygame.display.set_mode(size)

	# configure keyboard and mouse events
	pygame.event.set_allowed(None)
	pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.KEYDOWN])
    
	# render the surface
	pygame.display.flip()
	return screen

# draw image on board
def drawImage(imageToDraw, position, screen):
	screen.blit(imageToDraw, position)

# get square number (0-8) from game surface X,Y position
# returns -1 if position is not on the board
def squareFromXY(xyPosition):
	(x, y) = xyPosition
	x -= 50
	y -= 50
	if 0 <= x <= 450 and 0 <= y <= 450:
		squareNumber = int(x / 150) + 3 * int(y / 150)
	else:
		squareNumber = -1
	return squareNumber

# get X,Y of center of square from index (0-8)
def XYFromSquare(squareNumber):
	x = int(squareNumber % 3) * 150 + 50 + 75
	y = int(squareNumber / 3) * 150 + 50 + 75
	return (x, y)


# display board
def displayBoard(boardState, message, screen):
	# define colors
	whiteColor = (255,255,255)
	blackColor = (0,0,0)
	blueColor = (0,0,255)

	# clear canvas
	screen.fill(whiteColor)
	clock = pygame.time.Clock()

	# set fonts    
	gameFont = pygame.font.SysFont("monospace", 15)
	gameFont2 = pygame.font.SysFont("monospace", 30)
	gameFont2.set_bold(True)
	gameFont2.set_italic(True)
    
	# create text
	titleLabel = gameFont2.render("Tic Tac Toe", 1, blackColor)
	computerStartsFirstLabel = gameFont.render("Click here for computer to make first move", 1, blackColor)

	# show title
	screen.blit(titleLabel, (165, 10))

	# show computer starts first message if game not already in progress
	# TODO: refactor to use the emptyBoard from board object
	if boardState == '---------':
		screen.blit(computerStartsFirstLabel, (530, 70))
    
	# create X and O images
	xImage = pygame.image.load("images/x.png")
	xImage = pygame.transform.scale(xImage, (135, 135))
	oImage = pygame.image.load("images/o.png")
	oImage = pygame.transform.scale(oImage, (135, 135))

	# show lines
	lineThickness = 8
	lineRect = pygame.draw.line(screen, blueColor, (200, 50), (200, 500), lineThickness)	# left vertical
	lineRect = pygame.draw.line(screen, blueColor, (350, 50), (350, 500), lineThickness)	# right vertical
	lineRect = pygame.draw.line(screen, blueColor, (50, 200), (500, 200), lineThickness)	# top horizontal
	lineRect = pygame.draw.line(screen, blueColor, (50, 350), (500, 350), lineThickness)	# bottom horizontal

	# show computer start button

	# show board state
	for squareNumber, boardPosition in enumerate(boardState):
		# determine X,Y position for a square number
		padding = 10
		pos = ( (50 + 150 * int(squareNumber % 3)) + padding, (50 + 150 * int(squareNumber / 3)) + padding )
		# draw the image
		if boardPosition == "X":
			# draw X
			drawImage(xImage, pos, screen)
		elif boardPosition == "O":
			# draw O
			drawImage(oImage, pos, screen)

	# show message
	messageLabel = gameFont.render(message, 1, blueColor)
	screen.blit(messageLabel, (100, 530))

	# render the surface
	pygame.display.flip()
	pygame.event.pump()

	# log the board state to the console
	print("Board: ", str(boardState))

# display a line on the winning row
def displayWinningLine(winningRow, screen):

	x0, y0 = XYFromSquare(winningRow[0])
	x1, y1 = XYFromSquare(winningRow[2])

	greenColor = (0, 255, 0)
	lineThickness = 21 if x0 != x1 and y0 != y1 else 15		# thicker diagonal because of the angle

	pygame.draw.line(screen, greenColor, (x0, y0), (x1, y1), lineThickness)

	# render the surface
	pygame.display.flip()
	pygame.event.pump()

# adjustable delay for speed control of automatic play
def delayForEffect(delayTimeSeconds):
	time.sleep(delayTimeSeconds)


################################
#
#   R E S U L T S
#

resultsFileName = "data/GameResults.txt"

# save results to a file
def saveResults(resultsString):
	try:
		with open(resultsFileName, "w") as text_file:
			print(resultsString, file=text_file)
		print("Results: " + resultsString)
	except:
		print("ERROR - Problem saving game results to file.")


drawsPer100GamesFileName = "data/DrawsPer100Games.txt"

def saveDrawsPer100(drawsCount):
	try:
		with open(drawsPer100GamesFileName, "w") as text_file:
			print(str(drawsCount), file=text_file)
		print("Results: " + resultsString)
	except:
		print("ERROR - Problem saving draws-per-100-games results to file.")


################################
#
#   G A M E   P L A Y
#

# play a game
def playGame(automaticMode, showGraphics, screen , gamecounter, experiences, message):

	# define game variables
	currentTurn = 'player'
	playerMoveMade = False
	automaticDelayTimeSeconds = 0.001

	# initialize the board
	board = Board(experiences)
	displayBoard(board.state, message, screen)

	# loop playing the game
	while not board.gameOver:

		# tickle the event handler
		pygame.event.pump()

		# get and process any mouse events
		playersSquare = -1
		computersSquare = -1
		message = ''
		for event in pygame.event.get():

			#print("Event: " + str(event))
			if event.type == pygame.MOUSEBUTTONUP:
				# determine square number from the mouse position
				pos = event.pos
				playersSquare = squareFromXY(pos)
				playerMoveMade = True
				message = "POS: " + str(pos)
				# check if click not on board
				if playersSquare == -1:
					# player click not on the board
					playerMoveMade = False
					# if start of game, set computer to start first
					if not board.isGameStarted:
						board.currentTurn = 'computer'
			if event.type == pygame.KEYDOWN:
				# get the square number from the keyboard (1-9)
				playersSquare = int(event.key) - 1
				playerMoveMade = True
				# check if 0 pressed (computer to start with first move)
				if playersSquare == -1:
					playerMoveMade = False
					# if start of game, set computer to start first
					if not board.isGameStarted:
						board.currentTurn = 'computer'

		# check if computer's turn; make move and update board
		if board.currentTurn == 'computer':
			# determine the computer's move
			(computersSquare, map) = board.nextMove(board.currentTurn)
			# pause for effect
			delayForEffect(automaticDelayTimeSeconds)
			# update the board with the computer's new move
			board.placeMove(computersSquare, 'computer')
			# display the player's new move
			if showGraphics:
				displayBoard(board.state, message, screen)
			board.currentTurn = 'player'
		elif playerMoveMade or automaticMode:
			if automaticMode:
				# determine the player's move
				(playersSquare, map) = board.nextMove(board.currentTurn)
			# pause for effect
			delayForEffect(automaticDelayTimeSeconds)
			if playersSquare != -1:
				# check if valid move
				if board.state[playersSquare] == '-':
					# valid move
					# place move onto the board
					board.placeMove(playersSquare, 'player')
					#message = str(board.moveList)
					# display the player's new move
					board.currentTurn = 'computer'
				else:
					# invalid move; update the message
					print("INVALID MOVE: " + str(playersSquare) + "   Map: " + str(map))
					message = "Invalid move. Select an empty square."
					playerMoveMade = False
				if showGraphics:
					displayBoard(board.state, message, screen)

	# game over
	# display the final board
	if board.winner == 'draw':
		if showGraphics:
			message = "The game is a draw."
			displayBoard(board.state, message, screen)
		result = 'D'
	else:
		message = "The " + board.winner + " wins!"
		if showGraphics:
			displayBoard(board.state, message, screen)
		if not automaticMode:
			time.sleep(0.35)
		displayWinningLine(board.winningRow, screen)
		result = 'P' if board.winner == 'player' else 'C'
 
	# adjust experiences based on the outcome
	board.adjustExperiences('computer')
	if automaticMode:
		board.adjustExperiences('player')

	# save the updated experiences to a file
	print("Game: " + str(gamecounter))
	if automaticMode:
		if gamecounter % 100 == 0:
			board.saveExperiences()
	else:
		board.saveExperiences()

	# delay to show the board before resetting for the next game
	if not automaticMode:
		time.sleep(3)
	
	return result


################################
#
# main
#

# start the program
screen = startGameEngine()

# get command line parameters
automaticMode = ('auto' in sys.argv)
showGraphics = ('nographics' not in sys.argv)

# loop playing games
gamecounter = 0
experiences = Experiences()
print("Experience board states: " + str(len(experiences.values)))
results = ""
drawsPer100Text = ""
message = ""
while True:	
	result = playGame(automaticMode, showGraphics, screen, gamecounter, experiences, message)
	results += result
	gamecounter += 1
	if automaticMode:
		# determine and save the instantaneous number of draws / 100 games
		if gamecounter % 100 == 0:
			saveResults(results)
			drawsPer100 = len([r for r in list(results[-100:]) if r == "D"])
			drawsPer100Text += str(drawsPer100) + "\n"
			saveDrawsPer100(drawsPer100Text)
		# check if training completed (1000 games in a row all draws)
		if len(results) > 1000:
			if len([r for r in list(results[-1000:]) if r == "D"]) == 1000:
				# terminate automatic mode
				automaticMode = False
				message = "Training completed."
				
	else:
		saveResults(results)
		message = ""

#
#
#################################

