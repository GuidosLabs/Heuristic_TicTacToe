################################
#
#   T I C - T A C - T O E   E X P E R I E N C E S
#

from random import randint

class Experiences:

	# remappings for horizontal, vertical and rotational symmetries
	remapPatterns = [	(False, False, False),
						(True, False, False), 
						(False, True, False), 
						(False, False, True),
						(True, True, False),
						(True, False, True),
						(False, True, True),
						(True, True, True)
	]
	experiencesFileName = "data/TicTacToeExperiences"
	values = {}

	# initialize; get experiences
	def __init__(self):
		self.values = self.fromFile()
		print("Experiences from File: ", self.values)

	def __repr__(self):
		return self.values

	# retrieve experiences from file
	def fromFile(self):
		try:
			with open(self.experiencesFileName, "r") as text_file:
				experienceText = text_file.read()
				experiences = eval(experienceText)
		except:
			experiences = {}
		self.values = experiences
		return experiences

	# save experiences to file
	def toFile(self):
		experiencesText = str(self.values)
		try:
			with open(self.experiencesFileName, "w") as text_file:
				print(experiencesText, file=text_file)
			#print("Experiences written to file: " + experiencesText)
		except:
			alert("ERROR - Problem saving experiences to file.")

	# flip a square index horizontally
	@classmethod
	def flipH(cls, index):
		return [2,1,0,5,4,3,8,7,6][index]

	# flip a square index vertically
	@classmethod
	def flipV(cls, index):
		return [6,7,8,3,4,5,0,1,2][index]

	# rotate a square index clockwise (CCW not needed; it's a CW and a flipH)
	@classmethod
	def rotateCW(cls, index):
		return [6,3,0,7,4,1,8,5,2][index]

	# rotated and reflected square index for a square index using a remap pattern
	# H, V and R are rotations/reflections (horizontal, vertical and rotational-clockwise)
	@classmethod
	def remappedIndex(cls, index, map):
		remappedIndex = index
		if map:
			(H, V, R) = map
			if H:
				remappedIndex = Experiences.flipH(remappedIndex)
			if V:
				remappedIndex = Experiences.flipV(remappedIndex)
			if R:
				remappedIndex = Experiences.rotateCW(remappedIndex)
		return remappedIndex

	# inverse of remappedIndex function
	@classmethod
	def inverseRemappedIndex(cls, index, map):
		remappedIndex = [i for i in range(9) if Experiences.remappedIndex(i, map) == index][0]
		return remappedIndex

	# remapped board state from board state and remap pattern
	# remapPattern is (H, V, R) which are rotations/reflections (horizontal, vertical and rotational-clockwise)
	@classmethod
	def remappedBoardState(cls, boardState, map):
		state = list('         ')
		for index in range(9):
			state[Experiences.remappedIndex(index, map)] = boardState[index]
		return "".join(state)

	# flip board state (X's swapped with O's if playerMark is 'O')
	@classmethod
	def normalizedState(cls, boardState, playerMark):
		nState = boardState
		if playerMark == 'O':
			nState = nState.replace('X', 'x')
			nState = nState.replace('O', 'X')
			nState = nState.replace('x', 'O')
		return nState

	# create a new experience
	# creates possible move list of all open squares, unless one or more of the open squares is a win for the computer,
	# in which case the winning move squares are removed from the list of possible moves and added to the winning moves list.
	# since no games have been played with the new experience, the lose and draw lists are empty.
	@classmethod
	def newExperience(cls, boardState):
		possibleMoves = [i for i in range(9) if boardState[i] == '-']	# empty squares
		winningMoves = []
		drawMoves = []
		losingMoves = []
		experience = (possibleMoves, winningMoves, drawMoves, losingMoves)
		return experience

	# find current board position in experiences list
	# creates new experience if not found and adds it to the list
	# returns index of found/new experience and remap list
	def foundExperienceAndMap(self, boardState, playerMark):
		foundState = None
		foundExperience = None
		foundMap = None
		# find the experience
		nState = Experiences.normalizedState(boardState, playerMark)
		for map in Experiences.remapPatterns:
			if not foundExperience: 
				rmbs = Experiences.remappedBoardState(nState, map)
				try:
					if self.values[rmbs]:
						foundState = rmbs
						foundExperience = self.values[rmbs]
						foundMap = map
				except:
					notFound = True
		if foundExperience is None:
			foundExperience = Experiences.newExperience(nState)
			foundMap = None
			self.values[nState] = foundExperience
			print("NEW: " + boardState + "   " + str(foundExperience))
		return (foundState, foundExperience, foundMap)

	# update experience values
	def updateExperience(self, state, experienceValues, playerMark):
		nState = Experiences.normalizedState(state, playerMark)
		self.values[nState] = experienceValues

	# select the best next move for the computer for the current board position
	# returns remapped square of best move
	@classmethod
	def bestMove(self, experienceAndMap):
		(state, (possibleMoves, winningMoves, drawMoves, losingMoves), map) = experienceAndMap
		# select random empty square from highest non-empty category
		bestSquareRemapped = None
		for category in (possibleMoves, winningMoves, drawMoves, losingMoves):
			if bestSquareRemapped is None and len(category) > 0:
				bestSquareRemapped = category[randint(0, len(category) - 1)]
		bestSquare = Experiences.inverseRemappedIndex(bestSquareRemapped, map)
		print("Best move: ", bestSquare, "   Exp.State: " + str(state), "  Map: " + str(map), "   RemappedSquare: " + str(bestSquareRemapped), "  P: " + str(possibleMoves), "  W: " + str(winningMoves), "  D: " + str(drawMoves), "  L: " + str(losingMoves)) 
		return (bestSquare, map)


	# test mapping
	@classmethod
	def testMap(cls):
		for map in Experiences.remapPatterns:
			for index in range(9):
				remappedIndex = Experiences.remappedIndex(index, map)
				remappedRemappedIndex = Experiences.inverseRemappedIndex(remappedIndex, map)
				print("testMap: " + str(index) + " - " + str(remappedRemappedIndex) + "   Map: " + str(map))

'''

	B O N E Y A R D

	_values = {}
	@property
	def values(self):
		return self._values

	@values.setter
	def values(self, vals):
		self._values = vals


'''