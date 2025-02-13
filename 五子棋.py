import pygame
import random
import math

# 初始化窗口和棋盘
pygame.init()
window_size = (600, 600)
screen = pygame.display.set_mode(window_size)
board_size = 15
cell_size = 40
board_offset = (cell_size, cell_size)
board_width = cell_size * board_size
board_height = cell_size * board_size
background_color = (255, 255, 255)
line_color = (0, 0, 0)
player_color = (255, 0, 0)  # 将玩家棋子颜色修改为红色
ai_color = (0, 0, 255)  # 将AI棋子颜色修改为蓝色

# 初始化棋盘和棋局状态
board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
game_over = False


# 绘制棋盘网格
def draw_board():
    screen.fill(background_color)
    for i in range(1, board_size):
        pygame.draw.line(screen, line_color, (board_offset[0], board_offset[1] + i * cell_size),
                         (board_offset[0] + board_width, board_offset[1] + i * cell_size))
        pygame.draw.line(screen, line_color, (board_offset[0] + i * cell_size, board_offset[1]),
                         (board_offset[0] + i * cell_size, board_offset[1] + board_height))

    # 绘制棋子
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 'X':
                draw_piece(i, j, player_color)
            elif board[i][j] == 'O':
                draw_piece(i, j, ai_color)


# 绘制棋子
def draw_piece(row, col, color):
    x = board_offset[0] + col * cell_size
    y = board_offset[1] + row * cell_size
    pygame.draw.circle(screen, color, (x, y), cell_size // 2 - 2)


# 判断是否存在五子连珠的胜利局面
def check_win(row, col):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        count += count_in_direction(row, col, dx, dy)
        count += count_in_direction(row, col, -dx, -dy)
        if count >= 5:
            return True
    return False


# 在指定方向上统计棋局中相同颜色的棋子数量
def count_in_direction(row, col, dx, dy):
    count = 0
    r, c = row + dx, col + dy
    while r >= 0 and r < board_size and c >= 0 and c < board_size and board[r][c] == board[row][col]:
        count += 1
        r += dx
        c += dy
    return count


# AI的落子策略，使用蒙特卡洛树搜索算法
def ai_move():
    # 创建一个模拟棋盘，用于进行模拟对局
    simulation_board = [row[:] for row in board]

    # 蒙特卡洛树搜索参数
    simulations = 1000  # 模拟次数
    scores = [[0 for _ in range(board_size)] for _ in range(board_size)]  # 每个位置的得分

    for _ in range(simulations):
        # 判断是否还有空位可供落子
        if not any(' ' in row for row in simulation_board):
            break

        # 在模拟棋盘上随机下一步棋，直到模拟结束
        simulate_game(simulation_board)

        # 更新得分
        for i in range(board_size):
            for j in range(board_size):
                if simulation_board[i][j] == 'O':
                    scores[i][j] += 1

    # 找到得分最高的位置作为AI的落子位置
    max_score = -math.inf
    best_move = None
    for i in range(board_size):
        for j in range(board_size):
            if scores[i][j] > max_score and board[i][j] == ' ':
                max_score = scores[i][j]
                best_move = (i, j)

    return best_move


# 在模拟棋盘上执行一次模拟对局
def simulate_game(simulation_board):
    while True:
        # 随机选择一个空位落子
        empty_positions = [(i, j) for i in range(board_size) for j in range(board_size) if
                           simulation_board[i][j] == ' ']
        row, col = random.choice(empty_positions)
        simulation_board[row][col] = 'O'

        if check_win(row, col):
            break

        # 切换到玩家继续模拟对局
        empty_positions = [(i, j) for i in range(board_size) for j in range(board_size) if
                           simulation_board[i][j] == ' ']
        row, col = random.choice(empty_positions)
        simulation_board[row][col] = 'X'

        if check_win(row, col):
            break


# 主游戏循环
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                col = (pos[0] - board_offset[0]) // cell_size
                row = (pos[1] - board_offset[1]) // cell_size
                if 0 <= row < board_size and 0 <= col < board_size:  # 检查row和col的值是否在有效范围内
                    if board[row][col] == ' ':
                        board[row][col] = 'X'

                        if check_win(row, col):
                            print("恭喜您，您获胜了！")
                            game_over = True

                        if not game_over:
                            ai_row, ai_col = ai_move()
                            board[ai_row][ai_col] = 'O'

                            if check_win(ai_row, ai_col):
                                print("很遗憾，您输了！")
                                game_over = True

    draw_board()
    pygame.display.update()

pygame.quit()
print("游戏结束")