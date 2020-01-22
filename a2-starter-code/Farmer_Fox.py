'''Farmer_Fox.py
by Saasha Mor
UWNetID: saashm
Student number: 1738927

Assignment 2, in CSE 415, Winter 2020.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

#<METADATA>
SOLUTION_VERSION = "2.0"
PROBLEM_NAME = "Farmer Fox Chicken Grain problem"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Mor']
PROBLEM_CREATION_DATE = "21-JAN-2020"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The <b> Farmer, Fox, Chicken, and Grain.</b> puzzle is a traditional puzzle which goes as follows
A farmer needs to take a fox, chicken and sack of grain across a river using a small
boat. He can only take one of the three items in the boat with him at one time. The
fox must never be left alone with the chicken, and the chicken must never be left alone
with the grain. How can he get everything across the river? 
'''
#
#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
f=0  # array index to access farmer counts
fo=1  # same idea for fox
c=2  # chicken
g=3  # grain
LEFT=0 # same idea for left side of river
RIGHT=1 # etc.

class State():

  def __init__(self, d=None):
    if d==None:
      d = {'people':[[0,0],[0,0],[0,0],[0,0]],
           'boat':LEFT}
    self.d = d
    self.names =['Farmer', 'Fox', 'Chicken', 'Grain']

  def __eq__(self,s2):
    for prop in ['people', 'boat']:
      if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    p = self.d['people']
    txt = "\n"
    for i in range(0, 4):
        txt += self.names[i] +" on LEFT:" + str(p[i][LEFT]) + "\n"
    # right side
    for i in range(0, 4):
        txt += self.names[i] + " on RIGHT:" + str(p[i][RIGHT]) + "\n"
    side='left'
    if self.d['boat']==1: side='right'
    txt += " boat is on the "+side+".\n"
    return txt

    # # LEFT side
    # txt = "\n Farmer on LEFT:" + str(p[f][LEFT]) + "\n"
    # txt += " Fox on LEFT:" + str(p[fo][LEFT]) + "\n"
    # txt += " Chicken on LEFT:" + str(p[c][LEFT]) + "\n"
    # txt += " grain on LEFT:" + str(p[g][LEFT]) + "\n"
    # # right side
    # txt += "\n Farmer on right:" + str(p[f][RIGHT]) + "\n"
    # txt += " Fox on right:" + str(p[fo][RIGHT]) + "\n"
    # txt += " Chicken on right:" + str(p[c][RIGHT]) + "\n"
    # txt += " grain on right:" + str(p[g][RIGHT]) + "\n"
    # # boat
    # side = 'LEFT'
    # if self.d['boat'] == 1: side = 'right'
    # txt += " boat is on the " + side + ".\n"
    # return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.d['people']=[self.d['people'][which_animal][:] for which_animal in [0, 1, 2, 3]]
    news.d['boat'] = self.d['boat']
    return news

  def can_move(self,f1,fo1,c1,g1):
    '''Tests whether it's legal to move the boat and take
     m missionaries and c cannibals.'''
    side = self.d['boat'] # Where the boat is.
    p = self.d['people']
    if f1<1: return False # Need an farmer to steer boat.
    # Asking for more animals than available
    if (p[f][side] < f1) or (p[fo][side] < fo1) or (p[c][side] < c1) or (p[g][side] < g1):
        return False
    f_remaining = p[f][side] - f1
    fo_remaining = p[fo][side] - fo1
    c_remaining = p[c][side] - c1
    g_remaining = p[g][side] - g1
    # fox must never be left alone with the chicken
    # chicken must never be left alone with the grain
    if (f_remaining == 0) and (fo_remaining == 1) and (c_remaining == 1) and (g_remaining == 0):
        return False
    if (f_remaining == 0) and (fo_remaining == 0) and (c_remaining == 1) and (g_remaining == 1):
        return False


  def move(self,f1,fo1,c1,g1):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the boat carrying
     m missionaries and c cannibals.'''
    news = self.copy()      # start with a deep copy.
    side = self.d['boat']         # where is the boat?
    p = news.d['people']          # get the array of arrays of people.
    p[f][side] = p[f][side]-f1     # Remove people from the current side.
    p[fo][side] = p[fo][side]-fo1
    p[c][side] = p[c][side] - c1
    p[g][side] = p[g][side] - g1
    p[f][1-side] = p[f][1-side]+f1 # Add them at the other side.
    p[fo][1-side] = p[fo][1-side]+fo1
    [c][1 - side] = p[c][1 - side] + c1
    [g][1 - side] = p[g][1 - side] + g1
    news.d['boat'] = 1-side       # Move the boat itself.
    return news

def goal_test(s):
  '''If all animals are on the right, then s is a goal state.'''
  p = s.d['people']
  return (p[f][RIGHT]==1 and p[fo][RIGHT]==1 and p[c][RIGHT]==1 and p[g][RIGHT]==1)

def goal_message(s):
  return "Congratulations on successfully guiding everyone across the river!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
# Farmer[left, right], Fox[Left, right], chicken, grain
CREATE_INITIAL_STATE = lambda : State(d={'people':[[1, 0], [1, 0], [1, 0], [1, 0]], 'boat':LEFT })
#</INITIAL_STATE>

#<OPERATORS>

combinations = [(1, 0, 0, 0), (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1)]

OPERATORS = [Operator(
  "Cross the river with "+str(f)+" farmers, "+str(fo) + " foxes, " + str (c)+ " chickens and "+str(g)+" grains",
  lambda s, f1 = f, fo1 = fo, c1=c, g1=g: s.can_move(f1, fo1, c1, g1),
  lambda s, f1 = f, fo1 = fo, c1=c, g1=g: s.move(f1, fo1, c1, g1))
  for (f,fo,c,g) in combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>



