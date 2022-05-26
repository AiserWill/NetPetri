import json
import math

import pygame
from pygame.font import Font

import widget

def checkPlusPlace(pos):
    if (965 <= pos[0] <= 1065) and (160 <= pos[1] <= 210):
        return True
    return

def checkClear(pos):
    if (1075 <= pos[0] <= 1175) and (220 <= pos[1] <= 270):
        return True
    return False


def checkPlusTrans(pos):
    if (1075 <= pos[0] <= 1175) and (160 <= pos[1] <= 210):
        return True
    return False
#
# def saveToFile(objList):
#      jsonStr = json.dumps(objList.__dict__)
#      with open('data.txt', 'w') as outfile:
#          json.dump(jsonStr, outfile)

def drawZonaWork(sc):
    pygame.draw.rect(sc, (0, 0, 0), (10, 10, 900, 680), 5)
    pygame.draw.rect(sc, (255, 255, 255), (15, 15, 890, 670))
    pygame.draw.rect(sc, (0, 0, 0), (950, 10, 240, 680), 5)

def clearZonaWork(sc):
    pygame.draw.rect(sc, (255, 255, 255), (15, 15, 890, 670))

def checkDeleteObj(pos):
    if (965 <= pos[0] <= 1065) and (220 <= pos[1] <= 270):
        return True
    return False

def checkPlusPoint(pos):
    if (965 <= pos[0] <= 1065) and (85 <= pos[1] <= 135):
        return True
    return False

def checkMinusPoint(pos):
    if (1075 <= pos[0] <= 1175) and (85 <= pos[1] <= 135):
        return True
    return False

def checkRunProg(pos):
    if (965 <= pos[0] <= 1065) and (290 <= pos[1] <= 340):
        return True
    return False

def checkSave(pos):
    if (965 <= pos[0] <= 1065) and (360 <= pos[1] <= 410):
        return True
    return False

def checkRestore(pos):
    if (1075 <= pos[0] <= 1175) and (360 <= pos[1] <= 410):
        return True
    return False

def checkMatrix(pos):
    if (965 <= pos[0] <= 1175) and (480 <= pos[1] <= 530):
        return True
    return False

def checkDescr(pos):
    if (965 <= pos[0] <= 1175) and (550 <= pos[1] <= 600):
        return True
    return False

def checkSaveFile(pos):
    if (1075 <= pos[0] <= 1175) and (420 <= pos[1] <= 470):
        return True
    return False

def checkOpenFile(pos):
    if (965 <= pos[0] <= 1065) and (420 <= pos[1] <= 470):
        return True
    return False

def checkSaveMIandPTIO(pos):
    if (965 <= pos[0] <= 1175) and (620 <= pos[1] <= 670):
        return True
    return False

def addButton(sc):
    but_plusPoint = widget.but_plus(sc, 965, 85, 100, 50, "+", (68, 148, 74))
    but_minusPoint = widget.but_plus(sc, 1075, 85, 100, 50, "-", (68, 148, 74))

    butt_plusPlace = widget.but_plus(sc, 965, 160, 100, 50, "+ позицию", (204, 204, 255))
    butt_plusTransition = widget.but_plus(sc, 1075, 160, 100, 50, "+ переход", (204, 204, 255))

    but_deleteObject = widget.but_plus(sc, 965, 220, 100, 50, "Удалить", (204, 204, 255))
    but_clearObject = widget.but_plus(sc, 1075, 220, 100, 50, "Очистить", (204, 204, 255))

    but_runWeb = widget.but_whitetext(sc, 965, 290, 210, 50, "Запустить", (225, 39, 0))

    but_saveWeb = widget.but_whitetext(sc, 965, 360, 100, 50, "Сохранить", (37, 109, 123))
    but_restoreWeb = widget.but_whitetext(sc, 1075, 360, 100, 50, "Откатить", (37, 109, 123))
    but_openWeb = widget.but_whitetext(sc, 965, 420, 100, 50, "Открыть", (37, 109, 123))
    but_downloadWeb = widget.but_whitetext(sc, 1075, 420, 100, 50, "Скачать", (37, 109, 123))

    but_drawMatrixInce = widget.but_plus(sc, 965, 480, 210, 50, "Матрица инцедентности", (255, 200, 168))
    but_drawDescrNet = widget.but_plus(sc, 965, 550, 210, 50, "Описание сети Петри", (255, 200, 168))
    but_drawDiagramNet = widget.but_whitetext(sc, 965, 620, 210, 50, "Сохранение МИ и PTIO", (37, 109, 123))
