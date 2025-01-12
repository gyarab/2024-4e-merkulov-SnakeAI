class Graph:
    def __init__(self, vertices, cell_size, number_of_nodes_on_side):
        # Inicializace seznamu sousedů
        self.vertices = vertices
        self.adjacency_list = [[] for _ in range(vertices)]
        self.cell_size = cell_size
        self.number_of_nodes_on_side = number_of_nodes_on_side

    def is_valid(self, x, y):
        # Kontrola, zda je vrchol uvnitř mřížky
        return 0 <= x < self.vertices and 0 <= y < self.vertices

    def add_edge(self, x, y):
        # Přidání hrany mezi vrcholy x a y (orientovaný graf)
        self.adjacency_list[x].append(y)

    def display_list(self):
        # Zobrazení seznamu sousedů
        for index, neighbors in enumerate(self.adjacency_list):
            print(f"{index}: {' '.join(map(str, neighbors))}")

    def initialize_graph(self, snake_body):
        # Inicializace grafu s pravidly
        for x in range(self.vertices):
            for y in range(self.vertices):
                # Preskoci vrcholy v tele hada
                if x != y and x not in snake_body[1:-1] and y not in snake_body[1:-1]:
                    if (x == (
                            y + 1) and x % self.number_of_nodes_on_side != 0) or y == x + self.number_of_nodes_on_side or (
                            x == (
                            y - 1) and x % self.number_of_nodes_on_side != self.number_of_nodes_on_side - 1) or y == x - self.number_of_nodes_on_side:
                        self.add_edge(x, y)
                    elif x % self.number_of_nodes_on_side == 0 and (y == x + self.number_of_nodes_on_side or x == (
                            y - 1) or y == x - self.number_of_nodes_on_side):
                        self.add_edge(x, y)
                    elif x % self.number_of_nodes_on_side == self.number_of_nodes_on_side - 1 and (
                            y == x + self.number_of_nodes_on_side or x == (
                            y + 1) or y == x - self.number_of_nodes_on_side):
                        self.add_edge(x, y)
        for telo in range(len(snake_body) - 2, -1, -1):
            self.add_edge(snake_body[telo + 1], snake_body[telo])  # Orientovaná hrana

    def initialize_smaller_graph(self):
        # Inicializace grafu s pravidly
        for x in range(self.vertices):
            for y in range(self.vertices):
                # Preskoci vrcholy v tele hada
                if (x == (
                        y + 1) and x % self.number_of_nodes_on_side != 0) or y == x + self.number_of_nodes_on_side or (
                        x == (
                        y - 1) and x % self.number_of_nodes_on_side != self.number_of_nodes_on_side - 1) or y == x - self.number_of_nodes_on_side:
                    self.add_edge(x, y)
                elif x % self.number_of_nodes_on_side == 0 and (
                        y == x + self.number_of_nodes_on_side or x == (y - 1) or y == x - self.number_of_nodes_on_side):
                    self.add_edge(x, y)
                elif x % self.number_of_nodes_on_side == self.number_of_nodes_on_side - 1 and (
                        y == x + self.number_of_nodes_on_side or x == (y + 1) or y == x - self.number_of_nodes_on_side):
                    self.add_edge(x, y)

    def spanning_tree(self):
        visited = [False] * self.vertices  # Track visited vertices
        spanning_tree_edges = []  # Store the edges of the spanning tree

        # Perform DFS starting from vertex 0
        def dfs(v):
            visited[v] = True
            for neighbor in self.adjacency_list[v]:
                if not visited[neighbor]:
                    # Add the edge to the spanning tree
                    spanning_tree_edges.append((v, neighbor))
                    dfs(neighbor)

        dfs(0)  # Start DFS from vertex 0

        # Clear the adjacency list and add only spanning tree edges
        self.adjacency_list = [[] for _ in range(self.vertices)]
        for u, v in spanning_tree_edges:
            self.add_edge(u, v)
            self.add_edge(v, u)  # Add edge to adjacency list
        return self.adjacency_list

    # Writes 4 nodes that are neighbors for 1 node in smaller graph to dictionary
    def neighbor_nodes(self):
        nodes_for_smaller_nodes = {}
        for x in range(self.vertices):
            left_up = ((x // self.number_of_nodes_on_side) * 4 * self.number_of_nodes_on_side) + (
                    (x % self.number_of_nodes_on_side) * 2)
            right_up = left_up + 1
            left_down = left_up + (self.number_of_nodes_on_side * 2)
            right_down = left_down + 1
            # Uložení do slovníku s klíčem x
            nodes_for_smaller_nodes[x] = {
                "left_up": left_up,
                "right_up": right_up,
                "left_down": left_down,
                "right_down": right_down
            }
        return nodes_for_smaller_nodes

    def dfs_hamilton(self, vertex, hamiltonian_cycle, visited):
        # Base case: if the Hamiltonian cycle includes all vertices, return the cycle
        if len(hamiltonian_cycle) == self.vertices:
            return hamiltonian_cycle

        # Mark the current vertex as visited
        visited[vertex] = True

        # Explore neighbors
        for neighbor in self.adjacency_list[vertex]:
            if not visited[neighbor]:
                hamiltonian_cycle.append(neighbor)
                result = self.dfs_hamilton(neighbor, hamiltonian_cycle, visited)
                if result:  # If a valid cycle is found, return it
                    return result
                hamiltonian_cycle.pop()  # Backtrack

        # Backtrack: unmark the current vertex
        visited[vertex] = False
        return None  # Return None if no cycle is found

    def hamiltonian_cycle(self, spanning_tree, nodes, nodes_on_side, nodes_for_smaller_nodes, small_adjacency_list):
        visited = [False] * nodes
        visited_big_graph = [False] * self.vertices
        hamiltonian_cycle = [0]  # Start the cycle from vertex 0

        # Build the graph based on the grid structure
        for node in range(nodes):
            left_up = nodes_for_smaller_nodes[node]["left_up"]
            right_up = nodes_for_smaller_nodes[node]["right_up"]
            left_down = nodes_for_smaller_nodes[node]["left_down"]
            right_down = nodes_for_smaller_nodes[node]["right_down"]

            # Add edges based on position in the grid
            if node // nodes_on_side == 0:  # Top row
                self.add_edge(left_up, right_up)
                self.add_edge(right_up, left_up)
            if node // nodes_on_side == nodes_on_side - 1:  # Bottom row
                self.add_edge(left_down, right_down)
                self.add_edge(right_down, left_down)
            if node % nodes_on_side == 0:  # Leftmost column
                self.add_edge(left_down, left_up)
                self.add_edge(left_up, left_down)
            if node % nodes_on_side == nodes_on_side - 1:  # Rightmost column
                self.add_edge(right_down, right_up)
                self.add_edge(right_up, right_down)

        # Connect nodes based on the spanning tree and adjacency list
        for node in range(nodes):
            visited[node] = True
            for neighbor in small_adjacency_list[node]:
                if not visited[neighbor]:
                    if neighbor in spanning_tree[node]:  # If the neighbor is part of the spanning tree
                        # Connect edges within the spanning tree
                        if neighbor - node == 1:  # Right neighbor
                            self.connect_horizontal_edges(node, neighbor, nodes_for_smaller_nodes)
                        else:  # Bottom neighbor
                            self.connect_vertical_edges(node, neighbor, nodes_for_smaller_nodes)
                    else:  # If the neighbor is not part of the spanning tree
                        if neighbor - node == 1:  # Right neighbor
                            self.connect_horizontal_edges_not_tree(node, neighbor, nodes_for_smaller_nodes)
                        else:  # Bottom neighbor
                            self.connect_vertical_edges_not_tree(node, neighbor, nodes_for_smaller_nodes)

        # Find the Hamiltonian cycle using DFS
        result = self.dfs_hamilton(0, hamiltonian_cycle, visited_big_graph)
        return result if result else []

    def connect_horizontal_edges(self, node, neighbor, nodes_for_smaller_nodes):
        """Helper function to connect horizontal edges."""
        right_up = nodes_for_smaller_nodes[node]["right_up"]
        right_down = nodes_for_smaller_nodes[node]["right_down"]
        left_up = nodes_for_smaller_nodes[neighbor]["left_up"]
        left_down = nodes_for_smaller_nodes[neighbor]["left_down"]
        self.add_edge(right_up, left_up)
        self.add_edge(left_up, right_up)
        self.add_edge(right_down, left_down)
        self.add_edge(left_down, right_down)

    def connect_vertical_edges(self, node, neighbor, nodes_for_smaller_nodes):
        """Helper function to connect vertical edges."""
        left_down = nodes_for_smaller_nodes[node]["left_down"]
        right_down = nodes_for_smaller_nodes[node]["right_down"]
        left_up = nodes_for_smaller_nodes[neighbor]["left_up"]
        right_up = nodes_for_smaller_nodes[neighbor]["right_up"]
        self.add_edge(left_up, left_down)
        self.add_edge(left_down, left_up)
        self.add_edge(right_up, right_down)
        self.add_edge(right_down, right_up)

    def connect_horizontal_edges_not_tree(self, node, neighbor, nodes_for_smaller_nodes):
        left_up = nodes_for_smaller_nodes[node]["left_up"]
        left_down = nodes_for_smaller_nodes[node]["left_down"]
        right_up = nodes_for_smaller_nodes[neighbor]["right_up"]
        right_down = nodes_for_smaller_nodes[neighbor]["right_down"]
        self.add_edge(left_up, left_down)
        self.add_edge(left_down, left_up)
        self.add_edge(right_up, right_down)
        self.add_edge(right_down, right_up)

    def connect_vertical_edges_not_tree(self, node, neighbor, nodes_for_smaller_nodes):
        left_down = nodes_for_smaller_nodes[node]["left_down"]
        right_down = nodes_for_smaller_nodes[node]["right_down"]
        left_up = nodes_for_smaller_nodes[neighbor]["left_up"]
        right_up = nodes_for_smaller_nodes[neighbor]["right_up"]
        self.add_edge(left_up, right_up)
        self.add_edge(right_up, left_up)
        self.add_edge(left_down, right_down)
        self.add_edge(right_down, left_down)

    def game_to_graph(self, snake_game_body):
        snake_graph_body = []
        if isinstance(snake_game_body, list):
            snake_body_for_graph = [(x // self.cell_size, y // self.cell_size) for x, y in snake_game_body]
            for i, j in snake_body_for_graph:
                snake_graph_body.append(j * self.number_of_nodes_on_side + i)
            return snake_graph_body
        else:
            x, y = snake_game_body
            i = x // self.cell_size
            j = y // self.cell_size
            snake_graph_body.append(j * self.number_of_nodes_on_side + i)
            return snake_graph_body

    def graph_to_game(self, snake_graph_body):
        snake_game_body = []
        for telo in snake_graph_body:
            x = (telo % self.number_of_nodes_on_side) * self.cell_size
            y = (telo // self.number_of_nodes_on_side) * self.cell_size
            snake_game_body.append((x, y))
        return snake_game_body

    '''
    def is_safe_to_add(self, v, pos, path):
        if self.graph[path[pos-1]][v] == 0:
            return False

        for vertex in path:
            if vertex == v:
                return False

        return True

    def hamiltonian_cycle_util(self, path, pos):
        if pos == self.vertices:
            if self.graph[path[pos-1]][path[0]] == 1:
                return True
            else:
                return False

        for v in range(1, self.vertices):
            if self.is_safe_to_add(v, pos, path):
                path[pos] = v

                if self.hamiltonian_cycle_util(path, pos+1):
                    return True

                path[pos] = -1

        return False

    def find_hamiltonian_cycle(self):
        path = [-1] * self.vertices

        path[0] = 0

        if not self.hamiltonian_cycle_util(path, 1):
            print ("No\n")
            return False

        path = self.graph_to_game(path)
        return path

    def print_solution(self, path):
        print ("Yes\n")
        for vertex in path:
            print (vertex )


'''
