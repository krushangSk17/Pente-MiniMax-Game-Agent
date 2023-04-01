import time
import copy
import timeit
import numpy as np

start_time = time.time()

neg_inf = float('-inf')
pos_inf = float('inf')
board_len = 19
resulttime = 0
blackpieces = {}
whitepieces = {}

termianl_board = {}


def isTerminal(blackpieces, whitepieces):
    point = 1000000
    found = False
    for piece in whitepieces:
        if (count(5, piece, whitepieces)):
            found = 'w'
            break

    for piece in blackpieces:
        if (count(5, piece, blackpieces)):
            found = 'b'
            break

    froz_b = frozenset(blackpieces)
    froz_w = frozenset(whitepieces)

    if (found != False):
        termianl_board[(froz_b, froz_w)] = point * (1 if player == found else -1)
        return termianl_board[(froz_b, froz_w)]
    termianl_board[(froz_b, froz_w)] = False
    return False


def count(number, piece, playerpieces):
    neigh = [(0, 1), (1, 0), (1, 1), (1, -1)]
    count = 0
    for next in neigh:
        (a, b) = piece
        for i in range(number - 1):
            (a, b) = (a + next[0], b + next[1])
            if ((a, b) in playerpieces):
                flag = True
            else:
                flag = False
                break

        if (flag == True):
            count += 1
    return count


def counteightdir(number, piece, playerpieces):
    neigh = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    count = 0
    for next in neigh:
        (a, b) = piece
        for i in range(number - 1):
            (a, b) = (a + next[0], b + next[1])
            if ((a, b) in playerpieces):
                flag = True
            else:
                flag = False
                break

        if (flag == True):
            count += 1
    return count


def is2capture(player, piece, blackpieces, whitepieces):
    playerpieces = whitepieces if player == 'w' else blackpieces
    oppopieces = whitepieces if player == 'b' else blackpieces

    neigh = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    count = 0
    for next in neigh:
        (a, b) = piece
        for i in range(3):
            (a, b) = (a + next[0], b + next[1])
            if (i == 2):
                if ((a, b) not in playerpieces and (a, b) not in oppopieces):
                    flag = True
                else:
                    flag = False
                    break
            else:
                if ((a, b) in oppopieces):
                    flag = True
                else:
                    flag = False
                    break

        if (flag == True):
            count += 1
    return count


def reduceGrid(board):
    top = False
    for i in range(len(board)):
        for j in range(len(board[0])):
            if (board[i][j] != '.'):
                if (top == False):
                    top = (i, j)
                bottom = (i, j)
            if (board[i][j] == 'w'):
                whitepieces[(i, j)] = 1
            if (board[i][j] == 'b'):
                blackpieces[(i, j)] = 1

    left = False
    for i in range(len(board[0])):
        for j in range(len(board)):
            if (board[j][i] != '.'):
                if (left == False):
                    left = (j, i)
                right = (j, i)

    if (top == False):
        return (9, 10, 9, 10)

    i_start = max(0, top[0] - gap)
    i_end = min(19, bottom[0] + gap + 1)
    j_start = max(0, left[1] - gap)
    j_end = min(19, right[1] + gap + 1)

    return (i_start, i_end, j_start, j_end)


def isopen(number, piece, playerpieces, oppopieces):
    neigh = [(0, 1), (1, 0), (1, 1), (1, -1)]
    count = 0
    for next in neigh:
        (a, b) = piece
        if ((a - next[0], b - next[1]) in playerpieces or (a - next[0], b - next[1]) in oppopieces):
            continue
        flag = False
        for i in range(number):
            (a, b) = (a + next[0], b + next[1])
            if (i == number - 1):
                if ((a, b) not in oppopieces and (a, b) not in playerpieces):
                    flag = True
                else:
                    flag = False
                    break
            else:
                if ((a, b) in playerpieces):
                    flag = True
                else:
                    flag = False
                    break

        if (flag == True):
            count += 1
    return count

def isopenoneside(number, piece, playerpieces, oppopieces):
    neigh = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    count = 0
    for next in neigh:
        (a, b) = piece
        flag = False
        for i in range(number):
            (a, b) = (a + next[0], b + next[1])
            if (i == number - 1):
                if ((a, b) not in oppopieces and (a, b) not in playerpieces):
                    flag = True
                else:
                    flag = False
                    break
            else:
                if ((a, b) in playerpieces):
                    flag = True
                else:
                    flag = False
                    break

        if (flag == True):
            count += 1
    return count


evalboard_dict = {}


