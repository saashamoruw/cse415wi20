'''
SBG_Agent.py
Stochastic Simplified Backgammon Agent
By Saasha Mor and Divit Jawa
UWNetID: saashm, divitj
Assignment 3, in CSE 415, Winter 2020.
Version of Backgammon that has simplified rules and
the dice is rolled normally. It uses expectimax.
'''

from backgState import *
from testStates import *


# Define a class for agent
class Agent:
    def __init__(self):
        self.STATES = 0
        self.MAX_PLY = -1

    def __eq__(self, s2):
        for i in range(3):
            for j in range(3):
                if self.b[i][j] != s2.b[i][j]: return False
        return True

    def __str__(self):
        txt = "\n["
        for i in range(3):
            txt += str(self.b[i]) + "\n "
        return txt[:-2] + "]"

    def __hash__(self):
        return (self.__str__()).__hash__()

    def move(self, state, die1, die2):
        ans = self.expectiMiniMax(state=state,
                                  playerMove=state.playerMove,
                                  max_depth=3,
                                  die1=die1,
                                  die2=die2,
                                  depth=0)
        return ans

    # This will be used by an autograder to set a specific limit on
    # the depth of your agent's searches, so that a specific best
    # move can be defined
    def setMaxPly(self, maxply=-1):
        self.MAX_PLY = maxply
    # search algorithms should use this function until called again
    # with None as the value of the function. Then your agent should
    # revert to using your own static evaluation function.
    def useSpecialStaticEval(self, func):
        pass

    # If your agent just assumes the uniform distribution then your
    # implementation of this method can simply "pass" and not do anything.
    def useUniformDistribution(self):
        pass

    def expectiMiniMax(self, state, playerMove, max_depth, die1, die2, depth=0):
        if (depth == max_depth):
            return staticEval(state)
        admissableMoves = findAdmissibleMoves(state, playerMove, die1, die2)
        for m in admissableMoves:
            val = 0
            prev1 = die1
            prev2 = die2
            for die1 in range(1, 7):
                for die2 in range(1, 7):
                    val += calcProbability(die1, die2) * self.expectiMiniMax(
                        updateState(state, m, prev1, prev2, playerMove), 1 - playerMove, max_depth, die1, die2,
                        depth + 1)
                    self.STATES += 1
                    if (m == admissableMoves[0]):
                        best = val
                        best_move = m
                    else:
                        if (playerMove == W):
                            if val > best:
                                best = val
                                best_move = m
                        else:
                            if val < best:
                                best = val
                                best_move = m
        if (depth == 0):
            return best_move
        else:
            return best


def calcProbability(die1, die2):
    return 1.0 / 36


# Will take any state and return a real number, based on whatever
# static evaluation method you design as part of your agent.
# This value should be positive when the state is relatively good for
# the maximizing player (white) and negative when relatively good for
# the minimizing player (red).
def staticEval(state):
    wPos = [i.count(False) for i in state.pointLists]
    wOff = sum([(24 - i[0]) * i[1] for i in enumerate(wPos)])
    rPos = [i.count(True) for i in state.pointLists]
    rOff = sum([(i[0] + 1) * i[1] for i in enumerate(rPos)])
    return (rOff - wOff)


def findAdmissibleMoves(state, playerMove, die1, die2):
    position = [i + 1 for i, e in enumerate(state.pointLists) if e.count(playerMove) > 0]
    combinations = [','.join((str(x), str(y))) for x in position for y in position if x != y]
    dice_list = [die1, die2]
    sameCombi = [','.join((str(x), str(x + d))) for d in dice_list for x in position]
    combinations.extend(sameCombi)
    combinations.append('p')
    passCombi = [','.join((str(x), 'p')) for x in position]
    combinations.extend(passCombi)

    if playerMove in state.bar:
        combinations.append(('0,p'))
        if (state.bar.count(playerMove) == 1):
            bar_combos = [','.join(('0', str(x))) for x in position]
            combinations.extend(bar_combos)
            combinations.append(','.join('0', die1))
            combinations.append(','.join('0', die2))
        else:
            combinations.append('0,0')
    admissible_moves = [i for i in combinations if ifLegalMove(i, state, playerMove, die1, die2)]
    return (admissible_moves)



