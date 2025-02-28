import os
import sys

from settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True

        super().__init__(tetromino.tetris.sprite_group)
        self.image = tetromino.image
        self.rect = self.image.get_rect()

    def is_alive(self):
        if not self.alive:
            self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE_SIZE

    def update(self):
        self.is_alive()
        self.set_rect_pos()

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (
                y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True

class Tetromino:
    def __init__(self, tetris, current = True):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.image = random.choice(tetris.app.img)
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landing = False
        self.current  = current

    def rotate(self):
        pivot_pos = self.blocks[0].pos
        
        if self.blocks[0].tetromino.shape != 'O':
            new_block_pos = [block.rotate(pivot_pos) for block in self.blocks]
        else:
            new_block_pos = [block.pos for block in self.blocks]

        if not self.is_collide(new_block_pos):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_pos[i]

    def is_collide(self, block_pos):
        return any(map(Block.is_collide, self.blocks, block_pos))

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_pos = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_pos)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True
    def update(self):
        self.move(direction='down')
