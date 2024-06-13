import tkinter as tk
from copy import deepcopy
from tkinter import messagebox


HUMAN_VS_COMPUTER = "Human vs. Computer"
HUMAN_VS_HUMAN = "Human vs. Human"


class DifficultyAndPlayerSelectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Othello - Difficulty and Player Selection")
        self.difficulty = "Easy"  # Default difficulty
        self.player_type = HUMAN_VS_COMPUTER  # Default player type
        self.create_widgets()

    def create_widgets(self):
        difficulty_label = tk.Label(self.root, text="Select Difficulty:")
        difficulty_label.pack()
        self.difficulty_var = tk.StringVar()
        difficulty_options = ["Easy", "Medium", "Hard"]
        self.difficulty_var.set("Easy")  # Default selection
        difficulty_menu = tk.OptionMenu(self.root, self.difficulty_var, *difficulty_options)
        difficulty_menu.pack()

        player_label = tk.Label(self.root, text="Select Player Type:")
        player_label.pack()
        self.player_var = tk.StringVar()
        player_options = [HUMAN_VS_COMPUTER, HUMAN_VS_HUMAN]
        self.player_var.set(HUMAN_VS_COMPUTER)  # Default selection
        player_menu = tk.OptionMenu(self.root, self.player_var, *player_options)
        player_menu.pack()

        start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        start_button.pack()

    def start_game(self):
        self.difficulty = self.difficulty_var.get()
        self.player_type = self.player_var.get()
        self.root.destroy()  # Close the current window
        game_window = tk.Tk()
        game_app = OthelloGameGUI(game_window, self.difficulty, self.player_type)
        game_window.mainloop()

