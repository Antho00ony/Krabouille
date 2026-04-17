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

        self.npc_dialogue_text.width = 600 * self.win_width / main.DEFAULT_WIN_WIDTH

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
        self.npc_dialogue_name.position = int(round(80 * scale_x)), int(round(110 * scale_y))
        self.npc_dialogue_text.position = int(round(100 * scale_x)), int(round(90 * scale_y))

def npc_dialogue(self):
    for npc in self.npc_dialogues_dict:
        if distance(self.player_sprite.position, self.npc_dialogues_dict[npc]["position"]) < 15:
            self.npc_dialogue_text.color = 255, 255, 255, 255
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
                self.npc_dialogues_dict[npc]["actions"].pop("others")
                self.npc_show_dialogue = False
                self.can_move = True

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
                    self.npc_dialogue_name.text = action["name"]
                    self.npc_dialogue_text.text = action["content"]
                    self.npc_show_dialogue = True
                    action = action_list[self.npc_dialogue_index]
                else:
                    self.object_given = False
                    self.npc_dialogue_index = 0
                    self.npc_show_dialogue = False
                    self.can_move = True
                    break

def distance(pos1, pos2):
        return (((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2)) ** 0.5


if __name__ == "__main__":
    main.main()
