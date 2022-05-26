import copy
import json
import os
import sys
import tkinter.filedialog

import pygame
import pygame_widgets

import Object
import Table
import modul
import widget


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def prompt_open_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfile(parent=top)
    top.destroy()
    return file_name


def prompt_save_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.asksaveasfilename(parent=top)
    top.destroy()
    return file_name


pygame.init()

sc = pygame.display.set_mode([1800, 750])
pygame.display.set_caption("Сети Петри")
sc.fill([250, 238, 221])

# объект класс, где вся логика программы
objectList = Object.ObjectList("newName")

# класс, для отката к сохраненной версии
objectListSave = Object.ObjectList("saveOnj")

# класс, для рисования таблицы инцидентности
table = Table.Table(1210, 25, 500, 350)

# рисуем рабочие зоны
modul.drawZonaWork(sc)

# добавляем кнопки
modul.addButton(sc)

# поле для вывода название выделенного объекта
textCountPoint = widget.textOutput(sc, 965, 25, 210, 50)
textHelp = widget.textOutput(sc, 65, 692, 500, 50)
# флаги

# флаг для стрелки: True - первый клик, выбран объект, False - выбран объект куда идёт стрелка
flagMoveArrow = False
# флаг для зажатия, если True - кнопка мыши зажата и объект двигается, False - кнопка мыши отпустили и объект не двигается
flagNotPress = False
# флаг для запуска программы, True - цикл запущен
flagRunProg = False

flagShowHelp = 0

leftClick = False
rightCLick = False

# картинка, для обозначения стоп или старт
imageStart = pygame.image.load("play.png")
imageStop = pygame.image.load("pause.png")
imageStart = pygame.transform.scale(imageStart, (50, 50))
imageStop = pygame.transform.scale(imageStop, (50, 50))

