import dayloop
from time import sleep

def everloop(loop) :
    while loop :
        dayloop.dayloop(loop)
        sleep(60)

if __name__ == '__main__' :
    loop = True
    everloop(loop)
