import curses
from math import *
from os import listdir
from os.path import isfile, join


screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad( 1 )
curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
highlightText = curses.color_pair( 1 )
normalText = curses.A_NORMAL
screen.border( 0 )
curses.curs_set( 0 )
max_row,max_col = screen.getmaxyx()
box = curses.newwin( max_row-2, int(max_col/2), 1, 1 )
box.box()


mypath = './words/'
strings = [f for f in listdir(mypath) if isfile(join(mypath, f))]
selected = []

# strings = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "l", "m", "n" ] #list of strings
row_num = len( strings )

pages = int( ceil( row_num / max_row ) )
position = 1
page = 1
for i in range( 1, max_row + 1 ):
    if row_num == 0:
        box.addstr( 1, 1, "There aren't strings", highlightText )
    else:
        if (i == position):
            box.addstr( i, 2, f"[{'#' if strings[i-1]in selected else ' '}]"+ " " + strings[ i - 1 ], highlightText )
        else:
            box.addstr( i, 2, f"[{'#' if strings[i-1]in selected else ' '}]" + " " + strings[ i - 1 ], normalText )
        if i == row_num:
            break

screen.refresh()
box.refresh()

x = screen.getch()
while x != 27:
    if x == curses.KEY_DOWN:
        if page == 1:
            if position < i:
                position = position + 1
            else:
                if pages > 1:
                    page = page + 1
                    position = 1 + ( max_row * ( page - 1 ) )
        elif page == pages:
            if position < row_num:
                position = position + 1
        else:
            if position < max_row + ( max_row * ( page - 1 ) ):
                position = position + 1
            else:
                page = page + 1
                position = 1 + ( max_row * ( page - 1 ) )
    if x == curses.KEY_UP:
        if page == 1:
            if position > 1:
                position = position - 1
        else:
            if position > ( 1 + ( max_row * ( page - 1 ) ) ):
                position = position - 1
            else:
                page = page - 1
                position = max_row + ( max_row * ( page - 1 ) )
    if x == curses.KEY_LEFT:
        if page > 1:
            page = page - 1
            position = 1 + ( max_row * ( page - 1 ) )

    if x == curses.KEY_RIGHT:
        if page < pages:
            page = page + 1
            position = ( 1 + ( max_row * ( page - 1 ) ) )
    if x == ord( "\n" ) and row_num != 0:
        screen.erase()
        screen.border( 0 )
        # screen.addstr( 14, 3, "YOU HAVE PRESSED '" + strings[ position - 1 ] + "' ON POSITION " + str( position ) )
        if strings[position-1] in selected: selected.remove(strings[position-1]) 
        else: selected.append(strings[position-1])
        screen.addstr(3, int(max_col/2)+2, f"")
    box.erase()
    screen.border( 0 )
    box.border( 0 )

    for i in range( 1 + ( max_row * ( page - 1 ) ), max_row + 1 + ( max_row * ( page - 1 ) ) ):
        if row_num == 0:
            box.addstr( 1, 1, "There aren't strings",  highlightText )
        else:
            if ( i + ( max_row * ( page - 1 ) ) == position + ( max_row * ( page - 1 ) ) ):
                box.addstr( i - ( max_row * ( page - 1 ) ), 2, f"[{'#' if strings[i-1]in selected else ' '}]"+ " " + strings[ i - 1 ], highlightText )
            else:
                box.addstr( i - ( max_row * ( page - 1 ) ), 2, f"[{'#' if strings[i-1]in selected else ' '}]"+ " " + strings[ i - 1 ], normalText )
            if i == row_num:
                break



    screen.refresh()
    box.refresh()
    x = screen.getch()

curses.endwin()
import main
main.main(selected)
exit()