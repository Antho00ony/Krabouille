import arcade
from arcade import gl

import levels, functions
from classes import *
from on_key_press import key_press

arcade.SpriteList.DEFAULT_TEXTURE_FILTER = gl.NEAREST, gl.NEAREST
arcade.resources.load_kenney_fonts()
arcade.load_font("assets/Fipps-Regular.otf")

# TODO
# Château (tuiles poussables)
### Portes
### Casse tête
### Dialogue krabouille (type item_wait ==> None; END)


TITLE = "Krabouille"
DEFAULT_WIN_WIDTH = 800
DEFAULT_WIN_HEIGHT = 450

class GameView(arcade.Window):
    def __init__(self):
        self.win_width = DEFAULT_WIN_WIDTH
        self.win_height = DEFAULT_WIN_HEIGHT
        self.win_scale = 1
        super().__init__(self.win_width, self.win_height, TITLE, fullscreen=False, vsync=True)

        ###### Player ######

        self.player_texture = arcade.load_spritesheet("assets/bobby/bobby_spritesheet.png").get_texture_grid(size = (80, 80), columns = 4, count = 20)

        # Hitbox texture
        self.player_sprite = Player(self.player_texture, scale = 0.4)

        self.player_sprite.center_x, self.player_sprite.center_y = 16, 16

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.can_move = True
        self.speed = 1
        self.moving = False
        self.climb_ladder = False

        # Limites de déplacement
        self.player_min_x = 0
        self.player_min_y = 0
        self.player_max_x, self.player_max_y = 0, 0

        ###### NPCs ######

        self.npc_dialogues_dict = {}
        self.places_allowed = set()
        self.places_allowed.add("map")
        self.places_allowed.add("map_1")

        self.npc_dialogue_name = arcade.Text("Name", 0, 0, (255, 255, 255, 255), 16, font_name="Fipps") # position dans functions.py ==> change_cam_limits()
        self.npc_dialogue_text = arcade.Text("Dialogue", 0, 0, (255, 255, 255, 255), 10, font_name="Fipps", width=500, multiline=True)
        self.npc_show_dialogue = False

        self.npc_dialogue_background = arcade.Sprite(arcade.load_texture("assets/dialogue_background.png"))

        self.npc_dialogue_background_list = arcade.SpriteList()
        self.npc_dialogue_background_list.append(self.npc_dialogue_background)

        self.npc_dialogue_index = 0

        ###### Sprites annexes ######

        # Chest

        self.chest_texture = arcade.load_spritesheet("assets/chest_tilemap.png").get_texture_grid(size = (16, 16), columns = 2, count = 2)
        self.chest_sprite = AnimationSprites(self.chest_texture)

        # Torches

        self.torch_texture = arcade.load_spritesheet("assets/torch_tilemap.png").get_texture_grid(size = (20, 20), columns = 1, count = 2)
        self.torch_sprite1 = AnimationSprites(self.torch_texture)
        self.torch_sprite2 = AnimationSprites(self.torch_texture)
        self.torch_sprite3 = AnimationSprites(self.torch_texture)

        self.torch_sprite1.scale = 1.5
        self.torch_sprite2.scale = 1.5
        self.torch_sprite3.scale = 1.5

        # Ladders

        self.ladders_texture = arcade.load_texture("assets/ladders.png")
        self.ladders_sprite = arcade.Sprite(self.ladders_texture)

        # Doors

        self.doors_texture = arcade.load_spritesheet("assets/doors_spritesheet.png").get_texture_grid(size = (32, 32), columns = 2, count = 2)
        self.doors_sprite = AnimationSprites(self.doors_texture)

        self.doors_sprite.scale = 1.5
        
        self.castle_doors_texture = arcade.load_spritesheet("assets/castle_doors_spritesheet.png").get_texture_grid(size = (32, 16), columns = 6, count = 84)
        self.castle_doors_sprite = AnimationSprites(self.castle_doors_texture)

        self.castle_doors_sprite.set_texture(0) # 0 = fermé, 1 = ouvert

        # Maze shadow

        self.maze_shadow_texture = arcade.load_texture("assets/maze_shadow.png")
        self.maze_shadow_sprite = arcade.Sprite(self.maze_shadow_texture, scale = 0.25)


        # Spritelists

        self.sprite_list = arcade.SpriteList()

        self.shadow_list = arcade.SpriteList()
        self.shadow_list.append(self.maze_shadow_sprite)

        self.ladders_sprite_list = arcade.SpriteList()
        self.ladders_sprite_list.append(self.ladders_sprite)

        self.hitboxes = arcade.SpriteList()

        ###### Map ######

        self.tile_map = None
        self.scaling = 1 # Taille map
        self.scene = None
        self.show_hitboxes = False

        ###### Cameras ######

        self.game_camera = None
        self.ui_camera = None
        self.camera_zoom = 2.5
        self.cam_mode = "player"   # player, target
        self.cam_target = (0.0, 0.0)

        # Limites de la caméra
        self.visible_width = 0
        self.visible_height = 0
        self.cam_min_x = 0
        self.cam_max_x = 0
        self.cam_min_y = 0
        self.cam_max_y = 0
        self.cam_limits = ()

        ###### Player spawn ######

        self.spawn_x = 0
        self.spawn_y = 0

        ###### Others ######

        self.physics_engine = None
        self.level_name = "castle" # map, maze_trial, torch_trial, castle
        self.exit = None
        self.level_changes_dict = {}
        self.inventory = set()
        self.object_given = False
        self.castle_door_opened = False
        self.ladders_unlocked = False

        # Animations

        self.time_elapsed = 0
        self.time_elapsed_ladders = 0

        # Enregistrement touches clavier

        self.keys = set()

    def setup(self):
        self.game_camera = arcade.Camera2D(zoom = self.camera_zoom)
        self.ui_camera = arcade.Camera2D(zoom=1.0, position=(self.win_width/2, self.win_height/2))
        levels.load_level(self, self.level_name)

    def on_draw(self):
        self.clear()
        levels.draw_level(self, self.level_name)

    def on_update(self, delta_time):
        if self.cam_mode == "player" and self.can_move:
            if self.level_name != "torch_trial":
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                if arcade.key.UP in self.keys and self.player_sprite.position[1] <= self.player_max_y: 
                    self.player_sprite.change_y = self.speed
                elif arcade.key.DOWN  in self.keys and self.player_sprite.position[1] >= self.player_min_y: 
                    self.player_sprite.change_y = -self.speed
                elif arcade.key.LEFT  in self.keys and self.player_sprite.position[0] >= self.player_min_x: 
                    self.player_sprite.change_x = -self.speed
                elif arcade.key.RIGHT  in self.keys and self.player_sprite.position[0] <= self.player_max_x: 
                    self.player_sprite.change_x = self.speed
            else:
                self.player_sprite.change_x = 0
                self.ladders_unlocked = self.torch_sprite1.cur_texture_index == 1 and self.torch_sprite2.cur_texture_index == 1 and self.torch_sprite3.cur_texture_index == 1
                ladder_entry_x = self.ladders_sprite.position[0]
                ladder_entry_y = self.ladders_sprite.position[1] - 65
                near_ladder_entry = (
                    abs(self.player_sprite.position[0] - ladder_entry_x) < 12
                    and abs(self.player_sprite.position[1] - ladder_entry_y) < 20
                )

                # Leave ladder mode when UP is released or top is reached.
                if self.climb_ladder and arcade.key.UP not in self.keys or self.player_sprite.position[1] >= 140:
                    self.climb_ladder = False

                if arcade.key.UP in self.keys:
                    if self.ladders_unlocked and near_ladder_entry:
                        self.player_sprite.state = "back"
                        self.player_sprite.set_texture(8)
                        self.climb_ladder = True
                    elif not self.climb_ladder and self.physics_engine.can_jump():
                        self.player_sprite.change_y = 7
                if arcade.key.LEFT in self.keys:
                    self.player_sprite.change_x = -self.speed
                if arcade.key.RIGHT in self.keys:
                    self.player_sprite.change_x = self.speed
            functions.move_camera_to(self.game_camera, self.player_sprite.position[0], self.player_sprite.position[1], self.cam_limits)
        elif self.cam_mode == "target":
            functions.move_camera_to(self.game_camera, self.cam_target[0], self.cam_target[1], self.cam_limits, speed=0.05)
            

        if self.level_name == "maze_trial":
            self.maze_shadow_sprite.position = self.player_sprite.position

        if self.level_name == "torch_trial" and self.ladders_unlocked:
            self.time_elapsed_ladders += delta_time
            if "statue" in self.inventory:
                self.ladders_sprite.position = self.ladders_sprite.position[0], 90
                self.climb_ladder = False
            elif self.time_elapsed_ladders > 0.01 and self.ladders_sprite.position[1] > 90:
                self.ladders_sprite.position = self.ladders_sprite.position[0], self.ladders_sprite.position[1] - 0.5
                self.time_elapsed_ladders = 0
            if self.climb_ladder and self.player_sprite.position[1] < 140:
                self.player_sprite.position = self.player_sprite.position[0], self.player_sprite.position[1] + 1
                self.player_sprite.change_y = 0
            else:
                self.climb_ladder = False

        if self.npc_dialogue_text.text != "":
            if self.npc_dialogue_text.text[-1] == "‎":
                self.npc_dialogue_text.align = "center"
                if self.npc_dialogue_text.color[3] > 0:
                    self.npc_dialogue_text.color = self.npc_dialogue_text.color[0], self.npc_dialogue_text.color[1], self.npc_dialogue_text.color[2], max(0, self.npc_dialogue_text.color[3] - round(50 * delta_time))
                    self.npc_dialogue_background.color = self.npc_dialogue_background.color[0], self.npc_dialogue_background.color[1], self.npc_dialogue_background.color[2], 0
                else:
                    self.npc_show_dialogue = False
                    self.npc_dialogue_text.color = self.npc_dialogue_text.color[0], self.npc_dialogue_text.color[1], self.npc_dialogue_text.color[2], 0
                    self.npc_dialogue_text.text = ""
                    self.npc_dialogue_text.align = "left"
        
        self.time_elapsed += delta_time
        if self.level_name == "torch_trial" and self.climb_ladder:
            self.player_sprite.state = "back"
            self.player_sprite.set_texture(8)
            self.time_elapsed = 0
        elif self.moving and self.can_move:
            if self.time_elapsed >= 0.12:
                self.player_sprite.next_frame(self.can_move)
                self.time_elapsed = 0
        else:
            self.player_sprite.no_moving_position(self.can_move)
            self.time_elapsed = 0
       
        if "castle_doors" in self.inventory:
            self.castle_doors_sprite.set_texture(1)
            self.castle_door_opened = True
            self.inventory.remove("castle_doors")

        if self.level_name == "torch_trial" and self.climb_ladder:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
        else:
            self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        key_press(self, key, modifiers)        

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            if self.level_name == "torch_trial":
                self.player_sprite.change_x = 0
            self.keys.discard(key)
            self.moving = bool(self.keys) # False si self.keys est vide


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()





