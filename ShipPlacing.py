import random
from enum import Enum

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

BATTLEGROUND_SIZE = 10
LIST_OF_SHIPS = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
BATTLEGROUND_GRID = [[0 for i in range(BATTLEGROUND_SIZE)] for j in range(BATTLEGROUND_SIZE)]

random.shuffle(LIST_OF_SHIPS)


class Orientation(Enum):
    VERTICAL = 1,
    HORIZONTAL = 2


def topBorder(x, y):
    matchedCondition = False
    if y == 0:
        if BATTLEGROUND_GRID[x][y] == 0 and BATTLEGROUND_GRID[x][y + 1] == 0 and \
                BATTLEGROUND_GRID[x + 1][y] == 0 and \
                BATTLEGROUND_GRID[x + 1][y + 1] == 0:
            matchedCondition = True

    elif y > 0 and y < BATTLEGROUND_SIZE - 1:
        if BATTLEGROUND_GRID[x][y] == 0 and BATTLEGROUND_GRID[x][y - 1] == 0 and \
                BATTLEGROUND_GRID[x][y + 1] == 0 and \
                BATTLEGROUND_GRID[x + 1][y - 1] == 0 and BATTLEGROUND_GRID[x + 1][y] == 0 \
                and BATTLEGROUND_GRID[x + 1][y + 1] == 0:
            matchedCondition = True

    else:
        if BATTLEGROUND_GRID[x][y] == 0 and BATTLEGROUND_GRID[x][y - 1] == 0 and \
                BATTLEGROUND_GRID[x + 1][y] == 0 and \
                BATTLEGROUND_GRID[x + 1][y - 1] == 0:
            matchedCondition = True
    return matchedCondition


def bottomBorder(x, y):
    matchedCondition = False
    if y == 0:
        if BATTLEGROUND_GRID[x][y] == 0 and BATTLEGROUND_GRID[x][y + 1] == 0 and \
                BATTLEGROUND_GRID[x - 1][y] == 0 and BATTLEGROUND_GRID[x - 1][y + 1] == 0:
            matchedCondition = True
    elif y > 0 and y < BATTLEGROUND_SIZE - 1:
        if BATTLEGROUND_GRID[x][y] == 0 and BATTLEGROUND_GRID[x][y - 1] == 0 and \
                BATTLEGROUND_GRID[x][y + 1] == 0 and \
                BATTLEGROUND_GRID[x - 1][y] == 0 and BATTLEGROUND_GRID[x - 1][y - 1] == 0 and \
                BATTLEGROUND_GRID[x - 1][y + 1] == 0:
            matchedCondition = True
    else:
        if BATTLEGROUND_GRID[x][y] == 0 and BATTLEGROUND_GRID[x][y - 1] == 0 and \
                BATTLEGROUND_GRID[x - 1][y] == 0 and BATTLEGROUND_GRID[x - 1][y - 1] == 0:
            matchedCondition = True
    return matchedCondition


def middleCells(x, y):
    matchedCondition = False
    if y == 0:
        if BATTLEGROUND_GRID[x][y] == 0 and BATTLEGROUND_GRID[x][y + 1] == 0 and BATTLEGROUND_GRID[x + 1][
            y] == 0 and \
                BATTLEGROUND_GRID[x + 1][y + 1] == 0 and BATTLEGROUND_GRID[x - 1][y] == 0 and \
                BATTLEGROUND_GRID[x - 1][y + 1] == 0:
            matchedCondition = True
    elif y > 0 and y < BATTLEGROUND_SIZE - 1:
        if BATTLEGROUND_GRID[x][y] == 0 and BATTLEGROUND_GRID[x][y - 1] == 0 and \
                BATTLEGROUND_GRID[x][y + 1] == 0 and \
                BATTLEGROUND_GRID[x - 1][y] == 0 and BATTLEGROUND_GRID[x - 1][y - 1] == 0 and \
                BATTLEGROUND_GRID[x - 1][y + 1] == 0 and BATTLEGROUND_GRID[x + 1][y] == 0 and \
                BATTLEGROUND_GRID[x + 1][y - 1] == 0 and \
                BATTLEGROUND_GRID[x + 1][y + 1] == 0:
            matchedCondition = True
    else:
        if BATTLEGROUND_GRID[x][y] == 0 and BATTLEGROUND_GRID[x][y - 1] == 0 and \
                BATTLEGROUND_GRID[x - 1][y] == 0 and BATTLEGROUND_GRID[x - 1][y - 1] == 0 and \
                BATTLEGROUND_GRID[x + 1][y] == 0 and BATTLEGROUND_GRID[x + 1][y - 1] == 0:
            matchedCondition = True
    return matchedCondition


