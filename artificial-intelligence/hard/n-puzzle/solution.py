#!/bin/python3

from collections import deque
import heapq
import sys


# Movement of the EMPTY cell (0)
DIRECTIONS = (
    (-1, 0, "UP"),
    (1, 0, "DOWN"),
    (0, -1, "LEFT"),
    (0, 1, "RIGHT"),
)


def solve_puzzle(k, board):
    n = k * k

    # pos[value] = current linear index of that tile.
    pos = [0] * n
    for i, value in enumerate(board):
        pos[value] = i

    # Cells already placed permanently.
    fixed = set()

    # Final sequence of empty-cell movements.
    answer = []

    def neighbours(index):
        r, c = divmod(index, k)

        if r > 0:
            yield index - k, "UP"
        if r + 1 < k:
            yield index + k, "DOWN"
        if c > 0:
            yield index - 1, "LEFT"
        if c + 1 < k:
            yield index + 1, "RIGHT"

    def apply_move(move):
        """Apply one movement of the empty cell to the real board."""
        zero = pos[0]

        if move == "UP":
            nxt = zero - k
        elif move == "DOWN":
            nxt = zero + k
        elif move == "LEFT":
            nxt = zero - 1
        else:
            nxt = zero + 1

        moved_tile = board[nxt]

        board[zero], board[nxt] = board[nxt], board[zero]

        pos[0] = nxt
        pos[moved_tile] = zero

        answer.append(move)

    def find_group_path(tiles, goals):
        """
        BFS only tracks:
          - requested tiles
          - empty cell

        All other unfixed tiles are treated as interchangeable.
        This keeps the search space very small even for a 5x5 board.
        """

        start = tuple(pos[tile] for tile in tiles) + (pos[0],)
        goal_positions = tuple(goals)

        if start[:-1] == goal_positions:
            return []

        queue = deque([start])

        # state -> (previous_state, move)
        parent = {start: (None, None)}

        end_state = None

        while queue:
            state = queue.popleft()

            # Requested tiles are correctly positioned.
            if state[:-1] == goal_positions:
                end_state = state
                break

            zero = state[-1]
            tile_positions = state[:-1]

            for nxt, move in neighbours(zero):

                # Never disturb already solved cells.
                if nxt in fixed:
                    continue

                new_state = list(state)

                # If zero swaps with one of the tracked tiles,
                # update that tile's position.
                tracked_index = -1

                for i, p in enumerate(tile_positions):
                    if p == nxt:
                        tracked_index = i
                        break

                if tracked_index != -1:
                    new_state[tracked_index] = zero

                new_state[-1] = nxt
                new_state = tuple(new_state)

                if new_state not in parent:
                    parent[new_state] = (state, move)
                    queue.append(new_state)

        # Reconstruct path.
        moves = []
        current = end_state

        while parent[current][0] is not None:
            previous, move = parent[current]
            moves.append(move)
            current = previous

        moves.reverse()
        return moves

    def place_group(cells):
        """
        Goal board is:

        0 1 2 ...
        k k+1 ...

        Therefore the desired tile value for linear position x
        is exactly x.
        """
        tiles = cells

        moves = find_group_path(tiles, cells)

        for move in moves:
            apply_move(move)

        # Lock these cells permanently.
        for cell in cells:
            fixed.add(cell)

    # ------------------------------------------------------------
    # STEP 1:
    # Solve rows from the BOTTOM upward.
    #
    # We leave the top-left 3x3 area unsolved because it contains
    # the final position of the empty tile (0).
    # ------------------------------------------------------------
    for row in range(k - 1, 2, -1):

        # Place all except the final two tiles individually.
        for col in range(k - 2):
            cell = row * k + col
            place_group([cell])

        # Last two cells must be positioned together.
        # Doing them independently can trap the final tile.
        last_two = [
            row * k + (k - 2),
            row * k + (k - 1),
        ]

        place_group(last_two)

    # ------------------------------------------------------------
    # STEP 2:
    # Only the top three rows remain.
    # Solve rightmost columns from RIGHT to LEFT.
    #
    # All three tiles of each column are positioned simultaneously
    # to avoid trapping a tile at the edge.
    # ------------------------------------------------------------
    for col in range(k - 1, 2, -1):

        cells = [
            col,
            k + col,
            2 * k + col,
        ]

        place_group(cells)

    # ------------------------------------------------------------
    # STEP 3:
    # Exactly the top-left 3x3 puzzle remains.
    # Solve it optimally using A* + Manhattan distance.
    # ------------------------------------------------------------

    active_cells = [
        r * k + c
        for r in range(3)
        for c in range(3)
    ]

    start = tuple(board[index] for index in active_cells)
    goal = tuple(active_cells)

    if start != goal:

        # Goal position inside the local 3x3 board.
        goal_index = {
            value: i
            for i, value in enumerate(goal)
        }

        def heuristic(state):
            """Manhattan-distance heuristic."""
            distance = 0

            for i, value in enumerate(state):
                if value == 0:
                    continue

                target = goal_index[value]

                r1, c1 = divmod(i, 3)
                r2, c2 = divmod(target, 3)

                distance += abs(r1 - r2) + abs(c1 - c2)

            return distance

        # Heap entries: (f_score, g_score, state)
        heap = [(heuristic(start), 0, start)]

        best_cost = {start: 0}
        parent = {start: (None, None)}

        final_state = None

        while heap:
            _, cost, state = heapq.heappop(heap)

            if cost != best_cost[state]:
                continue

            if state == goal:
                final_state = state
                break

            zero = state.index(0)
            zr, zc = divmod(zero, 3)

            for dr, dc, move in DIRECTIONS:
                nr = zr + dr
                nc = zc + dc

                if not (0 <= nr < 3 and 0 <= nc < 3):
                    continue

                nxt = nr * 3 + nc

                new_state = list(state)
                new_state[zero], new_state[nxt] = (
                    new_state[nxt],
                    new_state[zero],
                )
                new_state = tuple(new_state)

                new_cost = cost + 1

                if new_cost < best_cost.get(new_state, float("inf")):
                    best_cost[new_state] = new_cost
                    parent[new_state] = (state, move)

                    priority = new_cost + heuristic(new_state)

                    heapq.heappush(
                        heap,
                        (priority, new_cost, new_state)
                    )

        # Reconstruct final 3x3 solution.
        final_moves = []
        current = final_state

        while parent[current][0] is not None:
            previous, move = parent[current]
            final_moves.append(move)
            current = previous

        final_moves.reverse()

        for move in final_moves:
            apply_move(move)

    return answer


def main():
    k = int(sys.stdin.readline().strip())

    board = [
        int(sys.stdin.readline().strip())
        for _ in range(k * k)
    ]

    moves = solve_puzzle(k, board)

    print(len(moves))

    for move in moves:
        print(move)


if __name__ == "__main__":
    main()