import main
from time import sleep
import datetime

time_set = ['18:00']
time_today = datetime.datetime.now()

def dayloop(loop) :
    for action_time_set in time_set :

        action_time = datetime.datetime.strptime(str("{0:%Y-%m-%d}".format(time_today)) + ' ' + action_time_set, '%Y-%m-%d %H:%M')

        time_now = datetime.datetime.now()
        if action_time + datetime.timedelta(hours = 2) < time_now :
            continue

        print(f'Next start at {action_time}.')
        print('sleep')
        while action_time > time_now :
            sleep(60)
            time_now = datetime.datetime.now()

        main.main(action_time_set)
        sleep(10)

if __name__ == '__main__' :
    print('Action Day Loop.')
    loop = True
    dayloop(loop)
