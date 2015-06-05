#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtGui import *
from PySide.QtCore import *


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.image = QImage()
        self.imageCopy = QImage()
        self.filePath = None

        self.mIsEdited = False
        self.mIsPaint = False
        self.mIsResize = False
        self.mRightButtonPressed = False

        self.mPixmap = None
        self.mCurrentCursor = None
        self.mZoomFactor = 1.0
        self.mUndoStack = QUndoStack()
        self.mInstrumentHandler = None

        self.setMouseTracking(True)

        # TODO: ай-ай-ай
        from pencil_instrument import PencilInstrument
        self.mInstrumentHandler = PencilInstrument()
        self.image = QImage(400, 400, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.transparent)

    # Send primary color for ToolBar.
    sendPrimaryColorView = Signal()

    # Send secondary color for ToolBar.
    sendSecondaryColorView = Signal()

    sendNewImageSize = Signal()
    sendCursorPos = Signal()
    sendColor = Signal()

    # Send signal to restore previous checked instrument for ToolBar.
    sendRestorePreviousInstrument = Signal()

    # Send instrument for ToolBar.
    sendSetInstrument = Signal()

    # Send signal to enable copy cut actions in menu.
    sendEnableCopyCutActions = Signal()

    # Send signal to selection instrument.
    sendEnableSelectionInstrument = Signal()

    def save(self):
        pass

    def saveAs(self):
        pass

    def print(self):
        pass

    def resizeImage(self):
        pass

    def resizeImage(self):
        pass

    def rotateImage(self, flag):
        pass

    def getFileName(self):
        pass

    def getImage(self):
        return self.image

    def setImage(self, im):
        self.image = im

    def setEdited(self, flag):
        pass

    def getEdited(self):
        pass

    def applyEffect(self, effect):
        pass

    def restoreCursor(self):
        pass

    def zoomImage(self, factor):
        pass

    def setZoomFactor(self, factor):
        pass

    def getZoomFactor(self):
        pass

    def getUndoStack(self):
        pass

    def setIsPaint(self, isPaint):
        self.mIsPaint = isPaint

    def isPaint(self):
        return self.mIsPaint

    def emitPrimaryColorView(self):
        pass

    def emitSecondaryColorView(self):
        pass

    def emitColor(self, color):
        pass

    def emitRestorePreviousInstrument(self):
        pass

    def copyImage(self):
        pass

    def pasteImage(self):
        pass

    def cutImage(self):
        pass

    def saveImageChanges(self):
        pass

    def clearSelection(self):
        pass

    def pushUndoCommand(self, command):
        pass

    def initializeImage(self):
        pass

    def open(self):
        pass

    def open(self, filePath):
        pass

    def drawCursor(self):
        pass

    def makeFormatsFilters(self):
        pass

    def autoSave(self):
        pass

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and \
                event.pos().x() < self.image.rect().right() + 6 and \
                event.pos().x() > self.image.rect().right() and \
                event.pos().y() > self.image.rect().bottom() and \
                event.pos().y() < self.image.rect().bottom() + 6:
            self.mIsResize = True
            self.setCursor(Qt.SizeFDiagCursor)

        # TODO: выбор какого-нибудь иснтрумента
        # else if(DataSingleton::Instance()->getInstrument() != NONE_INSTRUMENT)
        # {
        #     mInstrumentHandler = mInstrumentsHandlers.at(DataSingleton::Instance()->getInstrument());
        #     mInstrumentHandler->mousePressEvent(event, *this);
        # }

        else:
            self.mInstrumentHandler.mousePressEvent(event, self)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # InstrumentsEnum instrument = DataSingleton::Instance()->getInstrument();
        # mInstrumentHandler = mInstrumentsHandlers.at(DataSingleton::Instance()->getInstrument());
        # if(mIsResize)
        # {
        #      mAdditionalTools->resizeCanvas(event->x(), event->y());
        #      emit sendNewImageSize(mImage->size());
        # }
        # else if(event->pos().x() < mImage->rect().right() + 6 &&
        #         event->pos().x() > mImage->rect().right() &&
        #         event->pos().y() > mImage->rect().bottom() &&
        #         event->pos().y() < mImage->rect().bottom() + 6)
        # {
        #     setCursor(Qt::SizeFDiagCursor);
        #     if (qobject_cast<AbstractSelection*>(mInstrumentHandler))
        #         return;
        # }
        # else if (!qobject_cast<AbstractSelection*>(mInstrumentHandler))
        # {
        #     restoreCursor();
        # }
        # if(event->pos().x() < mImage->width() &&
        #         event->pos().y() < mImage->height())
        # {
        #     emit sendCursorPos(event->pos());
        # }
        #
        # if(instrument != NONE_INSTRUMENT)
        # {
        #     mInstrumentHandler->mouseMoveEvent(event, *this);
        # }

        # TODO: проверка дублирует ту, что в mousePressEvent
        if event.pos().x() < self.image.rect().right() + 6 and \
                event.pos().x() > self.image.rect().right() and \
                event.pos().y() > self.image.rect().bottom() and \
                event.pos().y() < self.image.rect().bottom() + 6:
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            # TODO: курсор должен зависить от текущего инструмента
            self.setCursor(Qt.ArrowCursor)

        # Рисуем, используя инструмент
        self.mInstrumentHandler.mouseMoveEvent(event, self)

        super().mouseMoveEvent(event)
    #
    # def mouseReleaseEvent(self, event):
    # if(mIsResize)
    # {
    #    mIsResize = false;
    #    restoreCursor();
    # }
    # else if(DataSingleton::Instance()->getInstrument() != NONE_INSTRUMENT)
    # {
    #     mInstrumentHandler = mInstrumentsHandlers.at(DataSingleton::Instance()->getInstrument());
    #     mInstrumentHandler->mouseReleaseEvent(event, *this);
    # }
    #
    #     super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)

        # TODO: рисуем шахматную доску
        # TODO: иконки через ресурсы брать
        painter.setBrush(QBrush(QPixmap("transparent.jpg")))
        painter.drawRect(0, 0,
                         self.image.rect().right() - 1,
                         self.image.rect().bottom() - 1)

        painter.drawImage(event.rect(), self.image, event.rect())

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(QRect(self.image.rect().right(), self.image.rect().bottom(), 6, 6))

        painter.end()

        super().paintEvent(event)









