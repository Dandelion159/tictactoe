from Tkinter import *
import tkMessageBox
import socket as sk 

def init_connection():
	addr = raw_input("address: ")
	port = int(raw_input("port: "))

	cli = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
	print "Waiting for connection"
	cli.connect((addr,port))
	print "Connected"
	return cli

def oponent_move(cli):
	move = ""
	while move not in range(9):
		try:
			move = int(cli.recv(8))
			b[move].config(text="X")
			board[move] = -1
		except:
			break
def press(button):
	global cli
	if board[button] == 0:
		b[button].config(text="O")
		board[button] = 1
		cli.send(str(button))
		check_win()
		window.wm_title("Opponents move")
		window.update()
		oponent_move(cli)
		check_win()
		window.wm_title("Your move")

def check_win():
	v = [sum(board[i::3]) for i in range(3)]
	h = [sum(board[i:i+3]) for i in range(0,9,3)]
	d = [board[0]+board[4]+board[8],board[2]+board[4]+board[6]]
	print v
	print h
	print d
	if 3 in v+h+d:
		tkMessageBox.showinfo("Win","You win")
		window.quit()
	if -3 in v+h+d:
		tkMessageBox.showinfo("Win","Opponent wins")
		window.quit()

def on_closing():
	global cli
	cli.close()


cli = init_connection()
window = Tk()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.wm_title("You are O")

lines = [Frame(window) for i in range(3)]
map(lambda x: x.pack(), lines)

board = [
	0,0,0,
	0,0,0,
	0,0,0,
	]

b = map(lambda i: Button(
			lines[i/3],
			height = 4,
			width = 4,
			text = "",
			command = lambda: press(i)
			),
		range(9))

map(lambda x: x.pack(side = LEFT), b)
oponent_move(cli)
window.mainloop()
