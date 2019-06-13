#!/usr/bin/python2
# coding: utf-8

from Tkinter import *
from random import *
from functools import partial


class Game:
    def __init__(self):
        self.col = 20
        self.row = 10
        self.bomb_num = self.col * self.row // 6
        self.bomb_count = self.bomb_num
        self.bomb_find = 0
        self.field = []
        self.game = "stop" #stop, run, boom, victory
        self.interface()

    def mainloop(self):
        self.tk.mainloop()

    def interface(self):
        self.tk = Tk()
        self.tk.title("Минер")
        self.lbl = Label(self.tk, text="Привет!!!", font="14")
        self.lbl.grid(row=0, column=0, columnspan=self.col)
        self.mm = Menu()
        self.mm.add_command(label="Новая", command=self.new_game)
        self.mm.add_command(label="Выход", command=self.close)
        self.tk.config(menu=self.mm)
        self.btns = []
        for r in range(self.row):
            for c in range(self.col):
                btn = Button(self.tk, text="", width=1, font="14", 
                        command=partial(self.click, r, c))
                btn.bind('<Button-3>', 
                    lambda event, row=r, col=c: self.right_click(row, col))
                btn.grid(row=r+1, column=c)
                self.btns.append(btn)

    def close(self):
        self.tk.destroy()

    def new_game(self):
        self.lbl["text"] = "Новая игра. Мин: " + \
            str(self.bomb_find) + " / " + str(self.bomb_num)
        for b in range(self.col * self.row):
            btn = self.btns[b]
            btn["text"] = ""
            btn["relief"] = "raise"
            btn["bg"] = "gray95"
            btn["fg"] = "black"
        self.field = ["space" for i in range(self.row * self.col)]
        for i in range(self.bomb_num):
            self.field[i] = "bomb"
        shuffle(self.field)
        self.game = "run"

    def click(self, row, col):
        if self.game != "run":
            return
        index = row * self.col + col
        btn = self.btns[index]
        if btn["relief"] == "sunken":
            return
        btn["relief"] = "sunken"
        btn["bg"] = "gray80"
        if self.field[index] == "bomb":
            btn["text"] = "б"
            btn["bg"] = "red"
            self.game_over(index)
            return
        bomb = self.calck_bomb(index)
        if bomb > 0:
            btn["text"] = bomb
        else:
            self.clear_space(index)

    def right_click(self, row, col):
        if self.game != "run":
            return
        index = row * self.col + col
        btn = self.btns[index]
        if btn["relief"] == "sunken":
            return
        if btn["text"] == "":
            btn["text"] = "!"
            self.bomb_find += 1
        elif btn["text"] == "!":
            btn["text"] = "?"
            self.bomb_find -= 1
        else:
            btn["text"] = ""
        self.lbl["text"] = "Мин: " + \
            str(self.bomb_find) + " / " + str(self.bomb_num)
        if self.bomb_find == self.bomb_num:
            if self.check_game():
                self.game = "victory"
                self.lbl["text"] = "П О Б Е Д А ! ! !"

    def game_over(self, index):
        self.game = "boom"
        self.lbl["text"] = "П Р О В А Л ! ! !"
        for i in range(self.row * self.col):
            if i != index and self.field[i] == "bomb":
                btn = self.btns[i]
                btn["relief"] = "sunken"
                btn["text"] = "б"
                btn["bg"] = "black"
                btn["fg"] = "red"

    def calck_bomb(self, index):
        num = 0
        col = index % self.col
        row = index // self.col
        col_nw = col
        row_nw = row
        col_se = col
        row_se = row
        if col > 0:
            col_nw -= 1
        if col < self.col - 1:
            col_se += 1
        if row > 0:
            row_nw -= 1
        if row < self.row - 1:
            row_se += 1
        for r in range(row_nw, row_se + 1):
            for c in range(col_nw, col_se + 1):
                if c == col and r == row:
                    pass
                else:
                    i = r * self.col + c
                    if self.field[i] == "bomb":
                        num += 1
        return num

    def clear_space(self, index):
        space_base = self.clear(index)
        while len(space_base) > 0:
            i = space_base.pop()
            space = self.clear(i)
            if len(space) > 0:
                for j in space:
                    if j in space_base:
                        space.remove(j)
            space_base.extend(space)

    def clear(self, index):
        col = index % self.col
        row = index // self.col
        col_nw = col
        row_nw = row
        col_se = col
        row_se = row
        space = []
        if col > 0:
            col_nw -= 1
        if col < self.col - 1:
            col_se += 1
        if row > 0:
            row_nw -= 1
        if row < self.row - 1:
            row_se += 1
        for r in range(row_nw, row_se + 1):
            for c in range(col_nw, col_se + 1):
                if c == col and r == row:
                    pass
                else:
                    i = r * self.col + c
                    bomb = self.calck_bomb(i)
                    btn = self.btns[i]
                    if bomb > 0:
                        btn["text"] = bomb
                    else:
                        if btn["relief"] != "sunken":
                            space.append(i)
                    btn["relief"] = "sunken"
                    btn["bg"] = "gray80"
        return space

    def check_game(self):
        for i in range(self.row * self.col):
            if self.field[i] == "bomb":
                if self.btns[i]["text"] != "!":
                    return False
        return True

if __name__ == "__main__":
    g = Game()
    g.mainloop()
