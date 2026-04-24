import arcade

import main

clamp = lambda minimum, maximum, x : max(minimum, min(x, maximum))

def move_camera_to(camera: arcade.Camera2D, target_x: float, target_y: float, limits: tuple, speed: float = 0.08):
    cur_x, cur_y = camera.position
    new_x = cur_x + (target_x - cur_x) * speed
    new_y = cur_y + (target_y - cur_y) * speed
    camera.position = (clamp(limits[0][0], limits[1][0], new_x), clamp(limits[0][1], limits[1][1], new_y))

def change_cam_limits(self):
        self.win_width = self.width
        self.win_height = self.height

        # Adapter le zoom à la résolution de l'écran
        scale_x = self.win_width / main.DEFAULT_WIN_WIDTH
        scale_y = self.win_height / main.DEFAULT_WIN_HEIGHT
        scale = min(scale_x, scale_y)
        adapted_zoom = self.camera_zoom * scale

        self.npc_dialogue_text.width = 500 * self.win_width / main.DEFAULT_WIN_WIDTH

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

            self.player_min_x = self.player_sprite.width / 2 * self.player_sprite.scale[0]
            self.player_min_y = self.player_sprite.height * self.player_sprite.scale[0]
            self.player_max_x = self.tile_map.width * self.tile_map.tile_width - self.player_sprite.width / 2 * self.player_sprite.scale[0]
            self.player_max_y = self.tile_map.height * self.tile_map.tile_height - self.player_sprite.height / 2 * self.player_sprite.scale[0]

        # Keep dialogue text compact with the custom pixel font.
        self.npc_dialogue_name.font_size = max(10, int(round(16 * scale)))
        self.npc_dialogue_text.font_size = max(6, int(round(10 * scale)))
        self.npc_dialogue_name.position = int(round(150 * scale_x)), int(round(130 * scale_y))
        self.npc_dialogue_text.position = int(round(160 * scale_x)), int(round(100 * scale_y))
        self.npc_dialogue_background.scale = 1.6 * scale
        self.npc_dialogue_background.position = self.win_width / 2, int(round(90 * scale_y))
        self.end_screen.scale = 0.5 * scale
        self.end_screen.position = self.win_width / 2, self.win_height / 2

def npc_dialogue(self, pressed_key=None):
    self.npc_dialogue_background.color = self.npc_dialogue_background.color[0], self.npc_dialogue_background.color[1], self.npc_dialogue_background.color[2], 150
    for npc in self.npc_dialogues_dict:
        if distance(self.player_sprite.position, self.npc_dialogues_dict[npc]["position"]) < 15:
            self.npc_dialogue_text.color = self.npc_dialogue_text.color[0], self.npc_dialogue_text.color[1], self.npc_dialogue_text.color[2], 255
            self.npc_dialogue_text.align = "left"
            self.npc_dialogue_name.text = self.npc_dialogues_dict[npc]["name"]
            if self.npc_dialogues_dict[npc]["place"] is not None:
                self.places_allowed.add(self.npc_dialogues_dict[npc]["place"])
            npc_data = self.npc_dialogues_dict[npc]
            actions_data = npc_data["actions"]
            self.object_given = False                  

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
            if self.npc_dialogue_index >= dialogue_len:
                if dialogue_first == "first_encounter" and "first_encounter" in self.npc_dialogues_dict[npc]["actions"]: 
                    self.npc_dialogues_dict[npc]["actions"].pop("first_encounter")
                self.npc_dialogue_index = 0
                self.npc_waiting_key = None
                self.npc_show_dialogue = False
                self.can_move = True
                break
            else:
                self.npc_show_dialogue = True
                self.can_move = False
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
            
            action = action_list[self.npc_dialogue_index]
            self.npc_dialogue_index += 1

            if action["type"] == "finish":
                npc_data["completed"] = True
                self.npc_dialogue_index = 0
                self.npc_waiting_key = None
                self.npc_dialogues_dict[npc]["actions"].pop("others")
                self.npc_show_dialogue = False
                self.can_move = True
                if action["action"] == "show_puzzle":
                    self.transition = "in"
                    self.pending_action = "show_puzzle"

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
                if action["id"] in self.inventory:
                    self.object_given = True
                    self.inventory.remove(action["id"])
                    if action["item_given"] != None:
                        self.inventory.add(action["item_given"])
                    self.npc_dialogue_name.text = action["name"]
                    self.npc_dialogue_text.text = action["content"]
                    self.npc_show_dialogue = True
                    action = action_list[self.npc_dialogue_index]
                else:
                    self.object_given = False
                    self.npc_dialogue_index = 0
                    self.npc_waiting_key = None
                    self.npc_show_dialogue = False
                    self.can_move = True
                    break
            elif action["type"] == "item_give":
                self.inventory.add(action["id"])
            elif action["type"] == "key_wait":
                self.npc_dialogue_name.text = "Intentional Game Design"
                self.npc_dialogue_text.text = action["content"]
                self.npc_show_dialogue = True
                self.cam_mode = "player"
                expected_key = action.get("id")

                if pressed_key == expected_key:
                    self.npc_waiting_key = None
                    if action.get("action") == "puzzle_reset":
                        self.transition = "in"
                        self.pending_action = "puzzle_reset"
                        break
                    npc_dialogue(self)
                    break

                self.npc_waiting_key = expected_key
                self.npc_dialogue_index -= 1
                break

