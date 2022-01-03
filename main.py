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


word_files = {}
max_words_len = 0

avaliable_words = set()
screen_words = {}
green,yellow,red,magenta = 0,0,0,0

write_str = ""

### STATS
score = 0

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
        self.color = green
    def get_x(self):
        return max(self.x,1)

    def kill(self):
        # avaliable_words.add(self.word)
        if(self.x<w-1): main_win.addstr(self.y,self.get_x(),len(str(self))*" ") 
        del screen_words[self.word]

    def __str__(self):
        if self.x > w/4*3: self.color = red
        elif self.x > w/2: self.color = yellow

        front=(self.word[-self.x+1:] if self.x<=0 else self.word)
        return front[:w-self.x-1] if self.x+len(front)>=w else front

def newWord(num):
    global all_words

    
    for _ in range(num):
        w = RandomWordFromFile()
        if w not in screen_words:
            avaliable_words.add(w)

            if(len(avaliable_words)==0):return
            all_words+=1

            pos_y = random.randint(1, h-stats_h-2)
            w = list(avaliable_words)[-1]
            screen_words[w] = Word(w,pos_y)
            avaliable_words.remove(w)

def RandomWordFromFile():
    k, v = random.choice(list(word_files.items()))
    r = random.randint(1, v)
    with open(f"./words/{k}", "r") as a_file:
            for line in a_file:
                r-=1
                if(r==0):
                    return line.strip('\n')


def gameTick():
    global main_win, screen_words, failed_points, score

    
    for word in list(screen_words.values()):
        if(word!=None):

            word.x+=1
            if(word.get_x()>=w):
                main_win.addstr(word.y,w-2,' ')
                failed_points+=1
                score-=len(word.word)
                word.kill()
            else:
                main_win.addstr(word.y,word.get_x(),str(word), word.color)
                if(word.get_x()>1):
                    main_win.addch(word.y, word.get_x()-1, ' ')

def InputField():
    global write_str, success_points, all_words, game_loop, score, magenta

    inpt = sc.getch()
    if(inpt == 127):#backspace
        write_str = write_str[:-1]
        
    elif(33<inpt<165 and len(write_str)<max_words_len):
        write_str+=str(chr(inpt))

        if(write_str in screen_words):
            score+=len(write_str)**2
            success_points+=1
            screen_words[write_str].kill()
            write_str=''
    
    elif(inpt == 27):#ESC
        game_loop=False


    stats_win.addstr(1,2,' '*max_words_len,curses.A_UNDERLINE)
    stats_win.addstr(1,2,write_str,curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(3))

    stats_win.addstr(1,max_words_len+3,f"{success_points}/{all_words}",curses.color_pair(1))
    
    sc.addstr(0,int(w/2-len(str(score))/2),"{"+str(score)+"}",magenta|curses.A_BOLD)

    stats_win.addstr(1, w-4, str(failed_points), curses.color_pair(2))

game_loop = True
def wrap(sc):
    global green,yellow,red,magenta

    if curses.has_colors():
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_CYAN, -1)

        curses.init_pair(4, curses.COLOR_GREEN, -1)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)

        green = curses.color_pair(4)
        yellow = curses.color_pair(5)
        red = curses.color_pair(2)

        curses.init_pair(6, curses.COLOR_WHITE, -1)
        magenta = curses.color_pair(6)


    

    last_game_tick=0
    game_tick = 0.3

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
            last_nextIn=time.time()
            nextIn = random.randint(3, 5)
            newWord(random.randint(0, 5))

        InputField()
        
        stats_win.refresh()

        main_win.refresh()

    
def main(selected = ["words.txt"]):
    global max_words_len

    for f in selected:
        word_files[f] = sum(1 for l in open(f'./words/{f}'))
        max_words_len = max( max([len(l) for l in open(f'./words/{f}')]),max_words_len)
    curses.wrapper(wrap)

    curses.nocbreak()
    sc.keypad(False)
    curses.echo()
    curses.endwin()

    print("\nGood Game, You have impressed me")
    print(f"Your score is {success_points} out of {all_words}\n")

    print(screen_words)

if __name__ == '__main__':
    main()