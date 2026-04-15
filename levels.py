import arcade
import main, npc_dialogues
from copy import deepcopy

def load_level(self, name):
    if name == "map":
        self.player_sprite.texture = self.player_hitbox_texture
        self.player_sprite.sync_hit_box_to_texture()
        self.player_sprite.texture = self.player_texture

        self.hitboxes = arcade.SpriteList()

        self.tile_map = arcade.load_tilemap("assets/maps/map.json", scaling = self.scaling)

        self.visible_width = self.win_width / self.camera_zoom
        self.visible_height = self.win_height / self.camera_zoom

        self.cam_min_x = self.visible_width / 2
        self.cam_max_x = self.tile_map.width * self.tile_map.tile_width - (self.visible_width / 2)
        self.cam_min_y = self.visible_height / 2
        self.cam_max_y = self.tile_map.height * self.tile_map.tile_height - (self.visible_height / 2)

        self.cam_limits = ((self.cam_min_x, self.cam_min_y), (self.cam_max_x, self.cam_max_y))
        
        self.player_max_x = self.tile_map.width * self.tile_map.tile_width - self.player_sprite.width / 2
        self.player_max_y = self.tile_map.height * self.tile_map.tile_height - self.player_sprite.height / 2

        self.level_changes_dict = {}
        self.npc_dialogues_dict = {}
        for obj in self.tile_map.object_lists.get("objects", []):
            if obj.name == "spawn":
                self.spawn_x = obj.shape[0]
                self.spawn_y = obj.shape[1]
            if obj.name in ("wizard", "ghost", "cactus"):
                source_data = npc_dialogues.npc_dialogues_dict[obj.name]
                self.npc_dialogues_dict.update({
                    obj.name: {
                        "name": source_data["name"],
                        "position": (obj.shape[0], obj.shape[1]),
                        "actions": deepcopy(source_data["actions"]),
                        "completed": source_data.get("completed", False),
                        "first_encounter_done": False
                    }
                })
            if obj.name in ("torch_trial", "maze_trial"):
                self.level_changes_dict.update({obj.name: {"position": (obj.shape[0], obj.shape[1])}})

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # pnjs offset
        self.scene["pnjs"].move(-6, -5.33333)
        self.scene["pnjs_over"].move(-6, -5.33333)
        self.scene["pnjs_hitboxes"].move(-6, -5.33333)

        # position caméra, joueur
        self.game_camera.position = self.spawn_x, self.spawn_y
        self.player_sprite.position = self.spawn_x, self.spawn_y

        self.scene.add_sprite("Player", self.player_sprite)

        # physics engine
        self.hitboxes.extend(self.scene["hitboxes"])
        self.hitboxes.extend(self.scene["pnjs_hitboxes"])
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, walls = self.hitboxes)
    elif name == "maze_trial":
        self.player_sprite.texture = self.maze_player_texture
        self.player_sprite.sync_hit_box_to_texture()
        self.player_sprite.texture = self.player_texture

        self.hitboxes = arcade.SpriteList()

        self.tile_map = arcade.load_tilemap("assets/maps/maze_trial.json", scaling = self.scaling)

        self.visible_width = self.win_width / self.camera_zoom
        self.visible_height = self.win_height / self.camera_zoom

        self.cam_min_x = self.visible_width / 2
        self.cam_max_x = self.tile_map.width * self.tile_map.tile_width - (self.visible_width / 2)
        self.cam_min_y = self.visible_height / 2
        self.cam_max_y = self.tile_map.height * self.tile_map.tile_height - (self.visible_height / 2)

        self.cam_limits = ((self.cam_min_x, self.cam_min_y), (self.cam_max_x, self.cam_max_y))
        
        self.player_max_x = self.tile_map.width * self.tile_map.tile_width - self.player_sprite.width / 2
        self.player_max_y = self.tile_map.height * self.tile_map.tile_height - self.player_sprite.height / 2

        self.npc_dialogues_dict = {}
        self.level_changes_dict = {}
        for obj in self.tile_map.object_lists.get("objects", []):
            if obj.name == "spawn":
                self.spawn_x = obj.shape[0]
                self.spawn_y = obj.shape[1]
            if obj.name == "map":
                self.level_changes_dict.update({obj.name: {"position": (obj.shape[0], obj.shape[1])}})
            if obj.name == "chest":
                self.chest_sprite.position = obj.shape[0][0] + 8, obj.shape[0][1] - 2
            if obj.name in ("guard_l", "guard_r"):
                source_data = npc_dialogues.npc_dialogues_dict[obj.name]
                self.npc_dialogues_dict.update({
                    obj.name: {
                        "name": source_data["name"],
                        "position": (obj.shape[0], obj.shape[1]),
                        "actions": deepcopy(source_data["actions"]),
                        "completed": source_data.get("completed", False),
                        "first_encounter_done": False
                    }
                })

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # pnjs offset
        self.scene["items"].move(-5.33, -1)

        # position caméra, joueur
        self.game_camera.position = self.spawn_x, self.spawn_y
        self.player_sprite.position = self.spawn_x, self.spawn_y

        self.scene.add_sprite("Player", self.player_sprite)

        # physics engine
        self.hitboxes.extend(self.scene["hitboxes"])
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, walls = self.hitboxes)


def draw_level(self, name):
    if name == "map":
        self.game_camera.use()

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

        # NPCs dialogues avec UI Camera
        if self.npc_show_dialogue:
            self.ui_camera.use()
            self.npc_dialogue_name.draw()
            self.npc_dialogue_text.draw()


        if self.show_hitboxes:
            self.game_camera.use()
            self.scene["hitboxes"].draw_hit_boxes(arcade.color.GREEN)
            self.scene["pnjs_hitboxes"].draw_hit_boxes(arcade.color.GREEN)
            self.player_sprite.draw_hit_box(arcade.color.RED)
    elif name == "maze_trial":
        self.game_camera.use()

        # Layers sous le joueur
        self.scene["ground"].draw()
        self.scene["ground2"].draw()
        self.scene["walls_behind"].draw()
        self.scene["walls"].draw()
        self.scene["pnjs"].draw()
        self.scene["items"].draw()

        self.sprite_list.draw()
        self.player_list.draw()

        self.scene["walls_front"].draw()

        self.shadow_list.draw()

        arcade.draw_lbwh_rectangle_filled(self.player_sprite.position[0] - 330, self.player_sprite.position[1] - 180, 230, 420, (0, 0, 0)) # Gauche
        arcade.draw_lbwh_rectangle_filled(self.player_sprite.position[0] + 100, self.player_sprite.position[1] - 180, 300, 450, (0, 0, 0)) # Droite
        arcade.draw_lbwh_rectangle_filled(self.player_sprite.position[0] - 150, self.player_sprite.position[1] - 220, 300, 150, (0, 0, 0)) # Bas
        arcade.draw_lbwh_rectangle_filled(self.player_sprite.position[0] - 150, self.player_sprite.position[1] + 80, 250, 150, (0, 0, 0)) # Haut

        # NPCs dialogues avec UI Camera
        if self.npc_show_dialogue:
            self.ui_camera.use()
            self.npc_dialogue_name.draw()
            self.npc_dialogue_text.draw()

        if self.show_hitboxes:
            self.game_camera.use()
            self.scene["hitboxes"].draw_hit_boxes(arcade.color.GREEN)
            self.scene["hitboxes2"].draw_hit_boxes(arcade.color.GREEN)
            self.player_sprite.draw_hit_box(arcade.color.RED)



if __name__ == "__main__":
    main.main()
