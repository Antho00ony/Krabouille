import arcade
from arcade import gl
import levels

arcade.SpriteList.DEFAULT_TEXTURE_FILTER = gl.NEAREST, gl.NEAREST
arcade.resources.load_kenney_fonts()

TITLE = "Krabouille"

clamp = lambda minimum, maximum, x : max(minimum, min(x, maximum))

def move_camera_to(camera: arcade.Camera2D, target_x: float, target_y: float, limits: tuple, speed: float = 0.08):
    cur_x, cur_y = camera.position
    new_x = cur_x + (target_x - cur_x) * speed
    new_y = cur_y + (target_y - cur_y) * speed
    camera.position = (clamp(limits[0][0], limits[1][0], new_x), clamp(limits[0][1], limits[1][1], new_y))

class GameView(arcade.Window):
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
        self.npc_dict = {
            "wizard": {
                "name": "Sorcier",
                "position": (None, None),
                "actions": [
                    {
                        "type": "dialogue",
                        "content": "I'm the evil wizard"
                    },
                    {
                        "type": "dialogue",
                        "content": "I kidnapped your family, bring me 5€ if you want to see them again."
                    }
                ]
            },
            "ghost": {
                "name": "Le fantôme",
                "position": (None, None),
                "actions": [
                    {
                        "type": "dialogue",
                        "content": "I'm the ghost!"
                    },
                    {
                        "type": "target",
                        "position": (240, 214)
                    }
                ]
            },
            "cactus": {
                "name": "Cactus",
                "position": (None, None),
                "actions": [
                    {
                        "type": "dialogue",
                        "content": "I'm the ghost!"
                    },
                    {
                        "type": "target",
                        "position": (240, 214)
                    }
                ]
            }
        }

        self.npc_dialogue_name = arcade.Text("Name", 80, 110, arcade.color.WHITE, 48, font_name="Kenney Pixel")
        self.npc_dialogue_text = arcade.Text("Dialogue", 100, 90, arcade.color.WHITE, 16, font_name="Kenney Pixel")
        self.npc_show_dialogue = False

        self.npc_dialogue_index = 0

        # Player
        self.player_texture = arcade.load_texture("assets/bobby/front.png")

        ## Créer le sprite avec la texture d'hitbox pour générer la bonne hitbox
        hitbox_texture = arcade.load_texture("assets/bobby/hitbox.png")
        self.player_sprite = arcade.Sprite(hitbox_texture)

        ## Remplacer la texture par celle d'affichage (la hitbox reste)
        self.player_sprite.texture = self.player_texture

        self.player_sprite.center_x = 8
        self.player_sprite.center_y = 8
        self.speed = 1

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.can_move = True

        ## Limites de déplacement
        self.player_min_x = self.player_sprite.width / 2
        self.player_max_x = 0
        self.player_min_y = self.player_sprite.height / 2
        self.player_max_y = 0

        self.physics_engine = None
        self.level_name = "map"
        self.level_entrance_dict = {}

        # Suivi des touches appuyées
        self.keys_pressed = set()

    def setup(self):
        self.game_camera = arcade.Camera2D(zoom = self.camera_zoom)
        self.ui_camera = arcade.Camera2D(zoom=1.0, position=(self.win_width/2, self.win_height/2))
        self.load_level(self.level_name)

    def load_level(self, name):
        levels.load_level(self, name)

        

    def on_draw(self):
        self.clear()

        levels.draw_level(self, self.level_name)

    def on_update(self, delta_time):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.cam_mode == "player" and self.can_move:
            move_camera_to(self.game_camera, self.player_sprite.position[0], self.player_sprite.position[1], self.cam_limits)
            if arcade.key.UP in self.keys_pressed and self.player_sprite.position[1] <= self.player_max_y:
                self.player_sprite.change_y = self.speed
            if arcade.key.DOWN in self.keys_pressed and self.player_sprite.position[1] >= self.player_min_y:
                self.player_sprite.change_y = -self.speed
            if arcade.key.LEFT in self.keys_pressed and self.player_sprite.position[0] >= self.player_min_x:
                self.player_sprite.change_x = -self.speed
            if arcade.key.RIGHT in self.keys_pressed and self.player_sprite.position[0] <= self.player_max_x:
                self.player_sprite.change_x = self.speed
        elif self.cam_mode == "target":
            move_camera_to(self.game_camera, self.cam_target[0], self.cam_target[1], self.cam_limits, speed=0.05)
            

        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.win_width = self.width
            self.win_height = self.height
            # Adapter le zoom proportionnellement à la résolution
            # Pour voir la même zone de la carte peu importe la résolution
            adapted_zoom = self.camera_zoom * (self.win_width / 800)
            # Recréer la caméra avec le zoom adapté
            self.game_camera = arcade.Camera2D(zoom=adapted_zoom)
            self.game_camera.position = self.player_sprite.position
        if key == arcade.key.H:
            self.show_hitboxes = not self.show_hitboxes

        # NPCs & level change
        if key == arcade.key.SPACE:
            distance = lambda x : (((x[0] - self.player_sprite.position[0]) ** 2) + ((x[1] - self.player_sprite.position[1]) ** 2)) ** 0.5
            
            for npc in self.npc_dict:
                if distance(self.npc_dict[npc]["position"]) < 15:
                    if self.npc_dialogue_index >= len(self.npc_dict[npc]["actions"]):
                        pass
                    elif self.npc_dict[npc]["actions"][self.npc_dialogue_index]["type"] == "dialogue":
                        self.npc_show_dialogue = True
                        self.cam_mode = "player"
                        self.npc_dialogue_name.text = self.npc_dict[npc]["name"]
                        self.npc_dialogue_text.text = self.npc_dict[npc]["actions"][self.npc_dialogue_index]["content"]
                    elif self.npc_dict[npc]["actions"][self.npc_dialogue_index]["type"] == "target":
                        self.cam_target = self.npc_dict[npc]["actions"][self.npc_dialogue_index]["position"]
                        self.cam_mode = "target"
                        move_camera_to(self.game_camera, self.cam_target[0], self.cam_target[1], self.cam_limits)
                
                    if self.npc_dialogue_index >= len(self.npc_dict[npc]["actions"]):
                        self.npc_dialogue_index = 0
                        self.npc_show_dialogue = False
                        self.can_move = True
                        self.cam_mode = "player"
                    else:
                        self.npc_dialogue_index += 1
                        self.can_move = False

            for entrance in self.level_entrance_dict:
                if distance(self.level_entrance_dict[entrance]["position"]) < 15:
                    levels.load_level(self, entrance)
                    self.level_name = entrance
                    self.player_sprite.position = self.spawn_x, self.spawn_y

    # Enregistrer la touche comme appuyée
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        # Retirer la touche du suivi
        self.keys_pressed.discard(key)


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