def distance(pos1, pos2):
        return (((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2)) ** 0.5

def sprite_in_map_bounds(self, sprite: arcade.Sprite, center_x: float, center_y: float):
        map_width = self.tile_map.width * self.tile_map.tile_width
        map_height = self.tile_map.height * self.tile_map.tile_height
        half_width = sprite.width / 2
        half_height = sprite.height / 2

        return (
            half_width <= center_x <= map_width - half_width
            and half_height <= center_y <= map_height - half_height
        )

def snap_pushables_to_grid(self):
    if self.level_name != "castle":
        return

    # Tiles in this project are 16x16, centered on +8 offsets.
    tile_size = self.tile_map.tile_width
    half_tile = tile_size / 2

    for pushable in self.pushable_list:
        old_pos = pushable.position
        snapped_x = round((pushable.center_x - half_tile) / tile_size) * tile_size + half_tile
        snapped_y = round((pushable.center_y - half_tile) / tile_size) * tile_size + half_tile

        if not sprite_in_map_bounds(self, pushable, snapped_x, snapped_y):
            continue

        pushable.position = snapped_x, snapped_y

        blocked_by_wall = len(arcade.check_for_collision_with_list(pushable, self.hitboxes)) > 0
        blocked_by_tile = any(
            other is not pushable and arcade.check_for_collision(pushable, other)
            for other in self.pushable_list
        )
        blocked_by_player = arcade.check_for_collision(pushable, self.player_sprite)

        if blocked_by_wall or blocked_by_tile or blocked_by_player:
            # Never snap into an invalid state (especially inside the player).
            pushable.position = old_pos

def try_push_castle_tile(self):
    if self.level_name != "castle":
        return
    if self.player_sprite.change_x == 0 and self.player_sprite.change_y == 0:
        return

    old_player_pos = self.player_sprite.position
    next_player_pos = (
        self.player_sprite.center_x + self.player_sprite.change_x,
        self.player_sprite.center_y + self.player_sprite.change_y
    )

    self.player_sprite.position = next_player_pos
    touching_tiles = arcade.check_for_collision_with_list(self.player_sprite, self.pushable_list)
    self.player_sprite.position = old_player_pos

    if len(touching_tiles) == 0:
        return
    if len(touching_tiles) > 1:
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        return

    pushed_tile = touching_tiles[0]
    new_tile_x = pushed_tile.center_x + self.player_sprite.change_x
    new_tile_y = pushed_tile.center_y + self.player_sprite.change_y
 
    if not sprite_in_map_bounds(self, pushed_tile, new_tile_x, new_tile_y):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        return

    old_tile_pos = pushed_tile.position
    pushed_tile.position = new_tile_x, new_tile_y

    blocked_by_wall = len(arcade.check_for_collision_with_list(pushed_tile, self.hitboxes)) > 0
    blocked_by_tile = any(
        other is not pushed_tile and arcade.check_for_collision(pushed_tile, other)
        for other in self.pushable_list
    )

    if blocked_by_wall or blocked_by_tile:
        pushed_tile.position = old_tile_pos
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
    else:
        # Keep the moved tile in place; the physics engine will then move the player.
        pass

def reset_pushables_to_initial_positions(self):
    if self.level_name == "castle":
        for pushable, position in self.pushable_initial_positions:
            pushable.position = position






if __name__ == "__main__":
    main.main()
