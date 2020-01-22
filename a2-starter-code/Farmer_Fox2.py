'''Farmer_Fox.py
by Yutong Liu
UWNetID: yliu21
Student number:

Assignment 2, in CSE 415, Autumn 2019.

This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in
# the format shown.
SOLUZION_VERSION = "2.0"
PROBLEM_NAME = "Farmer and fox"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Yutong']
PROBLEM_CREATION_DATE = "10/11/2019"

PROBLEM_DESC = \
    ''' "A farmer needs to take a fox, chicken and sack of grain across a river using a small
    boat. He can only take one of the three items in the boat with him at one time. The
    fox must never be LEFT alone with the chicken, and the chicken must never be LEFT alone
    with the grain. How can he get everything across the river?" '''

LEFT = 0  # same idea for LEFT side of river
RIGHT = 1  # etc.
farmer = 0
fox = 1
chicken = 2
grain = 3


class State():

    def __init__(self, d=None):
        if d == None:
            d = {'passengers': [[0, 0], [0, 0], [0, 0], [0, 0]],
                 'boat': LEFT
                 }
        self.d = d
        self.names =['Farmer', 'Fox', 'Chicken', 'Grain']

    def __eq__(self, s2):
        for prop in ['passengers', 'boat']:
            if self.d[prop] != s2.d[prop]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        p = self.d['passengers']
        txt = "\n"
        for i in range(0, 4):
            txt += self.names[i] + " on LEFT:" + str(p[i][LEFT]) + "\n"
        # right side
        for i in range(0, 4):
            txt += self.names[i] + " on RIGHT:" + str(p[i][RIGHT]) + "\n"
        side = 'left'
        if self.d['boat'] == 1: side = 'right'
        txt += " boat is on the " + side + ".\n"
        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        news.d['passengers'] = [self.d['passengers'][F_F_C_G][:] for F_F_C_G in [0, 1, 2, 3]]
        news.d['boat'] = self.d['boat']
        return news

    def can_move(self, fa, fo, c, g):
        '''Tests whether it's legal to move the boat and take
         farmer, fox, chicken, grain.'''
        side = self.d['boat']  # Where the boat is.
        p = self.d['passengers']

        # farmer always exist
        if fa < 1:
            return False

        # farmer fox chicken grain > available_passengers
        if (p[farmer][side] < fa) or (p[fox][side] < fo) or (p[chicken][side] < c) or (p[grain][side] < g):
            return False

        famer_remaining = p[farmer][side] - fa
        fox_remaining = p[fox][side] - fo
        c_remaining = p[chicken][side] - c
        g_remaining = p[grain][side] - g

        if (famer_remaining == 0) and (fox_remaining == 1) and (c_remaining == 1) and (g_remaining == 0):
            return False
        if (famer_remaining == 0) and (fox_remaining == 0) and (c_remaining == 1) and (g_remaining == 1):
            return False

        return True

    def move(self, fa, fo, c, g):
        '''Assuming it's legal to make the move, this computes
         the new state resulting from moving the boat carrying
         m missionaries and c cannibals.'''
        news = self.copy()  # start with a deep copy.
        side = self.d['boat']  # where is the boat?
        p = news.d['passengers']  # get the array of arrays of passengers.
        # Remove passengers from the current side.
        p[farmer][side] = p[farmer][side] - fa
        p[fox][side] = p[fox][side] - fo
        p[chicken][side] = p[chicken][side] - c
        p[grain][side] = p[grain][side] - g
        # Add them at the other side.
        p[farmer][1 - side] = p[farmer][1 - side] + fa
        p[fox][1 - side] = p[fox][1 - side] + fo
        p[chicken][1 - side] = p[chicken][1 - side] + c
        p[grain][1 - side] = p[grain][1 - side] + g
        news.d['boat'] = 1 - side  # Move the boat itself.
        return news


def goal_test(s):
    '''If all Ms and Cs are on the right, then s is a goal state.'''
    p = s.d['passengers']
    return (p[farmer][RIGHT] == 1 and p[fox][RIGHT] == 1 and p[chicken][RIGHT] == 1 and p[grain][RIGHT])


def goal_message(s):
    return "Congratulations on successfully transfer all passengers from LEFT to right!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <INITIAL_STATE>
CREATE_INITIAL_STATE = lambda: State(d={'passengers': [[1, 0], [1, 0], [1, 0], [1, 0]], 'boat': LEFT})
# </INITIAL_STATE>

# <OPERATORS>
Ffcg_combinations = [(1, 0, 0, 0), (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1)]

OPERATORS = [Operator(
    "Cross the river with " + str(fa) + " farmer and " + str(fo) + " fox and " + str(c) + " chicken and" + str(
        g) + " grain",
    lambda s, Fa=fa, Fo=fo, Ch=c, Gr=g: s.can_move(Fa, Fo, Ch, Gr),
    lambda s, Fa=fa, Fo=fo, Ch=c, Gr=g: s.move(Fa, Fo, Ch, Gr))
    for (fa, fo, c, g) in Ffcg_combinations]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>
