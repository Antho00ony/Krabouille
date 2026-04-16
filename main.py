import arcade
from arcade import gl
import levels

arcade.SpriteList.DEFAULT_TEXTURE_FILTER = gl.NEAREST, gl.NEAREST
arcade.resources.load_kenney_fonts()


# TODO
# Ombres en plein écran (maze_trial)
# Réinitialisation dialogues lors du changement de carte (enlever)
# Réparer les dialogues des guardes
# Sprite personnage



TITLE = "Krabouille"
BASE_WIDTH = 800
BASE_HEIGHT = 450

clamp = lambda minimum, maximum, x : max(minimum, min(x, maximum))

def move_camera_to(camera: arcade.Camera2D, target_x: float, target_y: float, limits: tuple, speed: float = 0.08):
    cur_x, cur_y = camera.position
    new_x = cur_x + (target_x - cur_x) * speed
    new_y = cur_y + (target_y - cur_y) * speed
    camera.position = (clamp(limits[0][0], limits[1][0], new_x), clamp(limits[0][1], limits[1][1], new_y))

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
    def __init__(self, texture_list: list[arcade.Texture], scale: float = 1):
        super().__init__(texture_list[0], scale = scale)

        self.textures = texture_list
        self.sync_hit_box_to_texture()
        self.cur_texture_index = 3

        self.state = "front" # front, back, left, right

        self.set_texture(3)

    def set_texture(self, index: int):
        self.cur_texture_index = index
        super().set_texture(index)

    def next_frame(self):
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

    def no_moving_position(self):
        if self.state == "front":
            self.set_texture(4)
        elif self.state == "back":
            self.set_texture(8)
        elif self.state == "left":
            self.set_texture(12)
        elif self.state == "right":
            self.set_texture(16)




