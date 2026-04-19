import arcade

import functions, levels, main

def key_press(self, key, modifiers):
    if key == arcade.key.F:
        self.set_fullscreen(not self.fullscreen)
        functions.change_cam_limits(self)
    if key == arcade.key.H:
        self.show_hitboxes = not self.show_hitboxes
    if key == arcade.key.B:
        print(self.player_sprite.position)
        self.places_allowed.add("maze_trial")
        self.places_allowed.add("torch_trial")
        print(self.places_allowed)
        self.inventory.add("potion_rouge")
        self.inventory.add("briquet")
        self.inventory.add("statue")
        self.inventory.add("cle")
        print(self.inventory)


    # NPCs & level change
    if key == arcade.key.SPACE:
        for entrance, data in list(self.level_changes_dict.items()):
            if entrance in self.places_allowed and functions.distance(self.player_sprite.position, data["position"]) <= 15:
                if entrance == "map_1":
                    target = "map"
                    self.exit = "torch_trial"
                elif entrance != "castle":
                    target = entrance
                    self.exit = self.level_name
                    self.npc_show_dialogue = False
                    levels.load_level(self, target)
                    self.level_name = target
                    self.player_sprite.position = (self.spawn_x, self.spawn_y)
                    break
            elif functions.distance(self.player_sprite.position, data["position"]) <= 15:
                self.npc_dialogue_text.align = "center"
                self.npc_dialogue_name.text = ""
                self.npc_dialogue_text.text = "Vous n'avez pas encore accès à cette zone, parlez d'abord au personnage associé.‎"
                self.npc_dialogue_text.color = 0, 0, 0, 255
                self.npc_show_dialogue = True

        functions.npc_dialogue(self)

        if functions.distance(self.player_sprite.position, self.chest_sprite.position) < 15:
            if self.can_move and self.chest_sprite.cur_texture_index == 0:
                self.chest_sprite.set_texture(1)
                self.can_move = False
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.npc_dialogue_name.text = "Nouvel objet!"
                if self.level_name == "maze_trial":
                    self.npc_dialogue_text.text = "Vous obtenez une potion rouge. Attendez, ne serait-ce pas du sang???"
                    self.inventory.add("potion_rouge")
                elif self.level_name == "torch_trial":
                    self.npc_dialogue_text.text = "Vous obtenez une statue. C'est lourd."
                    self.inventory.add("statue")
                self.npc_show_dialogue = True
                self.cam_mode = "player"
            else:
                self.npc_show_dialogue = False
                self.can_move = self.can_move = True

        
        if self.level_name == "torch_trial":
            near_torch = (
                functions.distance(self.player_sprite.position, (self.torch_sprite1.position[0], self.torch_sprite1.position[1] - 16)) < 15
                or functions.distance(self.player_sprite.position, (self.torch_sprite2.position[0], self.torch_sprite2.position[1] - 16)) < 15
                or functions.distance(self.player_sprite.position, (self.torch_sprite3.position[0], self.torch_sprite3.position[1] - 16)) < 15
            )

            if "briquet" in self.inventory:
                if near_torch:
                    if functions.distance(self.player_sprite.position, (self.torch_sprite1.position[0], self.torch_sprite1.position[1] - 16))  < 15 and self.torch_sprite1.cur_texture_index == 0:
                        self.torch_sprite1.set_texture(1)
                    if functions.distance(self.player_sprite.position, (self.torch_sprite2.position[0], self.torch_sprite2.position[1] - 16))  < 15 and self.torch_sprite2.cur_texture_index == 0:
                        self.torch_sprite2.set_texture(1)
                    if functions.distance(self.player_sprite.position, (self.torch_sprite3.position[0], self.torch_sprite3.position[1] - 16))  < 15 and self.torch_sprite3.cur_texture_index == 0:
                        self.torch_sprite3.set_texture(1)
                    if self.torch_sprite1.cur_texture_index == 1 and self.torch_sprite2.cur_texture_index == 1 and self.torch_sprite3.cur_texture_index == 1:
                        self.doors_sprite.set_texture(1)
            elif near_torch:
                self.npc_dialogue_text.align = "center"
                self.npc_dialogue_name.text = ""
                self.npc_dialogue_text.text = "Il vous faut un briquet.‎"
                self.npc_dialogue_text.color = 0, 0, 0, 255
                self.npc_show_dialogue = True

    if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
        if self.level_name != "torch_trial":
            if self.keys == set():
                self.keys.add(key)
                if key == arcade.key.UP: self.player_sprite.state = "back" 
                if key == arcade.key.DOWN: self.player_sprite.state = "front"
                if key == arcade.key.LEFT: self.player_sprite.state = "left" 
                if key == arcade.key.RIGHT: self.player_sprite.state = "right"
        else:
            self.keys.add(key)
            if key == arcade.key.LEFT: self.player_sprite.state = "left" 
            if key == arcade.key.RIGHT: self.player_sprite.state = "right"
            if key == arcade.key.UP and self.climb_ladder: self.player_sprite.state = "back"
        self.moving = True



if __name__ == "__main__":
    main.main()