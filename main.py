from collections import deque
import time
import random


def generate_maze():
    # Set the size of the maze
    rows = int(input("Enter the number of rows: "))  # Prompt the user to enter the number of rows for the maze
    cols = int(input("Enter the number of columns: "))  # Prompt the user to enter the number of columns for the maze

    # Initialize the maze with walls
    maze = [['#' for _ in range(cols)] for _ in range(rows)]  # Create a 2D list representing the maze, filled with walls '#'

    # Randomly select a starting cell and mark it as part of the maze
    start_row = random.randint(0, rows - 1)  # Generate a random row index for the starting cell
    start_col = random.randint(0, cols - 1)  # Generate a random column index for the starting cell
    maze[start_row][start_col] = 'S'  # Mark the starting cell as 'S' in the maze

    # Create a list of frontier cells
    frontier = [(start_row, start_col, (start_row, start_col))]  # Initialize a list with the starting cell as the frontier

    while frontier:
        # Randomly select a frontier cell
        index = random.randint(0, len(frontier) - 1)  # Generate a random index within the range of the frontier list
        current_row, current_col, previous_cell = frontier[index]  # Get the current cell and its previous cell from the frontier
        del frontier[index]  # Remove the current cell from the frontier list

        # Check the neighboring cells
        neighbors = [
            (current_row - 2, current_col, (current_row - 1, current_col)),  # Up
            (current_row + 2, current_col, (current_row + 1, current_col)),  # Down
            (current_row, current_col - 2, (current_row, current_col - 1)),  # Left
            (current_row, current_col + 2, (current_row, current_col + 1))   # Right
        ]

        for neighbor_row, neighbor_col, wall_cell in neighbors:
            # Check if the neighbor is within the maze bounds
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                # Check if the neighbor is a wall
                if maze[neighbor_row][neighbor_col] == '#':
                    # Check if the wall has exactly one passage to the maze
                    passage_row, passage_col = wall_cell
                    if maze[passage_row][passage_col] != ' ':
                        # Create a passage by removing the wall and connecting the current cell to the neighbor
                        maze[current_row][current_col] = ' '  # Mark the current cell as a passage
                        maze[passage_row][passage_col] = ' '  # Mark the passage cell in the wall as a passage
                        maze[neighbor_row][neighbor_col] = ' '  # Mark the neighbor cell as a passage
                        frontier.append((neighbor_row, neighbor_col, (current_row, current_col)))  # Add the neighbor to the frontier

    # Randomly select a goal cell and mark it as part of the maze
    goal_row = random.randint(0, rows - 1)  # Generate a random row index for the goal cell
    goal_col = random.randint(0, cols - 1)  # Generate a random column index for the goal cell
    maze[goal_row][goal_col] = 'G'  # Mark the goal cell as 'G' in the maze

    # Replace all path cells with dots '.'
    for row in range(rows):
        for col in range(cols):
            if maze[row][col] == ' ':
                maze[row][col] = '.'  # Replace the passage cells with dots

    # Replace a random dot '.' with the starting cell 'S'
    dot_cells = [(row, col) for row in range(rows) for col in range(cols) if maze[row][col] == '.']  # Find all dot cells in the maze
    random.shuffle(dot_cells)  # Shuffle the dot cells randomly
    maze[dot_cells[0][0]][dot_cells[0][1]] = 'S'  # Replace a dot cell with the starting cell

    return maze  # Return the generated maze


def create_maze_manually():
    rows = int(input("Enter the number of rows: "))  # Prompt the user to enter the number of rows for the maze
    cols = int(input("Enter the number of columns: "))  # Prompt the user to enter the number of columns for the maze

    maze = []  # Initialize an empty list to store the maze
    start_count = 0  # Initialize a counter for the number of start positions found
    goal_count = 0  # Initialize a counter for the number of goal positions found

    for i in range(rows):  # Iterate over the number of rows
        while True:
            # Prompt the user to enter the symbols for each cell in the current row
            row = list(input(f"Enter row {i + 1} of length {cols} ('#' for walls - '.' for path - 'S' for Start - 'G' for Goal): "))
            if len(row) == cols:  # Check if the length of the entered row matches the specified number of columns
                break  # Break out of the loop if the row length is correct
            else:
                print(f"Row length must be {cols}. Please try again.")  # Print an error message if the row length is incorrect

        start_count += row.count('S')  # Count the number of 'S' symbols in the current row and add it to the start count
        goal_count += row.count('G')  # Count the number of 'G' symbols in the current row and add it to the goal count

        maze.append(row)  # Add the entered row to the maze list

        # Print the current shape of the maze
        print(f"Maze shape so far:")
        for j in range(i + 1):
            print("         ".join(maze[j]))
        print()

    rows_left = rows - len(maze)  # Calculate the number of rows remaining to be entered
    print(f"Maze shape:")  # Print the final shape of the maze
    for row in maze:
        print("         ".join(row))
    print(f"\nRows left: {rows_left}")  # Print the number of rows left to be entered

    if start_count != 1:
        # Print an error message and exit if the number of start positions is not exactly one
        print(f"Invalid maze! Expected exactly one 'S' for the start position, but found {start_count}.")
        exit()

    if goal_count != 1:
        # Print an error message and exit if the number of goal positions is not exactly one
        print(f"Invalid maze! Expected exactly one 'G' for the goal position, but found {goal_count}.")
        exit()

    return maze  # Return the created maze



