import tkinter as tk
import random
import math

def initialize_board():
    return [[None, None, None] for _ in range(3)]

board = initialize_board()
current_player = 'X'  # X goes first
prev_row, prev_col = -1, -1 
game_started=False
playing_ai=False

def draw_board(canvas):
    canvas.delete("all")
    for i in range(1, 3):
        canvas.create_line(i * 266, 0, i * 266, 800, width=5)
        canvas.create_line(0, i * 266, 800, i * 266, width=5)

def display_winner(winner):
    global game_started
    game_started=False
    canvas.delete("all")  # Clear the canvas
    if winner == "tie":
        text = "It's a tie!"
    else:
        text = f"{winner} wins!"
    canvas.create_text(400, 350, text=text, font=('Arial', 40, 'bold'), fill="black")
    twoplayer_button = tk.Button(root, text="2 Players", command=lambda:restart_game(False))
    ai_button = tk.Button(root, text="AI vs Player", command=lambda:restart_game(True))
    canvas.create_window(300, 450, window=twoplayer_button) 
    canvas.create_window(500, 450, window=ai_button) 

def restart_game(x):
    global board, current_player,game_started,playing_ai
    game_started=True
    board = initialize_board()
    current_player = 'X'
    canvas.delete("all")
    draw_board(canvas)
    if(x):
        playing_ai=True
        ai()
    else:
        playing_ai=False
    canvas.bind("<Button-1>", canvas_click)  
    canvas.bind("<Motion>", hover) 

root = tk.Tk()
root.title("Tic Tac Toe")
canvas = tk.Canvas(root, width=800, height=800, bg='white')
canvas.pack()


def hover(event):
    global prev_row, prev_col, current_player
    if game_started:
        x, y = event.x, event.y
        row, col = y // 266, x // 266
        if(row!=prev_row or col!=prev_col):
            if prev_row >= 0 and prev_col >= 0 and board[prev_row][prev_col] is None:
                clear_cell(prev_row, prev_col)  # Clear previous hover
            if board[row][col] is None:
                if playing_ai:
                    draw_move(row, col, 'O', "gray")
                else:
                    draw_move(row, col, current_player, "gray")  # Draw new hover
            prev_row, prev_col = row, col

def clear_cell(row, col):
    x = col * 266 + 133
    y = row * 266 + 133
    canvas.create_rectangle(x - 110, y - 110, x + 110, y + 110, outline='', fill='white', width=0)

def canvas_click(event):
    global current_player,prev_col,prev_row
    x, y = event.x, event.y
    row, col = y // 266, x // 266  # Determine grid position
    prev_row,prev_col=row,col
    if board[row][col] is None:  # Check if cell is empty
        board[row][col] = current_player
        draw_move(row, col, current_player,"black")
        check_game_status(row,col,current_player)
        if playing_ai:
            ai()

def draw_move(row, col, player,color):
    x = col * 266 + 133  # Center of the cell
    y = row * 266 + 133
    if player == 'X':
        canvas.create_line(x - 100, y - 100, x + 100, y + 100, width=4,fill=color)
        canvas.create_line(x + 100, y - 100, x - 100, y + 100, width=4,fill=color)
    else:  # Draw O
        canvas.create_oval(x - 100, y - 100, x + 100, y + 100, width=4,outline=color)

def check_winner(row, col, player):
    # Horizontal, vertical, and diagonal checks
    win = all(board[row][i] == player for i in range(3)) or \
          all(board[i][col] == player for i in range(3)) or \
          (row == col and all(board[i][i] == player for i in range(3))) or \
          (row + col == 2 and all(board[i][2-i] == player for i in range(3)))
    return win

def check_tie():
    return all(all(cell is not None for cell in row) for row in board)

def avail_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]

def check_game_status(row, col, player):
    global current_player
    if check_winner(row, col, player):
        display_winner(player)
    elif check_tie():
        display_winner("tie")
    else:
        current_player = 'O' if player == 'X' else 'X'

def ai():
    moves=avail_moves(board)
    if len(moves)==9:
        global current_player
        row,col=random.choice(moves)
        draw_move(row,col,current_player,"black")
        board[row][col] = current_player
        current_player = 'O' if current_player == 'X' else 'X'
    else:
        row,col=minimax(board,current_player,prev_row,prev_col,current_player)['position']
        draw_move(row,col,current_player,"black")
        board[row][col] = current_player
        root.after(500, check_game_status, row, col, current_player)

def minimax(board,current_player,prev_row,prev_col,og_player):
    max_player=og_player
    other_player = 'O' if current_player == 'X' else 'X'
    if check_winner(prev_row,prev_col,other_player):
         return {'position': None, 'score': 1 * (len(avail_moves(board)) + 1) if other_player == max_player else -1 * (len(avail_moves(board)) + 1)}
    elif len(avail_moves(board))==0:
        return{'position':None,'score':0}
    
    if current_player == max_player:
        best = {'position': None, 'score': -math.inf}  # each score should maximize
    else:
        best = {'position': None, 'score': math.inf}  # each score should minimize
    for possible_move in avail_moves(board):
        row,col=possible_move
        board[row][col] = current_player
        sim_score=minimax(board,other_player,row,col,og_player)

        board[row][col]=None
        sim_score['position'] = possible_move  # this represents the move optimal next move

        if current_player == max_player:  # X is max player
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    print(best)
    return best
# Start the Tkinter event loop
if game_started:
    canvas.bind("<Button-1>", canvas_click)
    canvas.bind("<Motion>",hover)
else:
    canvas.create_text(400, 350, text="Choose Game Mode", font=('Arial', 40, 'bold'), fill="black")
    twoplayer_button = tk.Button(root, text="2 Players", command=lambda:restart_game(False))
    ai_button = tk.Button(root, text="AI vs Player", command=lambda:restart_game(True))
    canvas.create_window(300, 450, window=twoplayer_button) 
    canvas.create_window(500, 450, window=ai_button) 


root.mainloop()