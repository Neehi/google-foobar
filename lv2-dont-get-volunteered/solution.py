# 8 x8 board
GRID_SIZE = 8

# All valid moves a knight can make
KNIGHT_MOVES = [
    (2, 1), (2, -1),
    (-2, 1), (-2, -1),
    (1, 2), (1, -2),
    (-1, 2), (-1, -2),
]

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_coords(self, pos):
        """ Convert a board position to (x,y) coordinates """
        return pos % self.width, int(pos / self.height)

    def get_position(self, col, row):
        """ Convert a board position to (x,y) coordinates """
        return row * self.width + col

    def valid(self, col, row):
        """ Return true if the (x, y) coordinate is valid """
        return col >= 0 and col < self.width and row >= 0 and row < self.height

    def bfs(self, start, end, moves):
        """ Find the shortest path from A to B using a simple BFS """

        # Simple queue of possible moves
        queue = [(start, 0)]

        # List of squares already visited
        visited = []

        # Loop through the list of moves until we land on the destination
        while queue:
            # Get next move
            current_position, current_steps = queue.pop(0)
            current_col, current_row = self.get_coords(current_position)

            # Check if destination reached
            if current_position == end:
                return current_steps

            # Check if already visited
            if current_position in visited:
                continue

            # Get all valid moves and add them to the queue
            queue.extend([
                (self.get_position(current_col + x, current_row + y), current_steps + 1)
                for x, y in moves if self.valid(current_col + x, current_row + y)
            ])

        # Should never happen
        assert False

def solution(src, dest):
    # Create the 8x8 grid (0..63)
    grid = Grid(GRID_SIZE, GRID_SIZE)

    # Calculate the shortest number of steps from src to dest
    steps = grid.bfs(src, dest, KNIGHT_MOVES)

    return steps
