# solutions.py
# ------------
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

'''Implement the methods from the classes in inference.py here'''

import util
from util import raiseNotDefined
import random
import busters
import distanceCalculator

def normalize(self):
    """
    Normalize the distribution such that the total value of all keys sums
    to 1. The ratio of values for all keys will remain the same. In the case
    where the total value of the distribution is 0, do nothing.

    >>> dist = DiscreteDistribution()
    >>> dist['a'] = 1
    >>> dist['b'] = 2
    >>> dist['c'] = 2
    >>> dist['d'] = 0
    >>> dist.normalize()
    >>> list(sorted(dist.items()))
    [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0)]
    >>> dist['e'] = 4
    >>> list(sorted(dist.items()))
    [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0), ('e', 4)]
    >>> empty = DiscreteDistribution()
    >>> empty.normalize()
    >>> empty
    {}
    """
    "*** YOUR CODE HERE ***"
    total = self.total()
    if(total == 0):
        return
    for key in self.keys():##for each key divide its value by total to normalize dictionary
        value = self[key]
        value = value/total
        self[key] = value
    


def sample(self):
    """
    Draw a random sample from the distribution and return the key, weighted
    by the values associated with each key.

    >>> dist = DiscreteDistribution()
    >>> dist['a'] = 1
    >>> dist['b'] = 2
    >>> dist['c'] = 2
    >>> dist['d'] = 0
    >>> N = 100000.0
    >>> samples = [dist.sample() for _ in range(int(N))]
    >>> round(samples.count('a') * 1.0/N, 1)  # proportion of 'a'
    0.2
    >>> round(samples.count('b') * 1.0/N, 1)
    0.4
    >>> round(samples.count('c') * 1.0/N, 1)
    0.4
    >>> round(samples.count('d') * 1.0/N, 1)
    0.0
    """
    "*** YOUR CODE HERE ***"
    random_float = random.random()
    count = 0
    normal_set = self.copy().normalize()
    for key in self.keys():##for each key check if count > random_float, if not add the keys value
        count += self[key]
        if count > random_float:
            return key




def getObservationProb(self, noisyDistance, pacmanPosition, ghostPosition, jailPosition):
    """
    Return the probability P(noisyDistance | pacmanPosition, ghostPosition).
    """
    "*** YOUR CODE HERE ***"
    noisy_none = False
    jail_pos_ghost_pos = False
    if noisyDistance == None:
        noisy_none = True
    if ghostPosition == jailPosition:
        jail_pos_ghost_pos = True
    
    if(noisy_none and jail_pos_ghost_pos):
        return 1.0
    elif(noisy_none or jail_pos_ghost_pos):
        return 0.0
    
    true_distance = distanceCalculator.manhattanDistance(pacmanPosition,ghostPosition)
    return busters.getObservationProbability(noisyDistance, true_distance)





def observeUpdate(self, observation, gameState):
    """
    Update beliefs based on the distance observation and Pacman's position.

    The observation is the noisy Manhattan distance to the ghost you are
    tracking.

    self.allPositions is a list of the possible ghost positions, including
    the jail position. You should only consider positions that are in
    self.allPositions.

    The update model is not entirely stationary: it may depend on Pacman's
    current position. However, this is not a problem, as Pacman's current
    position is known.
    """
    "*** YOUR CODE HERE ***"
    #iterate over all positions
    for position in self.allPositions:
        oberservation_pos = getObservationProb(self,observation,gameState.getPacmanPosition(),position,self.getJailPosition())

        if oberservation_pos == 1: #if we get a one we know that means ghost is in jail position
            self.beliefs[position] = 1 #update to one to avoid multiplication by 0 when the ghost is teleported to jail
        self.beliefs[position] = self.beliefs[position] * oberservation_pos
    self.beliefs.normalize()


def elapseTime(self, gameState):
    """
    Predict beliefs in response to a time step passing from the current
    state.

    The transition model is not entirely stationary: it may depend on
    Pacman's current position. However, this is not a problem, as Pacman's
    current position is known.
    """
    "*** YOUR CODE HERE ***"
    newBeliefs = self.beliefs.copy()  # Initialize an empty distribution for the new beliefs
    for pos in self.allPositions:
        newBeliefs[pos] = 0

    for oldPos in self.allPositions:  # Iterate over all possible previous positions
        newPosDist = self.getPositionDistribution(gameState, oldPos)  # Get the distribution over new positions from oldPos

        for newPos, prob in newPosDist.items():  # For each new position and its probability
            if newPos in self.allPositions:  # Make sure newPos is a valid position
                newBeliefs[newPos] += self.beliefs[oldPos] * prob  # Update the newBeliefs distribution

    newBeliefs.normalize()  # Normalize the new beliefs
    self.beliefs = newBeliefs  # Update the agent's beliefs
