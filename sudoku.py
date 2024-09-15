import pygame
import random

pygame.init()

width, height = 540, 600 
diff = width // 9  
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku Solver")

white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

font = pygame.font.SysFont("Times New Roman", 40)
small_font = pygame.font.SysFont("Times New Roman", 20)

def generate_sudoku():
    base  = 3
    side  = base * base

    def pattern(r,c): 
        return (base*(r%base)+r//base+c)%side

    def shuffle(s): 
        return random.sample(s, len(s))
    
    rBase = range(base)
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ]
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1, base*base + 1))

    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

    squares = side * side
    empties = squares - random.randint(35, 40)
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board

def possible(row, column, number, grid):
    for i in range(9):
        if grid[row][i] == number and i != column:
            return False 
        
    for i in range(9):
        if grid[i][column] == number and i != row:
            return False
        
    x0 = (column // 3) * 3
    y0 = (row // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[y0 + i][x0 + j] == number and (y0 + i != row or x0 + j != column):
                return False 
    return True

def solve_sudoku(grid):
    for row in range(9):
        for column in range(9):
            if grid[row][column] == 0:
                for number in range(1, 10):
                    if possible(row, column, number, grid):
                        grid[row][column] = number
                        if solve_sudoku(grid):
                            return True
                        grid[row][column] = 0
                return False
    return True

def is_solvable(board):
    test_board = [row[:] for row in board]
    return solve_sudoku(test_board)

def draw_grid(selected, original_grid, correct_guesses):
    window.fill(white)
    
    for i in range(10):
        if i % 3 != 0:  
            pygame.draw.line(window, gray, (i * diff, 0), (i * diff, 540), 2)
            pygame.draw.line(window, gray, (0, i * diff), (540, i * diff), 2)

    for i in range(10):
        if i % 3 == 0: 
            pygame.draw.line(window, black, (i * diff, 0), (i * diff, 540), 7)
            pygame.draw.line(window, black, (0, i * diff), (540, i * diff), 7)

    if selected:
        row, col = selected
        pygame.draw.rect(window, blue, (col * diff, row * diff, diff, diff), 3)

    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                if original_grid[row][col] != 0:
                    color = black
                elif correct_guesses[row][col]:
                    color = green
                else:
                    color = red
                value = font.render(str(grid[row][col]), True, color)
                text_rect = value.get_rect(center=(col * diff + diff // 2, row * diff + diff // 2))
                window.blit(value, text_rect)

    pygame.display.update()

def solve():
    global grid
    solve_sudoku(grid)
    for row in range(9):
        for col in range(9):
            correct_guesses[row][col] = True
    draw_grid(None, original_grid, correct_guesses)

def display_message(message):
    text = small_font.render(message, True, black)
    window.blit(text, (20, 550))
    pygame.display.update()

def main():
    global grid, original_grid, correct_guesses
    solvable = False
    selected = None
    while not solvable:
        grid = generate_sudoku()
        if is_solvable(grid):
            solvable = True
            original_grid = [row[:] for row in grid]  
            correct_guesses = [[False] * 9 for _ in range(9)] 
        else:
            print("Generated Sudoku board was not solvable. Generating a new board.")
    
    running = True
    while running:
        draw_grid(selected, original_grid, correct_guesses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected = (pos[1] // diff, pos[0] // diff)
            if event.type == pygame.KEYDOWN:
                if selected:
                    row, col = selected
                    if original_grid[row][col] == 0: 
                        if event.key == pygame.K_1:
                            grid[row][col] = 1
                        elif event.key == pygame.K_2:
                            grid[row][col] = 2
                        elif event.key == pygame.K_3:
                            grid[row][col] = 3
                        elif event.key == pygame.K_4:
                            grid[row][col] = 4
                        elif event.key == pygame.K_5:
                            grid[row][col] = 5
                        elif event.key == pygame.K_6:
                            grid[row][col] = 6
                        elif event.key == pygame.K_7:
                            grid[row][col] = 7
                        elif event.key == pygame.K_8:
                            grid[row][col] = 8
                        elif event.key == pygame.K_9:
                            grid[row][col] = 9
                        elif event.key == pygame.K_BACKSPACE:
                            grid[row][col] = 0
                            correct_guesses[row][col] = False 
                if event.key == pygame.K_SPACE:
                    solve()
                if event.key == pygame.K_RETURN:
                    if selected:
                        row, col = selected
                        if grid[row][col] != 0: 
                            if possible(row, col, grid[row][col], grid):
                                correct_guesses[row][col] = True 
                                display_message(f"Value {grid[row][col]} is correct for cell ({row + 1}, {col + 1})")
                            else:
                                correct_guesses[row][col] = False  
                                display_message(f"Value {grid[row][col]} is incorrect for cell ({row + 1}, {col + 1})")

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
