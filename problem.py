from player import Player


class Problem:

    def __init__(self,players,roles,teams,budget,nPlayersRequired,nPlayersPerRole,extraPlayers,maxNPlayersOfATeam,minTeamsRepresented):
        self.players = players
        self.teams = teams
        self.roles = roles
        self.nPlayersRequired = nPlayersRequired
        self.nPlayersPerRole = nPlayersPerRole
        self.extraPlayers = extraPlayers
        self.maxNPlayersOfATeam = maxNPlayersOfATeam
        self.minTeamsRepresented = minTeamsRepresented
        self.budget = budget
        
    def getTeamSize(self,team):
        size = 0
        for p in self.players:
            if p.team == team:
                size = size + 1
        return size

    def printInfo(self):
        print "++++ PLAYERS ++++++++"
        for player in self.players:
            player.printInfo()
        print "++++ TEAMS ++++++++"
        for team in self.teams:
            print team
        print "++++ ROLES ++++++++"
        for role in self.roles:
            print role
        print 'Required ',self.nPlayersRequired
        for role,number in self.nPlayersPerRole.items():
            print role,' -> ',number
        print 'Extras ', self.extraPlayers
        print 'For a team ',self.maxNPlayersOfATeam
        print 'Teams Represented ',self.minTeamsRepresented
        print 'Budget ', self.budget

        
        
