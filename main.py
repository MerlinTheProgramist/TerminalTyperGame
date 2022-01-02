import curses
import time
import random
import math as m
# import traceback


stats_h = 3

sc = curses.initscr()

h, w = sc.getmaxyx()
main_win = curses.newwin(h-stats_h, w, 0, 0)
main_win.clear()

main_win.border(0)

stats_win = curses.newwin(stats_h,w,h-stats_h,0)



avaliable_words = set()
screen_words = {}

write_str = ""

### STATS
success_points = 0
all_words = 0
failed_points = 0
# ...


class Stats():
    pass

class Word():
    def __init__(self,word,pos):
        self.word = str(word)
        self.y = pos
        self.x = -len(self.word)+1
    def get_x(self):
        return max(self.x,1)

    def kill(self):
        avaliable_words.add(self.word)
        if(self.x<w-1): main_win.addstr(self.y,self.get_x(),len(str(self))*" ") 
        del screen_words[self.word]

    def __str__(self):
        front=(self.word[-self.x+1:] if self.x<=0 else self.word)
        return front[:w-self.x-1] if self.x+len(front)>=w else front

def newWord(num):
    global all_words

    
    for _ in range(num):
        avaliable_words.add(RandomWordFromFile())

        if(len(avaliable_words)==0):return
        all_words+=1

        pos_y = random.randint(1, h-stats_h-2)
        w = list(avaliable_words)[-1]
        screen_words[w] = Word(w,pos_y)
        avaliable_words.remove(w)

def RandomWordFromFile():
    r = random.randint(1, 286753)
    with open("words.txt", "r") as a_file:
            for line in a_file:
                r-=1
                if(r==0):
                    return line.strip('\n')


def gameTick():
    global main_win, screen_words, failed_points

    
    for word in list(screen_words.values()):
        if(word!=None):

            word.x+=1
            if(word.get_x()>=w):
                main_win.addstr(word.y,w-2,' ')
                failed_points+=1
                word.kill()
            else:
                main_win.addstr(word.y,word.get_x(),str(word))
                if(word.get_x()>1):
                    main_win.addch(word.y, word.get_x()-1, ' ')

def InputField():
    global write_str, success_points, all_words, game_loop

    inpt = sc.getch()
    if(inpt == 127):#backspace
        write_str = write_str[:-1]
        
    elif(33<inpt<165 and len(write_str)<10):
        write_str+=str(chr(inpt))

        if(write_str in screen_words):
            success_points+=1
            screen_words[write_str].kill()
            write_str=''
    
    elif(inpt == 27):#ESC
        game_loop=False


    stats_win.addstr(1,2,' '*15,curses.A_UNDERLINE)
    stats_win.addstr(1,2,write_str,curses.A_UNDERLINE | curses.color_pair(3))

    stats_win.addstr(1,20,f"{success_points}/{all_words}",curses.color_pair(1))
    stats_win.addstr(1, w-4, str(failed_points), curses.color_pair(2))

game_loop = True
def main(sc):

    if curses.has_colors():
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_MAGENTA, -1)


    

    last_game_tick=0
    game_tick = 0.5

    nextIn = 5#s
    last_nextIn = 0

    #START
    curses.noecho()
    curses.cbreak()
    sc.keypad(True)
    curses.curs_set(False)
    sc.timeout(20)

    newWord(4)

    
    while game_loop:
        

        if(time.time()-last_game_tick>game_tick):
            gameTick()
            last_game_tick=time.time()

        if(time.time()-last_nextIn>nextIn):
            nextIn -=random.randint(1, 3)/10
            last_nextIn=time.time()
            newWord(random.randint(0, 3))

        InputField()
        
        stats_win.refresh()

        main_win.refresh()

    

curses.wrapper(main)

curses.nocbreak()
sc.keypad(False)
curses.echo()
curses.endwin()

print("\nGood Game, You have impressed me")
print(f"Your score is {success_points} out of {all_words}\n")

print(screen_words)