def evalBoard(player, blackpieces, whitepieces, cap_by_black, cap_by_white,caller):
    black_capture_count = 0
    white_capture_count = 0

    black_capture_3_count = 0
    white_capture_3_count = 0

    w_open3 = 0
    b_open3 = 0
    w_open4 = 0
    w_open4_1side = 0
    b_open4 = 0
    b_open4_1side = 0

    w_2_ct = 0
    w_3_ct = 0
    w_4_ct = 0
    b_2_ct = 0
    b_3_ct = 0
    b_4_ct = 0

    for piece in blackpieces:
        if (caller == 'min'):
            b_open4_1side += isopenoneside(4, piece, blackpieces, whitepieces)
            if (b_open4_1side > 0 and player == 'w'):
                return neg_inf
        b_4_ct += count(4, piece, blackpieces)
        b_3_ct += count(3, piece, blackpieces)
        b_2_ct += count(2, piece, blackpieces)
        white_capture_3_count += counteightdir(4, piece, whitepieces)
        white_capture_count += is2capture('b', piece, blackpieces, whitepieces)
        b_open3 += isopen(3, piece, blackpieces, whitepieces)
        b_open4 += isopen(4, piece, blackpieces, whitepieces)


    for piece in whitepieces:
        if (caller == 'min'):
            w_open4_1side += isopenoneside(4, piece, whitepieces, blackpieces)
            if (w_open4_1side > 0 and player == 'b'):
                return neg_inf
        w_4_ct += count(4, piece, whitepieces)
        w_3_ct += count(3, piece, whitepieces)
        w_2_ct += count(2, piece, whitepieces)
        black_capture_3_count += counteightdir(4, piece, blackpieces)
        black_capture_count += is2capture('w', piece, blackpieces, whitepieces)
        w_open3 += isopen(3, piece, whitepieces, blackpieces)
        w_open4 += isopen(4, piece, whitepieces, blackpieces)


    point = {2: 400, 3: 900, 4: 800, 'capture': -1000, '3_capture': -5000, '3open': 10000, '4open': 100000,
             'capturepoints': 5000}

    white_point = w_4_ct * point[4] + w_3_ct * point[3] + w_2_ct * point[2] + white_capture_count * point[
        'capture'] + white_capture_3_count * point['3_capture'] \
                  + cap_by_white * point['capturepoints'] + w_open3 * point['3open'] + w_open4 * point['4open']
    black_point = b_4_ct * point[4] + b_3_ct * point[3] + b_2_ct * point[2] + black_capture_count * point[
        'capture'] + black_capture_3_count * point['3_capture'] \
                  + cap_by_black * point['capturepoints'] + b_open3 * point['3open'] + b_open4 * point['4open']

    cost = (white_point - black_point) if player == 'w' else (black_point - white_point)
    evalboard_dict[(player, frozenset(blackpieces), frozenset(whitepieces), cap_by_black, cap_by_white,caller)] = cost
    return cost


resultboard_dict = {}


