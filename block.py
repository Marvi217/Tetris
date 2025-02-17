import pygame as pg

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tettromino = tetromino
