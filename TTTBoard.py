#
# TTTBoard.py
# Handles TicTacToe board and moves
#
# Designed by David Guidos, Sep 2017

from TTTExperiences import Experiences
from random import randint

class Board:
	
	rows = [[0,1,2], [3,4,5], [6,7,8],  # horizontal
			[0,3,6], [1,4,7], [2,5,8],  # vertical
			[0,4,8], [2,4,6]            # diagonal
	]
	emptyBoard = '---------'
	experiences = {}

	# initialize board for new game
	def __init__(self, experiences):
		self.state = self.emptyBoard
		self.moveList = []
		self.computersMoveList = []
		self.playersMoveList = []
		self.experiences = experiences
		self.isGameStarted = False
		self.currentTurn = 'player'
		self.gameOver = False
		self.winner = None					# 'player' or 'computer' if winner found; draw if game tied; None if not started
		self.winningRow = None				# index of winning row

	# determine if game is over
	# sets winner to 'player' or 'computer' if winner found, 'draw' if game tied or None if game isn't over
	def evaluateBoard(self):
		for row in self.rows:
			if self.state[row[0]] == self.state[row[1]] == self.state[row[2]] and self.state[row[0]] != '-':
				if self.state[row[0]] == 'X':
					self.winner = 'player'
				else:
					self.winner = 'computer'
				self.winningRow = row
		if self.winner is None and len(self.moveList) == 9:
			self.winner = 'draw'
			self.winningRow = None
		if self.winner:
			self.gameOver = True

	# place a move onto the board
	# competitor is 'player' or 'computer'
	def placeMove(self, moveSquareIndex, competitor):
		playerMark = 'X' if competitor == 'player' else 'O'
		(state, exp, map) = self.experiences.foundExperienceAndMap(self.state, playerMark)
		updatedState = list(self.state)
		self.moveList.append(moveSquareIndex)
		self.isGameStarted = True
		if competitor == 'player':
			self.playersMoveList.append((self.state, (state, exp, map), moveSquareIndex))
			updatedState[moveSquareIndex] = 'X'
			self.currentTurn = 'computer'
		else:
			self.computersMoveList.append((self.state, (state, exp, map), moveSquareIndex))
			updatedState[moveSquareIndex] = 'O'
			self.currentTurn = 'player'
		self.state = "".join(updatedState)
		self.evaluateBoard()

	# determine next move (computer or player; dependent only on the state)
	def nextMove(self, competitorType):
		playerMark = 'X' if competitorType == 'player' else 'O'
		foundExperience = self.experiences.foundExperienceAndMap(self.state, playerMark)
		(foundExperienceSquareIndex, foundRemap) = self.experiences.bestMove(foundExperience)
		print("Remapped Board: " + Experiences.remappedBoardState(self.state, foundRemap))
		print("Remapped Square: " + str(foundExperienceSquareIndex))
		return (foundExperienceSquareIndex, foundRemap)

	# adjust experiences based on the game outcome and write the experiences to the file
	# competitorType is either 'computer' or 'player'
	def adjustExperiences(self, competitorType):
		# use move list for the specified competitor
		moves = self.computersMoveList if competitorType == 'computer' else self.playersMoveList
		# determine if win, loss or draw for this competitor
		if self.winner == competitorType:
			competitorResult = 'W'
		elif self.winner == 'draw':
			competitorResult = 'D'
		else:
			competitorResult = 'L'
		# loop through move list in reverse order
		correctionMade = False
		print("CompetitorType: " + competitorType + "   Result: " + competitorResult)
		for (state, (s, e, m), square) in reversed(moves):
			remappedSquare = self.experiences.remappedIndex(square, m)
			remappedState = s # Experiences.remappedBoardState(state, m)
			print("State: " + state + "   RemappedState: " + remappedState + "   Square: " + str(square) + "   RMSquare: " + str(remappedSquare) + "   E: " + str(e) + "   Map: " + str(m))
			# update possible move list
			if remappedSquare in e[0] and not correctionMade:
				e[0].remove(remappedSquare)
				if competitorResult == 'W':
					e[1].append(remappedSquare)
					correctionMade = True
				elif competitorResult == 'D':
					e[2].append(remappedSquare)
					correctionMade = True
				elif competitorResult == 'L':
					e[3].append(remappedSquare)
					correctionMade = True
			# update win move list
			elif remappedSquare in e[1] and not correctionMade:
				if competitorResult == 'D':
					e[1].remove(remappedSquare)
					e[2].append(remappedSquare)
					correctionMade = True
				elif competitorResult == 'L':
					e[1].remove(remappedSquare)	
					e[3].append(remappedSquare)	
					correctionMade = True
			# update draw move list
			elif remappedSquare in e[2] and not correctionMade:
				if competitorResult == 'L':
					e[2].remove(remappedSquare)	
					e[3].append(remappedSquare)	
					correctionMade = True
			# apply the updated experiences to the master experiences list
			playerMark = 'X' if competitorType == 'player' else 'O'
			self.experiences.updateExperience(remappedState, e, playerMark)
		
	# write the updated experiences to a file
	def saveExperiences(self):
		self.experiences.toFile()
		


'''

	B O N E Y A R D

		nextMoveSquareIndex = -1
		while nextMoveSquareIndex == -1:
			randomSquareIndex = randint(0, 8)
			if self.state[randomSquareIndex] == '-':
				nextMoveSquareIndex = randomSquareIndex
		remappedIndex = nextMoveSquareIndex
		#if remapIndexList:
		#	remappedIndex = remapIndexList[moveSquareIndex]

		winningMoves = [move for move in possibleMoves if winner(updatedBoard(boardState, move, None, 'computer'))[0] == 'computer']
		possibleMoves = list(set(possibleMoves) - set(winningMoves))

'''

'''
	# place a player move onto the board
	def placePlayerMove(self, moveSquareIndex):
		(state, exp, map) = self.experiences.foundExperienceAndMap(self.state, 'X')
		self.playersMoveList.append((self.state, (state, exp, map), moveSquareIndex))
		updatedState = list(self.state)
		updatedState[moveSquareIndex] = 'X'
		self.state = "".join(updatedState)
		self.moveList.append(moveSquareIndex)
		self.isGameStarted = True
		self.evaluateBoard()
		self.currentTurn = 'computer'

	# place a computer move onto the board
	def placeComputerMove(self, moveSquareIndex):
		(state, exp, map) = self.experiences.foundExperienceAndMap(self.state, 'O')
		self.computersMoveList.append((self.state, (state, exp, map), moveSquareIndex))
		updatedState = list(self.state)
		updatedState[moveSquareIndex] = 'O'
		self.state = "".join(updatedState)
		self.moveList.append(moveSquareIndex)
		self.isGameStarted = True
		self.evaluateBoard()
		self.currentTurn = 'player'
'''
