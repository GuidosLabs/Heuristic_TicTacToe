# CalcTTTStates
# Determine number of unique valid Tic Tac Toe board states
# Designed by David Guidos, Oct 2017

# TODO: eliminate reflections and rotations

import numpy 

rows = [[0,1,2], [3,4,5], [6,7,8],  # horizontal
		[0,3,6], [1,4,7], [2,5,8],  # vertical
		[0,4,8], [2,4,6]            # diagonal
]

def validState(b):
	isValid = True
	# check for incorrect number of X's and O's
	nX = len([s for s in b if s == 'X'])
	nO = len([s for s in b if s == 'O'])
	if numpy.abs(nX - nO) > 1:
		isValid = False
	else:
		# check for invalid winning rows
		wr = []
		for r in rows:
			if b[r[0]] == b[r[1]] and b[r[1]] == b[r[2]] and b[r[0]] != '-':
				wr.append(r)
		if len(wr) > 2:
			isValid = False
		elif len(wr) < 2:
			isValid = True
		else:
			# check if winning row for X and O; impossible
			if b[wr[0][0]] != b[wr[1][0]]:
				isValid = False
			else:
				# two winning rows; check for a square in common
				if len(set(wr[0]) - set(wr[1])) == 3:
					isValid = False	
	return isValid						

stateCount = 0
validCount = 0
board = ['' for _ in range(9)]
for s0 in ('-', 'X', 'O'):
	board[0] = s0
	for s1 in ('-', 'X', 'O'):
		board[1] = s1
		for s2 in ('-', 'X', 'O'):
			board[2] = s2
			for s3 in ('-', 'X', 'O'):
				board[3] = s3
				for s4 in ('-', 'X', 'O'):
					board[4] = s4
					for s5 in ('-', 'X', 'O'):
						board[5] = s5
						for s6 in ('-', 'X', 'O'):
							board[6] = s6
							for s7 in ('-', 'X', 'O'):
								board[7] = s7
								for s8 in ('-', 'X', 'O'):
									board[8] = s8
									stateCount += 1
									if validState(board):
										validCount += 1 
										print("".join(board))

print("Total states: " + str(stateCount - 1))
print("Valid states: " + str(validCount - 1))
print("Valid states with X/O interchange: " + str((validCount - 1) / 2))
#print("Valid states less reflections: " + str((validCount - 1) / 8)

		