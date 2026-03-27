import arcade
from arcade import gl

arcade.SpriteList.DEFAULT_TEXTURE_FILTER = gl.NEAREST, gl.NEAREST

title = "aaaa"

class GameView(arcade.Window):
    def __init__(self):
        self.win_width = 800
        self.win_height = 450
        self.scaling = 1  # tilemap chargée à 1 pour éviter double mise à l'échelle
        super().__init__(self.win_width, self.win_height, title, fullscreen=True)
        self.background_color = arcade.csscolor.BLACK
        self.tile_map = None
        self.camera = None
        self.keys = set()
        self.spawn_x = 0
        self.spawn_y = 0

        self.camera_zoom = 1.7

        self.player_texture = arcade.load_texture("assets/bobby/front.png")
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 8
        self.player_sprite.center_y = 8

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

    def setup(self):
        # Initialise Camera2D avec zoom par défaut
        self.camera = arcade.Camera2D(zoom=self.camera_zoom)
        self.load_level()

    def load_level(self):
        self.tile_map = arcade.load_tilemap("assets/map.json", scaling=self.scaling)

        # récupérer position spawn
        for obj in self.tile_map.object_lists.get("objects", []):
            if obj.name == "spawn":
                self.spawn_x = obj.shape[0]
                self.spawn_y = obj.shape[1]

        # position caméra
        self.camera.position = (self.spawn_x, self.spawn_y)
        print(self.player_sprite.position)
        self.player_sprite.position = self.spawn_x, self.spawn_y

    def on_draw(self):
        self.clear()
        self.camera.use()  # applique camera.zoom et camera.position
        for sprite_list in self.tile_map.sprite_lists.values():
            sprite_list.draw()

        self.player_list.draw()

    def on_update(self, delta_time):
        x, y = self.camera.position
        speed = max(min((12 - ((delta_time / self.camera_zoom) * 1000)), 2), 0.1)
        print(self.camera_zoom, (delta_time / self.camera_zoom) * 1000, speed)

        # déplacement caméra simple
        if arcade.key.UP in self.keys:
            y += speed
        if arcade.key.DOWN in self.keys:
            y -= speed
        if arcade.key.LEFT in self.keys:
            x -= speed
        if arcade.key.RIGHT in self.keys:
            x += speed

        self.camera.position = (x, y)

        # Zoom dynamique avec Z / D
        if arcade.key.Z in self.keys:
            self.camera_zoom *= 1.05
        elif arcade.key.D in self.keys:
            self.camera_zoom /= 1.05

        # appliquer le zoom à Camera2D
        self.camera.zoom = max(min(self.camera_zoom, 7), 1.7)

    def on_key_press(self, key, modifiers):
        self.keys.add(key)
        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.win_width = self.width
            self.win_height = self.height

    def on_key_release(self, key, modifiers):
        self.keys.discard(key)


def main():
    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()