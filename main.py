import arcade
from arcade import gl

arcade.SpriteList.DEFAULT_TEXTURE_FILTER = gl.NEAREST, gl.NEAREST

title = "Krabouille"


class GameView(arcade.Window):
    def __init__(self):
        self.win_width = 800
        self.win_height = 450
        self.scaling = 1  # tilemap chargée à 1 pour éviter double mise à l'échelle
        super().__init__(self.win_width, self.win_height, title, fullscreen = True)
        self.background_color = arcade.csscolor.BLACK

        self.tile_map = None
        self.scene = None
        self.hitboxes = arcade.SpriteList()

        self.camera = None
        self.spawn_x = 0
        self.spawn_y = 0

        self.camera_zoom = 5.5

        self.player_texture = arcade.load_texture("assets/bobby/front.png")
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 8
        self.player_sprite.center_y = 8
        self.speed = 1

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.physics_engine = None

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

        # Le joueur
        self.player_list.draw()

        # Layers au-dessus du joueur
        self.scene["top_walls"].draw()
        self.scene["items"].draw()
        self.scene["plus"].draw()
        self.scene["pnjs_over"].draw()

    def on_update(self, delta_time):
        self.physics_engine.update()

        self.camera.position = self.player_sprite.position

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.win_width = self.width
            self.win_height = self.height

        # déplacement caméra simple
        if key == arcade.key.UP:
            self.player_sprite.change_y = self.speed
        if key == arcade.key.DOWN:
            self.player_sprite.change_y = -self.speed
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -self.speed
        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = self.speed

        # Zoom dynamique avec Z / D
        if key == arcade.key.Z:
            self.camera_zoom *= 1.05
        elif key == arcade.key.D:
            self.camera_zoom /= 1.05

        # appliquer le zoom à Camera2D
        self.camera.zoom = min(max(self.camera_zoom, 1.7), 7)

    def on_key_release(self, key, modifiers):
        # déplacement caméra simple
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
        if key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
