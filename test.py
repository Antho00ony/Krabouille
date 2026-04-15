import arcade

def move_camera_to():
    pass 

npc_dialogues_dict_ = {
    "cactus": {
        "name": "Cactus",
        "position": (None, None),
        "nb_encounters": 0,
        "completed": False,
        "actions": {
                "first_encounter": [
                    {
                        "type": "dialogue",
                        "content": "Hey! Je suis le cactus!"
                    },
                    {
                        "type": "dialogue",
                        "content": "..."
                    },
                    {
                        "type": "dialogue",
                        "content": "Qu'est-ce qu'il y a? T'as jamais vu de cactus qui parle???"
                    },
                    {
                        "type": "dialogue",
                        "content": "NON??? Ces jeunes ne sont tellement pas cultivés..."
                    },
                    {
                        "type": "dialogue",
                        "content": "Bref, peux-tu me ramener une potion rouge? J'en ai besoin pour me substenter des mes besoins."
                    },
                    {
                        "type": "dialogue",
                        "content": "Elle se trouve ici"
                    },
                    {
                        "type": "target",
                        "position": (248, 485)
                    },
                    {
                        "type": "dialogue",
                        "content": "Je crois en toi!"
                    }
                ],
                "others": [
                    {
                        "type": "dialogue",
                        "content": "Rapporte-moi une potion rouge."
                    },
                    {
                        "type": "item_wait",
                        "name": "potion_rouge"
                    },
                    {
                        "type": "dialogue",
                        "content": "Merci! En échange, voilà mon briquet. Je n'en ai plus besoin."
                    }
                ],
                "completed": [
                    {
                        "type": "dialogue",
                        "content": "Merci pour la potion. Maintenant, va découvrir le monde!"
                    }
                ]
        }
    }
}

class Temp(arcade.Window):
    def __init__(self):
        super().__init__(800, 450, "TITLE", fullscreen=False, vsync=True)
        self.cam_mode = "player"   # "player" ou "target"
        self.cam_target = (0.0, 0.0)

        self.npc_dialogues_dict = npc_dialogues_dict_

        self.npc_dialogue_name = arcade.Text("Name", 80, 110, arcade.color.WHITE, 48, font_name="Kenney Pixel")
        self.npc_dialogue_text = arcade.Text("Dialogue", 100, 90, arcade.color.WHITE, 16, font_name="Kenney Pixel")
        self.npc_show_dialogue = False

        self.npc_dialogue_index = 0

        self.aaaaaaa = False

        self.inventory = []
        self.object_given = False

    def on_update(self, delta_time):
        pass

    def a(self):
        for npc in self.npc_dialogues_dict:
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
                break
            
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


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.D:
            self.inventory.append("potion_rouge")
        if symbol == arcade.key.SPACE:
            self.a()






window = Temp()
arcade.run()

window.a()