def resultBoard(nextmove, player, blackpieces, whitepieces):
    froz_b_old = frozenset(blackpieces)
    froz_w_old = frozenset(whitepieces)

    copy_blackpieces = copy.copy(blackpieces)
    copy_whitepieces = copy.copy(whitepieces)

    if (player == 'w'):
        copy_whitepieces[(nextmove[0], nextmove[1])] = 1
    if (player == 'b'):
        copy_blackpieces[(nextmove[0], nextmove[1])] = 1

    i = nextmove[0]
    j = nextmove[1]
    white_point = 0
    black_point = 0

    if (player == 'w'):
        if ((i, j + 1) in copy_blackpieces and (i, j + 2) in copy_blackpieces and (i, j + 3) in whitepieces):
            white_point += 2
            del copy_blackpieces[(i, j + 1)]
            del copy_blackpieces[(i, j + 2)]

        if ((i, j - 1) in copy_blackpieces and (i, j - 2) in copy_blackpieces and (i, j - 3) in whitepieces):
            white_point += 2
            del copy_blackpieces[(i, j - 1)]
            del copy_blackpieces[(i, j - 2)]

        if ((i + 1, j) in copy_blackpieces and (i + 2, j) in copy_blackpieces and (i + 3, j) in whitepieces):
            white_point += 2
            del copy_blackpieces[(i + 1, j)]
            del copy_blackpieces[(i + 2, j)]

        if ((i - 1, j) in copy_blackpieces and (i - 2, j) in copy_blackpieces and (i - 3, j) in whitepieces):
            white_point += 2
            del copy_blackpieces[(i - 1, j)]
            del copy_blackpieces[(i - 2, j)]

        if ((i + 1, j + 1) in copy_blackpieces and (i + 2, j + 2) in copy_blackpieces and (
                i + 3, j + 3) in whitepieces):
            white_point += 2
            del copy_blackpieces[(i + 1, j + 1)]
            del copy_blackpieces[(i + 2, j + 2)]

        if ((i - 1, j - 1) in copy_blackpieces and (i - 2, j - 2) in copy_blackpieces and (
                i - 3, j - 3) in whitepieces):
            white_point += 2
            del copy_blackpieces[(i - 1, j - 1)]
            del copy_blackpieces[(i - 2, j - 2)]

        if ((i - 1, j + 1) in copy_blackpieces and (i - 2, j + 2) in copy_blackpieces and (
                i - 3, j + 3) in whitepieces):
            white_point += 2
            del copy_blackpieces[(i - 1, j + 1)]
            del copy_blackpieces[(i - 2, j + 2)]

        if ((i + 1, j - 1) in copy_blackpieces and (i + 2, j - 2) in copy_blackpieces and (
                i + 3, j - 3) in whitepieces):
            white_point += 2
            del copy_blackpieces[(i + 1, j - 1)]
            del copy_blackpieces[(i + 2, j - 2)]
    else:
        if ((i, j + 1) in copy_whitepieces and (i, j + 2) in copy_whitepieces and (i, j + 3) in copy_blackpieces):
            black_point += 2
            del copy_whitepieces[(i, j + 1)]
            del copy_whitepieces[(i, j + 2)]

        if ((i, j - 1) in copy_whitepieces and (i, j - 2) in copy_whitepieces and (i, j - 3) in copy_blackpieces):
            black_point += 2
            del copy_whitepieces[(i, j - 1)]
            del copy_whitepieces[(i, j - 2)]

        if ((i + 1, j) in copy_whitepieces and (i + 2, j) in copy_whitepieces and (i + 3, j) in copy_blackpieces):
            black_point += 2
            del copy_whitepieces[(i + 1, j)]
            del copy_whitepieces[(i + 2, j)]

        if ((i - 1, j) in copy_whitepieces and (i - 2, j) in copy_whitepieces and (i - 3, j) in copy_blackpieces):
            black_point += 2
            del copy_whitepieces[(i - 1, j)]
            del copy_whitepieces[(i - 2, j)]

        if ((i + 1, j + 1) in copy_whitepieces and (i + 2, j + 2) in copy_whitepieces and (
                i + 3, j + 3) in copy_blackpieces):
            black_point += 2
            del copy_whitepieces[(i + 1, j + 1)]
            del copy_whitepieces[(i + 2, j + 2)]

        if ((i - 1, j - 1) in copy_whitepieces and (i - 2, j - 2) in copy_whitepieces and (
                i - 3, j - 3) in copy_blackpieces):
            black_point += 2
            del copy_whitepieces[(i - 1, j - 1)]
            del copy_whitepieces[(i - 2, j - 2)]

        if ((i - 1, j + 1) in copy_whitepieces and (i - 2, j + 2) in copy_whitepieces and (
                i - 3, j + 3) in copy_blackpieces):
            black_point += 2
            del copy_whitepieces[(i - 1, j + 1)]
            del copy_whitepieces[(i - 2, j + 2)]

        if ((i + 1, j - 1) in copy_whitepieces and (i + 2, j - 2) in copy_whitepieces and (
                i + 3, j - 3) in copy_blackpieces):
            black_point += 2
            del copy_whitepieces[(i + 1, j - 1)]
            del copy_whitepieces[(i + 2, j - 2)]

    resultboard_dict[(nextmove, player, froz_b_old, froz_w_old)] = (
        copy_blackpieces, copy_whitepieces, black_point, white_point)
    return (copy_blackpieces, copy_whitepieces, black_point, white_point)


maximize_dict = {}


