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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** Our Code Starts Here ***"

        # The idea is to get that if a position is close from food, we return a high value and if it is far, a small
        # value. We also have to consider the ghosts. If there are a ghost nearby a position, we should give it less
        # points.

        # Level of fear that the pacman will feel towards the ghosts. It is also the range of vision of the pacman
        fearLevel = 4



        closestFood = None
        disClosestFood = None

        ghostsNearby = False

        # We store in food the x,y values for the closest food
        for food in currentGameState.getFood().asList():

            if disClosestFood > manhattanDistance(food, currentGameState.getPacmanPosition()) or disClosestFood == None:
                closestFood = food

        # Distance from closest food to the evaluated position
        disClosestFood = manhattanDistance(closestFood, newPos)


        # Value that reflects how safe a position is, depending on the ghosts
        safeness = 0

        # fearLevel is a variable that represents how far the pacman will consider that a ghost is dangerous.
        # If the distance between the evaluated position and the ghosts surpasses the fear level, the ghost will
        # be ignored.
        # A low FearLevel means that the pacman will not change its behaviour unless the ghost is really close.

        # If the distances betweem the ghosts and the new positions are long, this will reflect on a high level
        # of safeness

        for ghost in newGhostStates:
            if manhattanDistance(newPos, ghost.getPosition()) <= fearLevel:

                safeness += manhattanDistance(newPos, ghost.getPosition())

                ghostsNearby = True

        if ghostsNearby:

            # The level of safeness minus the distance to the closest food gives us an idea of how good this
            # choice is.
            return safeness - disClosestFood

        elif newPos == currentGameState.getPacmanPosition():

                #If the Pacman Was not going to move, now it will move for sure
                return -999

        else:

            # If there are no ghosts nearby, the position with has food the closest will get a higher score
            return 70 - disClosestFood

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
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

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
      Your minimax agent (question 2)
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

        "*** Our Code Starts Here ***"

        # We get the PacMan Legal actions
        legalMoves = gameState.getLegalActions(0)

        # For now, we asume that the best direction for the PacMan is to stay still
        bestMove = Directions.STOP

        # We execute the first max manually
        topScore = -9999999

        # For every possible move of the PacMan, we chose the one with the best score and we return its move
        for move in legalMoves:

            scoreTemp = max(topScore, self.minval(gameState.generateSuccessor(0, move), self.depth, 1))
            if scoreTemp > topScore:
                topScore = scoreTemp
                bestMove = move
        return bestMove


    # For every possible move of every ghost agent, we return the min score of the potential move
    def minval(self, gameState, depth, agent):

        result = 99999999

        if gameState.isLose() or gameState.isWin() or depth <= 0:
            return self.evaluationFunction(gameState)

        # We update the variable result with every ghost
        if agent != gameState.getNumAgents() - 1:
            legalMoves = gameState.getLegalActions(agent)

            # For every posible move of the agent, we update resutl with the one with the minimum value
            for move in legalMoves:
                result = min(result, self.minval(gameState.generateSuccessor(agent, move), depth, agent + 1))

        # When we reach the last ghost, we return the min option depending on the PacMan best choice for every of its
        # Potential Moves
        elif agent == gameState.getNumAgents() - 1:
            legalMoves = gameState.getLegalActions(agent)
            for move in legalMoves:
                result = min(result, self.maxval(gameState.generateSuccessor(agent, move), depth - 1))

        return result


    # We return the best of the moves taking into account the next move of ghosts
    def maxval(self, gameState, depth):

        result = -99999999

        if gameState.isLose() or gameState.isWin() or depth <= 0:
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(0)
        for move in legalMoves:
            result = max(result, self.minval(gameState.generateSuccessor(0, move), depth, 1))
        return result

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** Our Code Starts Here ***"

        # This algirithm is esentially the same as in exercise two, with the only difference of the inclusion of alpha
        # and beta and the pruning when beta is higher than

        legalMoves = gameState.getLegalActions(0)

        bestMove = Directions.STOP
        score = -9999999
        alpha = -9999999
        beta = 9999999
        for move in legalMoves:
            scoreprov = max(score, self.min(gameState.generateSuccessor(0, move), self.depth, 1, alpha, beta))
            if scoreprov > score:
                score = scoreprov
                bestMove = move
            if score > beta:
                return bestMove
            alpha = max(score, alpha)
        return bestMove

    def min(self, gameState, depth, agent, alpha, beta):

        if gameState.isLose() or gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)
        result = 99999999
        if agent != gameState.getNumAgents() - 1:
            legalMoves = gameState.getLegalActions(agent)
            for move in legalMoves:

                result = min(result, self.min(gameState.generateSuccessor(agent, move), depth, agent + 1, alpha, beta))
                if result < alpha:
                    return result
                beta = min(beta, result)
        elif agent == gameState.getNumAgents() - 1:   
            legalMoves = gameState.getLegalActions(agent)
            for move in legalMoves:
                result = min(result, self.max(gameState.generateSuccessor(agent, move), depth - 1, alpha, beta))
                if result < alpha:
                    return result
                beta = min(beta, result)
        return result



    def max(self, gameState, depth, alpha, beta):
        if gameState.isLose() or gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)
        result = -99999999
        legalMoves = gameState.getLegalActions(0)
        for move in legalMoves:
            result = max(result, self.min(gameState.generateSuccessor(0, move), depth, 1, alpha, beta))
            if result > beta:
                return result
            alpha = max(alpha, result)
        return result



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your s expectimax agent (question 4)
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
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

