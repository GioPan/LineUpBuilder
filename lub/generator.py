from player import Player
from problem import Problem

class Generator:
                   
    @staticmethod
    def generate(players_file,data_file):

        # Reads the players from the instance file
        players = []
        roles = []
        teams = []
        with open(players_file) as file:
            for line in file:
                role,name, salary, team, projection, duplicateCode = (s for s in line.split())
                if role not in roles:
                    roles.append(role)
                if team not in teams:
                    teams.append(team)
                salary = float(salary)
                projection = float(projection)
                duplicateCode = int(duplicateCode)
                players.append(Player(name,role,salary,team,projection,duplicateCode))
        problem = None
        with open(data_file) as file:
            # Skips the first line
            file.readline()
            nLineUps,nDifferences,budget,nPlayers,gks,dfs,mfs,fws,extras,maxPerTeam,minTeams = (int(s) for s in file.readline().split())
            playersPerRole = {}
            playersPerRole['GK'] = gks
            playersPerRole['D'] = dfs
            playersPerRole['M'] = mfs
            playersPerRole['F'] = fws
            problem = Problem(nLineUps,nDifferences,players,roles,teams,budget,nPlayers,playersPerRole,extras,maxPerTeam,minTeams)            
        return problem
    
