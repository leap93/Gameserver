from datetime import date

from django.shortcuts import render

from app.models import DailyPuzzle
from app.utils import get_translations
import random, json
from datetime import datetime

def sudoku_view(request):
    language = request.user.userinfo.language
    now = datetime.now()
    daily = DailyPuzzle.objects.filter(type="sudoku", created_at__date=date(now.year, now.month, now.day))
    if len(daily) == 0:
        sudoku = random_sudoku()
        daily = DailyPuzzle.objects.create(type="sudoku", puzzle_text=json.dumps(sudoku))
    else:
        daily = daily[0]
        sudoku = json.loads(daily.puzzle_text)
    sudoku = solve_recursive_up(empty_sudoku(), empty_sudoku(), -1, 0)
    context = {'translations': get_translations(language), "language": language, "sudoku": sudoku}
    print_sudoku(context["sudoku"])


    return render(request, 'sudoku.html', context)

def random_sudoku():
    sudoku = empty_sudoku()

    solved_up = solve_recursive_up(sudoku, copy_sudoku(sudoku), -1, 0)
    solved_down = solve_recursive_down(sudoku, copy_sudoku(sudoku), -1, 0)
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

        if counter >= 20:
            print("Up")
            solved_up = solve_recursive_up(sudoku, copy_sudoku(sudoku), -1, 0)
            print("Down")
            solved_down = solve_recursive_down(sudoku, copy_sudoku(sudoku), -1, 0)
        counter = counter + 1
        print(counter)
    return sudoku

def print_sudoku(sudoku):
    for y in range(0, 9):
        for x in range(0, 9):
            print(sudoku[x][y], end=" ")
        print()

def solve_recursive_up(sudoku, solved, x, y):
    for p in range(1, 10):
        next_coords = next_location(sudoku, x, y)
        x_next = next_coords[0]
        y_next = next_coords[1]
        solved[x_next][y_next] = p
        if check_sudoku(solved):
            if x_next == 8 and y_next == 8:
                return solved
            result = solve_recursive_up(sudoku, solved, x_next, y_next)
            if result != 0:
                return result
        solved[x_next][y_next] = 0
    return 0

def solve_recursive_down(sudoku, solved, x, y):
    for p in range(9, 0, -1):
        next_coords = next_location(sudoku, x, y)
        x_next = next_coords[0]
        y_next = next_coords[1]
        solved[x_next][y_next] = p
        if check_sudoku(solved):
            if x_next == 8 and y_next == 8:
                return solved
            result = solve_recursive_down(sudoku, solved, x_next, y_next)
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