from constraint import *
from variable import *

import copy

class Problem(object):
    variableSet = []
    no_of_solutions = 0
    def __init__(self, vset=None):
        #If nothing has been passed into the problem, then define a whole new set of variables
        if vset == None:
            self.english = variable('Englishman') #1,1
            self.spanish = variable('Spaniard') #1,2
            self.Ukrain = variable('Ukranian') #1,3
            self.Norway = variable('Norwegian') #1,4
            self.Japan = variable('Japanese') #1,5
            
            self.countries = [self.english, self.spanish, self.Ukrain, self.Norway, self.Japan]
            
            self.red = variable('Red') #2,1
            self.green = variable('Green') #2,2
            self.ivory = variable('Ivory') #2,3
            self.yellow = variable('Yellow') #2,4
            self.blue = variable('Blue') #2,5
            
            self.colors = [self.red, self.green, self.ivory, self.yellow, self.blue]
            
            self.dog = variable('Dog') #3,1
            self.snail = variable('Snails') #3,2
            self.fox = variable('Fox')#3,3
            self.horse = variable('Horse') #3,4
            self.zebra = variable('zebra') #3,5
            
            self.pets = [self.dog, self.snail, self.fox, self.horse, self.zebra]
            
            self.snl = variable('Snakes and Ladders')#4,1
            self.cluedo = variable('Cluedo')#4,2
            self.pictionary = variable('Pictionary')#4,3
            self.ttw = variable('Travel the world')#4,4
            self.backg = variable('Backgammon')#4,5
            
            self.game = [self.snl, self.cluedo, self.pictionary, self.ttw, self.backg]
            
            self.coffee = variable('Coffee')#5,1
            self.tea = variable('Tea')#5,2
            self.milk = variable('Milk')#5,3
            self.oj = variable('Orange Juice')#5,4
            self.water = variable('Water')#5,5
            
            self.drink = [self.coffee, self.tea, self.milk, self.oj, self.water]
            
            #Create  a list containing each category list to store all the variables
            self.variableSet = [self.countries, self.colors, self.pets, self.game, self.drink]
            
        else:
            self.variableSet = vset
    
        #Defining all teh constraints in a list allows to easily iterate over and check each constraint
        self.constraintSet = [Constraint_equality_var_var(self.variableSet[0][0], self.variableSet[1][0]),
                         Constraint_equality_var_var(self.variableSet[0][1],self.variableSet[2][0]),
                         Constraint_equality_var_var(self.variableSet[4][0],self.variableSet[1][1]),
                         Constraint_equality_var_var(self.variableSet[0][2],self.variableSet[4][1]),
                         Constraint_equality_var_plus_cons(self.variableSet[1][1], self.variableSet[1][2], 1),
                         Constraint_equality_var_var(self.variableSet[3][0], self.variableSet[2][1]),
                         Constraint_equality_var_var(self.variableSet[3][1], self.variableSet[1][3]),
                         Constraint_equality_var_cons(self.variableSet[4][2], 3),
                         Constraint_equality_var_cons(self.variableSet[0][3], 1),
                         constraint_difference_var_plus_cons(self.variableSet[2][2],self.variableSet[3][2]),
                         constraint_difference_var_plus_cons(self.variableSet[3][1], self.variableSet[2][3]),
                         Constraint_equality_var_var(self.variableSet[3][3],self.variableSet[4][3]),
                         Constraint_equality_var_var(self.variableSet[0][4],self.variableSet[3][4]),
                         constraint_difference_var_plus_cons(self.variableSet[0][3], self.variableSet[1][4])]
                         #Constraint_difference_var_var(self.variableSet[4][2], self.variableSet[4][3])]
    
    #add the difference constraints using a loop
    
        for i in self.variableSet:
            for x in range(5):
                for y in range(x+1, 5):
                    self.constraintSet.append(Constraint_difference_var_var(i[x], i[y]))
                
    def largest_domain(self):
        #returns the index of the variable with the largest domain in the set
        max_len = 0
        for i in range(5):
            for j in range(5):
                if len(self.variableSet[i][j].getDomain()) > max_len:
                    max_len = len(self.variableSet[i][j].getDomain())
                    x = i
                    y = j
                    
        return x,y
    
    def smallest_domain(self):
        #returns the index of the variable with the smallest domain that has at least 2 values
        min_len = 6
        for i in range(5):
            for j in range(5):
                if len(self.variableSet[i][j].getDomain()) < min_len and len(self.variableSet[i][j].getDomain()) >= 2:
                    min_len = len(self.variableSet[i][j].getDomain())
                    x = i
                    y = j
                    
        return x,y
        
    
    def solve(self):
        '''This is the primary solve function. Calling this goes through each problem constraint. IF a solution
        is found it will print it, if there is an empty domain it will return False otherwise it will begin
        to split the domains to try and solve the problem'''
        solved = False
        change = True
        broken = False
        
        while change == True:
            change = False
            #self.printVariableSet()
            checkset = copy.deepcopy(self.variableSet)
            changed = False
            count = 0
            for i in self.constraintSet:
                if i.is_satisfied() == False:
                        #print("Unsolvable")
                        return False
                    
            #compare the initial set to the new variableset to see if anything is happening
            for x in range(5):
                for y in range(5):
                    if checkset[x][y] != self.variableSet[x][y]:
                        change = True
                        #print(checkset[x][y].name, "is reduced")
                        
            
        
        #check if all variables are reduced to one
        if self.checkSolved():
            print("SOLUTION")
            self.printVariableSet()
            Problem.no_of_solutions += 1
            return True
        else:
            #get the index of the smallest/largest domain
            #x,y = self.smallest_domain()
            x,y = self.largest_domain()
           
            #split the domain and return the two smaller domains
            d1,d2 = self.variableSet[x][y].split()
            
            #create two new subproblems with the current variable set
            sub_problem_1 = Problem(copy.deepcopy(self.variableSet))
            sub_problem_2 = Problem(copy.deepcopy(self.variableSet))
            
            #replace the smallest domain with it's splits
            sub_problem_1.variableSet[x][y].setDomain(d1)
            sub_problem_2.variableSet[x][y].setDomain(d2)

            #solve the two new problems recursively
            sub_problem_1.solve()
            sub_problem_2.solve()

            
    def printVariableSet(self):
        for x in range(5):
            for y in range(5):
                self.variableSet[x][y].printVariable()
                   
    
    def checkSolved(self):
        #this function returns true if all the domains in the variableset only have one vale
        result = True
        for x in range(5):
            for y in range(5):
                
                if self.variableSet[x][y].is_reduced_to_1() == False:
                    result = False
                    
        return result
    
                
    
            
    