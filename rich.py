import pygame
import sys
import random

# Dictionary mapping property names to their prices
NamesToPrice = {
    "陶朱隱園": 1,
    "世界明珠": 2,
    "帝寶": 3,
    "西華富邦": 4,
    "敦南霖園": 5,
    "管圖": 6,
    "金色陽光": 7,
    "翠綠花園": 8,
    "豪門世家": 9,
    "水晶湖畔": 10,
    "鑽石山莊": 11,
    "皇家御苑": 12,
    "龍城豪庭": 13,
    "天際花園": 14,
    "碧海藍天": 15,
    "盛世名門": 16,
    "富貴園": 17,
    "天鵝湖": 18,
    "雲頂華府": 19,
    "繽紛花城": 20,
    "麗景花園": 21,
    "金都豪宅": 22,
    "幸福莊園": 23,
    "水岸人家": 24,
    "星光大道": 25,
    "皇后花園": 26,
    "白金豪庭": 27,
    "頤和園": 28,
    "紫禁城": 29,
    "東方明珠": 30,
    "珠江御景": 31,
    "紫苑花都": 32
}

# List of property names shuffled for random board setup
GridToInfo = list(NamesToPrice.keys())
random.shuffle(GridToInfo)

class BoardAttr:
    """Class representing attributes of a board cell."""
    def __init__(self, name, price, playerId, color, x=0, y=0):
        self.name = name
        self.price = price
        self.who = playerId  # Owner of the property (-1 if unowned)
        self.x = x
        self.y = y
        self.color = color