class Othello:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.current_player = 'B'
        self.black_tiles_placed = 2
        self.white_tiles_placed = 2

    def is_valid_move(self, row_index, col, next_player=None):
        if self.board[row_index][col] != ' ':
            return False
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        opponent = next_player if next_player else ('W' if self.current_player == 'B' else 'B')
        for dr, dc in directions:
            r, c = row_index + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    return True
        return False
    def execute_move(self, move, color):
        row, col = move
        if self.is_valid_move(row, col, color):
            self.board[row][col] = color
            self.flip_tiles(row, col, color)
    def make_move(self, row_index, col):
        if not self.is_valid_move(row_index, col):
            return False
        self.board[row_index][col] = self.current_player
        self.update_tiles_count(self.current_player)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        opponent = 'W' if self.current_player == 'B' else 'B'
        for dr, dc in directions:
            r, c = row_index + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    r -= dr
                    c -= dc
                    while self.board[r][c] == opponent:
                        self.board[r][c] = self.current_player
                        self.update_tiles_count(self.current_player)
                        r -= dr
                        c -= dc
        self.current_player = 'W' if self.current_player == 'B' else 'B'
        return True

    def update_tiles_count(self, player):
        if player == 'B':
            self.black_tiles_placed += 1
        else:
            self.white_tiles_placed += 1

    def check_valid_moves(self,player=None):
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j,player):
                    return True
        return False

    def count_pieces(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return black_count, white_count

    def is_game_over(self):
        whitemoves = self.get_legal_moves('W')
        blackmoves = self.get_legal_moves('B')
        black_count, white_count = self.count_pieces()
        if black_count + white_count == 64 or (not whitemoves and not blackmoves):
            return True
        return False

    def get_winner(self):
        black_count, white_count = self.count_pieces()
        if black_count > white_count:
            return 'Black'
        elif white_count > black_count:
            return 'White'
        else:
            return 'Draw'

    def get_legal_moves(self, color):
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == ' ':
                    for dr, dc in directions:
                        r, c = i + dr, j + dc
                        if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != ' ' and self.board[r][c] != color:
                            while 0 <= r < 8 and 0 <= c < 8:
                                r += dr
                                c += dc
                                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == color:
                                    moves.append((i, j))
                                    break
                                elif 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == ' ':
                                    break
        return moves
    def skip_turn(self):
        # Skip the turn if no valid moves are available for the current player
        self.current_player = 'W' if self.current_player == 'B' else 'B'

    def flip_tiles(self, row, col, color):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != ' ' and self.board[r][c] != color:
                to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == color:
                for flip_row, flip_col in to_flip:
                    self.board[flip_row][flip_col] = color

class AIPlayer:
    def __init__(self, color, difficulty):
        self.color = color
        self.difficulty = difficulty
        self.depth = self.set_depth()

    def set_depth(self):
        if self.difficulty == "Easy":
            return 1
        elif self.difficulty == "Medium":
            return 3
        elif self.difficulty == "Hard":
            return 5

    def minmax_with_alpha_beta(self, board, color, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            return self.evaluation(board, color), None

        moves = board.get_legal_moves(color)
        if not moves:
            return self.evaluation(board, color), None

        best_score = float('-inf') if color == self.color else float('inf')
        best_move = None

        for move in moves:
            new_board = deepcopy(board)
            new_board.execute_move(move, color)
            score, _ = self.minmax_with_alpha_beta(new_board, 'W' if color == 'B' else 'B', depth - 1, alpha, beta)

            # Handle the case where score is None
            if score is None:
                score = float('-inf') if color == self.color else float('inf')

            if color == self.color:
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        return best_score, best_move

    def max_score_alpha_beta(self, board, color, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            return self.evaluation(board, self.color)

        moves = board.get_legal_moves(color)
        if not moves:
            return self.evaluation(board, self.color)

        best_score = -float('inf')
        for move in moves:
            new_board = deepcopy(board)
            new_board.execute_move(move, color)
            score = self.min_score_alpha_beta(new_board, -color, depth - 1, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_score

    def min_score_alpha_beta(self, board, color, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            return self.evaluation(board, self.color)

        moves = board.get_legal_moves(color)
        if not moves:
            return self.evaluation(board, self.color)

        best_score = float('inf')
        for move in moves:
            new_board = deepcopy(board)
            new_board.execute_move(move, color)
            score = self.max_score_alpha_beta(new_board, -color, depth - 1, alpha, beta)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return best_score
    def evaluation(self, board, color):
        # Define weights for different features of the board
        corner_weight = 25
        edge_weight = 5
        mobility_weight = 2

        # Evaluate the number of pieces on the board
        black_count, white_count = board.count_pieces()
        if color == 'B':
            score = black_count - white_count
        else:
            score = white_count - black_count

        # Evaluate the presence of pieces in corners
        corner_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for corner in corner_positions:
            if board.board[corner[0]][corner[1]] == color:
                score += corner_weight if color == 'B' else -corner_weight
            elif board.board[corner[0]][corner[1]] != ' ':
                score -= corner_weight if color == 'B' else -corner_weight

        # Evaluate the presence of pieces on edges
        edge_positions = [(0, 2), (0, 3), (0, 4), (0, 5),
                          (2, 0), (3, 0), (4, 0), (5, 0),
                          (2, 7), (3, 7), (4, 7), (5, 7),
                          (7, 2), (7, 3), (7, 4), (7, 5)]
        for edge in edge_positions:
            if board.board[edge[0]][edge[1]] == color:
                score += edge_weight if color == 'B' else -edge_weight
            elif board.board[edge[0]][edge[1]] != ' ':
                score -= edge_weight if color == 'B' else -edge_weight

        # Evaluate the mobility of the player (number of legal moves)
        mobility = len(board.get_legal_moves(color))
        score += mobility * mobility_weight

        # Evaluate the stability of the player's pieces
        # You can implement more advanced stability evaluation techniques here

        return score
    def get_best_move(self, game):
        _, best_move = self.minmax_with_alpha_beta(game, self.color, self.depth, -float('inf'), float('inf'))
        if best_move is not None:
            return best_move  # Returning the move tuple (row, col)
        else:
            return None  # Or handle the case where no move is found

class OthelloGameGUI:
    def __init__(self, root, difficulty, player_type):
        self.root = root
        self.root.title("Othello - Game")
        self.game = Othello()
        self.difficulty = difficulty
        self.player_type = player_type
        self.current_player = 'B'
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='green')
        self.canvas.pack()

        self.draw_board()

        self.canvas.bind("<Button-1>", self.play)

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        if self.player_type == HUMAN_VS_COMPUTER and self.current_player == 'W':
            self.computer_move()

    def draw_board(self):
        self.canvas.delete("pieces")
        for i in range(8):
            for j in range(8):
                x0, y0 = 50 * j, 50 * i
                x1, y1 = 50 * (j + 1), 50 * (i + 1)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='green', outline='black')
                if self.game.board[i][j] == 'B':
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill='black', tags="pieces")
                elif self.game.board[i][j] == 'W':
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill='white', tags="pieces")
                elif (i, j) in self.get_valid_moves():
                    self.canvas.create_oval(x0 + 20, y0 + 20, x1 - 20, y1 - 20, fill='grey', tags="pieces")

    def get_valid_moves(self):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.game.is_valid_move(i, j):
                    valid_moves.append((i, j))
        return valid_moves

    def play(self, event):
        if not self.game.is_game_over():
            if self.player_type == HUMAN_VS_HUMAN:
                # For Human vs. Human mode
                col = event.x // 50
                row = event.y // 50
                if self.game.make_move(row, col):
                    self.draw_board()
                    if self.game.is_game_over():
                        winner = self.game.get_winner()
                        messagebox.showinfo("Game Over", f"The winner is {winner}")
                        self.root.destroy()
                    else:
                        self.current_player = 'W' if self.current_player == 'B' else 'B'
            elif self.player_type == HUMAN_VS_COMPUTER:
                if self.current_player == 'B':
                    # For Human vs. Computer mode when it's the human player's turn
                    col = event.x // 50
                    row = event.y // 50
                    if self.game.make_move(row, col):
                        self.draw_board()
                        if self.game.is_game_over():
                            winner = self.game.get_winner()
                            messagebox.showinfo("Game Over", f"The winner is {winner}")
                            self.root.destroy()
                        else:
                            self.current_player = 'W'
                            self.computer_move()
                else:
                    # For Human vs. Computer mode when it's the computer's turn
                    self.computer_move()

        if not self.game.check_valid_moves():
            # If no valid moves for the current player, skip the turn
            self.game.skip_turn()
            self.current_player = 'W' if self.current_player == 'B' else 'B'
        if not self.game.is_game_over():
            self.draw_board()

    def computer_move(self):
        ai_player = AIPlayer('W', self.difficulty)
        move = ai_player.get_best_move(self.game)
        if move:
            self.game.make_move(move[0], move[1])
            self.draw_board()
            if self.game.is_game_over():
                winner = self.game.get_winner()
                messagebox.showinfo("Game Over", f"The winner is {winner}")
                self.root.destroy()
            else:
                self.current_player = 'B'


def main():
    selection_window = tk.Tk()
    selection_app = DifficultyAndPlayerSelectionGUI(selection_window)
    selection_window.mainloop()


if __name__ == "__main__":
    main()