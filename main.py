import tkinter
import threading
import copy
import random


def change_color(color, ratio):
    """
    colorに入れた色をratioに入れた濃さで調整する
    :param color: #000000の形式で入力すること
    :param ratio: 0-200の整数で入力すること
    :return: 16進数の色情報を返す
    """
    color_rgb_r: int = int(color[1:3], 16)  # 16進数を10進数の整数に変換
    color_rgb_g: int = int(color[3:5], 16)  # int(s, base)はbaseで指定した進数を10進数に変換できる
    color_rgb_b: int = int(color[5:7], 16)

    if ratio > 100:  # 明るい色を作成
        rgb_r: int = int(((255 - color_rgb_r) * (ratio - 100) / 100) + color_rgb_r)
        rgb_g: int = int(((255 - color_rgb_g) * (ratio - 100) / 100) + color_rgb_g)
        rgb_b: int = int(((255 - color_rgb_b) * (ratio - 100) / 100) + color_rgb_b)

    else:  # 暗い色を作成
        rgb_r: int = int(color_rgb_r * ratio / 100)
        rgb_g: int = int(color_rgb_g * ratio / 100)
        rgb_b: int = int(color_rgb_b * ratio / 100)

    return '#%02x%02x%02x' % (rgb_r, rgb_g, rgb_b)  # %変換フォーマットを使用して10進数を16進数に変換


class BoardSize:
    """
    ボードのサイズを設定する定数を定義
    """
    PIECE: int = 20
    WIDTH: int = 10
    HEIGHT: int = 22


class Mino:
    """
    ブロックの形を定義
    [-1, -1], [0, -1], [1, -1]
    [-1, 0], [0, 0], [1, 0]
    [-1, 1], [0, 1], [1, 1]
    [-1, 2], [0, 2], [1, 2]
    """
    MINO_NO: list = [[0, 0], [0, 0], [0, 0], [0, 0]]
    MINO_Z: list = [[0, -1], [0, 0], [-1, 0], [-1, 1]]
    MINO_S: list = [[0, -1], [0, 0], [1, 0], [1, 1]]
    MINO_I: list = [[0, -1], [0, 0], [0, 1], [0, 2]]
    MINO_T: list = [[-1, 0], [0, 0], [1, 0], [0, 1]]
    MINO_O: list = [[0, 0], [1, 0], [0, 1], [1, 1]]
    MINO_L: list = [[-1, -1], [0, -1], [0, 0], [0, 1]]
    MINO_J: list = [[1, -1], [0, -1], [0, 0], [0, 1]]
    RED: str = '#ff0000'
    GREEN: str = '#00ff00'
    CYAN: str = '#00ffff'
    PURPLE: str = '#800080'
    YELLOW: str = '#ffff00'
    ORANGE: str = '#ffa500'
    BLUE: str = '#0000ff'
    MINO_TABLE: list = [MINO_NO,  # 0
                        MINO_Z,   # 1
                        MINO_S,   # 2
                        MINO_I,   # 3
                        MINO_T,   # 4
                        MINO_O,   # 5
                        MINO_L,   # 6
                        MINO_J]   # 7
    COLORS: list = ['black',
                    RED,
                    GREEN,
                    CYAN,
                    PURPLE,
                    YELLOW,
                    ORANGE,
                    BLUE]
    LIGHT: list = ['black']
    DARK: list = ['black']
    for i in range(1, 8):
        LIGHT.append(change_color(COLORS[i], 150))
        DARK.append(change_color(COLORS[i], 50))


class GameBoard(tkinter.Canvas):
    """
    ゲームボードを描画するクラス
    """
    def __init__(self, window: tkinter.Tk):
        """
        :param window: ウィンドウオブジェクトの名前(主にrootが入る)
        """
        tkinter.Canvas.__init__(self, window)
        self.init_game_board()
        self.draw_mino()

    def init_game_board(self):
        """
        ゲームボードを初期化
        :return:
        """
        self.mino_table: list = Mino.MINO_TABLE
        self.colors: list = Mino.COLORS
        self.light: list = Mino.LIGHT
        self.dark: list = Mino.DARK
        # 10x22マスのボードを作成
        self.board: list = []
        for number in range(BoardSize.HEIGHT):
            board_row: list = [0] * BoardSize.WIDTH
            self.board.append(board_row)

    def set_mino(self, set_board, mino_coords, x, y, mino_shape):
        for i in range(4):
            piece_y = mino_coords[i][1] + y
            piece_x = mino_coords[i][0] + x
            set_board[piece_y][piece_x] = mino_shape

    def draw_mino(self):
        """
        図形を描画
        """
        [x0, y0] = [2, 2]
        peace_size = BoardSize.PIECE - 1
        self.set_mino(self.board, self.mino_table[1], 5, 4, 1)
        self.set_mino(self.board, self.mino_table[2], 1, 10, 2)
        self.set_mino(self.board, self.mino_table[3], 4, 10, 3)
        self.set_mino(self.board, self.mino_table[4], 7, 10, 4)
        self.set_mino(self.board, self.mino_table[5], 1, 16, 5)
        self.set_mino(self.board, self.mino_table[6], 5, 16, 6)
        self.set_mino(self.board, self.mino_table[7], 7, 16, 7)

        for row in range(BoardSize.HEIGHT):
            for column in range(BoardSize.WIDTH):
                shape: int = self.board[row][column]
                tag_name = 'piece_' + str(row) + '_' + str(column)

                if shape != 0:
                    [xs, ys] = [x0 + column * BoardSize.PIECE, y0 + row * BoardSize.PIECE]
                    [xe, ye] = [xs + peace_size, ys + peace_size]
                    self.create_rectangle(xs + 1, ys + 1, xe, ye, fill=self.colors[shape],
                                          outline=self.dark[shape], width='2', tags=tag_name)
                    self.create_line(xs, ys + 1, xe - 1, ys + 1, fill=self.light[shape],
                                     width='2', tags=tag_name)
                    self.create_line(xs+1, ys, xs + 1, ye + 1, fill=self.light[shape],
                                     width='2', tags=tag_name)


class TetrisGame:
    """
    テトリスのゲーム作成クラス
    """
    def __init__(self, window: tkinter.Tk):
        """
        :param window: ウィンドウオブジェクトの名前(主にrootが入る)
        """
        self.window = window
        self.width = BoardSize.PIECE * BoardSize.WIDTH
        self.height = BoardSize.PIECE * BoardSize.HEIGHT
        game_board = GameBoard(window)
        game_board.place(x=0, y=0)
        game_board.config(width=self.width, height=self.height, bg='black', highlightthickness=2)
        self.center()

    def center(self):
        """
        canvasをスクリーンの中央に配置する
        """
        screen_width: int = self.window.winfo_screenwidth()
        screen_height: int = self.window.winfo_screenheight()
        x = int((screen_width / 2) - ((self.width + 4) / 2))
        y = int((screen_height / 2) - ((self.height + 4) / 2))
        self.window.geometry(f'{self.width + 4}x{self.height + 4}+{x}+{y}')


root = tkinter.Tk()
root.title('Tetris')
root.resizable(False, False)
tetris_game = TetrisGame(root)
root.mainloop()