def find_start_and_goal(maze):
    start = None  # Initialize the start position as None
    goal = None  # Initialize the goal position as None

    for i in range(len(maze)):  # Iterate over the rows of the maze
        for j in range(len(maze[i])):  # Iterate over the columns of each row
            if maze[i][j] == 'S':  # Check if the current cell contains the start symbol 'S'
                start = (i, j)  # Set the start position to the current coordinates (i, j)
            elif maze[i][j] == 'G':  # Check if the current cell contains the goal symbol 'G'
                goal = (i, j)  # Set the goal position to the current coordinates (i, j)

    return start, goal  # Return the found start and goal positions



def validate_maze(maze, start, goal):
    visited = set()  # Initialize a set to keep track of visited positions
    queue = deque([start])  # Initialize a queue with the starting position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Define the four directions: Up, Down, Left, Right

    while queue:
        position = queue.popleft()  # Get the next position from the front of the queue

        if position == goal:  # Check if the current position is the goal
            return True  # Return True indicating that a valid path to the goal exists

        if position not in visited:  # Check if the position has not been visited before
            visited.add(position)  # Mark the current position as visited
            x, y = position  # Extract the coordinates of the current position

            for dx, dy in directions:  # Iterate over the four directions
                nx, ny = x + dx, y + dy  # Calculate the coordinates of the neighbor in the current direction

                if (
                    0 <= nx < len(maze) and  # Check if the neighbor is within the maze boundaries (row)
                    0 <= ny < len(maze[0]) and  # Check if the neighbor is within the maze boundaries (column)
                    maze[nx][ny] != '#' and  # Check if the neighbor is not a wall ('#')
                    (nx, ny) not in visited  # Check if the neighbor has not been visited before
                ):
                    queue.append((nx, ny))  # Add the neighbor to the queue for further exploration

    return False  # If the queue is empty and the goal has not been found, return False indicating that no valid path exists



def dfs(maze, start, goal, visited):
    if start == goal:  # Check if the current position is the goal
        return [start]  # Return a list containing only the current position

    visited.add(start)  # Mark the current position as visited

    x, y = start  # Extract the coordinates of the current position
    neighbors = [
        (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)  # Define the four neighbors: Up, Down, Left, Right
    ]

    for neighbor in neighbors:
        nx, ny = neighbor  # Extract the coordinates of the neighbor

        if (
            0 <= nx < len(maze) and  # Check if the neighbor is within the maze boundaries (row)
            0 <= ny < len(maze[0]) and  # Check if the neighbor is within the maze boundaries (column)
            maze[nx][ny] != '#' and  # Check if the neighbor is not a wall ('#')
            (nx, ny) not in visited  # Check if the neighbor has not been visited before
        ):
            path = dfs(maze, (nx, ny), goal, visited)  # Recursively call the DFS function with the neighbor as the new starting position

            if path:
                return [(x, y)] + path  # If a path is found, prepend the current position to the path and return it

    return None  # If no path is found, return None



def bfs(maze, start, goal):
    # Breadth-First Search (BFS) algorithm
    # Explores all neighboring nodes at the current level before moving to the next level
    
    visited = set()
    queue = deque([(start, [])])  # Initialize the queue with the starting position and an empty path
    
    while queue:
        position, path = queue.popleft()  # Retrieve the position and path from the front of the queue
        
        if position == goal:
            return path + [position]  # Return the path if the goal is reached
        
        if position not in visited:
            visited.add(position)  # Mark the position as visited
            x, y = position

            neighbors = [
                (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)  # Up, Down, Left, Right
            ]
            
            for neighbor in neighbors:
                nx, ny = neighbor
                
                if (
                    0 <= nx < len(maze) and
                    0 <= ny < len(maze[0]) and
                    maze[nx][ny] != '#' and
                    (nx, ny) not in visited
                ):
                    queue.append(((nx, ny), path + [position]))  # Add neighboring positions to the queue along with the updated path
        
    return None  # Return None if no path is found 


