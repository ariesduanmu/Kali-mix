def get_neighbours(board, position):
    directions = ((0, -1), (0, 1), (-1, 0), (1, 0))
    for direction in directions:
        new_x, new_y = (p+d for d, p in zip(direction, position))
        print(new_x, new_y)
        if new_x in range(1, len(board[0]) - 1) and new_y in range(1, len(board) - 1):
            yield new_x, new_y

def dfs(board, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            for x, y in get_neighbours(board, vertex):
                if (x, y) not in visited  and board[x][y] == "O":
                    stack.append((x, y))
    return visited

def solve(board):
    all_o = [(x, y) for x, row in enumerate(board) for y, col in enumerate(row) if col == 'O']
    grouped_o = []
    done = set()

    # Group the O's
    for current_o in all_o:
        if current_o not in done:
            group = dfs(board, current_o)
            done |= group
            if not any(x in (0, len(board) - 1) or y in (0, len(board[0]) - 1) for x, y in group):
                grouped_o.append(list(group))

    # Change the O's
    for group in grouped_o:
        for pos in group:
            board[pos[0]][pos[1]] = "X"

    return board

if __name__ == '__main__':
    board = [["X", "X", "X", "X"],
             ["X", "O", "O", "X"],
             ["X", "X", "O", "X"],
             ["X", "O", "X", "X"]]
    print(solve(board))