# class Canvas(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.pressed = False
#         # self.image = None
#         self.image = QImage(400, 400, QImage.Format_ARGB32)
#         self.image.fill(Qt.transparent)
#
#         self.last_point = None
#
#         # self.commands = []
#
#     # def resizeEvent(self, event):
#     #     if self.image:
#     #         self.image = self.image.copy(0, 0, event.size().width(), event.size().height())
#     #     else:
#     #         self.image = QImage(event.size(), QImage.Format_ARGB32)
#     #         self.image.fill(Qt.transparent)
#     #
#     #     super().resizeEvent(event)
#
#     def mouseMoveEvent(self, event):
#         if self.pressed:
#             x = event.pos().x()
#             y = event.pos().y()
#
#             p = QPainter(self.image)
#             p.setRenderHint(QPainter.Antialiasing)
#             p.setPen(QPen(Qt.black, 3.0))
#
#             p.drawLine(QPoint(x, y), QPoint(self.last_point[0], self.last_point[1]))
#
#             self.last_point = x, y
#
#             # p.drawPoint(x, y)
#
#             # p.drawPoints(
#             #     [QPoint(x, y),
#             #      QPoint(x + 1, y),
#             #      QPoint(x - 1, y),
#             #      QPoint(x, y + 1),
#             #      QPoint(x, y - 1)]
#             # )
#
#             self.update()
#
#         super().mouseMoveEvent(event)
#
#     def mousePressEvent(self, event):
#         self.pressed = True
#         self.last_point = event.pos().x(), event.pos().y()
#
#         super().mousePressEvent(event)
#
#     def mouseReleaseEvent(self, event):
#         self.pressed = False
#
#         super().mouseReleaseEvent(event)
#
#     def paintEvent(self, event):
#         p = QPainter(self)
#         p.setRenderHint(QPainter.Antialiasing)
#
#         p.setBrush(Qt.gray)
#         p.drawRect(self.rect())
#
#         p.setBrush(Qt.white)
#         p.drawRect(self.image.rect())
#         p.drawImage(0, 0, self.image)
#
#         super().paintEvent(event)