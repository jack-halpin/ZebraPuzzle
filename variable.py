class domain(object):
    def __init__(self):
        self.domain = [1,2,3,4,5]
        
    def printDomain(self):
        print(self.domain)
        
    def split(self):
        #retusn the two halfs of the domain
        a = []
        b = []
        for i in range(0, len(self.domain)//2):
            a.append(self.domain[i])
        for i in range(len(self.domain)//2, len(self.domain)):
            b.append(self.domain[i])
            
        return a,b
    
    def is_empty(self):
        return len(self.domain) == 0
    
    def is_reduced_to_1(self):
        return len(self.domain) == 1
    
class variable(domain):
    def __init__(self, n):
        domain.__init__(self)
        self.name = n
        
    def setDomain(self, newDomain):
        self.domain = newDomain
    
    def getDomain(self):
            return self.domain
    
    def printVariable(self):
        print(self.name, ': ', self.domain)
        
    def checkCommonValue(self, other):
        #Check if variable domain has at least one value in commmon with other variable
        for i in self.domain:
            if i in other.domain:
                return True
            
        return False
    
    
    def __eq__(self, other):
        if len(self.domain) != len(other.domain):
            return False
        else:
            for i in range(len(self.domain)):
                if self.domain[i] != other.domain[i]:
                    return False
        return True
    
    def __ne__(self, other):
        if len(self.domain) != len(other.domain):
            return True
        else:
            for i in range(len(self.domain)):
                if self.domain[i] != other.domain[i]:
                    return True
        return False
    
    
    
    
