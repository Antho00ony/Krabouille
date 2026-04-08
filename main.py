import arcade
from arcade import gl

arcade.SpriteList.DEFAULT_TEXTURE_FILTER = gl.NEAREST, gl.NEAREST

TITLE = "Krabouille"

def move_camera_to(camera: arcade.Camera2D, target_x: float, target_y: float, speed: float = 0.08):
    cur_x, cur_y = camera.position
    new_x = cur_x + (target_x - cur_x) * speed
    new_y = cur_y + (target_y - cur_y) * speed
    camera.position = (new_x, new_y)

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

        self.camera = None
        self.spawn_x = 0
        self.spawn_y = 0

        self.camera_zoom = 2.5
        self.cam_mode = "player"   # "player" ou "target"
        self.cam_target = (0.0, 0.0)

        # NPCs
        self.npc_dict = {
            "wizard": {
                "position": (None, None),
                "dialogue": "WIP",
                "action": None
            },
            "ghost": {
                "position": (None, None),
                "dialogue": "WIP",
                "action": {
                    "type": "target",
                    "position": (200, 300)
                }
            },
            "cactus": {
                "position": (None, None),
                "dialogue": "WIP",
                "action": {
                    "type": "target",
                    "position": (400, 500)
                }
            }
        }

        self.player_texture = arcade.load_texture("assets/bobby/front.png")

        # Créer le sprite avec la texture d'hitbox pour générer la bonne hitbox
        hitbox_texture = arcade.load_texture("assets/bobby/hitbox.png")
        self.player_sprite = arcade.Sprite(hitbox_texture)

        # Remplacer la texture par celle d'affichage (la hitbox reste)
        self.player_sprite.texture = self.player_texture

        self.player_sprite.center_x = 8
        self.player_sprite.center_y = 8
        self.speed = 1

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.physics_engine = None

        # Suivi des touches appuyées
        self.keys_pressed = set()

    def setup(self):
        # Initialise Camera2D avec zoom par défaut
        self.camera = arcade.Camera2D(zoom = self.camera_zoom)
        self.load_level()

    def load_level(self):
        self.tile_map = arcade.load_tilemap("assets/map.json", scaling = self.scaling)

        # récupérer position spawn
        for obj in self.tile_map.object_lists.get("objects", []):
            if obj.name == "spawn":
                self.spawn_x = obj.shape[0]
                self.spawn_y = obj.shape[1]
            if obj.name in ("wizard", "ghost", "cactus"):
                self.npc_dict[obj.name]["position"] = (obj.shape[0], obj.shape[1])

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # pnjs offset
        self.scene["pnjs"].move(-6, -5.33333)
        self.scene["pnjs_over"].move(-6, -5.33333)
        self.scene["pnjs_hitboxes"].move(-6, -5.33333)

        # position caméra, joueur
        self.camera.position = self.spawn_x, self.spawn_y
        self.player_sprite.position = self.spawn_x, self.spawn_y

        self.scene.add_sprite("Player", self.player_sprite)

        # physics engine
        self.hitboxes.extend(self.scene["hitboxes"])
        self.hitboxes.extend(self.scene["pnjs_hitboxes"])
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, walls = self.hitboxes)

    def on_draw(self):
        self.clear()
        self.camera.use()

        # Layers sous le joueur
        self.scene["ground"].draw()
        self.scene["rails"].draw()
        self.scene["walls"].draw()
        self.scene["doors"].draw()
        self.scene["gravestones"].draw()
        self.scene["pnjs"].draw()
        self.scene["minecarts"].draw()

        # Le joueur
        self.player_list.draw()

        # Layers au-dessus du joueur
        self.scene["top_walls"].draw()
        self.scene["items"].draw()
        self.scene["plus"].draw()
        self.scene["pnjs_over"].draw()

        if self.show_hitboxes:
            self.scene["hitboxes"].draw()
            self.scene["pnjs_hitboxes"].draw()
            self.player_sprite.draw_hit_box(arcade.color.RED)


    def on_update(self, delta_time):
        # Calculer la vélocité basée sur les touches appuyées
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.cam_mode == "player":
            move_camera_to(self.camera, self.player_sprite.position[0], self.player_sprite.position[1])
            if arcade.key.UP in self.keys_pressed:
                self.player_sprite.change_y = self.speed
            if arcade.key.DOWN in self.keys_pressed:
                self.player_sprite.change_y = -self.speed
            if arcade.key.LEFT in self.keys_pressed:
                self.player_sprite.change_x = -self.speed
            if arcade.key.RIGHT in self.keys_pressed:
                self.player_sprite.change_x = self.speed
        else:
            move_camera_to(self.camera, self.cam_target[0], self.cam_target[1], speed=0.05)
            

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
            self.camera = arcade.Camera2D(zoom=adapted_zoom)
            self.camera.position = self.player_sprite.position
        if key == arcade.key.H:
            self.show_hitboxes = not self.show_hitboxes

        # NPCs
        if key == arcade.key.SPACE:
            distance = lambda x : (((x[0] - self.player_sprite.position[0]) ** 2) + ((x[1] - self.player_sprite.position[1]) ** 2)) ** 0.5
            for npc in self.npc_dict:
                if distance(self.npc_dict[npc]["position"]) < 15:
                    print(self.npc_dict[npc]["dialogue"])
                    if self.npc_dict[npc]["action"] is not None:
                        if self.npc_dict[npc]["action"]["type"] == "target":
                            if self.cam_mode == "target":
                                self.cam_mode = "player"
                            else:
                                self.cam_mode = "target"
                                self.cam_target = self.npc_dict[npc]["action"]["position"]

        # Enregistrer la touche comme appuyée
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.keys_pressed.add(key)


        """ ZOOM DYNAMIQUE
        # Zoom dynamique avec Z / D
        if key == arcade.key.Z:
            self.camera_zoom *= 1.05
        elif key == arcade.key.D:
            self.camera_zoom /= 1.05

        # appliquer le zoom à Camera2D
        self.camera.zoom = min(max(self.camera_zoom, 1.7), 7)"""

    def on_key_release(self, key, modifiers):
        # Retirer la touche du suivi
        self.keys_pressed.discard(key)


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
