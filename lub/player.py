
class Player:
    "Represents a football player"
    def __init__(self,name,role,salary,team,projection,duplicateCode):
        self.name = name
        self.role = role
        self.team = team
        self.projection = projection 
        self.salary = salary
        self.duplicateCode = duplicateCode


    # Printing Methods
    def printInfo(self):
        print "Name: %s, Projection : %.2f, Salary: %.2f, Role: %s, Team: %s" % (self.name,self.projection,
                                                                               self.salary,self.role,self.team)
    

