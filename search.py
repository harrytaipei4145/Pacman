# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# P2-1
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    "[Project 2] YOUR CODE HERE"
    
    from util import Stack
    from game import Directions
    visited = []
    svisited= []
    s1 = Stack()
    
    coor = Stack()
    move = []
    s=problem.getStartState()
    coor.push(s)
    cur=s
    visited.append(s)
    while True:
          final=0
          if len(move)>=1:
                cur = coor.pop()
                coor.push(cur) 
          else:
                cur = s
          
          if cur not in svisited:  
              successor = problem.getSuccessors(cur)
              s1.push(successor)
              svisited.append(cur)
          else: 
              
              while True:
                  x=s1.pop()
                  s1.push(x)
                  if s1.isEmpty()!=True:
                      x=s1.pop()
                      if x not in svisited:
                          successor=s1.pop()
                          break
                      
          
              
          for group in successor:
              if group[0] not in visited:
                 coor.push(group[0])
                 move.append(group[1])
                 visited.append(group[0])
                 move.append(group[1])
                 coor.push(group[0])
                 if problem.isGoalState(group[0]):
                    move.pop()
                    final=1
                 break
          if final==1:
              
              break;
          coor.pop()
          move.pop()
    return move
    
            
        
        
    
    
    
    util.raiseNotDefined()

# P2-2
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    "[Project 2] YOUR CODE HERE"    
    from util import Queue
    from util import Stack

    ss = Stack()
    q = Queue()
    svisited= []
    s1 = Stack()
    visited = []
    nnn = []
    curr = problem.getStartState()
    q.push(curr)
    visited.append(curr)
    while True: 
        curr = q.pop()
        if problem.isGoalState(curr):
            break
        if curr not in svisited:  
              succ = problem.getSuccessors(curr)
              s1.push(succ)
              svisited.append(curr)
        else: 
              
              while True:
                  x=s1.pop()
                  s1.push(x)
                  if s1.isEmpty()!=True:
                      x=s1.pop()
                      if x not in svisited:
                          succ=s1.pop()
                          break      
        for a in reversed(succ):
            if a[0] not in visited:
                q.push(a[0])
                visited.append(a[0])
                ss.push((curr,a[0],a[1]))

    now = curr
    while True:
        aaa,s,pp= ss.pop()
      #  print pa
        if s == now:

            now = aaa
       #     print 1123
            nnn.append(pp)
        if ss.isEmpty():
            break
    ans = []
    for i in reversed(nnn):
        ans.append(i)
        
    return ans
      
    util.raiseNotDefined()   
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# P2-3
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "print heuristic(problem.getStartState(), problem)"
    
    "[Project 2] YOUR CODE HERE"
    import time
    from util import PriorityQueue
    #print heuristic((33,16), problem)
    visit = []
    coor = PriorityQueue()
    move = PriorityQueue()
    cur = problem.getStartState()
    h= heuristic(cur, problem)
    act=[]
    coor.push(cur,h)
    move.push([],h)
    while True:
        cur=coor.pop()
        act=move.pop()
        

        if problem.isGoalState(cur):
            
            return act

        visit.append(cur)
        successor= problem.getSuccessors(cur)

        for a in successor:
            if not a[0] in visit:
                h=heuristic(a[0], problem)
                act2=act+[a[1]]
                g=problem.getCostOfActions(act2)
                f = g + h
                coor.push( a[0], f)
                move.push( act2, f)
        

    return []


    util.raiseNotDefined()


# Abbreviations
astar = aStarSearch
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