class GameView(arcade.Window):
    def distance(self, pos):
        return (((pos[0] - self.player_sprite.position[0]) ** 2) + ((pos[1] - self.player_sprite.position[1]) ** 2)) ** 0.5

    def npc_dialogue(self):
        for npc in self.npc_dialogues_dict:
                if self.distance(self.npc_dialogues_dict[npc]["position"]) < 15:
                    self.npc_dialogue_name.text = self.npc_dialogues_dict[npc]["name"]
                    npc_data = self.npc_dialogues_dict[npc]
                    actions_data = npc_data["actions"]
                    self.object_given = False                  

                    if npc_data["completed"] is None:
                        action_list = actions_data
                    else:
                        if isinstance(actions_data, dict):
                            if "first_encounter" in actions_data:
                                action_list = actions_data["first_encounter"]
                            elif "others" in actions_data:
                                action_list = actions_data["others"]
                            else:
                                action_list = actions_data.get("completed", [])
                        else:
                            action_list = actions_data

                    dialogue_first = [x for x in self.npc_dialogues_dict[npc]["actions"]][0]
                    dialogue_len = len(self.npc_dialogues_dict[npc]["actions"][dialogue_first])
                    print(dialogue_first, self.npc_dialogue_index, dialogue_len)
                    if self.npc_dialogue_index >= dialogue_len:
                        if dialogue_first == "first_encounter" and "first_encounter" in self.npc_dialogues_dict[npc]["actions"]: 
                            self.npc_dialogues_dict[npc]["actions"].pop("first_encounter")
                        self.npc_dialogue_index = 0
                        self.npc_show_dialogue = False
                        self.can_move = True
                        break
                    else:
                        self.npc_show_dialogue = True
                        self.can_move = False
                    
                    action = action_list[self.npc_dialogue_index]
                    self.npc_dialogue_index += 1

                    if action["type"] == "dialogue":
                        self.npc_dialogue_name.text = npc_data["name"]
                        self.npc_dialogue_text.text = action["content"]
                        self.npc_show_dialogue = True
                        self.cam_mode = "player"
                    elif action["type"] == "target":
                        self.cam_target = action["position"]
                        self.cam_mode = "target"
                        move_camera_to(self.game_camera, self.cam_target[0], self.cam_target[1], self.cam_limits)
                    elif action["type"] == "item_wait":
                        if action["name"] in self.inventory:
                            self.npc_dialogue_name.text = npc_data["name"]
                            self.npc_dialogue_text.text = action_list[self.npc_dialogue_index]["content"]
                            self.object_given = True
                            npc_data["completed"] = True
                            self.inventory.remove(action["name"])
                            action = action_list[self.npc_dialogue_index]
                            self.npc_dialogue_index = 0
                            if dialogue_first == "others" and "others" in self.npc_dialogues_dict[npc]["actions"]: 
                                self.npc_dialogues_dict[npc]["actions"].pop("others")
                        else:
                            self.object_given = False
                            self.npc_dialogue_index = 0
                            break

                    print(action)

    def __init__(self):
        self.win_width = 800
        self.win_height = 450
        self.scaling = 1  # tilemap chargée à 1 pour éviter double mise à l'échelle
        super().__init__(self.win_width, self.win_height, TITLE, fullscreen=False, vsync=True)
        self.background_color = arcade.csscolor.BLACK

        self.show_hitboxes = False

        self.tile_map = None
        self.scene = None
        self.hitboxes = arcade.SpriteList()

        self.game_camera = None
        self.spawn_x = 0
        self.spawn_y = 0

        self.camera_zoom = 2.5
        self.cam_mode = "player"   # "player" ou "target"
        self.cam_target = (0.0, 0.0)

        # Limites de la caméra
        self.visible_width = 0
        self.visible_height = 0
        self.cam_min_x = 0
        self.cam_max_x = 0
        self.cam_min_y = 0
        self.cam_max_y = 0
        self.cam_limits = ()

        # NPCs
        self.npc_dialogues_dict = {}

        self.npc_dialogue_name = arcade.Text("Name", 80, 110, arcade.color.WHITE, 48, font_name="Kenney Pixel")
        self.npc_dialogue_text = arcade.Text("Dialogue", 100, 90, arcade.color.WHITE, 16, font_name="Kenney Pixel")
        self.npc_show_dialogue = False

        self.npc_dialogue_index = 0

        # Player
        self.player_texture = arcade.load_spritesheet("assets/bobby/bobby_spritesheet.png").get_texture_grid(size = (80, 80), columns = 4, count = 20)

        ## Apply hitbox shape from a dedicated texture to the animated player sprite
        self.player_sprite = Player(self.player_texture, scale = 0.4)

        self.player_sprite.center_x, self.player_sprite.center_y = 16, 16
        self.speed = 1

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.can_move = True
        self.moving = False

        ## Limites de déplacement
        self.player_min_x = self.player_sprite.width / 2
        self.player_min_y = self.player_sprite.height / 2
        self.player_max_x, self.player_max_y = 0, 0

        # Sprites annexes
        self.sprite_list = arcade.SpriteList()
        self.shadow_list = arcade.SpriteList()

        self.chest_texture = arcade.load_spritesheet("assets/chest_tilemap.png").get_texture_grid(size = (16, 16), columns = 2, count = 2)
        self.chest_sprite = AnimationSprites(self.chest_texture)

        self.maze_shadow_texture = arcade.load_texture("assets/maze_shadow.png")
        self.maze_shadow_sprite = arcade.Sprite(self.maze_shadow_texture, scale = 0.25)

        self.sprite_list.append(self.chest_sprite)
        self.shadow_list.append(self.maze_shadow_sprite)

        self.physics_engine = None
        self.level_name = "map"
        self.level_changes_dict = {}
        self.inventory = ["potion_rouge"]
        self.object_given = False
        self.time_elapsed = 0

        self.keys = set()

    def setup(self):
        self.game_camera = arcade.Camera2D(zoom = self.camera_zoom)
        self.ui_camera = arcade.Camera2D(zoom=1.0, position=(self.win_width/2, self.win_height/2))
        levels.load_level(self, self.level_name)

    def on_draw(self):
        self.clear()
        levels.draw_level(self, self.level_name)

    def on_update(self, delta_time):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.cam_mode == "player" and self.can_move:
            if arcade.key.UP in self.keys and self.player_sprite.position[1] <= self.player_max_y: 
                self.player_sprite.change_y = self.speed
            elif arcade.key.DOWN  in self.keys and self.player_sprite.position[1] >= self.player_min_y: 
                self.player_sprite.change_y = -self.speed
            elif arcade.key.LEFT  in self.keys and self.player_sprite.position[0] >= self.player_min_x: 
                self.player_sprite.change_x = -self.speed
            elif arcade.key.RIGHT  in self.keys and self.player_sprite.position[0] <= self.player_max_x: 
                self.player_sprite.change_x = self.speed
            move_camera_to(self.game_camera, self.player_sprite.position[0], self.player_sprite.position[1], self.cam_limits)
        elif self.cam_mode == "target":
            move_camera_to(self.game_camera, self.cam_target[0], self.cam_target[1], self.cam_limits, speed=0.05)
            

        if self.level_name == "maze_trial":
            self.maze_shadow_sprite.position = self.player_sprite.position

        self.time_elapsed += delta_time
        if self.time_elapsed > 0.3 and self.moving:
            self.player_sprite.next_frame()
            self.time_elapsed = 0
        if not self.moving:
            self.player_sprite.no_moving_position()

        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.win_width = self.width
            self.win_height = self.height

            # Adapter le zoom à la résolution pour garder un cadrage cohérent.
            scale_x = self.win_width / BASE_WIDTH
            scale_y = self.win_height / BASE_HEIGHT
            scale = min(scale_x, scale_y)
            adapted_zoom = self.camera_zoom * scale

            # Recréer les caméras avec la nouvelle taille de fenêtre.
            self.game_camera = arcade.Camera2D(zoom=adapted_zoom)
            self.game_camera.position = self.player_sprite.position
            self.ui_camera = arcade.Camera2D(zoom=1.0, position=(self.win_width / 2, self.win_height / 2))

            # Mettre à jour les limites caméra selon le zoom réellement utilisé.
            if self.tile_map is not None:
                self.visible_width = self.win_width / adapted_zoom
                self.visible_height = self.win_height / adapted_zoom

                self.cam_min_x = self.visible_width / 2
                self.cam_max_x = self.tile_map.width * self.tile_map.tile_width - (self.visible_width / 2)
                self.cam_min_y = self.visible_height / 2
                self.cam_max_y = self.tile_map.height * self.tile_map.tile_height - (self.visible_height / 2)
                self.cam_limits = ((self.cam_min_x, self.cam_min_y), (self.cam_max_x, self.cam_max_y))

            # Adapter l'UI sans jamais tomber à 0/négatif.
            self.npc_dialogue_name.font_size = max(24, int(round(48 * scale)))
            self.npc_dialogue_text.font_size = max(12, int(round(16 * scale)))
            self.npc_dialogue_name.position = int(round(80 * scale_x)), int(round(110 * scale_y))
            self.npc_dialogue_text.position = int(round(100 * scale_x)), int(round(90 * scale_y))
        if key == arcade.key.H:
            self.show_hitboxes = not self.show_hitboxes
        if key == arcade.key.N:
            self.player_sprite.next_frame()

        # NPCs & level change
        if key == arcade.key.SPACE:
            self.npc_dialogue()

            for entrance in self.level_changes_dict:
                if self.distance(self.level_changes_dict[entrance]["position"]) < 15:
                    levels.load_level(self, entrance)
                    self.level_name = entrance
                    self.player_sprite.position = self.spawn_x, self.spawn_y
                    print(self.level_name)

            if self.distance(self.chest_sprite.position) < 15:
                if self.can_move and self.chest_sprite.cur_texture_index == 0:
                    self.chest_sprite.set_texture(1)
                    self.can_move = False
                    self.npc_dialogue_name.text = "Nouvel objet!"
                    self.npc_dialogue_text.text = "Vous obtenez une potion rouge. Attendez, ne serait-ce pas du sang???"
                    self.npc_show_dialogue = True
                    self.cam_mode = "player"
                else:
                    self.can_move = True
                    self.npc_show_dialogue = False

        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            if self.keys == set(): 
                self.keys.add(key)
                if key == arcade.key.UP: self.player_sprite.state = "back" 
                if key == arcade.key.DOWN: self.player_sprite.state = "front"
                if key == arcade.key.LEFT: self.player_sprite.state = "left" 
                if key == arcade.key.RIGHT: self.player_sprite.state = "right"
            self.moving = True

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.keys.discard(key)
            self.moving = False


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

