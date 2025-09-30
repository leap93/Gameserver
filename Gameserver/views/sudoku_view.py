from datetime import date
from django.shortcuts import render
from app.models import DailyPuzzle
from app.utils import get_translations
import random, json
from datetime import datetime
import time


def sudoku_view(request):
    language = request.user.userinfo.language
    now = datetime.now()
    daily = DailyPuzzle.objects.filter(type="sudoku", created_at__date=date(now.year, now.month, now.day))

    context = {'translations': get_translations(language), "language": language}
    if len(daily) == 0:
        sudoku = empty_sudoku()
        message = context["translations"]["no_daily_sudoku"]
        context["message"] = message
    else:
        daily = daily[0]
        sudoku = json.loads(daily.puzzle_text)
    context["sudoku"] = sudoku
    return render(request, 'sudoku.html', context)

def random_sudoku():
    sudoku = empty_sudoku()

    solved_up = solve_recursive_up(sudoku, copy_sudoku(sudoku), -1, 0, time.time() + 10)
    solved_down = solve_recursive_down(sudoku, copy_sudoku(sudoku), -1, 0, time.time() + 10)
    counter = 0
    while solved_up != solved_down:
        while True:
            x = random.randrange(0,9)
            y = random.randrange(0,9)

            if sudoku[x][y] == 0:
                break
        if random.randint(0, 1) == 1:
            sudoku[x][y] = solved_up[x][y]
        else:
            sudoku[x][y] = solved_down[x][y]

        solved_down = solve_recursive_down(sudoku, copy_sudoku(sudoku), -1, 0, time.time() + 30)
        counter = counter + 1
        print(counter)
        if counter > 35 or solved_up == -1 or solved_down == -1:
            print("Starting over")
            sudoku = empty_sudoku()
            counter = 0
            solved_up = solve_recursive_up(sudoku, copy_sudoku(sudoku), -1, 0, time.time() + 10)
            solved_down = solve_recursive_down(sudoku, copy_sudoku(sudoku), -1, 0, time.time() + 10)
    return sudoku

def print_sudoku(sudoku):
    for y in range(0, 9):
        for x in range(0, 9):
            print(sudoku[x][y], end=" ")
        print()

def solve_recursive_up(sudoku, solved, x, y, timeout):
    if time.time() > timeout:
        print("STOP")
        return -1
    for p in range(1, 10):
        next_coords = next_location(sudoku, x, y)
        x_next = next_coords[0]
        y_next = next_coords[1]
        solved[x_next][y_next] = p
        if check_entry(solved, x_next, y_next, p):
            if x_next == 8 and y_next == 8:
                return solved
            result = solve_recursive_up(sudoku, solved, x_next, y_next, timeout)
            if result != 0:
                return result
        solved[x_next][y_next] = 0
    return 0

def solve_recursive_down(sudoku, solved, x, y, timeout):
    if time.time() > timeout:
        print("STOP")
        return -1
    for p in range(9, 0, -1):
        next_coords = next_location(sudoku, x, y)
        x_next = next_coords[0]
        y_next = next_coords[1]
        solved[x_next][y_next] = p
        if check_entry(solved, x_next, y_next, p):
            if x_next == 8 and y_next == 8:
                return solved
            result = solve_recursive_down(sudoku, solved, x_next, y_next, timeout)
            if result != 0:
                return result
        solved[x_next][y_next] = 0
    return 0

def next_location(sudoku, x, y):
    while True:
        x = x + 1
        if x == 9:
            x = 0
            y = y + 1
        if y == 9:
            return [8, 8]
        if sudoku[x][y] == 0:
            return [x, y]

def check_rows(sudoku):
    for y in range(9):
        found = []
        for x in range(9):
            cell = sudoku[x][y]
            if cell == 0:
                continue
            if cell in found:
                return False
            found.append(cell)
    return True

def check_row_entry(sudoku, x, y, h):
    for n in range(9):
        if n == x:
            continue
        cell = sudoku[n][y]
        if cell == h:
            return False
    return True

def check_column_entry(sudoku, x, y, h):
    for n in range(9):
        if n == y:
            continue
        cell = sudoku[x][n]
        if cell == h:
            return False
    return True

def check_box_entry(sudoku, x, y, h):
    x_corner = x
    y_corner = y
    while x_corner % 3 != 0:
        x_corner -= 1
    while y_corner % 3 != 0:
        y_corner -= 1
    for a in range(x_corner, x_corner + 3):
        for b in range(y_corner, y_corner + 3):
            if a == x and b == y:
                continue
            if sudoku[a][b] == h:
                return False
    return True

def check_entry(sudoku, x, y, h):
    return check_row_entry(sudoku, x, y, h) and check_column_entry(sudoku, x, y, h) and check_box_entry(sudoku, x, y, h)

def check_columns(sudoku):
    for x in range(9):
        found = []
        for y in range(9):
            cell = sudoku[x][y]
            if cell == 0:
                continue
            if cell in found:
                return False
            found.append(cell)
    return True

def check_box(sudoku, start_x, start_y):
    found = []
    for x in range(start_x, start_x + 3):
        for y in range(start_y, start_y + 3):
            cell = sudoku[x][y]
            if cell == 0:
                continue
            if cell in found:
                return False
            found.append(cell)
    return True

def check_boxes(sudoku):
    for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            if not check_box(sudoku, x, y):
                return False
    return True

def check_sudoku(sudoku):
    return check_boxes(sudoku) and check_columns(sudoku) and check_rows(sudoku)


def empty_sudoku():
    sudoku = []
    for x in range(0, 9):
        row = []
        for y in range(0, 9):
            row.append(0)
        sudoku.append(row)
    return sudoku

def copy_sudoku(sudoku):
    solved = empty_sudoku()
    for x in range(0, 9):
        for y in range(0, 9):
            solved[x][y] = sudoku[x][y]
    return solved