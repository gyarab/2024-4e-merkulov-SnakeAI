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
        visited = bool[self.vertices]
        start = 0
        dfs(self, start, visited)

    def dfs(self, start, visited):
        visited[start] = True

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
