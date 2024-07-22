import random

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

tLEFT = 1
tRIGHT = -1

#definicia class, umozni nam to vyuzit bodkovu notaciu, napr. point.x
class point(object):
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
    #repr a str umožňňuje vypis oboch suradnic naraz
    #teda print(point) vypise (x, y)
    def __repr__(self):
        return "(%s, %s)" % (self.x, self.y)
    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

def make_point(x, y):
    point = point(x, y)
    return point

class player(object):
    name = ""
    lobby = point(0,0)
    start = point(0,0)
    path = []
    pos = []
    roll = 0
    pawn = 0

    def __init__(self, name, lobby, start, path, pos, roll, pawn):
        self.name = name
        self.lobby = lobby
        self.start = start
        self.path = path
        self.pos = pos
        self.onBoard = roll
        self.pawn = pawn

def make_player(name, lobby, start, path, pos, roll, pawn):
    player = player(name, lobby, start, path, pos, roll, pawn)
    return player

class Dir(object):
    direction = 0
    distance = 0

    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance
  
def make_Dir(direction, distance):
    Dir = Dir(direction, distance)


def createMatrix(row, col, dataList):
    matrix = []
    for i in range(row):
        rowList = []
        for j in range(col):
            rowList.append(dataList[row * i + j])
        matrix.append(rowList)

    return matrix

def tlacsachovnicu(sachovnica):
    print('\n'.join(map(''.join, sachovnica)))
    print()

