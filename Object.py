import copy
import json
import math
import threading

import pygame
from pygame.font import Font

# пустая болванка,(костыль программы)
class RezObj:
    nameTeg = "L"
    name = ""

    def __init__(self):
        self.nameTeg = "L"

# класс который содержит маршрут построение движущихся маркеров
class Point:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cx = []
        self.cy = []
        self.LineWithBrezenhema(self.x1, self.y1, self.x2, self.y2)


# функция которая расчитывает координаты для построение маркера по прямой линии
    def LineWithBrezenhema(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
        if dx < 0: dx = -dx
        if dy < 0: dy = -dy

        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy

        x = []
        y = []
        x.append(x1)
        y.append(y1)

        error, t = el / 2, 0

        while t < el:
            error -= es
            if error < 0:
                error += el
                x.append(x[-1] + sign_x)
                y.append(y[-1] + sign_y)
            else:
                x.append(x[-1] + pdx)
                y.append(y[-1] + pdy)
            t += 1
        self.cx = x
        self.cy = y


# класс стрелки
class Arrow:
    objStart = 0  # объект, откуда выходит стрелка
    objEnd = 0  # объект, на котором кончается стрелка
    # countOneWay, отступ который надо взять, если стрелок больше одной в одном направление, Reverse, в обратном
    countOneWay = 0
    countReverseWay = 0
    nameTeg = "A"  # тег, для  проверок

    def __init__(self, newName):
        self.name = newName
        self.objStart = 0
        self.objEnd = 0
        self.countOneWay = 0
        self.countReverseWay = 0
        self.nameTeg = "A"

# класс позиции, визуальное представление в виде круга
class Place:
    point = 0 #количество маркеров
    nameTeg = "P" #название класс, для поисков

    def __init__(self, newX, newY, newName, point=0):
        # координаты позиции
        self.x = newX
        self.y = newY
        # имя позиции
        self.name = newName
        self.point = point
        self.nameTeg = "P"

# класс переходов, визуальное представление в виде прямоугольника
class Transition:
    nameTeg = "T" #название класса, для поиска
    connectionStart: list  # содержит позиции, у которых связь T->P
    connectionEnd: list  # содержит позиции, у которых связь P -> T

    def __init__(self, newX, newY, newName):
        # координаты перехода
        self.x = newX
        self.y = newY
        # имя перехода
        self.name = newName
        self.connectionStart = []
        self.connectionEnd = []


class ObjectList:
    place: list # массив состоящий из объектов класса Place
    trans: list# массив состоящий из объектов класса Trans
    arrow: list# массив состоящий из объектов класса Arrow
    movePoint: list # массив состоящий из объектов класса Trans, которые могут передать маркер во время запуска графа
    pointsStart: list # массив состоящий из объектов класс Point, которые идут от P -> T
    pointsEnd: list # массив состоящий из объектов класс Point, которые идут от T -> P
    selected = False  # Флаг для выделения
    selectedObj = RezObj() # Сохранение выделенного объекта
    selectedId = 0 #Сохранение его id

    def __init__(self, newName):
        self.name = newName
        self.place = []
        self.trans = []
        self.arrow = []
        self.movePoint = []
        self.pointsStart = []
        self.pointsEnd = []
        self.selected = False  # Флаг для выделения
        self.selectedObj = RezObj()
        self.selectedId = 0

    def fillTransitionConnection(self):# функция которая добавляет связи в переходы, после загрузки json файла
        for i in range(len(self.arrow)):
            if self.arrow[i].objStart.nameTeg == "P":
                for j in range(len(self.place)):
                    if self.place[j].name == self.arrow[i].objStart.name:
                        self.trans[self.trans.index(self.arrow[i].objEnd)].connectionEnd.append(self.place[j])
            else:
                for j in range(len(self.place)):
                    if self.place[j].name == self.arrow[i].objEnd.name:
                        self.trans[self.trans.index(self.arrow[i].objStart)].connectionStart.append(self.place[j])

    def fillObjFromJson(self, data): # функция, которая разбирает документ json и заполняет этот объект класса
        for i in range(len(data['place'])):
            self.place.append(
                Place(data["place"][i]["x"], data["place"][i]["y"], data["place"][i]["name"],
                      data["place"][i]["point"]))
        for i in range(len(data['trans'])):
            self.trans.append(
                Transition(data["trans"][i]["x"], data["trans"][i]["y"], data["trans"][i]["name"]))
        for i in range(len(data['arrow'])):
            self.arrow.append(Arrow(str(len(self.arrow))))
            if "P" in data["arrow"][i]["objStart"]:
                for j in range(len(self.place)):
                    if self.place[j].name == data["arrow"][i]["objStart"]:
                        self.arrow[i].objStart = self.place[j]
                for j in range(len(self.trans)):
                    if self.trans[j].name == data["arrow"][i]["objEnd"]:
                        self.arrow[i].objEnd = self.trans[j]
            elif "T" in data["arrow"][i]["objStart"]:
                for j in range(len(self.trans)):
                    if self.trans[j].name == data["arrow"][i]["objStart"]:
                        self.arrow[i].objStart = self.trans[j]
                        continue
                for j in range(len(self.place)):
                    if self.place[j].name == data["arrow"][i]["objEnd"]:
                        self.arrow[i].objEnd = self.place[j]
                        continue
            self.arrow[i].countOneWay = data["arrow"][i]["countOneWay"]
            self.arrow[i].countReverseWay = data["arrow"][i]["countReverseWay"]
        self.fillTransitionConnection()

    # формирует json формат для сохранение
    def returnJson(self):
        data = copy.deepcopy(self.__dict__)
        data['place'] = []
        for i in range(len(self.place)):
            data['place'].append(copy.deepcopy(self.place[i].__dict__))
        data['trans'] = []
        for j in range(len(self.trans)):
            data['trans'].append(copy.deepcopy(self.trans[j].__dict__))
            data['trans'][-1]['connectionEnd'] = []
            data['trans'][-1]['connectionStart'] = []
            for i in range(len(self.trans[j].connectionEnd)):
                data['trans'][-1]['connectionEnd'].append(copy.deepcopy(self.trans[j].connectionEnd[i].__dict__))
            for i in range(len(self.trans[j].connectionStart)):
                data['trans'][-1]['connectionStart'].append(copy.deepcopy(self.trans[j].connectionStart[i].__dict__))
        data['arrow'] = []
        for i in range(len(self.arrow)):
            data['arrow'].append(copy.deepcopy(self.arrow[i].__dict__))
            if self.arrow[i].objStart.nameTeg == "T":
                data['arrow'][-1]['objStart'] = data['arrow'][-1]['objStart'].name
                data['arrow'][-1]['objEnd'] = data['arrow'][-1]['objEnd'].name
            if self.arrow[i].objStart.nameTeg == "P":
                data['arrow'][-1]['objStart'] = data['arrow'][-1]['objStart'].name
                data['arrow'][-1]['objEnd'] = data['arrow'][-1]['objEnd'].name
        data['selectedObj'] = 0
        return data

    def SaveMIandPTIO(self):
        fileText = "Описание сети Петри (PTIO)" + "\n"
        dNP = self.DescriptionNetPetri()
        MI = self.MatrixIncident()
        if self.checkLenObject():
            for i in range(len(dNP)):
                fileText += dNP[i] + "\n"
            fileText += "Матрица Инцидентности" + "\n"
            for i in range(len(MI)):
                fileText += "T" + str(i + 1) + str(MI[i]) + "\n"

        return fileText

    def MatrixIncident(self):# создает Матрицу Инцидентности, и возвращает её как словарь
        placeMatrix = []
        for i in range(len(self.trans)):
            placeDict = {self.place[i].name: 0 for i in range(0, len(self.place))}
            for j in range(len(self.trans[i].connectionEnd)):
                if placeDict.get(self.trans[i].connectionEnd[j].name) is not None:
                    placeDict[self.trans[i].connectionEnd[j].name] -= 1
            for j in range(len(self.trans[i].connectionStart)):
                if placeDict.get(self.trans[i].connectionStart[j].name) is not None:
                    placeDict[self.trans[i].connectionStart[j].name] += 1
            placeMatrix.append(placeDict)
        return placeMatrix

    def TransEnter(self): #находит переходы, которые могут принять маркер(у всех входящих позиции, должен быть маркер)
        if len(self.arrow) > 0:
            for i in range(len(self.trans)):
                flag = True
                c = copy.deepcopy(self.trans[i].connectionEnd)
                for j in range(len(c)):
                    if c[j].point != 0:
                        c[j].point -= 1
                    else:
                        flag = False
                if flag:
                    self.movePoint.append(self.trans[i])

    def runOneTrans(self):
        self.movePoint = []
        if len(self.arrow) > 0:
            flag = True
            c = copy.deepcopy(self.selectedObj.connectionEnd)
            for j in range(len(c)):
                if c[j].point != 0:
                    c[j].point -= 1
                else:
                    flag = False
            if flag:
                self.movePoint.append(self.selectedObj)

    def checkLenObject(self): #функция, которая проверяет, не пустые ли массивы из объектов
        if len(self.trans) != 0 and len(self.place) != 0:
            return True
        else:
            return False

    #формирует Описание сети Петри PTIO и рисует
    def drawDescrNP(self, sc):
        dest = self.DescriptionNetPetri()
        lenT = len(self.trans)
        text = Font(None, 25)
        maxLenStr = len(dest[2])
        textTitleTable = Font(None, 30)
        TitleTable = textTitleTable.render("Описание сети Петри", True, (0, 0, 0))
        sc.blit(TitleTable, (
            1210 + (1710 - 1210) / 2 - int(500 / 4),
            25 - 22))
        for i in range(3, len(dest)):
            if not "O(" in dest[i]:
                if maxLenStr < len(dest[i]):
                    maxLenStr = len(dest[i])
        for i in range(len(dest)):
            tD = text.render(dest[i], True, (0, 0, 0))
            if "O(" in dest[i] and i > 1:
                sc.blit(tD, (1210 + (maxLenStr * 8), 30 + ((i - lenT) * 30)))
            else:
                sc.blit(tD, (1210, 30 + (i * 30)))

    # формирует Описание сети Петри PTIO
    def DescriptionNetPetri(self):
        desNP = []
        desNP.append("P = { ")
        for i in range(len(self.place)):
            if len(self.place) == 1 or i == (len(self.place) - 1):
                desNP[-1] += self.place[i].name + " "
            else:
                desNP[-1] += self.place[i].name + ", "
        desNP[-1] += "}"
        desNP.append("T = { ")
        for i in range(len(self.trans)):
            if len(self.trans) == 1 or i == (len(self.trans) - 1):
                desNP[-1] += self.trans[i].name + " "
            else:
                desNP[-1] += self.trans[i].name + ", "
        desNP[-1] += "}"
        for i in range(len(self.trans)):
            desNP.append("I(" + self.trans[i].name + ") = { ")
            for j in range(len(self.trans[i].connectionEnd)):
                if len(self.trans[i].connectionEnd) == 1 or j == (len(self.trans[i].connectionEnd) - 1):
                    desNP[-1] += self.trans[i].connectionEnd[j].name + " "
                else:
                    desNP[-1] += self.trans[i].connectionEnd[j].name + ", "
            desNP[-1] += " }"
        for i in range(len(self.trans)):
            desNP.append("O(" + self.trans[i].name + ") = { ")
            for j in range(len(self.trans[i].connectionStart)):
                if len(self.trans[i].connectionStart) == 1 or j == (len(self.trans[i].connectionStart) - 1):
                    desNP[-1] += self.trans[i].connectionStart[j].name + " "
                else:
                    desNP[-1] += self.trans[i].connectionStart[j].name + ", "
            desNP[-1] += " }"
        return desNP
    #функция, которая добавляет маркеры в массив для их отрисовки
    def addPoint(self):
        if len(self.movePoint) != 0:
            for i in range(len(self.movePoint)):
                for j in range(len(self.movePoint[i].connectionEnd)):
                    xy = self.lenArrow(self.movePoint[i].connectionEnd[j], self.movePoint[i], 2)
                    self.pointsStart.append(Point(xy[0], xy[1], xy[2], xy[3]))

                for j in range(len(self.movePoint[i].connectionStart)):
                    xy = self.lenArrow(self.movePoint[i], self.movePoint[i].connectionStart[j], 1)
                    self.pointsEnd.append(Point(xy[0], xy[1], xy[2], xy[3]))
    #функция, которая высчитывает длину стрелки( для красивого вывода)
    def lenArrow(self, list, listC, flag):
        if flag == 1:
            xT = 10
            yT = 35
            xP = 0
            yP = 0
        elif flag == 2:
            xT = 0
            yT = 0
            xP = 10
            yP = 35
        rotation = (math.atan2(list.y - listC.y,
                                 listC.x - list.x)) + math.pi / 2
        x1 = list.x + xT + 50 * math.sin(rotation)
        y1 = list.y + yT + 50 * math.cos(rotation)
        x2 = listC.x + xP - 50 * math.sin(rotation)
        y2 = listC.y + yP - 50 * math.cos(rotation)
        return [x1, y1, x2, y2]
    #Отрисовывавет движущиеся маркеры
    def drawMovePoint(self, obj, sc):
        for i in range(0, len(obj.cx)):
            self.drawArrow(sc)
            # self.drawPlace(sc)
            # self.drawTrans(sc)
            pygame.draw.circle(sc, (0, 0, 0), (obj.cx[i], obj.cy[i]), 5)
            pygame.time.wait(5)
            pygame.display.flip()
            pygame.draw.circle(sc, (255, 255, 255), (obj.cx[i - 1], obj.cy[i - 1]), 5)

        pygame.draw.circle(sc, (255, 255, 255), (obj.cx[-1], obj.cy[-1]), 5)
    #Логика запуска Сети Петри, вычитание маркеров у начальных позиции, отрисовка их движений
    # , и добавление маркеров в конечную позици
    def MovePoint(self, sc):
        if self.selected:
            self.runOneTrans()
        else:
            self.TransEnter()
        threads = []
        if len(self.movePoint) != 0:
            for i in range(len(self.movePoint)):
                self.addPoint()
                obj = self.movePoint[i]
                for j in range(len(obj.connectionEnd)):
                    if obj.connectionEnd[j].point != 0:
                        obj.connectionEnd[j].point -= 1
            while len(self.pointsStart) != 0:
                t = threading.Thread(target=self.drawMovePoint, args=(self.pointsStart.pop(0), sc))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()

            while len(self.pointsEnd) != 0:
                t = threading.Thread(target=self.drawMovePoint, args=(self.pointsEnd.pop(0), sc))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            while len(self.movePoint) != 0:
                obj = self.movePoint.pop(0)
                for i in range(len(obj.connectionStart)):
                    obj.connectionStart[i].point += 1

    # Добавляем новый поинт
    def addNewPlace(self):
        self.place.append(Place(70, 90, ("P" + str(len(self.place) + 1))))

    # Добавляем новый переход
    def addNewTrans(self):
        self.trans.append(Transition(63, 55, ("T" + str(len(self.trans) + 1))))

    #функция которая добавляет в выделенную позицию маркер
    def addPointFromPlace(self, flag):
        if self.selectedObj.nameTeg == "P":
            if flag:
                self.place[self.selectedId].point += 1
            elif self.place[self.selectedId].point != 0:
                self.place[self.selectedId].point -= 1

    #отрисовывает все позиции, с учётом выделенный ли объект или нет
    def drawPlace(self, sc):
        for i in range(len(self.place)):
            textPole = Font(None, 30)
            textNamePlace = textPole.render(self.place[i].name, True, (0, 0, 200))
            sc.blit(textNamePlace, (self.place[i].x - 10, self.place[i].y - 55))
            if self.selectedObj.name == \
                    self.place[i].name:
                pygame.draw.circle(sc, (249, 132, 229), (self.place[i].x, self.place[i].y), 30)
            else:
                pygame.draw.circle(sc, (255, 204, 0), (self.place[i].x, self.place[i].y), 30)
            pygame.draw.circle(sc, (0, 0, 0), (self.place[i].x, self.place[i].y), 35, 5)
            if self.place[i].point > 0:
                textCountPoint = textPole.render(str(self.place[i].point), True, (0, 0, 0))
                if self.place[i].point >= 10:
                    sc.blit(textCountPoint, (self.place[i].x - 10, self.place[i].y - 10))
                else:
                    sc.blit(textCountPoint, (self.place[i].x - 5, self.place[i].y - 10))
    #функция, для передвижения объектов
    def MoveObject(self, pos):
        if self.selectedObj.nameTeg == "T":
            self.selectedObj.x = pos[0] - 10
            self.selectedObj.y = pos[1] - 35
        if self.selectedObj.nameTeg == "P":
            self.selectedObj.x = pos[0]
            self.selectedObj.y = pos[1]
    #отрисовывает все переходы
    def drawTrans(self, sc):
        for i in range(len(self.trans)):
            textPole = Font(None, 30)
            textNamePlace = textPole.render(self.trans[i].name, True, (0, 0, 200))
            sc.blit(textNamePlace, (self.trans[i].x, self.trans[i].y - 20))
            if self.selectedObj.name == self.trans[i].name:
                pygame.draw.rect(sc, (249, 132, 229), (self.trans[i].x + 2, self.trans[i].y + 2, 16, 66))
            else:
                pygame.draw.rect(sc, (0, 160, 0), (self.trans[i].x + 2, self.trans[i].y + 2, 16, 66))
            pygame.draw.rect(sc, (0, 0, 0), (self.trans[i].x, self.trans[i].y, 20, 70), 2)


    #проверка, пользователь попал по объекту или нет, если да, то выделяем
    def checkSelected(self, pos):
        if not self.selected:  # если у нас нет выделенного объекта, то начинаем его искать
            for i in range(len(self.trans)):
                if self.trans[i].x <= pos[0] <= self.trans[i].x + 20 and self.trans[i].y <= pos[1] <= self.trans[
                    i].y + 70:
                    self.selected = True
                    self.selectedObj = self.trans[i]
                    self.selectedId = i
                    return True
            for i in range(len(self.place)):
                if self.place[i].x - 35 <= pos[0] <= self.place[i].x + 35 and self.place[i].y - 35 <= pos[1] <= \
                        self.place[i].y + 35:
                    self.selected = True
                    self.selectedObj = self.place[i]
                    self.selectedId = i
                    return True
            for i in range(len(self.arrow)-1, 0, -1):
                if self.checkPointOnLine(self.arrow[i], pos):
                    self.selected = True
                    self.selectedObj = self.arrow[i]
                    self.selectedId = i
                    return True
        else:
            # если у нас уже есть выделенный объект, проверяем, куда нажал пользователь, если нажал на объект,
            # то ничего не происходит, если нажал в другое место, то проверяем: Новое место это другой объект?
            if self.selectedObj.nameTeg == "P":
                if not (self.selectedObj.x - 35 <= pos[0] <= self.selectedObj.x + 35 and self.selectedObj.y - 35 <= pos[
                    1] <= self.selectedObj.y + 35):
                    self.selected = False
                    self.selectedObj = RezObj()
                    self.selectedId = 0
            elif self.selectedObj.nameTeg == "T":
                if not (self.selectedObj.x <= pos[0] <= self.selectedObj.x + 20 and self.selectedObj.y <= pos[
                    1] <= self.selectedObj.y + 70):
                    self.selected = False
                    self.selectedObj = RezObj()
                    self.selectedId = 0
            elif self.selectedObj.nameTeg == "A":
                for i in range(len(self.arrow)-1, 0, -1):
                    if not self.checkPointOnLine(self.arrow[i], pos):
                        self.selected = False
                        self.selectedObj = RezObj()
                        self.selectedId = 0

            if not self.selected:  # Новое место это другой объект?
                for i in range(len(self.trans)):
                    if self.trans[i].x <= pos[0] <= self.trans[i].x + 20 and self.trans[i].y <= pos[1] <= self.trans[
                        i].y + 70:
                        self.selected = True
                        self.selectedObj = self.trans[i]
                        self.selectedId = i
                        return True
                for i in range(len(self.place)):
                    if self.place[i].x - 35 <= pos[0] <= self.place[i].x + 35 and self.place[i].y - 35 <= pos[1] <= \
                            self.place[i].y + 35:
                        self.selected = True
                        self.selectedObj = self.place[i]
                        self.selectedId = i
                        return True
                for i in range(len(self.arrow)-1, 0, -1):
                    if self.checkPointOnLine(self.arrow[i], pos):
                        self.selected = True
                        self.selectedObj = self.arrow[i]
                        self.selectedId = i
                        return True
        return True

    #возвращает строку с название выделенного объекта, если объект это стрелка, то возвращает связь
    def getSelectedObjName(self):
        if self.selected:
            if self.selectedObj.nameTeg == "A":
                return "{ " + self.selectedObj.objStart.name + " : " + self.selectedObj.objEnd.name + " }"
            else:
                return self.selectedObj.name
        else:
            return ""
    #удаление объекта
    def deleteObj(self):
        if self.selected:
            if self.selectedObj.nameTeg == "A":
                for i in range(len(self.arrow)):
                    if self.selectedObj == self.arrow[i]:
                        if self.selectedObj.objStart.nameTeg == "T":
                            idT = self.trans.index(self.selectedObj.objStart)
                            del (self.trans[idT].connectionStart[self.trans[idT].connectionStart.index(self.selectedObj.objEnd)])
                        else:
                            idT = self.trans.index(self.selectedObj.objEnd)
                            del (self.trans[idT].connectionEnd[self.trans[idT].connectionEnd.index(self.selectedObj.objStart)])
                        del (self.arrow[i])
                        self.selected = False
                        self.selectedObj = RezObj
                        return
            elif self.selectedObj.nameTeg == "P":
                for i in range(len(self.place)):
                    if self.selectedObj == self.place[i]:
                        self.selected = False
                        self.selectedObj = RezObj
                        a = []
                        for j in range(len(self.arrow)):
                            if self.arrow[j].objStart == self.place[i] or self.arrow[j].objEnd == self.place[i]:
                                a.append(j)
                        if len(a) != 0:
                            for j in range(len(a)):
                                del (self.arrow[a[j] - j])
                        del (self.place[i])
                        return
            elif self.selectedObj.nameTeg == "T":
                for i in range(len(self.trans)):
                    if self.selectedObj == self.trans[i]:
                        self.selected = False
                        self.selectedObj = RezObj
                        a = []
                        for j in range(len(self.arrow)):
                            if self.arrow[j].objStart == self.trans[i] or self.arrow[j].objEnd == self.trans[i]:
                                a.append(j)
                        if len(a) != 0:
                            for j in range(len(a)):
                                del (self.arrow[a[j] - j])
                        del (self.trans[i])
                        return
    #4 следующих функции для расчёта, попал ли пользователь по стрелки
    def pointCircle(self, px, py, cx, cy, r):
        distX = px - cx
        distY = py - cy
        distance = math.sqrt((distX * distX) + (distY * distY))
        if distance <= r:
            return True
        return False

    def dist(self, x1, y1, x2, y2):
        distX = x1 - x2
        distY = y1 - y2
        len = math.sqrt((distX * distX) + (distY * distY))
        return len

    def linePoint(self, x1, y1, x2, y2, px, py):
        d1 = self.dist(px, py, x1, y1)
        d2 = self.dist(px, py, x2, y2)
        lineLen = self.dist(x1, y1, x2, y2)
        buffer = 0.1
        if lineLen - buffer <= d1 + d2 <= lineLen + buffer:
            return True
        return False

    def checkPointOnLine(self, obj, pos):
        r = 5
        if obj.objStart.nameTeg == "T":
            xT = 10
            yT = 35
            xP = 0
            yP = 0
        elif obj.objStart.nameTeg == "P":
            xT = 0
            yT = 0
            xP = 10
            yP = 35
        if obj.countReverseWay != 0:
            countX = -7
        elif obj.countOneWay != 0:
            countX = 7
        rotation = (math.atan2(obj.objStart.y + countX - obj.objEnd.y + countX,
                               obj.objEnd.x - obj.objStart.x)) + math.pi / 2
        x1 = obj.objStart.x + xT + 50 * math.sin(rotation)
        y1 = obj.objStart.y + yT - countX + 50 * math.cos(rotation)
        x2 = obj.objEnd.x + xP - 50 * math.sin(rotation)
        y2 = obj.objEnd.y + yP - countX - 50 * math.cos(rotation)

        inside1 = self.pointCircle(x1, y1, pos[0], pos[1], 5)
        inside2 = self.pointCircle(x2, y2, pos[0], pos[1], 5)
        if inside1 or inside2:
            return True
        distX = x1 - x2
        distY = y1 - y2
        len = math.sqrt((distX * distX) + (distY * distY))
        dot = (((pos[0] - x1) * (x2 - x1)) + ((pos[1] - y1) * (y2 - y1))) / pow(len, 2)
        closestX = x1 + (dot * (x2 - x1))
        closestY = y1 + (dot * (y2 - y1))
        onSegment = self.linePoint(x1, y1, x2, y2, closestX, closestY)
        if not onSegment:
            return False
        distX = closestX - pos[0]
        distY = closestY - pos[1]
        distance = math.sqrt((distX * distX) + (distY * distY))
        if distance <= r:
            return True
        return False

    #очистка всех полей
    def clearPole(self):
        self.place = []
        self.trans = []
        self.arrow = []
        self.movePoint = []
        self.selected = False  # Флаг для выделения
        self.selectedObj = RezObj()

    #функция, которая создает стрелку, при первом нажатие добавляет объект в начало стрелки, при втором нажатие,
    # добавляет конечный объект в конец стрелки
    def checkArrow(self, pos, flag):
        if flag:
            for i in range(len(self.trans)):
                if self.trans[i].x <= pos[0] <= self.trans[i].x + 20 and self.trans[i].y <= pos[1] <= self.trans[
                    i].y + 70:
                    self.arrow.append(Arrow(str(len(self.arrow))))
                    self.arrow[-1].objStart = self.trans[i]
                    return True
            for i in range(len(self.place)):
                if self.place[i].x - 35 <= pos[0] <= self.place[i].x + 35 and self.place[i].y - 35 <= pos[1] <= \
                        self.place[i].y + 35:
                    self.arrow.append(Arrow(str(len(self.arrow))))
                    self.arrow[-1].objStart = self.place[i]
                    return True
            return False
        else:
            if self.arrow[-1].objStart.nameTeg == "T":
                for i in range(len(self.place)):
                    if self.place[i].x - 35 <= pos[0] <= self.place[i].x + 35 and self.place[i].y - 35 <= pos[1] <= \
                            self.place[i].y + 35:
                        self.arrow[-1].objEnd = self.place[i]
                        self.checkRepeatArrow(self.place[i])
                        self.trans[self.trans.index(self.arrow[-1].objStart)].connectionStart.append(self.place[i])
                        return True
            elif self.arrow[-1].objStart.nameTeg == "P":
                for i in range(len(self.trans)):
                    if self.trans[i].x <= pos[0] <= self.trans[i].x + 20 and self.trans[i].y <= pos[1] <= \
                            self.trans[i].y + 70:
                        self.arrow[-1].objEnd = self.trans[i]
                        self.checkRepeatArrow(self.trans[i])
                        self.trans[i].connectionEnd.append(self.arrow[-1].objStart)
                        return True
            del (self.arrow[-1])
        return False
    #проверка, сколько стрелок в одном направление(для отступа)
    def checkRepeatArrow(self, obj):
        for i in range(len(self.arrow)):
            if obj.nameTeg == "P" and self.arrow[-1].objStart.nameTeg == "T":
                if obj.name == self.arrow[i].objEnd.name and self.arrow[-1].objStart.name == self.arrow[
                    i].objStart.name:
                    self.arrow[-1].countOneWay += 1
            elif obj.name == self.arrow[i].objEnd.name and self.arrow[-1].objStart.name == self.arrow[i].objStart.name:
                self.arrow[-1].countReverseWay += 1

    #функция для красивого рисование стрелки
    def drawArrowMove(self, screen, lcolor, tricolor, start, end, trirad, thickness=2):
        pygame.draw.line(screen, lcolor, start, end, thickness)
        rad = math.pi / 180
        rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
        pygame.draw.polygon(screen, tricolor, ((end[0] + trirad * math.sin(rotation),
                                                end[1] + trirad * math.cos(rotation)),
                                               (end[0] + trirad * math.sin(rotation - 120 * rad),
                                                end[1] + trirad * math.cos(rotation - 120 * rad)),
                                               (end[0] + trirad * math.sin(rotation + 120 * rad),
                                                end[1] + trirad * math.cos(rotation + 120 * rad))))

    #функция которая отрисовывает все стрелки
    def drawArrow(self, sc):
        nameText = Font(None, 20)

        countX = 0
        xT = 0
        yT = 0
        xP = 0
        yP = 0
        if len(self.arrow) != 0:
            for i in range(len(self.arrow)):
                if self.arrow[i].objEnd != 0:
                    if self.arrow[i].objStart.nameTeg == "T":
                        xT = 10
                        yT = 35
                        xP = 0
                        yP = 0
                    elif self.arrow[i].objStart.nameTeg == "P":
                        xT = 0
                        yT = 0
                        xP = 10
                        yP = 35
                    if self.arrow[i].countReverseWay != 0:
                        countArrow = nameText.render(str(self.arrow[i].countReverseWay), True, (0, 0, 0))
                        countX = -7
                    elif self.arrow[i].countOneWay != 0:
                        countX = 7
                        countArrow = nameText.render(str(self.arrow[i].countOneWay), True, (0, 0, 0))
                    if self.selectedObj.name == self.arrow[i].name:
                        rgb = (227, 38, 54)
                    else:
                        rgb = (98, 99, 155)
                    pygame.draw.rect(sc, (255, 255, 255),
                                     (int(abs(self.arrow[i].objEnd.x + self.arrow[i].objStart.x) / 2)
                                      ,
                                      int(abs(self.arrow[i].objStart.y + (-(countX * 3)) + self.arrow[i].objEnd.y) / 2)
                                      , 15, 15))
                    sc.blit(countArrow, (int(abs(self.arrow[i].objEnd.x + self.arrow[i].objStart.x) / 2)
                                         , int(abs(self.arrow[i].objStart.y + (-(countX * 3)) + self.arrow[i].objEnd.y) / 2)))
                    rotation = (math.atan2(self.arrow[i].objStart.y + countX - self.arrow[i].objEnd.y + countX,
                                           self.arrow[i].objEnd.x - self.arrow[i].objStart.x)) + math.pi / 2
                    self.drawArrowMove(sc, rgb, rgb,
                                       (self.arrow[i].objStart.x + xT + 50 * math.sin(rotation),
                                        self.arrow[i].objStart.y + yT - countX + 50 * math.cos(rotation)),
                                       (self.arrow[i].objEnd.x + xP - 50 * math.sin(rotation),
                                        self.arrow[i].objEnd.y + yP - countX - 50 * math.cos(rotation)), 10,
                                       5)
                    countX = 0