def maximize(depth, alpha, beta, current_player, blackpieces, whitepieces, cap_by_black, cap_by_white):
    froz_b = frozenset(blackpieces)
    froz_w = frozenset(whitepieces)

    if (cap_by_black == 10):
        if (player == 'b'):
            term = 100000
        else:
            term = -100000
    elif (cap_by_white == 10):
        if (player == 'w'):
            term = 100000
        else:
            term = -100000
    elif ((froz_b, froz_w) in termianl_board):
        term = termianl_board[(froz_b, froz_w)]
    else:
        term = isTerminal(blackpieces, whitepieces)
    if (term):
        return term

    if (depth > depthlimit):
        if ((player, froz_b, froz_w, cap_by_black, cap_by_white,'max') in evalboard_dict):
            return evalboard_dict[(player, froz_b, froz_w, cap_by_black, cap_by_white,'max')]
        cost = evalBoard(player, blackpieces, whitepieces, cap_by_black, cap_by_white,'max')
        return cost

    v = neg_inf

    next_player = 'w' if current_player == 'b' else 'b'

    for (i, j) in sequenceofmoves:
        if ((i, j) not in whitepieces and (i, j) not in blackpieces and i_start <= i < i_end and j_start <= j < j_end):
            nextmove = (i, j)

            if ((nextmove, current_player, froz_b, froz_w) in resultboard_dict):
                (next_blackpieces, next_whitepieces, next_cap_by_black, next_cap_by_white) = resultboard_dict[
                    (nextmove, current_player, froz_b, froz_w)]
            else:
                (next_blackpieces, next_whitepieces, next_cap_by_black, next_cap_by_white) = resultBoard(nextmove,
                                                                                                         current_player,
                                                                                                         blackpieces,
                                                                                                         whitepieces)

            val = minimize(depth + 1, alpha, beta, next_player, next_blackpieces, next_whitepieces,
                                cap_by_black + next_cap_by_black, cap_by_white + next_cap_by_white)
            v = max(v, val)

            if (v >= beta):
                return v
            alpha = max(alpha, v)
    return v


minimize_dict = {}


def minimize(depth, alpha, beta, current_player, blackpieces, whitepieces, cap_by_black, cap_by_white):
    froz_b = frozenset(blackpieces)
    froz_w = frozenset(whitepieces)

    if (cap_by_black == 10):
        if (player == 'b'):
            term = 100000
        else:
            term = -100000
    elif (cap_by_white == 10):
        if (player == 'w'):
            term = 100000
        else:
            term = -100000

    elif ((froz_b, froz_w) in termianl_board):
        term = termianl_board[(froz_b, froz_w)]
    else:
        term = isTerminal(blackpieces, whitepieces)

    if (term):
        return term

    if (depth > depthlimit):
        if ((player, froz_b, froz_w, cap_by_black, cap_by_white,'min') in evalboard_dict):
            return evalboard_dict[(player, froz_b, froz_w, cap_by_black, cap_by_white,'min')]
        cost = evalBoard(player, blackpieces, whitepieces, cap_by_black, cap_by_white,'min')
        return cost

    v = pos_inf

    next_player = 'w' if current_player == 'b' else 'b'

    for (i, j) in sequenceofmoves:
        if ((i, j) not in whitepieces and (i, j) not in blackpieces and i_start <= i < i_end and j_start <= j < j_end):
            nextmove = (i, j)
            move = nextmove

            if ((nextmove, current_player, froz_b, froz_w) in resultboard_dict):
                (next_blackpieces, next_whitepieces, next_cap_by_black, next_cap_by_white) = resultboard_dict[
                    (nextmove, current_player, froz_b, froz_w)]
            else:
                (next_blackpieces, next_whitepieces, next_cap_by_black, next_cap_by_white) = resultBoard(nextmove,
                                                                                                         current_player,
                                                                                                         blackpieces,
                                                                                                         whitepieces)

            val =maximize(depth + 1, alpha, beta, next_player, next_blackpieces, next_whitepieces,
                     cap_by_black + next_cap_by_black, cap_by_white + next_cap_by_white)

            v = min(v, val)
            if (v <= alpha):
                return v
            beta = min(beta, v)
    return v


# MAIN STARTS FROM HERE

infile = open('input.txt', 'r')
input_data = infile.read().split('\n')

color = input_data[0]
player = 'b' if color == 'BLACK' else 'w'
opponent = 'w' if color == 'BLACK' else 'b'

timeleft = float(input_data[1])

caputered = input_data[2].split(',')

cap_by_white, cap_by_black = (int(caputered[0]), int(caputered[1]))

board = []
for i in range(3, 22):
    board.append(list(input_data[i]))
board = np.array(board)

depthlimit = 3
gap = 3

depth = 1
alpha = neg_inf
beta = pos_inf
move = None
maxVal = neg_inf

(i_start, i_end, j_start, j_end) = reduceGrid(board)
current_player = player

if (timeleft < 80 and timeleft > 10):
    depthlimit = 2
    gap = 2

if (timeleft < 10):
    depthlimit = 1
    gap = 1

next_player = 'w' if current_player == 'b' else 'b'

