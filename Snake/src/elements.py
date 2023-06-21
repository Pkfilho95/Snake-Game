from pygame import draw, Rect
from random import choice

from .settings import *

class Snake:

    def __init__(self):
        self._direction = choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self._body = [(MAP_WIDTH // 2 - SNAKE_SIZE // 2, MAP_HEIGHT // 2 - SNAKE_SIZE // 2)]
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, direction):
        self._direction = direction
    
    @property
    def body(self):
        return self._body
    
    @body.setter
    def body(self, new_body):
        self._body = new_body
    
    @property
    def head(self):
        return self.body[0]
    
    @property
    def length(self):
        return len(self.body)

    def movement(self):
        """
        Moves the snake.
        """

        if self.direction == 'UP':
            _new_position = (self.head[0], self.head[1] - SNAKE_SIZE)
        elif self.direction == 'DOWN':
            _new_position = (self.head[0], self.head[1] + SNAKE_SIZE)
        elif self.direction == 'LEFT':
            _new_position = (self.head[0] - SNAKE_SIZE, self.head[1])
        elif self.direction == 'RIGHT':
            _new_position = (self.head[0] + SNAKE_SIZE, self.head[1])
        
        self.body = [_new_position] + [self.body[i-1] for i in range(1, len(self.body))]

    def eatFood(self, food):
        """
        Check if the snake collides with the food.
        """

        _head = Rect(self.head[0], self.head[1], SNAKE_SIZE, SNAKE_SIZE)
        _food = Rect(food.position[0], food.position[1], food.size, food.size)

        if _head.colliderect(_food):
            self.grow()
            food.position = food.setPosition()

            # Check if the new food position collides with the snake
            _food = Rect(food.position[0], food.position[1], food.size, food.size)
            while (_food.x, _food.y) in self.body:
                food.position = food.setPosition()
                _food = Rect(food.position[0], food.position[1], food.size, food.size)
    
    def grow(self):
        """
        Creates a new body segment.
        """

        if self.direction == 'UP':
            _new_segment = (self.head[0], self.head[1] - SNAKE_SIZE)
        elif self.direction == 'DOWN':
            _new_segment = (self.head[0], self.head[1] + SNAKE_SIZE)
        elif self.direction == 'LEFT':
            _new_segment = (self.head[0] - SNAKE_SIZE, self.head[1])
        elif self.direction == 'RIGHT':
            _new_segment = (self.head[0] + SNAKE_SIZE, self.head[1])
        
        self.body.insert(0, _new_segment)
    
    def verifyCollision(self):
        """
        Verify if the snake collides with the wall or with its own body.
        """

        _collision_x = MAP_BEGIN_X < self.head[0] < (MAP_BEGIN_X + MAP_WIDTH - SNAKE_SIZE)
        _collision_y = MAP_BEGIN_Y < self.head[1] < (MAP_BEGIN_Y + MAP_HEIGHT - SNAKE_SIZE)

        if not _collision_x or not _collision_y:
            return True
        
        if self.head in self.body[1:]:
            return True

        return False

    def drawSnake(self, screen):
        """
        Draw the snake.
        """

        for segment in self.body:
            draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
    
class Food:

    def __init__(self):
        self._size = FOOD_SIZE
        self._color = FOOD_COLOR
        self._position = self.setPosition()
    
    @property
    def size(self):
        return self._size
    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        self._position = position

    def setPosition(self):
        """
        Set the random position of the food.
        """

        _x = [x for x in range(FOOD_BEGIN_X, FOOD_END_X, SNAKE_SIZE)]
        _y = [y for y in range(FOOD_BEGIN_Y, FOOD_END_Y, SNAKE_SIZE)]

        _position = (choice(_x), choice(_y))

        return _position

    def drawFood(self, screen):
        """
        Draw the food.
        """

        draw.rect(screen, FOOD_COLOR, (self.position[0], self.position[1], self.size, self.size))
    
    


