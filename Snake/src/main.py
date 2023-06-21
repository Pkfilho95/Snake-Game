import pygame
from pygame.locals import *

from .settings import *
from .elements import *

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        # Screen setup
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen_color = SCREEN_COLOR

        # Map setup
        self.map_rect = MAP_RECT
        self.map_color = MAP_COLOR

        # Game setup
        self.clock = pygame.time.Clock()
        self.valid_keys = {K_UP: 'UP', K_DOWN: 'DOWN', K_LEFT: 'LEFT', K_RIGHT: 'RIGHT'}
        self.game_over = False
        self.last_click = 0

        # Elements
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.snake = Snake()
        self.food = Food()

        # Scoreboard setup
        self.scoreboard_font = pygame.font.Font(None, 30)
        self.scoreboard = self.scoreboard_font.render(SCOREBOARD_TEXT.format(0), True, SCOREBOARD_COLOR)
        self.scoreboard_rect = self.scoreboard.get_rect()
        self.scoreboard_rect.centerx = SCOREBOARD_X
        self.scoreboard_rect.y = SCOREBOARD_Y - 10
    
    def events(self):
        """
        Check all events.
        """

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            elif event.type == KEYDOWN:
                if event.key in self.valid_keys:
                    _current_time = pygame.time.get_ticks()
                    if _current_time - self.last_click >= CLICK_INTERVAL:
                        self.updateDirection(event)
                        self.last_click = _current_time
            
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    if self.game_over:
                        self.restartGame()

    def updateDirection(self, event):
        """
        Update the snake direction.
        """

        _change = False

        if self.snake.length == 1:
            _change = True

        else:
            if event.key == K_UP and self.snake.direction != 'DOWN': _change = True
            elif event.key == K_DOWN and self.snake.direction != 'UP': _change = True
            elif event.key == K_LEFT and self.snake.direction != 'RIGHT': _change = True
            elif event.key == K_RIGHT and self.snake.direction != 'LEFT': _change = True
        
        if _change:
            self.snake.direction = self.valid_keys[event.key]
    
    def updateScore(self):
        """
        Update the scoreboard.
        """

        _points = self.snake.length - 1
        
        self.scoreboard = self.scoreboard_font.render(SCOREBOARD_TEXT.format(_points), True, SCOREBOARD_COLOR)
        self.screen.blit(self.scoreboard, self.scoreboard_rect)

    def drawElements(self):
        """
        Draw and update screen, map, snake and food.
        """

        self.screen.fill(self.screen_color)
        self.screen.fill(self.map_color, rect=self.map_rect)

        self.updateScore()
        self.snake.drawSnake(self.screen)
        self.food.drawFood(self.screen)

        pygame.display.update()

    def runGame(self):
        """
        Start the main loop.
        """

        while True:
            self.events()
            
            if not self.game_over:
                if self.snake.verifyCollision():
                    self.game_over = True
                    self.gameOver()
                    continue
                
                self.snake.movement()
                self.snake.eatFood(self.food)
                self.drawElements()

            self.clock.tick(SNAKE_VELOCITY)
    
    def restartGame(self):
        """
        Restart the game.
        """

        Game().runGame()
    
    def gameOver(self):
        """
        Show game over message and restart button.
        """

        # Game over setup
        _game_over_font = pygame.font.Font(None, 40)
        _game_over = _game_over_font.render(GAME_OVER_TEXT, True, GAME_OVER_COLOR)
        _game_over_rect = _game_over.get_rect()
        _game_over_rect.centerx = GAME_OVER_X
        _game_over_rect.y = GAME_OVER_Y - 30

        self.screen.blit(_game_over, _game_over_rect)

        _restart_font = pygame.font.Font(None, 30)
        _restart = _restart_font.render("Press ENTER to restart", True, 'black')
        _restart_rect = _restart.get_rect()
        _restart_rect.centerx = GAME_OVER_X
        _restart_rect.y = GAME_OVER_Y + 20

        self.screen.blit(_restart, _restart_rect)

        pygame.display.update()