sequenceofmoves = [(9, 9), (9, 8), (10, 8), (10, 9), (10, 10), (9, 10), (8, 10), (8, 9), (8, 8), (8, 7), (9, 7),
                   (10, 7), (11, 7), (11, 8), (11, 9), (11, 10), (11, 11), (10, 11), (9, 11), (8, 11), (7, 11), (7, 10),
                   (7, 9), (7, 8), (7, 7), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (12, 7), (12, 8), (12, 9),
                   (12, 10), (12, 11), (12, 12), (11, 12), (10, 12), (9, 12), (8, 12), (7, 12), (6, 12), (6, 11),
                   (6, 10), (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5),
                   (13, 5), (13, 6), (13, 7), (13, 8), (13, 9), (13, 10), (13, 11), (13, 12), (13, 13), (12, 13),
                   (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 12), (5, 11), (5, 10), (5, 9),
                   (5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4),
                   (13, 4), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12),
                   (14, 13), (14, 14), (13, 14), (12, 14), (11, 14), (10, 14), (9, 14), (8, 14), (7, 14), (6, 14),
                   (5, 14), (4, 14), (4, 13), (4, 12), (4, 11), (4, 10), (4, 9), (4, 8), (4, 7), (4, 6), (4, 5), (4, 4),
                   (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (15, 3),
                   (15, 4), (15, 5), (15, 6), (15, 7), (15, 8), (15, 9), (15, 10), (15, 11), (15, 12), (15, 13),
                   (15, 14), (15, 15), (14, 15), (13, 15), (12, 15), (11, 15), (10, 15), (9, 15), (8, 15), (7, 15),
                   (6, 15), (5, 15), (4, 15), (3, 15), (3, 14), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8),
                   (3, 7), (3, 6), (3, 5), (3, 4), (3, 3), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
                   (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (15, 2), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6),
                   (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15), (16, 16),
                   (15, 16), (14, 16), (13, 16), (12, 16), (11, 16), (10, 16), (9, 16), (8, 16), (7, 16), (6, 16),
                   (5, 16), (4, 16), (3, 16), (2, 16), (2, 15), (2, 14), (2, 13), (2, 12), (2, 11), (2, 10), (2, 9),
                   (2, 8), (2, 7), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
                   (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1),
                   (17, 2), (17, 3), (17, 4), (17, 5), (17, 6), (17, 7), (17, 8), (17, 9), (17, 10), (17, 11), (17, 12),
                   (17, 13), (17, 14), (17, 15), (17, 16), (17, 17), (16, 17), (15, 17), (14, 17), (13, 17), (12, 17),
                   (11, 17), (10, 17), (9, 17), (8, 17), (7, 17), (6, 17), (5, 17), (4, 17), (3, 17), (2, 17), (1, 17),
                   (1, 16), (1, 15), (1, 14), (1, 13), (1, 12), (1, 11), (1, 10), (1, 9), (1, 8), (1, 7), (1, 6),
                   (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0),
                   (18, 1), (18, 2), (18, 3), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (18, 10), (18, 11),
                   (18, 12), (18, 13), (18, 14), (18, 15), (18, 16), (18, 17), (18, 18), (17, 18), (16, 18), (15, 18),
                   (14, 18), (13, 18), (12, 18), (11, 18), (10, 18), (9, 18), (8, 18), (7, 18), (6, 18), (5, 18),
                   (4, 18), (3, 18), (2, 18), (1, 18), (0, 18), (0, 17), (0, 16), (0, 15), (0, 14), (0, 13), (0, 12),
                   (0, 11), (0, 10), (0, 9), (0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]

for (i, j) in sequenceofmoves:
    if ((i, j) not in whitepieces and (i, j) not in blackpieces and i_start <= i < i_end and j_start <= j < j_end):
        nextmove = (i, j)

        if (player == 'w' and len(whitepieces) == 1 and len(blackpieces) == 1):

            if (((9 - i) * 2 + (9 - j) * 2) < 9):
                continue

        (next_blackpieces, next_whitepieces, next_cap_by_black, next_cap_by_white) = resultBoard(nextmove,
                                                                                                 current_player,
                                                                                                 blackpieces,
                                                                                                     whitepieces)


        val = minimize(depth + 1, alpha, beta, next_player, next_blackpieces, next_whitepieces,
                       cap_by_black + next_cap_by_black, cap_by_white + next_cap_by_white)
        if (val > maxVal):
            alpha = val
            maxVal = val
            move = (i, j)

blackpieces, whitepieces, next_cap_by_black, next_cap_by_white = resultBoard(move, current_player, blackpieces,
                                                                             whitepieces)


alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
str1 = str(19 - move[0]) + alphabets[move[1]]

with open('output.txt', 'w') as f:
    f.write(str1)
