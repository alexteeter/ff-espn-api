from ff_espn_api import League
from getpass import getpass
import os
import json
import properties

def main():
    user = input('Enter username: ')
    password = getpass('Enter password: ')
    try:
        print('Loading league...')
        league = League(properties.league, properties.year, username=user, password=password)
    except:
        cont = input('Try again? (y/n): ')
        if cont == 'y':
            os.system('cls')
            main()
        else:
            exit()
    os.system('cls')
    print('League loaded!\n-------------------------------\n\n')
    week = input("Enter Week (starts at 0): ")
    try:
        int(week)
    except:
        print('Invalid Week value: \"' + str(week) + '\" is not an integer')
        exit()
    lastWeek = 0 ##last weeks poll points, will be gotten from file
    pollScore = 0 ## current week pollscore, written to file
    pollList = []
    scoreList = {}
    
    for team in league.teams:
        lastWeek = readScore(team.team_name, week)
        weeklyScore = team.scores[int(week)]
        print("\n" + str(team.team_name) + "\n" +\
            str(team.wins) + " wins\n" +\
            str(team.losses) + " losses\n" +\
            str(weeklyScore) + " weekly score\n")
        onlinePoll = input("\nOnline Poll Score: ")
        try:
            int(onlinePoll)
        except:
            print('Invalid Poll Score: \"' + str(onlinePoll) + '\" is not a number!' +\
                '\nExiting Program...')
            exit()
        print('-')
        pollScore = (round((lastWeek*.5)+int(onlinePoll)*2+weeklyScore+((team.wins-team.losses)*10),2))
        if properties.debug == 't':
            print('pollScore = ' + str(pollScore) + '\n-----\n')
        pollList.append((pollScore, team.team_name))
        scoreList[team.team_name] = pollScore
    ##write to file
    writeScores(scoreList, week)
    pollList.sort(reverse=True)
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    rank = 0
    for pair in pollList:
        rank += 1
        i = 0
        line = str(rank) + ") "
        for x in pair:
            if i == 1:
                print(line + pair[i] + " " + str(pair[i-1]))
            i += 1

def writeScores(scoreList, week):
    with open('week' + str(week) + '.txt', 'w') as json_file:
        json.dump(scoreList, json_file)

def readScore(teamName, week):
    if int(week) == 0:
        return 0
    else:
        try:
            with open('week' + str(int(week)-1) + '.txt') as j:
                data = json.load(j)
                score = data[teamName]
            if properties.debug == 't':
                print('\nlast week score: ' + str(score))
            return score
        except:
            print('Unable to open Last Week scores. Is week number valid?')
            exit()

main()