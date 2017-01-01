#Declare a super class constraint
class Constraint(object):
    def __init__(self):
        pass
    
    def is_satisfied(self):
        pass
    
    def reduction(self):
        pass

#The declare and implement each subclass 
class Constraint_equality_var_var(Constraint):
    '''This class takes in two variable parameters, finds the common values between them, and sets both 
    of the variables domains to only include those shared values'''
    def __init__(self, var1, var2):
        self.A = var1
        self.B = var2
        
    def is_satisfied(self):
        result = False
        if self.A.checkCommonValue(self.B):
            #reduce variable domains
            result = self.reduction()
        return result
    
    def reduction(self):
        #create a list of common Variables
        a = []
        for i in self.A.getDomain():
            if i in self.B.getDomain():
                a.append(i)
                
        #TODO: May have to revisit this check
        if len(a) == 0:
            return False
        
        self.A.setDomain(a)
        self.B.setDomain(a)
        
        return True
    
class Constraint_equality_var_cons(Constraint):
    '''This class takes in a constant and a variable as parameters. If the constant exists in the variables domain,
    the domain will be set to conatain just that constant'''
    def __init__(self, var1, constant):
        self.A = var1
        self.C = constant
        
    def is_satisfied(self):
        result = False
        if self.C in self.A.getDomain():
            #C is in A, therefore reduce
            result = self.reduction()
        return result
    
    def reduction(self):
        self.A.setDomain([self.C])
        
        if len(self.A.getDomain()) == 0:
            return False
        else:
            return True
        
class Constraint_equality_var_plus_cons(Constraint):
    '''This is a special class constraint that is only used once in the solver, primarily to satisfy the 
    green = ivory + 1 constraint'''
    def __init__(self, var1, var2, constant):
        self.A = var1
        self.B = var2
        self.C = constant
        
    def is_satisfied(self):
        #check if there is value in b such that a=b+c
        result = False
        for b in self.B.getDomain():
            if (b + self.C) in self.A.getDomain():
                #check complete, reduce
                result = self.reduction()
        return result
    
    def reduction(self):
        #store the values that meet the criteria in a list and 
        #assign the value of those lists to the variables
        av = []
        for x in self.A.getDomain():
            for b in self.B.getDomain():
                if b + self.C == x:
                    av.append(x)
                    break;
        bv = []     
        for x in self.B.getDomain():
            for a in self.A.getDomain():
                if a - self.C == x:
                    bv.append(x)
                    break;
                             
        self.A.setDomain(av)
        self.B.setDomain(bv)
        if (len(self.A.getDomain()) == 0 or len(self.B.getDomain()) == 0):
            return False
        else:
            return True
        
class Constraint_difference_var_var(Constraint):
    '''This class constraint is used to make sure that no two domains of the same category have equivalent single
    value domains'''
    def __init__(self, var1, var2):
        self.A = var1
        self.B = var2
        
    def is_satisfied(self):
        result = False
        #check if they are both the same length
        if len(self.A.getDomain()) == 1 and len(self.B.getDomain()) == 1:
            if self.A.getDomain() == self.B.getDomain():
                return result
        
        result = self.reduction()
        return result
        
        
    def reduction(self):
        #case for a
        a = self.A.getDomain()
        b = self.B.getDomain()
        if len(self.B.domain) == 1:
            if b[0] in self.A.getDomain():
                self.A.domain.remove(self.B.domain[0])
            
        #case for b
        elif len(self.A.domain) == 1:
            if a[0] in self.B.getDomain():
                self.B.domain.remove(self.A.domain[0])
                
        if len(self.A.domain) == 0 or len(self.B.domain) == 0:
            return False
        else:
            return True
                
class constraint_difference_var_plus_cons(Constraint):
    '''This class is used to replicate the 'next to constraint' such as |cluedo - horse| = 1.'''
    def __init__(self, var1, var2):
        self.A = var1
        self.B = var2
        
    def is_satisfied(self):
        result = False
        for i in self.A.getDomain():
            for x in self.B.getDomain():
                if abs(i-x) == 1:
                    return self.reduction()
        return result
    
    def reduction(self):
        a = []
        
        for x in self.A.getDomain():
            #print(x)
            for i in self.B.getDomain():
                if abs(x-i) == 1 and i not in a:
                    a.append(i)
                    
        a = sorted(a)
        
        if len(a) == 0:
            return False
        else:
            self.B.setDomain(a)
        
        
            