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
import heapq
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
        newGhostStates = successorGameState.getGhostStates()
        oldFood = currentGameState.getFood()           
        score = successorGameState.getScore()
        
            
            
    
        for ghost in newGhostStates:
                d=manhattanDistance(ghost.getPosition(), newPos)
                if(ghost.scaredTimer>1):
                    if(d<=3):
                        score+=200
                    else:
                        score+=10.0/d
                else:
                    if (d<=3):
                        score = score-400
                 
        for capsule in currentGameState.getCapsules():
                d=manhattanDistance(capsule,newPos)
                if(d<=0):
                    score+=100
                else:
                    score+=5.0/d    
        for x in xrange(oldFood.width):
                for y in xrange(oldFood.height):
                    if(oldFood[x][y]):
                        d=manhattanDistance((x,y),newPos)
                        if(d==0):
                            score += 50
                        elif(d==1):
                            score += 20
                        elif(d==2):
                            score += 10
                        else:
                            score += 1.0/(d*d)
                        
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
        
        "[Project 3] YOUR CODE HERE"       
        ans = Directions.STOP
        value = -(float("inf"))
        pacman_action = gameState.getLegalActions()
        for action in pacman_action:
          prevalue = value
          succ=gameState.generateSuccessor(0, action)
          value = max(value, self.minmax_void(succ, self.depth, 1))
          
          if value > prevalue:
              ans = action

        return ans
  
    def minmax_void(self,gameState, depth, agent_num):
        if gameState.isWin() or gameState.isLose() or depth == 0:
               return self.evaluationFunction(gameState)
        legal_action=gameState.getLegalActions(agent_num)
        num_agent= gameState.getNumAgents()
        if agent_num==0:
           val = -(float("inf"))
           for action in legal_action:
                   succ=gameState.generateSuccessor(agent_num, action)
                   val = max(val, self.minmax_void(succ, depth, 1))
           return val
        else:
           val = float("inf")
           for action in legal_action:
                   succ=gameState.generateSuccessor(agent_num, action)
                   if agent_num == num_agent - 1:
                         val = min(val, self.minmax_void(succ, depth - 1,0))
                   else:
                         val = min(val, self.minmax_void(succ, depth, agent_num + 1))
           return val
             



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        
        "[Project 3] YOUR CODE HERE"        
        ans = Directions.STOP
        value = -(float("inf"))
        a=-(float("inf"))
        b=float("inf")
        pacman_action = gameState.getLegalActions()
        for action in pacman_action:
          prevalue = value
          succ=gameState.generateSuccessor(0, action)
          value = max(value, self. minmax_void(succ, self.depth, 1,a,b))
          a = max(a, value)
          if value > prevalue:
              ans = action
          if value >= b:
              return ans
          

        return ans
    
    def minmax_void(self,gameState, depth, agent_num,a,b):
        if gameState.isWin() or gameState.isLose() or depth == 0:
               return self.evaluationFunction(gameState)
        legal_action=gameState.getLegalActions(agent_num)
        num_agent= gameState.getNumAgents()
        if agent_num==0:
           val = -(float("inf"))
           for action in legal_action:
                   succ=gameState.generateSuccessor(agent_num, action)
                   val = max(val, self.minmax_void(succ, depth, 1,a,b))
                   if val > b:
                       return val
                   a = max(a, val)
           return val
        else:
           val = float("inf")
           for action in legal_action:
                   succ=gameState.generateSuccessor(agent_num, action)
                   if agent_num == num_agent - 1:
                         val = min(val, self.minmax_void(succ, depth - 1,0,a,b))
                   else:
                         val = min(val, self.minmax_void(succ, depth, agent_num + 1,a,b))
                   b = min(b, val)
                   if val < a:
                       return val
                
           return val
        util.raiseNotDefined()



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

def betterEvaluationFunction(currentGameState):
  """
  
    
  """
  "*** YOUR CODE HERE ***"
  foodDist=[]
  capDist=[]
  currPos = currentGameState.getPacmanPosition()
  if currentGameState.isWin():
      return float("inf")
  if currentGameState.isLose():
      return - float("inf")
  score = scoreEvaluationFunction(currentGameState)
  newFood = currentGameState.getFood()
  foodPos = newFood.asList()
  capPos = currentGameState.getCapsules()
  foodNum = 0
  capv=0
  for cap in capPos:
      pactocap = 3+manhattanDistance(cap, currPos)
      capDist.append(-1*pactocap)
  
  if not foodDist:
      capDist.append(0)
      
  capv = max(capDist)    
      
  for food in foodPos:
      pactofood = manhattanDistance(food, currPos)
      foodDist.append(-1*pactofood )
      foodNum= foodNum+1
        
  if not foodDist:
      foodDist.append(0)    
  
  if foodNum > 6 :   
      d = heapq.nlargest(3,foodDist)  
      dist = 0;
      for index in range(0, 3 , 1):
          dist=dist+d[index]
  else :
      dist = max(foodDist)      
      
  
  return dist+capv*0.5+score
      
      
# Abbreviation
better = betterEvaluationFunction


