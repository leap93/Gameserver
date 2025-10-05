from datetime import date
from django.shortcuts import render
from app.models import DailyPuzzle, Play
from app.utils import get_translations
import random, json
from datetime import datetime
import time


def sudoku_view(request):
    language = request.user.userinfo.language
    now = datetime.now()
    daily = DailyPuzzle.objects.filter(type="sudoku", created_at__date=date(now.year, now.month, now.day))
    context = {'translations': get_translations(language), "language": language, "solved": 0}

    #Create Play obejct if player has completed the sudoku
    if request.method == "POST":
        dailies = Play.objects.filter(puzzle=daily, created_at__date=date(now.year, now.month, now.day), player=request.user)
        if len(dailies) == 0:
            Play.objects.create(puzzle=daily, player=request.user, attempts=1, time=request.POST['time'])

    #Error message if daily sudoku is not created
    if len(daily) == 0:
        sudoku = empty_sudoku()
        message = context["translations"]["no_daily_sudoku"]
        context["message"] = message
        context["sudoku"] = sudoku
        return render(request, 'sudoku.html', context)

    #Load daily sudoku from database
    daily = daily[0]
    sudoku = json.loads(daily.puzzle_text)

    plays = Play.objects.filter(puzzle=daily, player=request.user)
    #Show unfilled sudoku if player has not completed it
    if len(plays) == 0:
        context["sudoku"] = sudoku
    else:
        #Show completed sudoku
        context["sudoku"] = solve_recursive_up(sudoku, copy_sudoku(sudoku), -1, 0, time.time() + 10)
        context["message"] = context["translations"]["solved_sudoku"]
        context["solved"] = 1

    return render(request, 'sudoku.html', context)

def random_sudoku():
    sudoku = initial_sudoku(15)

    solved_up = -1
    solved_down = -1
    counter = 15
    while solved_up != solved_down and counter <= 20 and solved_down != -1 and solved_up != 0:
        print(counter)
        if solved_up != -1 and solved_down != -1:
            while True:
                x = random.randrange(0,9)
                y = random.randrange(0,9)

                if sudoku[x][y] == 0:
                    break
            if random.randint(0, 1) == 1:
                sudoku[x][y] = solved_up[x][y]
            else:
                sudoku[x][y] = solved_down[x][y]
        else:
            move = smart_insert(sudoku)
            sudoku[move[0]][move[1]] = move[2]

        solved_down = solve_recursive_down(sudoku, copy_sudoku(sudoku), -1, 0, time.time() + 10)
        if solved_down != 0 and solved_down != -1:
            solved_up = solve_recursive_up(sudoku, copy_sudoku(sudoku), -1, 0, time.time() + 10)
        counter += 1
        if counter > 35 or solved_up == -1 or solved_down == -1 or solved_up == 0 or solved_down == 0:
            if counter > 35:
                print("Too easy sudoku")
            if solved_up == -1 or solved_down == -1:
                print("Timeout")
                continue
            if solved_up == 0 or solved_down == 0:
                print("No solution")
            sudoku = initial_sudoku(10)
            counter = 10
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

def possibilities(sudoku):
    possibles = []
    for x in range(0, 9):
        row = []
        for y in range(0, 9):
            if sudoku[x][y] != 0:
                row.append([])
                continue
            cell = []
            for h in range(1, 10):
                if check_entry(sudoku, x, y, h):
                    cell.append(h)
            row.append(cell)
        possibles.append(row)
    return possibles

def smart_insert(sudoku):
    possibles = possibilities(sudoku)
    counts = []
    biggest = 0
    biggest_count = 0
    for x in range(0, 9):
        row = []
        for y in range(0, 9):
            amount = len(possibles[x][y])

            if amount > biggest:
                biggest_count = 0
                biggest = amount
            if amount == biggest:
                biggest_count += 1
            row.append(amount)
        counts.append(row)

    where_to_pick = random.randint(1, biggest_count)
    for x in range(0, 9):
        for y in range(0, 9):
            if counts[x][y] == biggest:
                where_to_pick -= 1
                if where_to_pick == 0:
                    return [x, y, random.choice(possibles[x][y])]

def initial_sudoku(n):
    sudoku = empty_sudoku()
    for x in range(0, n):
        next_insert = smart_insert(sudoku)
        sudoku[next_insert[0]][next_insert[1]] = next_insert[2]
    return sudoku