def checkConditionsForCell(x, y):
    matchedCondition = False
    if x == 0:
        matchedCondition = topBorder(x, y)

    elif x > 0 and x < BATTLEGROUND_SIZE - 1:
        matchedCondition = middleCells(x, y)

    else:
        matchedCondition = bottomBorder(x, y)

    return matchedCondition


def getPossibleLocationsForShip(ship, shipOrientation):
    possibleLocations = []
    for i in range(BATTLEGROUND_SIZE):
        for j in range(BATTLEGROUND_SIZE):
            if Orientation.HORIZONTAL == shipOrientation:
                if ship - 1 + j < BATTLEGROUND_SIZE:
                    flag = True
                    for k in range(0, ship):
                        if not checkConditionsForCell(i, k + j):
                            flag = False
                            break
                    if flag:
                        possibleLocations.append([i, j])
            else:
                if ship - 1 + i < BATTLEGROUND_SIZE:
                    flag = True
                    for k in range(0, ship):
                        if not checkConditionsForCell(k + i, j):
                            flag = False
                            break
                    if flag:
                        possibleLocations.append([i, j])

    return possibleLocations


def shipPlacing(indexOfShip, Points, shipOrientation):
    ship = LIST_OF_SHIPS[indexOfShip]
    isPlacingSuccessful = False
    while not isPlacingSuccessful:
        if len(Points):
            randomPoint = random.choice(Points)

            if shipOrientation == Orientation.VERTICAL:
                for i in range(ship):
                    BATTLEGROUND_GRID[randomPoint[0] + i][randomPoint[1]] = ship
            else:
                for i in range(ship):
                    BATTLEGROUND_GRID[randomPoint[0]][randomPoint[1] + i] = ship

            if indexOfShip < BATTLEGROUND_SIZE - 1:
                resultOfNextLevelRecursion = attemptToPlaceShipOnBatlleground(indexOfShip + 1)
                if resultOfNextLevelRecursion:
                    isPlacingSuccessful = True
                    break
                else:
                    for i in range(ship):
                        if Orientation.VERTICAL == shipOrientation:
                            BATTLEGROUND_GRID[randomPoint[0] + i][randomPoint[1]] = 0
                        else:
                            BATTLEGROUND_GRID[randomPoint[0]][randomPoint[1] + i] = 0
                    Points.remove(randomPoint)
                    isPlacingSuccessful = False
            else:
                isPlacingSuccessful = True
                break
        else:
            isPlacingSuccessful = False
            break
    return isPlacingSuccessful


def attemptToPlaceShipOnBatlleground(indexOfShip):
    endFlag = False
    horizontalPoints = getPossibleLocationsForShip(LIST_OF_SHIPS[indexOfShip], Orientation.HORIZONTAL)
    verticalPoints = getPossibleLocationsForShip(LIST_OF_SHIPS[indexOfShip], Orientation.VERTICAL)

    randomChoice = random.randint(1, 2)

    if randomChoice == 1:
        endFlag = shipPlacing(indexOfShip, horizontalPoints, Orientation.HORIZONTAL)
    else:
        endFlag = shipPlacing(indexOfShip, verticalPoints, Orientation.VERTICAL)

    if not endFlag and randomChoice == 1:
        endFlag = shipPlacing(indexOfShip, verticalPoints, Orientation.VERTICAL)
    elif not endFlag and randomChoice == 2:
        endFlag = shipPlacing(indexOfShip, horizontalPoints, Orientation.HORIZONTAL)

    return endFlag


def printResultBattlegroundGrid():
    for row in BATTLEGROUND_GRID:
        print('\t'.join([str(elem) for elem in row]))


def showMatplotlibPlot():
    cmap = ListedColormap(['w', 'r', 'g', 'c', 'm', 'y'])
    plt.matshow(BATTLEGROUND_GRID, cmap=cmap)

    y_axis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    plt.yticks(range(len(y_axis)), y_axis)

    x_axis = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    plt.xticks(range(len(x_axis)), x_axis)

    plt.grid(True)
    plt.title('Example of ships placing')
    plt.show()


def main():
    attemptToPlaceShipOnBatlleground(0)
    printResultBattlegroundGrid()
    showMatplotlibPlot()


if __name__ == "__main__":
    main()
