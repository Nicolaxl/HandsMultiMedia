import tkinter
from tkinter import *
from tkinter.ttk import *
import numpy as np
import mediapipe as tf  
# pip install protobuf>=3.20.X
import cv2
from playsound import playsound
# pip install playsound==1.2.2
from tkinter import filedialog as fd
import pygame as cg
import sys
import time
import random as rand


# REMINDER: SET PROTOBUF VERSION TO 3.20.X
# WARNING FIXED VERSION: pip install playsound==1.2.2

def select_file():
    filetypes = (
        ('MP4 Video Files', '*.mp4'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    settings.VideoPath = filename


def listToString(s):
    string = ""

    for element in s:
        string += element

    return string


print("Loading, Please Wait...")
TfLiteHands = tf.solutions.hands
fingers = TfLiteHands.Hands()
GetNetwork = tf.solutions.drawing_utils
FingerPos = [(8, 6), (12, 10), (16, 14), (20, 18)]
ThumbPos = (4, 2)

canvas_height = 576
canvas_width = 720


class snake_game:
    clk = cg.time.Clock()
    py_coor = [100, 50]
    py_obj = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
    con_coor = [rand.randrange(1, (650 // 10)) * 10, rand.randrange(1, (400 // 10)) * 10]
    con_revive = True
    directions = 'R'
    divert = directions
    score = 0


def fin():
    font_nametype = cg.font.SysFont('arial', 90)
    fin_top = font_nametype.render('GAME OVER', True, cg.Color(255, 255, 0))
    fin_pos = fin_top.get_rect()
    fin_pos.midtop = (650 / 2, 400 / 4)
    snackline.fill(cg.Color(0, 0, 0))
    snackline.blit(fin_top, fin_pos)

    score_font = cg.font.SysFont('arial', 20)
    score_top = score_font.render('Score : ' + str(snake_game.score), True, cg.Color(255, 255, 0))
    score_pos = score_top.get_rect()
    score_pos.midtop = (650 / 2, 400 / 1.25)
    snackline.blit(score_top, score_pos)

    cg.display.flip()
    time.sleep(3)
    terminateprogram()


def popupmsg():
    MSG_FONT = ("Times New Roman", 25)
    msg = "Created By 雷國亮 D0726433\n For IECS227 MULTI-MEDIA SYSTEMS \n Final Project"
    popup = tkinter.Tk()
    popup.wm_title("About 關於")
    label = tkinter.Label(popup, text=msg, font=MSG_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = tkinter.Button(popup, text="OK", command=popup.destroy)
    B1.pack()
    popup.mainloop()


class settings:
    defaultmode = 2
    defaultoutput = 1
    isRun = False
    HandPresent = False
    getfingernow = 0
    counter = 0
    selection_panel = np.zeros((canvas_height, canvas_width))
    string = []
    VideoPath = ""


def modetoggle():
    if settings.defaultmode == 2:
        settings.defaultmode = 1
        label_input["text"] = "Input source 輸入源: Live Camera 實時攝像頭"
        b_livecam["state"] = "disable"
        b_vfile["state"] = "enable"
        b_sfile["state"] = "disable"

    elif settings.defaultmode == 1:
        settings.defaultmode = 2
        label_input["text"] = "Input source 輸入源: Video File 影片檔案"
        b_livecam["state"] = "enable"
        b_vfile["state"] = "disable"
        b_sfile["state"] = "enable"


def sethtvactive():
    settings.defaultoutput = 1
    label_output["text"] = "Program Mode 程式模式: Hands To Voice 動手發字母表聲"
    b_htv["state"] = "disable"
    b_np5["state"] = "enable"
    b_snake["state"] = "enable"


def setnp5active():
    settings.defaultoutput = 2
    label_output["text"] = "Program Mode 程式模式: 5 notes piano 音符鋼琴"
    b_htv["state"] = "enable"
    b_np5["state"] = "disable"
    b_snake["state"] = "enable"


def setsnakeactive():
    settings.defaultoutput = 3
    label_output["text"] = "Program Mode 程式模式: Snake game 蛇遊戲"
    b_htv["state"] = "enable"
    b_np5["state"] = "enable"
    b_snake["state"] = "disable"


def runprogram():
    b_run["state"] = "disable"
    b_terminate["state"] = "enable"
    condition["text"] = "Program status 程式狀態: Running 運行中"
    settings.isRun = True
    global CamRec
    if settings.defaultmode == 1:
        global CamRec
        CamRec = cv2.VideoCapture(0)
    elif settings.defaultmode == 2:
        global cap
        cap = cv2.VideoCapture(settings.VideoPath)
        if (cap.isOpened() == False):
            ALERT_FONT = ("Times New Roman", 20)
            popup = tkinter.Tk()
            popup.wm_title("Video file access error!")
            label = tkinter.Label(popup, text="Unable to open/access video file \n"
                                              "無法打開/訪問影片文件", font=ALERT_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = tkinter.Button(popup, text="OK", command=popup.destroy)
            B1.pack()
            popup.mainloop()

    if settings.defaultoutput == 3:
        snake_game.clk = cg.time.Clock()
        snake_game.py_coor = [100, 50]
        snake_game.py_obj = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
        snake_game.con_coor = [rand.randrange(1, (650 // 10)) * 10, rand.randrange(1, (400 // 10)) * 10]
        snake_game.con_revive = True
        snake_game.directions = 'R'
        snake_game.divert = snake_game.directions
        snake_game.score = 0

        global game
        game = cg.init()
        global snackline
        snackline = cg.display.set_mode((650, 400))  # 螢幕大小為 400X650
        global score_font
        score_font = cg.font.SysFont('times new roman', 20)
        cg.display.set_caption("snackline")  # 視窗名稱: snackline
        if game[1] > 0:
            print("遊戲錯誤，錯誤代碼：" + game[1])
            sys.exit(-1)
        else:
            print("OK")


def terminateprogram():
    settings.isRun = False
    b_run["state"] = "enable"
    b_terminate["state"] = "disable"
    condition["text"] = "Program status 程式狀態: Not running 不運行"
    settings.selection_panel = np.zeros((canvas_height, canvas_width))
    cv2.destroyAllWindows()
    if settings.defaultmode == 1:
        CamRec.release()
    elif settings.defaultmode == 2:
        cap.release()

    if settings.defaultoutput == 1:
        settings.string.clear()
    if settings.defaultoutput == 3:
        cg.quit()


def inittogstanby():
    settings.isRun = False
    b_run["state"] = "enable"
    b_terminate["state"] = "disable"
    condition["text"] = "Program status 程式狀態: Not running 不運行"


def OnProgramRun():
    if settings.isRun:
        if settings.defaultmode == 1:
            retcode, streams = CamRec.read()
        elif settings.defaultmode == 2:
            retcode, streams = cap.read()
        DIP = cv2.cvtColor(streams, cv2.COLOR_BGR2RGB)
        process = fingers.process(DIP)
        FingersData = process.multi_hand_landmarks

        if FingersData:
            settings.HandPresent = True
            DataList = []
            for HandsProc in FingersData:
                GetNetwork.draw_landmarks(streams, HandsProc, TfLiteHands.HAND_CONNECTIONS)
                for i, j in enumerate(HandsProc.landmark):
                    x, y, discard = streams.shape
                    chord_x, chord_y = int(j.x * y), int(j.y * x)
                    DataList.append((chord_x, chord_y))
            for abstract in DataList:
                cv2.circle(streams, abstract, 10, (255, 255, 0), cv2.FILLED)
            FingerCount = 0
            for coop in FingerPos:
                if DataList[coop[0]][1] < DataList[coop[1]][1]:
                    FingerCount += 1
            if DataList[ThumbPos[0]][0] > DataList[ThumbPos[1]][0]:
                FingerCount += 1
            settings.getfingernow = FingerCount
            cv2.putText(streams, str(FingerCount), (150, 150), cv2.FONT_HERSHEY_TRIPLEX, 5, (0, 255, 0), 5)
            cv2.imshow("Hands detection panel", streams)
        else:
            settings.HandPresent = False
            cv2.putText(streams, "No hands", (30, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 2)
            cv2.imshow("Hands detection panel", streams)
            settings.getfingernow = -1

        if settings.defaultoutput == 1:
            if settings.getfingernow == 0:
                if settings.counter > 200:
                    settings.counter = 0
                settings.counter = settings.counter + 1
            if settings.counter <= 20:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "1 A B C", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F 4F 5F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('1')
                    print(listToString(settings.string))
                    playsound('sounds/1.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append('a')
                    print(listToString(settings.string))
                    playsound('sounds/a.mp3')
                elif settings.getfingernow == 4:
                    settings.string.append('b')
                    print(listToString(settings.string))
                    playsound('sounds/b.mp3')
                elif settings.getfingernow == 5:
                    settings.string.append('c')
                    print(listToString(settings.string))
                    playsound('sounds/c.mp3')
            elif settings.counter <= 40:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "2 D E F", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F 4F 5F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('2')
                    print(listToString(settings.string))
                    playsound('sounds/2.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append('d')
                    print(listToString(settings.string))
                    playsound('sounds/d.mp3')
                elif settings.getfingernow == 4:
                    settings.string.append('e')
                    print(listToString(settings.string))
                    playsound('sounds/e.mp3')
                elif settings.getfingernow == 5:
                    settings.string.append('f')
                    print(listToString(settings.string))
                    playsound('sounds/f.mp3')
            elif settings.counter <= 60:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "3 G H I", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F 4F 5F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('3')
                    print(listToString(settings.string))
                    playsound('sounds/3.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append('g')
                    print(listToString(settings.string))
                    playsound('sounds/g.mp3')
                elif settings.getfingernow == 4:
                    settings.string.append('h')
                    print(listToString(settings.string))
                    playsound('sounds/h.mp3')
                elif settings.getfingernow == 5:
                    settings.string.append('i')
                    print(listToString(settings.string))
                    playsound('sounds/i.mp3')
            elif settings.counter <= 80:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "4 J K L", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F 4F 5F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('4')
                    print(listToString(settings.string))
                    playsound('sounds/4.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append('j')
                    print(listToString(settings.string))
                    playsound('sounds/j.mp3')
                elif settings.getfingernow == 4:
                    settings.string.append('k')
                    print(listToString(settings.string))
                    playsound('sounds/k.mp3')
                elif settings.getfingernow == 5:
                    settings.string.append('l')
                    print(listToString(settings.string))
                    playsound('sounds/l.mp3')
            elif settings.counter <= 100:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "5 M N O", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F 4F 5F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('5')
                    print(listToString(settings.string))
                    playsound('sounds/5.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append('m')
                    print(listToString(settings.string))
                    playsound('sounds/m.mp3')
                elif settings.getfingernow == 4:
                    settings.string.append('n')
                    print(listToString(settings.string))
                    playsound('sounds/n.mp3')
                elif settings.getfingernow == 5:
                    settings.string.append('o')
                    print(listToString(settings.string))
                    playsound('sounds/o.mp3')
            elif settings.counter <= 120:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "6 P Q R", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F 4F 5F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('6')
                    print(listToString(settings.string))
                    playsound('sounds/6.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append('p')
                    print(listToString(settings.string))
                    playsound('sounds/p.mp3')
                elif settings.getfingernow == 4:
                    settings.string.append('q')
                    print(listToString(settings.string))
                    playsound('sounds/q.mp3')
                elif settings.getfingernow == 5:
                    settings.string.append('r')
                    print(listToString(settings.string))
                    playsound('sounds/r.mp3')
            elif settings.counter <= 140:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "7 S T U", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F 4F 5F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('7')
                    print(listToString(settings.string))
                    playsound('sounds/7.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append('s')
                    print(listToString(settings.string))
                    playsound('sounds/s.mp3')
                elif settings.getfingernow == 4:
                    settings.string.append('t')
                    print(listToString(settings.string))
                    playsound('sounds/t.mp3')
                elif settings.getfingernow == 5:
                    settings.string.append('u')
                    print(listToString(settings.string))
                    playsound('sounds/u.mp3')
            elif settings.counter <= 160:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "8 V W X", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F 4F 5F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('8')
                    print(listToString(settings.string))
                    playsound('sounds/8.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append('v')
                    print(listToString(settings.string))
                    playsound('sounds/v.mp3')
                elif settings.getfingernow == 4:
                    settings.string.append('w')
                    print(listToString(settings.string))
                    playsound('sounds/w.mp3')
                elif settings.getfingernow == 5:
                    settings.string.append('x')
                    print(listToString(settings.string))
                    playsound('sounds/x.mp3')
            elif settings.counter <= 180:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "9 Y Z", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F 4F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('9')
                    print(listToString(settings.string))
                    playsound('sounds/9.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append('y')
                    print(listToString(settings.string))
                    playsound('sounds/y.mp3')
                elif settings.getfingernow == 4:
                    settings.string.append('z')
                    print(listToString(settings.string))
                    playsound('sounds/z.mp3')
            elif settings.counter < 200:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "0 Space", (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)
                cv2.putText(settings.selection_panel, "2F 3F", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "1F: Pause", (200, 400), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                cv2.putText(settings.selection_panel, "0F: Next Panel", (100, 500), cv2.FONT_HERSHEY_TRIPLEX, 2,
                            (255, 0, 255), 2)
                if settings.getfingernow == 2:
                    settings.string.append('0')
                    print(listToString(settings.string))
                    playsound('sounds/0.mp3')
                elif settings.getfingernow == 3:
                    settings.string.append(' ')
                    print(listToString(settings.string))
                    playsound('sounds/space.mp3')
            cv2.imshow("Hands Motion Keypad", settings.selection_panel)

        elif settings.defaultoutput == 2:
            if settings.getfingernow == 0:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "Silence", (300, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255),
                            2)

            elif settings.getfingernow == 1:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "C", (300, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255), 2)
                playsound('sounds/C4.mp3')
            elif settings.getfingernow == 2:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "D", (300, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255), 2)
                playsound('sounds/D4.mp3')
            elif settings.getfingernow == 3:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "E", (300, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255), 2)
                playsound('sounds/E4.mp3')
            elif settings.getfingernow == 4:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "F", (300, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255), 2)
                playsound('sounds/F4.mp3')
            elif settings.getfingernow == 5:
                settings.selection_panel = np.zeros((canvas_height, canvas_width))
                cv2.putText(settings.selection_panel, "G", (300, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255), 2)
                playsound('sounds/G4.mp3')

            cv2.imshow("Piano Key Panel", settings.selection_panel)

        elif settings.defaultoutput == 3:
            if settings.getfingernow == 1:
                snake_game.divert = 'L'
            if settings.getfingernow == 2:
                snake_game.divert = 'U'
            if settings.getfingernow == 3:
                snake_game.divert = 'D'
            if settings.getfingernow == 4:
                snake_game.divert = 'R'

            if snake_game.divert == 'U' and snake_game.directions != 'D':
                snake_game.directions = 'U'
            if snake_game.divert == 'D' and snake_game.directions != 'U':
                snake_game.directions = 'D'
            if snake_game.divert == 'L' and snake_game.directions != 'R':
                snake_game.directions = 'L'
            if snake_game.divert == 'R' and snake_game.directions != 'L':
                snake_game.directions = 'R'

            if snake_game.directions == 'U':
                snake_game.py_coor[1] -= 10
            if snake_game.directions == 'D':
                snake_game.py_coor[1] += 10
            if snake_game.directions == 'L':
                snake_game.py_coor[0] -= 10
            if snake_game.directions == 'R':
                snake_game.py_coor[0] += 10

            snake_game.py_obj.insert(0, list(snake_game.py_coor))
            if snake_game.py_coor[0] == snake_game.con_coor[0] and snake_game.py_coor[1] == snake_game.con_coor[1]:
                snake_game.score += 1  # 到紅色圓點，貪吃蛇就會身體長長
                snake_game.con_revive = False
            else:
                snake_game.py_obj.pop()

            if not snake_game.con_revive:
                snake_game.con_coor = [rand.randrange(1, (650 // 10)) * 10, rand.randrange(1, (400 // 10)) * 10]
            snake_game.con_revive = True

            snackline.fill(cg.Color(0, 0, 0))
            for pos in snake_game.py_obj:
                cg.draw.rect(snackline,
                             cg.Color(rand.randrange(0, 200), rand.randrange(0, 200), rand.randrange(0, 200)),
                             cg.Rect(pos[0], pos[1], 10, 10))

            cg.draw.rect(snackline, cg.Color(255, 0, 0), cg.Rect(snake_game.con_coor[0],
                                                                 snake_game.con_coor[1], 10, 10))

            if snake_game.py_coor[0] < 0 or snake_game.py_coor[0] > 650 - 10:
                fin()
            if snake_game.py_coor[1] < 0 or snake_game.py_coor[1] > 400 - 10:
                fin()

            for blk in snake_game.py_obj[1:]:
                if snake_game.py_coor[0] == blk[0] and snake_game.py_coor[1] == blk[1]:
                    fin()

            if settings.isRun:
                score_surface = score_font.render('Score : ' + str(snake_game.score) +
                                                  "          Control Guide: -Left:1F -Up:2F -Down:3F -Right:4F", True,
                                                  cg.Color(255, 255, 255))
                score_pos = score_surface.get_rect()
                score_pos.midtop = (300, 15)
                snackline.blit(score_surface, score_pos)

                cg.display.update()
                snake_game.clk.tick(5)

    root.after(1, OnProgramRun)


root = Tk()
root.title('HandsMultiMedia手多媒體系統 By 雷國亮 D0726433 - Hands Interpreter Control Panel 手譯員控制面板')
root.resizable(width=True, height=True)

menubar = Menu(root)

file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Menu 畫面', menu=file)
file.add_command(label='About 關於', command=popupmsg)
file.add_separator()
file.add_command(label='Exit 結束程式', command=root.destroy)

root.config(menu=menubar)

header = Frame(root)
header.pack()
body = Frame(root)
body.pack()
footer = Frame(root)
footer.pack()

label_input = Label(header, text="Input source 輸入源:")
label_input.pack()

b_livecam = Button(header, text='Live Camera 實時攝像頭', command=modetoggle)
b_livecam.pack(side='left', ipadx=20)
b_vfile = Button(header, text='Video File 影片檔案', command=modetoggle)
b_vfile.pack(side='left', ipadx=20)
b_sfile = Button(body, text='Select video file 選擇影片文件', command=select_file)
b_sfile.pack()

modetoggle()

junk = Label(body, text='')
junk.pack()

label_output = Label(body, text='Program Mode 程式模式:')
label_output.pack()

b_htv = Button(body, text='Hands To Voice 動手發字母表聲', command=sethtvactive)
b_htv.pack(side='left', ipadx=20)
b_np5 = Button(body, text='5 notes piano 音符鋼琴', command=setnp5active)
b_np5.pack(side='left', ipadx=20)
b_snake = Button(body, text='Snake game 蛇遊戲', command=setsnakeactive)
b_snake.pack(side='left', ipadx=20)

sethtvactive()

junk2 = Label(footer, text="")
junk2.pack()
condition = Label(footer, text="Program Status 程式狀態:")
condition.pack()

b_run = Button(footer, text='Run 運行', command=runprogram)
b_run.pack(side='left', ipadx=20)
b_terminate = Button(footer, text='Terminate 終止', command=terminateprogram)
b_terminate.pack(side='left', ipadx=20)

inittogstanby()

fr = Frame(body, width=600, height=600)
fr.update()
root.after(1, OnProgramRun)
root.mainloop()
