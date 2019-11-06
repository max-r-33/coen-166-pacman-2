# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        # Useful information you can extract from a GameState (pacman.py)
        score = 0
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        
        newPos = successorGameState.getPacmanPosition()
        oldPos = currentGameState.getPacmanPosition()
        
        if newPos == oldPos:
            return -15
        
        # calculating new & old food counts
        newFood = successorGameState.getFood()
        newFoodCount, totalManhattanDistanceNew, newAvgMDist = 0, 0, 0
        for r, row in enumerate(newFood): 
            for c, f in enumerate(row):
                if f == True:
                    totalManhattanDistanceNew += manhattanDistance((r,c), newPos)
                    newFoodCount += 1

        oldFood = currentGameState.getFood()
        oldFoodCount, totalManhattanDistanceOld, oldAvgMDist = 0, 0, 0
        for r, row in enumerate(oldFood): 
            for c, f in enumerate(row):
                if f == True: 
                    totalManhattanDistanceOld += manhattanDistance((r,c), newPos)
                    oldFoodCount += 1
        
        newAvgMDist, oldAvgMDist = 0, 0
        if newFoodCount != 0:
            newAvgMDist = totalManhattanDistanceNew / newFoodCount
            oldAvgMDist = totalManhattanDistanceOld / oldFoodCount

        # if we've moved closer to the remaining pellets on average
        if oldAvgMDist - newAvgMDist >= 1:
            score += 30
        elif newAvgMDist < oldAvgMDist:
            score += 25

        # calculating if we moved closer to a ghost
        ghostStates = successorGameState.getGhostStates()
        for state in ghostStates:
            ghostState = state.getPosition()
            scaredTimer = state.scaredTimer
            newManhattanDist = manhattanDistance(ghostState, newPos)
            oldManhattanDist = manhattanDistance(ghostState, oldPos)
            # if we moved further from a ghost, increase score, otherwise decrease it
            if scaredTimer == 0:
                if newManhattanDist <= 1:
                    score -= 500
                if newManhattanDist > oldManhattanDist:
                    score += 5
                elif newManhattanDist < oldManhattanDist and newManhattanDist < 5:
                    score -= 5
            elif scaredTimer > 0:
                if newManhattanDist <= 1:
                    score += 50
                if newManhattanDist < oldManhattanDist:
                    score += 10
                elif newManhattanDist > oldManhattanDist:
                    score -= 7
        
        # increasing score if we consumed a pellet        
        # print(newFoodCount, oldFoodCount)
        if newFoodCount < oldFoodCount:
            score += 50
        
        x, y = newPos[0], newPos[1]
        
        # increasing score if we move next to a pellet
        # left
        if newFood[x-1][y] == 1:
            score += 40
        # right
        if newFood[x+1][y] == 1:
            score += 40
        # up
        if newFood[x][y-1] == 1:
            score += 40
        #down
        if newFood[x][y+1] == 1:
            score += 40

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 9).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

