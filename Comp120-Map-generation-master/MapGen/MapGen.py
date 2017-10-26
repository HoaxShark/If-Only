import pygame
import random


class MAP:
    SEA_CHANCE = 20  # Larger number, lower sea chance
    BLOCK_SIZE = 80
    SIZE_Y = 60
    SIZE_X = 60
    TILE_INFO = [  # INFORMATION ON TILES (SPAWN WEIGHT, FILE NAME)
        [20, "Images/Ground/temp_grass.jpg"],
        [3, "Images/Ground/temp_mountain.jpg"],
        [5, "Images/Ground/temp_grass2.jpg"],
        [2, "Images/Ground/temp_rock.jpg"],
        [1, "Images/Ground/temp_spooky.jpg"]
    ]
    SEA_TILE = [  # Information on sea tiles (filename)
        ["Images/Sea/Sand.jpg"],
        ["Images/Sea/Sea.jpg"],
    ]


class MapClass:
    """Fully extendible mapclass, image size and spawn weights can be edited"""
    map = [[0 for x in range(0, MAP.SIZE_X)] for y in range(0, MAP.SIZE_Y)]  # Generates a 2d array for Map size
    sea = [[False for x in range(0, MAP.SIZE_X)] for y in range(0, MAP.SIZE_Y)]
    img = pygame.Surface((MAP.SIZE_X, MAP.SIZE_Y))

    def __init__(self, seed=0):
        """Initilizes Map class with a seed"""
        if not (seed == 0):
            random.seed(seed)
        total_weight = 0
        for i in MAP.TILE_INFO:
            total_weight += i[0]  # Gets the total weight if everything in MAP.TILE_INFO
        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                rand = random.randint(0, total_weight)
                ndone = True
                for i in range(0, len(MAP.TILE_INFO)):  # Turns random number into Map tile
                    rand -= MAP.TILE_INFO[i][0]
                    if rand <= 0 and ndone:
                        ndone = False
                        self.map[x][y] = i
        self.map_render()
        self.create_sea()
        self.img = self.sea_render()

    def map_render(self):
        """Renders map array into img surface"""
        ret = pygame.Surface((MAP.SIZE_X * MAP.BLOCK_SIZE, MAP.SIZE_Y * MAP.BLOCK_SIZE))
        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                temp_img = pygame.image.load(MAP.TILE_INFO[self.map[x][y]][1]).convert()
                ret.blit(temp_img, (x * MAP.BLOCK_SIZE, y * MAP.BLOCK_SIZE))
        self.img = ret

    def create_sea(self):
        """Checks each on x,1 and 1,y to see if a sea starts, 1 is used as the array has a boarder"""
        for y in range(0, MAP.SIZE_Y):  # Spawns sea starts on the y axis
            number = random.randint(0, MAP.SEA_CHANCE)  # Generate random number to see if sea spawns
            if number == 0:  # If number is 0 change array position to True and run sea_flow_y
                self.sea[0][y] = True
                MapClass.sea_flow_y(self, y)
        for x in range(0, MAP.SIZE_X):  # Spawns sea starts on the x axis
            number = random.randint(0, MAP.SEA_CHANCE)
            if number == 0:  # If number is 0 change array position to True and run sea_flow_x
                self.sea[x][0] = True
                MapClass.sea_flow_x(self, x)

    def sea_flow_y(self, y):
        """Loops placing True in the array until hitting the edge of array,
        randomly picks the direction starting on y axis"""
        x = 0
        while not x >= MAP.SIZE_X-1 and not x < 0 and not y >= MAP.SIZE_Y-1 and not y < 0:
            # While not past the array boundary's
            which_tile = random.randint(0, 3)  # Random int used to pick which direction
            if which_tile == 0:
                if not y == 0:  # Don't check if at top of map
                    y -= 1
                    self.sea[x][y] = True  # Up
            if which_tile == 1:
                if not y == MAP.SIZE_Y-1:  # Don't check if at bottom of map
                    y += 1
                    self.sea[x][y] = True  # Down
            if which_tile >= 2:
                if not x == MAP.SIZE_X-1:  # Don't check if at right side of map
                    x += 1
                    self.sea[x][y] = True  # Right

    def sea_flow_x(self, x):
        """Loops placing True in the array until hitting the edge of array,
        randomly picks the direction starting on x axis"""
        y = 0
        while not y >= MAP.SIZE_Y-1 and not y < 0 and not x >= MAP.SIZE_X-1 and not x < 0:
            # While not past the array boundary's
            which_tile = random.randint(0, 3)  # Random int used to pick which direction
            if which_tile == 0:
                if not x == 0:  # Don't check if at left side of map
                    x -= 1
                    self.sea[x][y] = True  # Left
            if which_tile == 1:
                if not x == MAP.SIZE_X-1:  # Don't check if at right side of map'
                    x += 1
                    self.sea[x][y] = True  # Right
            if which_tile >= 2:
                if not y == MAP.SIZE_Y-1:  # Don't check if at bottom of map
                    y += 1
                    self.sea[x][y] = True  # Down

    def sea_render(self):
        """Blits sea images depending on what other places adjacent are seas and sand to some of the edges"""
        surf = self.img
        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                adj = MapClass.sea_check(self, x, y)  # Runs function to check whats next to current tile
                if x <= MAP.SIZE_X and y <= MAP.SIZE_Y:
                    if adj == 1 or adj == 10 or adj == 100 or adj == 1000:  # If at the edge of the sea
                        self.map[x][y] = -1  # Changes map array at location for sand
                        temp_riv = pygame.image.load(MAP.SEA_TILE[0][0]).convert()  # Get sand
                        surf.blit(temp_riv, ((x * MAP.BLOCK_SIZE), (y * MAP.BLOCK_SIZE)))
                    elif adj != 0 and adj != 1 and adj != 10 and adj != 100 and adj != 1000:  # If multiple sea connections
                        self.map[x][y] = -2  # Changes map array at location for sea
                        temp_riv = pygame.image.load(MAP.SEA_TILE[1][0]).convert()  # Get sea
                        surf.blit(temp_riv, ((x * MAP.BLOCK_SIZE), (y * MAP.BLOCK_SIZE)))

        return surf  # Return edited image

    def sea_check(self, x, y):
        """Checks adjacent tiles for seas"""
        num_adj = 0  # Variable to return
        if not x == 0:
            if self.sea[x - 1][y]:  # Check left
                num_adj += 1
        if not y == MAP.SIZE_Y - 1:
            if self.sea[x][y + 1]:  # Check up
                num_adj += 10
        if not y == 0:
            if self.sea[x][y - 1]:  # Check down
                num_adj += 100
        if not x == MAP.SIZE_X - 1:
            if self.sea[x + 1][y]:  # Check right
                num_adj += 1000
        return num_adj


screen = pygame.display.set_mode((800, 500))
Map = MapClass()
pygame.init()
temp_scroll = [0, 0]  # DELETE WHEN BUILT (Temporary scroll mechanic)
print MapClass.map


def display():
    """displays generated map"""
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

            """DELETE WHEN BUILT (Temporary scroll mechanic)"""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if temp_scroll[0] > 0:
                        temp_scroll[0] -= 50

                if event.key == pygame.K_RIGHT:
                    if temp_scroll[0] < (MAP.SIZE_X * MAP.BLOCK_SIZE - 800):
                        temp_scroll[0] += 50

                if event.key == pygame.K_UP:
                    if temp_scroll[1] > 0:
                        temp_scroll[1] -= 50

                if event.key == pygame.K_DOWN:
                    if temp_scroll[1] < (MAP.SIZE_Y * MAP.BLOCK_SIZE - 500):
                        temp_scroll[1] += 50
            """END -- DELETE WHEN BUILT (Temporary scroll mechanic)"""

        screen.blit(Map.img, (-temp_scroll[0], -temp_scroll[1]))
        pygame.display.flip()


display()
