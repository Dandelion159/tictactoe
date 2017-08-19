from Tkinter import *
import socket as sk 
import tkMessageBox

def init_connection():
	addr = raw_input("address: ")
	port = int(raw_input("port: "))

	srv = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
	srv.bind((addr,port))
	srv.listen(1)
	print "Waiting for connection"
	cli,addr = srv.accept()
	print "Connection established"
	return cli

def oponent_move(cli):
	move = ""
	while move not in range(9):
		move = cli.recv(8)
		if move:
			move = int(move)

	b[move].config(text="O")
	board[move] = -1
	
	
def press(button):
	global cli
	if board[button] == 0:
		b[button].config(text="X")
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
	global serv,cli
	serv.close()
	cli.close()


cli = init_connection()
window = Tk()
window.wm_title("You are X")
window.protocol("WM_DELETE_WINDOW", on_closing)

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
window.mainloop()