class Button:
    """Class representing a clickable button."""
    def __init__(self, text, position, color, hover_color, size=(100, 50)):
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont('arialunicode', 20)
        self.rect = pygame.Rect(position, size)
        self.text_surf = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        """Draws the button on the screen, changing color on hover."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        """Checks if the button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def check_hover(self):
        """Updates the button appearance based on mouse hover."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            self.draw(screen)
        else:
            self.current_color = self.color
            self.draw(screen)

# Load and scale dice images
dice = [
    pygame.transform.scale(pygame.image.load('dice/1.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('dice/2.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('dice/3.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('dice/4.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('dice/5.png'), (75, 75)),
    pygame.transform.scale(pygame.image.load('dice/6.png'), (75, 75))
]

# Initialize Pygame
pygame.init()

# Set up game window
width, height = 800, 800
grid_size = 10  # Number of cells per side
cell_size = width / 10  # Size of each cell
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("臺大富翁")  # "The Monopoly of NTU"
dice_rect = pygame.Rect(width / 2 - 40, cell_size * 2.5, 80, 80)
GridInfo = []

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_RED = (255, 182, 193)
LIGHT_GREEN = (144, 238, 144)
LIGHT_YELLOW = (255, 255, 224)
LIGHT_PURPLE = (216, 191, 216)
LIGHT_ORANGE = (255, 228, 181)
CORNER_COLOR = LIGHT_BLUE
SIDE_COLORS = [LIGHT_RED, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_ORANGE]
COLORS = [RED, BLUE, GREEN, YELLOW]
COLOR_NAMES = ["Red", "Blue", "Green", "Yellow"]

# Initialize board cells
for i in range((grid_size - 2) * 4):
    color = SIDE_COLORS[i // 8]
    thisGrid = BoardAttr(GridToInfo[i], NamesToPrice[GridToInfo[i]], -1, color)
    GridInfo.append(thisGrid)

# Add corner cells
color = CORNER_COLOR
thisGrid = BoardAttr("Start", 0, -1, color)
GridInfo.insert(0, thisGrid)
thisGrid = BoardAttr("機會", 0, -1, color)  # "Chance"
GridInfo.insert(9, thisGrid)
thisGrid = BoardAttr("監獄", 0, -1, color)  # "Jail"
GridInfo.insert(18, thisGrid)
thisGrid = BoardAttr("命運", 0, -1, color)  # "Fate"
GridInfo.insert(27, thisGrid)

# Set up the game clock
clock = pygame.time.Clock()

# Player selection screen
while True:
    screen.fill((255, 222, 173))  # Background color
    font = pygame.font.SysFont('arialunicode', 40)
    message = "請選擇玩家人數"  # "Please select number of players"
    text_surface = font.render(message, True, BLACK)
    message_bg_rect = pygame.Rect(200, 100, 400, 70)
    pygame.draw.rect(screen, (255, 250, 205), message_bg_rect.inflate(20, 10))
    text_rect = text_surface.get_rect(midtop=message_bg_rect.midtop)
    screen.blit(text_surface, text_rect)
    
    # Create player number buttons
    two_player = Button("2 Players", (340, 500), (255, 182, 193), (219, 112, 147), (120, 50))
    three_player = Button("3 Players", (340, 600), (135, 206, 235), (70, 130, 180), (120, 50))
    four_player = Button("4 Players", (340, 700), (60, 179, 113), (46, 139, 87), (120, 50))
    
    # Draw buttons
    two_player.draw(screen)
    three_player.draw(screen)
    four_player.draw(screen)
    
    pygame.display.flip()
    confirm = False
    while not confirm:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if two_player.is_clicked(event):
                confirm = True
                num_players = 2
            elif three_player.is_clicked(event):
                confirm = True
                num_players = 3
            elif four_player.is_clicked(event):
                confirm = True
                num_players = 4
        # Update button hover states
        two_player.check_hover()
        three_player.check_hover()
        four_player.check_hover()
        clock.tick(30)
        pygame.display.flip()
    break  # Exit the selection loop once a choice is made

# Function to draw the game board
def draw_board():
    count = 0
    font = pygame.font.SysFont('arialunicode', 20)
    
    # Draw top side
    for i in range(grid_size - 1):
        GridInfo[count].x = i * cell_size
        GridInfo[count].y = 0
        rect = pygame.Rect(GridInfo[count].x, GridInfo[count].y, cell_size, cell_size)
        pygame.draw.rect(screen, GridInfo[count].color, rect)
        border_thickness = 2
        if i == 0:
            border_thickness = 1  # Thinner border for the first cell
        # Draw ownership indicator
        if GridInfo[count].who != -1:
            house = pygame.Rect(
                GridInfo[count].x + cell_size - cell_size / 5,
                GridInfo[count].y + cell_size - cell_size / 5,
                cell_size / 5,
                cell_size / 5
            )
            pygame.draw.rect(screen, COLORS[GridInfo[count].who], house)
        pygame.draw.rect(screen, BLACK, rect, border_thickness)
        # Render property name
        text = font.render(GridInfo[count].name, True, BLACK)
        text_rect = text.get_rect(midtop=rect.midtop)
        screen.blit(text, text_rect)
        count += 1

    # Draw right side
    for i in range(grid_size - 1):
        GridInfo[count].x = (grid_size - 1) * cell_size
        GridInfo[count].y = i * cell_size
        rect = pygame.Rect(GridInfo[count].x, GridInfo[count].y, cell_size, cell_size)
        pygame.draw.rect(screen, GridInfo[count].color, rect)
        border_thickness = 2
        if i == 0:
            border_thickness = 1
        if GridInfo[count].who != -1:
            house = pygame.Rect(
                GridInfo[count].x + cell_size - cell_size / 5,
                GridInfo[count].y + cell_size - cell_size / 5,
                cell_size / 5,
                cell_size / 5
            )
            pygame.draw.rect(screen, COLORS[GridInfo[count].who], house)
        pygame.draw.rect(screen, BLACK, rect, border_thickness)
        text = font.render(GridInfo[count].name, True, BLACK)
        text_rect = text.get_rect(midtop=rect.midtop)
        screen.blit(text, text_rect)
        count += 1

    # Draw bottom side
    for i in range(grid_size - 1):
        GridInfo[count].x = (grid_size - 1 - i) * cell_size
        GridInfo[count].y = (grid_size - 1) * cell_size
        rect = pygame.Rect(GridInfo[count].x, GridInfo[count].y, cell_size, cell_size)
        pygame.draw.rect(screen, GridInfo[count].color, rect)
        border_thickness = 2
        if i == 0:
            border_thickness = 1
        if GridInfo[count].who != -1:
            house = pygame.Rect(
                GridInfo[count].x + cell_size - cell_size / 5,
                GridInfo[count].y + cell_size - cell_size / 5,
                cell_size / 5,
                cell_size / 5
            )
            pygame.draw.rect(screen, COLORS[GridInfo[count].who], house)
        pygame.draw.rect(screen, BLACK, rect, border_thickness)
        text = font.render(GridInfo[count].name, True, BLACK)
        text_rect = text.get_rect(midtop=rect.midtop)
        screen.blit(text, text_rect)
        count += 1

    # Draw left side
    for i in range(grid_size - 1):
        GridInfo[count].x = 0
        GridInfo[count].y = (grid_size - 1 - i) * cell_size
        rect = pygame.Rect(GridInfo[count].x, GridInfo[count].y, cell_size, cell_size)
        pygame.draw.rect(screen, GridInfo[count].color, rect)
        border_thickness = 2
        if i == 0:
            border_thickness = 1
        if GridInfo[count].who != -1:
            house = pygame.Rect(
                GridInfo[count].x + cell_size - cell_size / 5,
                GridInfo[count].y + cell_size - cell_size / 5,
                cell_size / 5,
                cell_size / 5
            )
            pygame.draw.rect(screen, COLORS[GridInfo[count].who], house)
        pygame.draw.rect(screen, BLACK, rect, border_thickness)
        text = font.render(GridInfo[count].name, True, BLACK)
        text_rect = text.get_rect(midtop=rect.midtop)
        screen.blit(text, text_rect)
        count += 1

def draw_players(positions, colors):
    """Draws player tokens on the board."""
    player_positions = {}
    for idx, position in enumerate(positions):
        if position not in player_positions:
            player_positions[position] = []
        player_positions[position].append(colors[idx])

    for position, player_colors in player_positions.items():
        x = GridInfo[position].x + cell_size / 2
        y = GridInfo[position].y + cell_size / 2
        offset = 0
        for player_color in player_colors:
            pygame.draw.circle(
                screen,
                player_color,
                (x, y + offset),
                (cell_size - 40) // 2 - 5
            )
            offset += 10  # Offset to prevent overlapping tokens

def draw_current_player_message(current_player, color):
    """Displays a message indicating the current player's turn."""
    font = pygame.font.Font(None, 36)
    message = f"{COLOR_NAMES[current_player]} Player's Turn"
    text_surface = font.render(message, True, BLACK)
    message_bg_rect = text_surface.get_rect(
        center=(width // 2, height - cell_size - 50)
    )
    pygame.draw.rect(screen, color, message_bg_rect.inflate(20, 10))
    screen.blit(text_surface, message_bg_rect)

def draw_player_money(player_money):
    """Displays each player's current money."""
    font = pygame.font.Font(None, 24)
    for idx, money in enumerate(player_money):
        message = f"{COLOR_NAMES[idx]}: ${money}"
        text_surface = font.render(message, True, BLACK)
        screen.blit(text_surface, (width // 2 - 40, 6 * cell_size + 30 * (idx + 1)))

def main():
    """Main game loop."""
    player_positions = [0] * num_players  # Initialize all players at 'Start'
    player_colors = COLORS[:num_players]
    player_money = [2000] * num_players  # Starting money for each player
    current_player = 0
    dice_result = -1
    diceturn = 0
    dice_image = None
    rolling = Button(
        "Roll Dice",
        (340, 100),
        (255, 215, 0),
        (218, 165, 32),
        (120, 50)
    )
    
    while True:
        screen.fill(WHITE)
        draw_board()
        draw_players(player_positions, player_colors)
        draw_current_player_message(current_player, player_colors[current_player])
        rolling.draw(screen)
        
        # Display dice if rolled
        if dice_result != -1:
            dice_image_rect = dice[dice_result].get_rect(center=dice_rect.center)
            screen.blit(dice[dice_result], dice_image_rect)
        
        draw_player_money(player_money)
        pygame.display.flip()
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if rolling.is_clicked(event):
                # Simulate dice rolling
                diceturn = random.randint(2, 6)
                while diceturn > 0:
                    dice_result = random.randint(0, 5)
                    dice_image_rect = dice[dice_result].get_rect(center=dice_rect.center)
                    screen.blit(dice[dice_result], dice_image_rect)
                    pygame.display.flip()
                    clock.tick(10)
                    diceturn -= 1
                
                # Update player position
                new_position = (player_positions[current_player] + dice_result + 1) % ((grid_size - 1) * 4)
                
                # Collect money if passing 'Start'
                if new_position < player_positions[current_player]:
                    player_money[current_player] += 500
                
                player_positions[current_player] = new_position
                screen.fill(WHITE)
                draw_board()
                rolling.draw(screen)
                pygame.display.flip()
                draw_players(player_positions, player_colors)
                pygame.display.flip()
                
                # Check if the landed cell is purchasable
                if (
                    GridInfo[new_position].who == -1 and
                    GridInfo[new_position].name not in ["Start", "機會", "命運", "監獄", "YouBike站"] and
                    player_money[current_player] >= GridInfo[new_position].price
                ):
                    dice_image_rect = dice[dice_result].get_rect(center=dice_rect.center)
                    screen.blit(dice[dice_result], dice_image_rect)
                    font = pygame.font.SysFont('arialunicode', 20)
                    message = f"你要買{GridInfo[new_position].name}嗎？價值：${GridInfo[new_position].price}"  # "Do you want to buy {name}? Price: ${price}"
                    text_surface = font.render(message, True, BLACK)
                    message_bg_rect = pygame.Rect(
                        cell_size * 2.75,
                        cell_size * 4,
                        4.5 * cell_size,
                        cell_size * 1.5
                    )
                    pygame.draw.rect(screen, GridInfo[new_position].color, message_bg_rect.inflate(20, 10))
                    text_rect = text_surface.get_rect(midtop=message_bg_rect.midtop)
                    text_rect.y += 10
                    screen.blit(text_surface, text_rect)
                    
                    # Create confirmation buttons
                    confirm_button = Button("確認", (300, 350), (155, 236, 173), (128, 189, 142))
                    reject_button = Button("拒絕", (450, 350), (215, 122, 128), (188, 75, 75))
                    confirm_button.rect.topleft = (message_bg_rect.left + 50, message_bg_rect.bottom - 60)
                    confirm_button.text_rect = confirm_button.text_surf.get_rect(center=confirm_button.rect.center)
                    reject_button.rect.topleft = (message_bg_rect.right - 150, message_bg_rect.bottom - 60)
                    reject_button.text_rect = reject_button.text_surf.get_rect(center=reject_button.rect.center)
                    
                    # Draw confirmation buttons
                    confirm_button.draw(screen)
                    reject_button.draw(screen)
                    pygame.display.flip()
                    
                    confirm = False
                    while not confirm:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if confirm_button.is_clicked(event):
                                confirm = True
                                GridInfo[new_position].who = current_player
                                player_money[current_player] -= GridInfo[new_position].price
                            elif reject_button.is_clicked(event):
                                confirm = True
                        # Update button hover states
                        confirm_button.check_hover()
                        reject_button.check_hover()
                        clock.tick(30)
                        draw_player_money(player_money)
                        draw_current_player_message(current_player, player_colors[current_player])
                        pygame.display.flip()
                
                # Move to the next player
                current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
