import arcade
from functions import *



class AnimationSprites(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture]):
        super().__init__(texture_list[0])

        self.textures = texture_list
        self.cur_texture_index = 0

        self.set_texture(0)

    def set_texture(self, index: int):
        self.cur_texture_index = index
        super().set_texture(index)

class Player(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture], scale: float = 1, hitbox_index: int = 0):
        super().__init__(texture_list[hitbox_index], scale = scale)

        self.textures = texture_list
        self.sync_hit_box_to_texture()
        self.cur_texture_index = 3

        self.state = "front" # front, back, left, right

        self.set_texture(3)

    def set_texture(self, index: int):
        self.cur_texture_index = index
        super().set_texture(index)

    def next_frame(self, can_move):
        if can_move:
            if self.state == "front":
                if self.cur_texture_index >= 7:
                    self.set_texture(4)
                else:
                    self.set_texture(clamp(4, 7, self.cur_texture_index + 1))
            elif self.state == "back":
                if self.cur_texture_index >= 11:
                    self.set_texture(8)
                else:
                    self.set_texture(clamp(8, 11, self.cur_texture_index + 1))
            elif self.state == "left":
                if self.cur_texture_index >= 15:
                    self.set_texture(12)
                else:
                    self.set_texture(clamp(12, 15, self.cur_texture_index + 1))
            elif self.state == "right":
                if self.cur_texture_index >= 19:
                    self.set_texture(16)
                else:
                    self.set_texture(clamp(16, 19, self.cur_texture_index + 1))

    def no_moving_position(self, can_move):
        if can_move:
            if self.state == "front":
                self.set_texture(4)
            elif self.state == "back":
                self.set_texture(8)
            elif self.state == "left":
                self.set_texture(12)
            elif self.state == "right":
                self.set_texture(16)



