import time
import threading
import scratchattach as scratch3
import os
import keep_alive

keep_alive.keep_alive()

session = scratch3.Session(os.environ['sesid'], username="Server--")
conn = session.connect_cloud("1031977307")

def getLevel():
    with open("level.txt") as file:
        return [l.rstrip("\n") for l in file]

def setLevel(input):
    with open('level.txt', 'w') as file:
        for item in input:
            file.write("%s\n" % item)

def compress(level, start):
    with open("counts.txt") as file:
        counts = [int(l.rstrip("\n")) for l in file]

    i = start
    output = str(start).zfill(4)
    while i < len(level) and len(output) < 256:
        count = 0
        while i + count < len(level) and level[i] == level[i + count]:
            count += 1
        while not(count in counts):
            count -= 1
        count = counts.index(count)

        if len(level[i]) == 2: 
            output += str(count + 50) + level[i][1]
        else:
            if len(str(count)) == 2:
                output += str(count) + level[i]
            else:
                output += "0" + str(count) + level[i]
        i += counts[count]
    return (output, i)

def getChangesForPlayer(PlayerNum, var):
    try:
        Player1 = var[52:]
        if not(Player1 is None):
            level = getLevel()
            for i in range(len(Player1) // 6):
                level[int(Player1[6*i:][0:4])] = str(int(Player1[6*i:][4:6]))
            setLevel(level)
    except TypeError as e:
        return

#import itertools

def resetLevel():
    setLevel("0" * 9999)
    numbers = list(map(str, range(2, 19)))
    cycle_iterator = itertools.cycle(numbers)
    result = [next(cycle_iterator) for _ in range(9999)]
    setLevel(result)

#resetLevel()

print("Ready")

def sendLoop():
    t = 0
    while True:
        j = compress(getLevel(), t)
        if j[1] == 9999:
            t = 0
        else:
            t = j[1]
        conn.set_var("Level1", j[0])

        time.sleep(0.1)

def receiveLoop():
    while True:
        variables = scratch3.get_cloud("1031977307")
        for i in range (1, 5):
            try:
                getChangesForPlayer(str(i), variables["Player" + str(i)])
            except KeyError:
                pass
            except TypeError:
                pass

thread1 = threading.Thread(target=sendLoop)
thread2 = threading.Thread(target=receiveLoop)

thread1.start()
thread2.start()