def ifLegalMove(move, state, playerMove, die1, die2):
    moves = move.split(',')
    if len(moves) == 3 and moves[2] in ['R', 'r']:
        dice_list = [die2, die1]
    else:
        dice_list = [die1, die2]
    if move == 'p':
        return True
    checker1, checker2 = moves[:2]
    tempState = bgstate(state)
    for i in range(2):
        if i == 1 and checker2 == 'p':
            return True
        pt = int([checker1, checker2][i])
        die = dice_list[i]
        if pt == 0:
            if not playerMove in tempState.bar:
                return False

            return ifMoveOffBar(playerMove, die, W, tempState)

        if barCheck(tempState, playerMove):
            return False
        if pt < 1 or pt > 24:
            return False
        if not playerMove in tempState.pointLists[pt - 1]:
            return False

        return ifLegalDest(playerMove, pt, die, die1, die2, checker1, tempState)

    return True

def ifMoveOffBar(playerMove, die, W, tempState):
    if playerMove == W:
        target_point = die
    else:
        target_point = 25 - die
    pointList = tempState.pointLists[target_point - 1]
    if pointList != [] and pointList[0] != who and len(pointList) > 1:
        return False
    return True

def ifLegalDest(playerMove, pt, die, die1, die2, checker1, tempState):
    if playerMove == W:
        dest_pt = pt + die
    else:
        dest_pt = pt - die
    if dest_pt > 24 or dest_pt < 1:
        return bearingCheck(tempState, playerMove)
    dest_pt_list = tempState.pointLists[dest_pt - 1]
    if len(dest_pt_list) > 1 and dest_pt_list[0] != playerMove:
        return False
    if (i == 0):
        tempState = updateState(tempState, ','.join((checker1, 'p')), die1, die2, playerMove)

def updateState(state, m, die1, die2, playerMove):
    tempState = bgstate(state)
    moves = m.split(',')
    if (len(moves) == 1):
        return state
    pos1 = int(moves[0])
    if (moves[1] == 'p'):
        tempState.pointLists[pos1 - 1].pop()
        dest1 = getDest(pos1, die1, playerMove)
        if (dest1 > 24 and playerMove == W):
            tempState.white_off.append(playerMove)
        elif (dest1 < 1 and playerMove == R):
            tempState.red_off.append(playerMove)
        else:
            tempState.pointLists[dest1 - 1].append(playerMove)
        return tempState
    if (len(moves) == 3):
        pos2 = pos1
        pos1 = int(moves[1])
    else:
        pos2 = int(moves[1])
    dest1 = getDest(pos1, die1, playerMove)
    dest2 = getDest(pos2, die2, playerMove)
    tempState.pointLists[pos1 - 1].pop()
    if (dest1 > 24 and playerMove == W):
        tempState.white_off.append(playerMove)
    elif (dest1 < 1 and playerMove == R):
        tempState.red_off.append(playerMove)
    else:
        tempState.pointLists[dest1 - 1].append(playerMove)
    tempState.pointLists[pos2 - 1].pop()
    if (dest2 > 24 and playerMove == W):
        tempState.white_off.append(playerMove)
    elif (dest2 < 1 and playerMove == R):
        tempState.red_off.append(playerMove)
    else:
        tempState.pointLists[dest2 - 1].append(playerMove)
    return tempState


def getDest(pos, die, playerMove):
    return (pos + die) if (playerMove == W) else (pos - die)


def bearingCheck(state, who):
    if barCheck(state, who): return False
    if who == W:
        pointsRange = range(0, 18)
    else:
        pointsRange = range(6, 24)
    pl = state.pointLists
    for i in pointsRange:
        if pl[i] == []: continue
        if pl[i][0] == who: return False
    return True


def barCheck(state, who):
    return who in state.bar