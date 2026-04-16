import arcade
import main, npc_dialogues

def define_player(self, hitbox_name, _scale: float = 0.4):
    # Player
    self.player_texture = arcade.load_spritesheet("assets/bobby/bobby_spritesheet.png").get_texture_grid(size = (80, 80), columns = 4, count = 20)

    ## Apply hitbox shape from a dedicated texture to the animated player sprite
    if hitbox_name == "map":
        temp = 0
    elif hitbox_name == "maze_trial":
        temp = 1
    elif hitbox_name == "torch_trial":
        temp = 2
    self.player_sprite = main.Player(self.player_texture, scale = _scale, hitbox_index = temp)

    self.player_sprite.center_x, self.player_sprite.center_y = 16, 16
    self.speed = 1

    self.player_list = arcade.SpriteList()
    self.player_list.append(self.player_sprite)

    self.can_move = True
    self.moving = False

    self.hitboxes = arcade.SpriteList()


def load_level(self, name):
    if name == "map":
        self.tile_map = arcade.load_tilemap("assets/maps/map.json", scaling = self.scaling)
        define_player(self, name)

        main.change_cam_limits(self)

        self.level_changes_dict = {}
        self.npc_dialogues_dict = {}
        for obj in self.tile_map.object_lists.get("objects", []):
            if obj.name == "spawn":
                self.spawn_x = obj.shape[0]
                self.spawn_y = obj.shape[1]
            if obj.name in ("wizard", "ghost", "cactus"):
                npc_dialogues.npc_dialogues_dict[obj.name] = npc_dialogues.npc_dialogues_dict[obj.name]
                self.npc_dialogues_dict.update({
                    obj.name: {
                        "name": npc_dialogues.npc_dialogues_dict[obj.name]["name"],
                        "position": (obj.shape[0], obj.shape[1]),
                        "actions": npc_dialogues.npc_dialogues_dict[obj.name]["actions"],
                        "completed": npc_dialogues.npc_dialogues_dict[obj.name].get("completed", False),
                        "first_encounter_done": False
                    }
                })
            if obj.name in ("torch_trial", "maze_trial"):
                self.level_changes_dict.update({obj.name: {"position": (obj.shape[0], obj.shape[1])}})

        if self.exit == "maze_trial":
            self.spawn_x, self.spawn_y = self.level_changes_dict["maze_trial"]["position"]
        elif self.exit == "torch_trial":
            self.spawn_x, self.spawn_y = self.level_changes_dict["torch_trial"]["position"]

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
        self.tile_map = arcade.load_tilemap("assets/maps/maze_trial.json", scaling = self.scaling)
        define_player(self, name)

        main.change_cam_limits(self)

        self.npc_dialogues_dict = {}
        self.level_changes_dict = {}
        for obj in self.tile_map.object_lists.get("objects", []):
            if obj.name == "spawn":
                self.spawn_x = obj.shape[0]
                self.spawn_y = obj.shape[1]
            if obj.name == "map":
                self.level_changes_dict.update({obj.name: {"position": (obj.shape[0], obj.shape[1])}})
                self.exit = obj.shape
            if obj.name == "chest":
                self.chest_sprite.position = obj.shape[0][0] + 8, obj.shape[0][1] - 2
            if obj.name in ("guard_l", "guard_r"):
                npc_dialogues.npc_dialogues_dict[obj.name] = npc_dialogues.npc_dialogues_dict[obj.name]
                self.npc_dialogues_dict.update({
                    obj.name: {
                        "name": npc_dialogues.npc_dialogues_dict[obj.name]["name"],
                        "position": (obj.shape[0], obj.shape[1]),
                        "actions": npc_dialogues.npc_dialogues_dict[obj.name]["actions"],
                        "completed": npc_dialogues.npc_dialogues_dict[obj.name].get("completed", False),
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
    elif name == "torch_trial":
            self.tile_map = arcade.load_tilemap("assets/maps/torch_trial.json", scaling = self.scaling)
            define_player(self, name)

            main.change_cam_limits(self)

            try:
                self.sprite_list.remove(self.chest_sprite)
            except:
                pass

            self.npc_dialogues_dict = {}
            self.level_changes_dict = {}
            for obj in self.tile_map.object_lists.get("objects", []):
                if obj.name == "spawn":
                    self.spawn_x = obj.shape[0]
                    self.spawn_y = obj.shape[1]
                if obj.name == "map":
                    self.level_changes_dict.update({obj.name: {"position": (obj.shape[0], obj.shape[1])}})
                    self.exit = obj.shape
                    self.doors_sprite.position = obj.shape[0], obj.shape[1] + 24
                if obj.name == "torch1":
                    self.torch_sprite1.position = obj.shape[0][0] + 10, obj.shape[0][1]
                if obj.name == "torch2":
                    self.torch_sprite2.position = obj.shape[0][0] + 10, obj.shape[0][1]
                if obj.name == "torch3":
                    self.torch_sprite3.position = obj.shape[0][0] + 10, obj.shape[0][1]
                if obj.name == "ladders":
                    self.ladders_sprite.position = obj.shape[0], obj.shape[1] + 74
                
            self.scene = arcade.Scene.from_tilemap(self.tile_map)

            # position caméra, joueur
            self.game_camera.position = self.spawn_x, self.spawn_y
            self.player_sprite.position = self.spawn_x, self.spawn_y

            self.scene.add_sprite("Player", self.player_sprite)

            # physics engine
            self.hitboxes.extend(self.scene["hitboxes"])
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, walls = self.hitboxes, gravity_constant = 0.5)


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
    elif name == "torch_trial":
        self.game_camera.use()

        # Layers sous le joueur
        self.scene["ground"].draw()
        self.scene["walls"].draw()
        self.scene["boxes"].draw()

        if self.torch_sprite1.cur_texture_index == 1 and self.torch_sprite2.cur_texture_index == 1 and self.torch_sprite3.cur_texture_index == 1:
            self.ladders_sprite_list.draw()
            
        self.sprite_list.draw()
        self.player_list.draw()


        # NPCs dialogues avec UI Camera
        if self.npc_show_dialogue:
            self.ui_camera.use()
            self.npc_dialogue_name.draw()
            self.npc_dialogue_text.draw()

        if self.show_hitboxes:
            self.game_camera.use()
            self.scene["hitboxes"].draw_hit_boxes(arcade.color.GREEN)
            self.player_sprite.draw_hit_box(arcade.color.RED)



if __name__ == "__main__":
    main.main()