def ids(maze, start, goal, max_depth):
    # Iteratively increase the depth limit
    for depth in range(max_depth):
        visited = set()
        # Perform depth-limited DFS search
        path = dfs_with_limit(maze, start, goal, visited, depth)
        
        if path:
            return path
        
        visited = set()
        # Perform depth-limited BFS search
        path = bfs_with_limit(maze, start, goal, visited, depth)
        
        if path:
            return path
    
    return None


def dfs_with_limit(maze, start, goal, visited, limit):
    if start == goal:
        return [start]
    
    if limit == 0:
        return None
    
    visited.add(start)
    
    x, y = start
    neighbors = [
        (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)  # Up, Down, Left, Right
    ]
    
    for neighbor in neighbors:
        nx, ny = neighbor
        
        if (
            0 <= nx < len(maze) and
            0 <= ny < len(maze[0]) and
            maze[nx][ny] != '#' and
            (nx, ny) not in visited
        ):
            # Recursive call with reduced depth limit
            path = dfs_with_limit(maze, (nx, ny), goal, visited, limit - 1)
            
            if path:
                return [(x, y)] + path
    
    return None



def bfs_with_limit(maze, start, goal, visited, limit):
    visited.add(start)
    
    if start == goal:
        return [start]
    
    if limit == 0:
        return None
    
    queue = deque([(start, [])])
    
    while queue:
        position, path = queue.popleft()
        
        if position == goal:
            return path + [position]
        
        x, y = position
        neighbors = [
            (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)  # Up, Down, Left, Right
        ]
        
        for neighbor in neighbors:
            nx, ny = neighbor
            
            if (
                0 <= nx < len(maze) and
                0 <= ny < len(maze[0]) and
                maze[nx][ny] != '#' and
                (nx, ny) not in visited
            ):
                queue.append(((nx, ny), path + [position]))
                visited.add((nx, ny))
    
    return None




# Mode selection
mode = input("\nEnter 'a' to auto-generate the maze or 'm' for manual maze creation: ")

if mode.lower() == 'a':
    maze = generate_maze()
elif mode.lower() == 'm':
    maze = create_maze_manually()
else:
    print("Invalid mode selection. Exiting...")
    exit()

# Print the maze
print("\nMaze Final Shape:")
for row in maze:
    print("         ".join(row))
print('\n')

# Find start and goal positions
start, goal = find_start_and_goal(maze)

# Validate the maze to ensure a valid path from start to goal
if not validate_maze(maze, start, goal):
    print("Invalid maze! There is no valid path from start to goal.")
    exit()

# Test DFS
visited_dfs = set()
start_time = time.time()
path_dfs = dfs(maze, start, goal, visited_dfs)
end_time = time.time()

if path_dfs:
    print('\n')
    print("DFS Path:", path_dfs)
    print("DFS Time:", "{:.6f}".format(end_time - start_time), "seconds")
else:
    print("DFS: No path found")

# Test BFS
start_time = time.time()
path_bfs = bfs(maze, start, goal)
end_time = time.time()

if path_bfs:
    print('\n')
    print("BFS Path:", path_bfs)
    print("BFS Time:", "{:.6f}".format(end_time - start_time), "seconds")
else:
    print("BFS: No path found")

# Test IDS
start_time = time.time()
max_depth = len(maze) * len(maze[0])  # Set max depth as the number of cells in the maze
path_ids = ids(maze, start, goal, max_depth)
end_time = time.time()

if path_ids:
    print('\n')
    print("IDS Path:", path_ids)
    print("IDS Time:", "{:.6f}".format(end_time - start_time), "seconds")
else:
    print("IDS: No path found")

# Compare the paths
if path_dfs and path_bfs and path_ids:
    print("\nComparison:")

    dfs_length = len(path_dfs)
    bfs_length = len(path_bfs)
    ids_length = len(path_ids)

    print(f"DFS Path Length: {dfs_length}")
    print(f"BFS Path Length: {bfs_length}")
    print(f"IDS Path Length: {ids_length}")

    if dfs_length == bfs_length == ids_length:
        print("All three algorithms have the same path length.")
    else:
        shortest_length = min(dfs_length, bfs_length, ids_length)

        if shortest_length == dfs_length == bfs_length == ids_length:
            print("All three algorithms have the same shortest path length.")
        elif shortest_length == dfs_length == bfs_length:
            print("DFS and BFS have the same shortest path length.")
        elif shortest_length == bfs_length == ids_length:
            print("BFS and IDS have the same shortest path length.")
        elif shortest_length == dfs_length == ids_length:
            print("DFS and IDS have the same shortest path length.")
        elif shortest_length == dfs_length:
            print("DFS has the shortest path.")
        elif shortest_length == bfs_length:
            print("BFS has the shortest path.")
        elif shortest_length == ids_length:
            print("IDS has the shortest path.")
else:
    print("Comparison: Not enough data to compare.")