def gensachovnicu(N):
    #dlzka zakladnej ciary
    LINE = (N//2)-1
    #suradnica stredu sachovnice
    CENTER = (N//2)+1
    #vytvorenie prazdneho listu
    BLANK = [' ' for i in range((N+1)*(N+1))]
    #vytvorenie prazdnej matice
    matrix = createMatrix(N+1, N+1, BLANK)
    #vygenerovanie hviezdiciek
    for i in range(N+1):
        for j in range(CENTER-1, CENTER+2):
            matrix[i][j] = '*'
            matrix[j][i] = '*'
    #vygenerovanie pomocnych cisel
    for i in range(0, N):
        matrix[i+1][0] = str(i%10)
        matrix[0][i+1] = str(i%10)
    #vygenerovanie D
    for i in range(2, N):
        matrix[CENTER][i] = 'D'
        matrix[i][CENTER] = 'D'
    #vygenerovanie X
    matrix[CENTER][CENTER] = 'X'

    return matrix

#funkcia pathGen generuje body drahy hraca
#deje sa to tak, ze posuvny bod "tracer" sa zo startovacieho
#bodu posuva na zaklade povelov v liste PATH_AROUND a PATH_HOME
#elementy listu PATH_AROUND sa skladaju z povelu
#otoc sa vlavo/vpravo (tLEFT/tRIGHT) a z dlzky, ktoru
#treba tymto smerom prejst
#kazdy bod ktorym tracer prejde sa uklada do listu "points"

def pathGen(player, N):
    #dlzka zakladnej ciary
    LINE = (N//2)-1
    #postupnost krokov drahy okolo kriza
    PATH_AROUND = [Dir(tRIGHT, LINE), Dir(tLEFT, LINE), Dir(tRIGHT, 2)]
    #krok pre vkrocenie do domceka
    PATH_HOME = [Dir(tRIGHT, LINE)]
    #definicia jednotkoveho vektora - UP, LEFT, DOWN, RIGHT
    uVector = [point(-1, 0), point(0, -1), point(1, 0), point(0, 1)]
    #do listu bodov ulozi mimocestny bod a startovaci bod
    points = [player.lobby, player.start]
    #nastavi pociatocnu polohu a natocenie "bezca"
    tracer = point(player.start.x, player.start.y)
    arrow = player.direction
    #vygeneruje body drahy okolo kriza zapomoci postupnosti krokov PATH_AROUND
    for i in range(4):
        for i in range(len(PATH_AROUND)):
            arrow += PATH_AROUND[i].direction
            arrow %= 4
            for j in range(PATH_AROUND[i].distance):
                tracer.x += uVector[arrow].x
                tracer.y += uVector[arrow].y
                temp = point(tracer.x, tracer.y)
                points.append(temp)
    #zmaze posledny bod
    del points[-1]
    #posunie bezec na novy posledny bod
    tracer.x = points[-1].x
    tracer.y = points[-1].y
    #prida body drahy domcekov zapomoci kroku PATH_HOME
    arrow += PATH_HOME[0].direction
    for i in range(PATH_HOME[0].distance):
        tracer.x += uVector[arrow].x
        tracer.y += uVector[arrow].y
        temp = point(tracer.x, tracer.y)
        points.append(temp)

    return points

def playerGen(player1, player2, matrix):
    #dlzka zakladnej ciary
    LINE = ((len(matrix)-1)//2)-1
    #vygenerovanie panakov
    for i in range(LINE):
        if(player1.pos[i] != 0):
            matrix[player1.path[player1.pos[i]].x][player1.path[player1.pos[i]].y] = player1.name
        if(player2.pos[i] != 0):
            matrix[player2.path[player2.pos[i]].x][player2.path[player2.pos[i]].y] = player2.name

    return matrix

def pathPrint(points, N):
    #vytvorenie prazdneho listu
    BLANK = [' ' for i in range((N+1)*(N+1))]
    #vytvorenie prazdnej matice
    matPath = createMatrix(N+1, N+1, BLANK)
    #vygenerovanie ocislovanych bodov drahy
    for i in range(len(points)):
        matPath[points[i].x][points[i].y] = str(i%10)
    #vykreslenie bodov drahy
    tlacsachovnicu(matPath)

def roll(player, turn):
    player.roll = random.randint(1, 6)
    print("%3d. tah, %s hodil %d" % (turn+1, player.name, player.roll))
    return 1

def dumpPawn(player, enemy):
    enemy.pos[enemy.pawn] = 0
    print("\t%s vyhodil panaka %s" % (player.name, enemy.name))


def move(rollingPlayer, player, turn, N):
    #dlzka zakladnej ciary
    LINE = (N//2)-1
    MAX_POS = len(rollingPlayer.path)
    TRESHOLD = MAX_POS-1 - LINE
    #dalsiu poziciu ziskame pricitavanim hodu ku aktualnej
    next_pos = rollingPlayer.pos[rollingPlayer.pawn]
    #na zaciatku hry moze hrac hadzat 3x, inokedy uz iba 1x
    if(rollingPlayer.pos[rollingPlayer.pawn] == 0):
        for i in range(3):
            #hod kockou
            turn += roll(rollingPlayer, turn)
            if(rollingPlayer.roll == 6):
                #vypocet novej pozicie panaka
                next_pos += 1;
                break   #ak 6tka padne skor, ako na 3. pokus, cyklus sa prerusi      
    else:
        #hod kockou
        turn += roll(rollingPlayer, turn)
        #vypocet novej pozicie panaka
        next_pos += rollingPlayer.roll
    #kontrola ci nova pozicia nie je mimo drahy
    if((next_pos < MAX_POS)):
        #kontrola ci sa neprekryvaju panaci rovnakeho hraca
        if(friendlyPawnsDontCollide(rollingPlayer, next_pos)):
            #posunutie panaka
            rollingPlayer.pos[rollingPlayer.pawn] = next_pos
            #vyhodenie superovho panaka
            if(enemyPawnsCollide(rollingPlayer, player)):
                dumpPawn(rollingPlayer, player)
            #ak panak skocil do domceka, treba hrat s dalsim
            if(rollingPlayer.pos[rollingPlayer.pawn] > TRESHOLD):
                rollingPlayer.pawn += 1
                     
    return turn

def friendlyPawnsDontCollide(player, pos):
    #panaka stojaceho na mieste netreba kontrolovat
    if(player.pos[player.pawn] != pos):
        #for preto aby sme skontrolovali vsetkych panakov
        for i in range(player.pawn):
            #panakov mimo hry netreba kontrolovat
            if(player.pos[i] != 0):
                #kontrola ci panaci su na rovnakom mieste
                if((player.path[pos].x == player.path[player.pos[i]].x) and
                (player.path[pos].y == player.path[player.pos[i]].y)):
                    return 0

    return 1

def enemyPawnsCollide(player, enemy):

    return ((player.path[player.pos[player.pawn]].x == enemy.path[enemy.pos[enemy.pawn]].x) and (player.path[player.pos[player.pawn]].y == enemy.path[enemy.pos[enemy.pawn]].y))
    

def main():

    N = int(input("velkost sachovnice = "))
    #program vypise chybu pre parne N
    if(N%2 == 0):
        print("chyba! velkost sachovnice musi byt neparna")
        return 0
    #dlzka zakladnej ciary
    LINE = (N//2)-1
    #suradnica stredu sachovnice
    CENTER = (N//2)+1

    pl = []
    pl.append(player("", point(0,0), point(0,0), 0, 0, 0, 0))
    pl.append(player("", point(0,0), point(0,0), 0, 0, 0, 0))

    #nastavenia startovacich parametrov hracov
    pl[0].name = "A"
    pl[0].lobby = point(1, N)
    pl[0].start = point(1, CENTER+1)
    pl[0].direction = RIGHT
    pl[0].pos = [0 for i in range(LINE)]
    pl[0].pos[0] = 1

    pl[1].name = "B"
    pl[1].lobby = point(N, 1)
    pl[1].start = point(N, CENTER-1)
    pl[1].direction = LEFT
    pl[1].pos = [0 for i in range(LINE)]
    pl[1].pos[0] = 1

    pl[0].path = pathGen(pl[0], N)
    pl[1].path = pathGen(pl[1], N)
    #vypis bodov na drahe ocislovanych podla poradia
    #pathPrint(pl[0].path, N)
    #pathPrint(pl[1].path, N)

    mat = []
    mat = gensachovnicu(N)
    mat = playerGen(pl[0], pl[1], mat)
    tlacsachovnicu(mat)

    turn = 0
    Round = 0
    #hra sa dokym niekto neschova vsetkych panakov do domceka
    while(pl[Round%2].pawn < LINE and pl[(Round+1)%2].pawn < LINE):
        Round += 1
        #hrac ide na tah iba ak pred nim super nehodil 6tku
        if(pl[Round%2].roll != 6):
            turn = move(pl[(Round+1)%2], pl[Round%2], turn, N)
            mat = gensachovnicu(N)
            mat = playerGen(pl[(Round+1)%2], pl[Round%2], mat)
            tlacsachovnicu(mat)

main()
