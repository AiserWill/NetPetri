import pygame
from pygame.font import Font

#класс, которые рисует таблиц Инцедентности
class Table:
    def __init__(self, sPx, sPy, lW, lS):
        self.startPostionX = sPx
        self.startPostionY = sPy
        self.lenWight = lW
        self.lenHight = lS
    #функция строит таблицу инцидентности и заполняет её
    def drawTableFromMatrix(self, sc, place, trans, matrixIn):
        textTitleTable = Font(None, 30)
        TitleTable = textTitleTable.render("Матрица инцидентности", True, (0, 0, 0))
        sc.blit(TitleTable, (
            self.centerCellformula(self.startPostionX, self.startPostionX + self.lenWight) - int(self.lenWight /4),
            self.startPostionY - 22))
        if len(place) != 0 and len(trans) != 0:
            self.drawZonaFromTable(sc)
            lenColumn = int(self.lenHight / (len(trans) + 1))
            lenLine = int(self.lenWight / (len(place) + 1))
            for i in range(len(trans) + 1):
                pygame.draw.line(sc, (0, 0, 0), (self.startPostionX,
                                                 self.startPostionY + lenColumn * (i + 1)),
                                 (self.startPostionX + self.lenWight,
                                  self.startPostionY + lenColumn * (i + 1)), 3)
            for i in range(len(place) + 1):
                pygame.draw.line(sc, (0, 0, 0), (self.startPostionX + lenLine * (i + 1),
                                                 self.startPostionY),
                                 (self.startPostionX + lenLine * (i + 1),
                                  self.startPostionY + self.lenHight), 3)
            if len(place) > 8 or len(trans) > 8:
                textPole = Font(None, 20)
            else:
                textPole = Font(None, 30)
            self.fillTable(sc, matrixIn, lenColumn, lenLine, place, trans, textPole)
    #функция для заполнения таблицы инцедентонсти
    def fillTable(self, sc, matrixIn, lC, lW, place, trans,textPole):
        for i in range(len(trans) + 1):
            for j in range(len(place) + 1):
                if i == 0 and j > 0:
                    self.centerCell(sc, str(place[j-1].name, ), lW, lC, i, j, textPole)
                elif j > 0 and i > 0:
                    self.centerCell(sc, str(matrixIn[i-1].get(place[j-1].name)), lW, lC, i,j,textPole )
                elif i > 0 and j == 0:
                    self.centerCell(sc, str(trans[i-1].name), lW, lC, i, j,textPole)
    #определение центра ячейки
    def centerCellformula(self, a, b):
        return a + int((b - a) / 2)
    #отрисовывает числа в центре ячейки
    def centerCell(self,sc, text, lW, lC, i, j, textPole):
        textNamePlace = textPole.render(text, True, (0, 0, 0))
        sc.blit(textNamePlace,
                (self.centerCellformula(self.startPostionX + lW * j, self.startPostionX + lW * (j + 1)) - 5,
                 self.centerCellformula(self.startPostionY + lC * i, self.startPostionY + lC * (i + 1))))
    #отрисовывает зону для таблицы
    def drawZonaFromTable(self, sc):
        pygame.draw.rect(sc, (0, 0, 0), (self.startPostionX, self.startPostionY, self.lenWight, self.lenHight), 5)
        pygame.draw.rect(sc, (255, 255, 255),
                         (self.startPostionX + 3, self.startPostionY + 3, self.lenWight - 6, self.lenHight - 6))