sc.blit(imageStop, (10, 690))
textCountPoint.disable()
clock = pygame.time.Clock()
pygame.display.update()
end_time = pygame.time.get_ticks() + 4000
while True:
    clock.tick(60)
    events = pygame.event.get()

    if flagShowHelp > 0:
        current_time = pygame.time.get_ticks()
        if current_time % 4000 == 0:
            flagShowHelp = 0

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                leftClick = True
            elif event.button == 3:
                rightCLick = True

        # После передвежения, убираем фокусировку с объекта
        if event.type == pygame.MOUSEBUTTONUP and (
                10 <= event.pos[0] <= 910 and 10 <= event.pos[1] <= 690) and flagNotPress:
            if objectList.checkSelected(event.pos):
                flagNotPress = False

    if leftClick:
        if modul.checkPlusPlace(event.pos):  # добавление поинта
            objectList.addNewPlace()

        elif modul.checkPlusTrans(event.pos):  # добавление перехода
            objectList.addNewTrans()

        elif modul.checkSaveMIandPTIO(event.pos):
            a = prompt_save_file()
            if a != "":
                with open(a, 'w') as f:
                    f.write(objectList.SaveMIandPTIO())

        elif modul.checkDescr(event.pos):
            if objectList.checkLenObject():
                pygame.draw.rect(sc, (250, 238, 221), (1210, 0, sc.get_width(), sc.get_height()))
                objectList.drawDescrNP(sc)
                flagShowHelp = 0
            else:
                flagShowHelp = 2

        elif modul.checkMatrix(event.pos):  # создание таблицы матрицы инцидентности
            if objectList.checkLenObject():
                pygame.draw.rect(sc, (250, 238, 221), (1210, 0, sc.get_width(), sc.get_height()))
                table.drawTableFromMatrix(sc, objectList.place, objectList.trans, objectList.MatrixIncident())
                flagShowHelp = 0
            else:
                flagShowHelp = 2

        elif modul.checkClear(event.pos):  # очищает поле и объект класс
            pygame.draw.rect(sc, (250, 238, 221), (0, 0, sc.get_width(), sc.get_height()))
            modul.drawZonaWork(sc)
            objectList.clearPole()

        elif modul.checkDeleteObj(event.pos):  # удаляет выделенный объект
            modul.drawZonaWork(sc)
            if objectList.selected:
                objectList.deleteObj()
                flagShowHelp = 0
            else:
                flagShowHelp = 1

        elif modul.checkPlusPoint(event.pos):  # добавляет точку в поинт
            if objectList.selected:
                objectList.addPointFromPlace(True)
                flagShowHelp = 0
            else:
                flagShowHelp = 1

        elif modul.checkMinusPoint(event.pos):  # убирает точку из поинта
            if objectList.selected:
                objectList.addPointFromPlace(False)
                flagShowHelp = 0
            else:
                flagShowHelp = 1

        elif modul.checkSave(event.pos):  # сохраняет объекты и все их положения
            objectListSave = copy.deepcopy(objectList)

        elif modul.checkRestore(event.pos):  # откатывает объект к сохраненной версии
            modul.drawZonaWork(sc)
            objectList = copy.deepcopy(objectListSave)

        elif modul.checkSaveFile(event.pos):
            # modul.saveToFile(objectList)

            a = prompt_save_file()
            if a != "":
                with open(a, 'w') as f:
                    json.dump(objectList.returnJson(), f)

        elif modul.checkOpenFile(event.pos):
            b = prompt_open_file()
            if b is not None:
                modul.drawZonaWork(sc)
                data = json.load(b)
                objectList = Object.ObjectList("newName")
                objectList.fillObjFromJson(data)


        elif modul.checkRunProg(event.pos):  # выставления флагов для запуска программы или остановки
            if flagRunProg:
                flagRunProg = False
                pygame.draw.rect(sc, (250, 238, 221), (5, 690, 50, 50))
                sc.blit(imageStop, (10, 690))
            else:
                flagRunProg = True
                pygame.draw.rect(sc, (250, 238, 221), (5, 690, 50, 50))
                sc.blit(imageStart, (10, 690))

        # проверка, попал ли пользователь по объекту, если да, то выделяем
        elif 10 <= event.pos[0] <= 910 and 10 <= event.pos[1] <= 690:
            if objectList.checkSelected(event.pos):
                flagNotPress = True
        leftClick = False

    pressed = pygame.mouse.get_pressed()
    # Передвигать объект
    if pressed[0] and event.type == pygame.MOUSEMOTION:
        if 50 <= event.pos[0] <= 870 and 65 <= event.pos[1] <= 650:
            # рисуем рабочую зону
            modul.drawZonaWork(sc)
            if objectList.selected:
                objectList.MoveObject(event.pos)
    # проверка, для создание связей, первый клик по объекту
    if rightCLick and (10 <= event.pos[0] <= 910 and 10 <= event.pos[1] <= 690) and not flagMoveArrow:
        if objectList.checkArrow(event.pos, True):
            flagMoveArrow = True
        rightCLick = False
    # проверка для создание связей, второй клик по объекту
    elif flagMoveArrow and rightCLick:
        if objectList.checkArrow(event.pos, False):
            modul.drawZonaWork(sc)
            flagMoveArrow = False
        rightCLick = False
        modul.drawZonaWork(sc)
        flagMoveArrow = False

    if flagShowHelp >= 0:
        if flagShowHelp == 0:
            textHelp.setText("")
        if flagShowHelp == 1:
            textHelp.setText("Сначала требуется выделить объект")
        elif flagShowHelp == 2:
            textHelp.setText("Сначала требуется добавить объекты")

    # запуск графа
    if flagRunProg:
        objectList.MovePoint(sc)

    # рисуем стрелку идущая от первого выбранного объекта
    if flagMoveArrow and (10 <= event.pos[0] <= 910 and 10 <= event.pos[1] <= 690) and len(objectList.arrow) != 0:
        modul.drawZonaWork(sc)
        objectList.drawArrowMove(sc, (98, 99, 155), (98, 99, 155),
                                 (objectList.arrow[-1].objStart.x, objectList.arrow[-1].objStart.y),
                                 event.pos, 15, 5)

    # передаём значение выделенного объекта в текстовое поле
    textCountPoint.setText(objectList.getSelectedObjName())
    # рисуем рабочие зоны
    objectList.drawArrow(sc)
    objectList.drawPlace(sc)
    objectList.drawTrans(sc)
    # modul.drarClearAroundZonaWork(sc)
    pygame_widgets.update(events)
    pygame.display.update()
