import sys
import pygame as pg
from settings import *
from tetris import Tetris, Text
import pathlib

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.img = self.load_img()
        self.tetris = Tetris(self)
        self.text = Text(self)

    def load_img(self):
        files = [item for item in pathlib.Path(SPRITE_DIR).rglob("*.png") if item.is_file()]
        img = [pg.image.load(str(file)).convert_alpha() for file in files]
        print(f"Original size: {img[0].get_size()}")  # Oryginalny rozmiar
        img = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in img]
        print(f"Scaled size: {img[0].get_size()}")  # Skalowany rozmiar
        return img

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIMATION_TIME)
        pg.time.set_timer(self.fast_user_event, FAST_ANIMATION)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0,0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def chceck_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.chceck_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()