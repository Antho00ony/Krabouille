import main

npc_dialogues_dict = {
    "wizard": {
        "name": "Sorcier",
        "position": (None, None),
        "completed": False,
        "actions": {
            "others": [
                {
                    "type": "dialogue",
                    "content": "I'm the evil wizard"
                },
                {
                    "type": "dialogue",
                    "content": "I kidnapped your family, bring me 5€ if you want to see them again."
                }
            ]
        }
    },
    "ghost": {
        "name": "Le fantôme",
        "position": (None, None),
        "completed": False,
        "actions": {
            "first_encounter": [
                {
                    "type": "dialogue",
                    "content": "Bouh!"
                },
                {
                    "type": "dialogue",
                    "content": "Je sais que t'as eu peur!"
                },{
                    "type": "dialogue",
                    "content": "..."
                },{
                    "type": "dialogue",
                    "content": "Je suis désolé... Pour me faire pardonner je vais t'offrir ce A DEFINIR" #####################################
                },{
                    "type": "dialogue",
                    "content": "En echange de quelque chose bien sûr! Ça se trouve ici:"
                },
                {
                    "type": "target",
                    "position": (240, 214)
                },
                {
                    "type": "dialogue",
                    "content": "Je crois en toi!"
                }
            ]
        }
    },
    "cactus": {
        "name": "Cactus",
        "position": (None, None),
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
    },
    "guard_l": {
        "name": "Gardien",
        "position": (None, None),
        "completed": None,
        "actions": {
            "others": [
                {
                    "type": "dialogue",
                    "content": "Qu'est-ce qu'il y a dans le coffre? Demande à l'autre gardien, il te dira la vérité."
                },
                {
                    "type": "dialogue",
                    "content": "Va le voir."
                }
            ]
        }
    },
    "guard_r": {
        "name": "Gardien",
        "position": (None, None),
        "completed": None,
        "actions": {
            "others": [
                {
                    "type": "dialogue",
                    "content": "..."
                },
                {
                    "type": "dialogue",
                    "content": "Quoi?"
                },
                {
                    "type": "dialogue",
                    "content": "Qu'est-ce qu'il y a dans le coffre? Bah je sais pas vas-y toi. T'es le seul à pouvoir bouger."
                }
            ]
        }
    }
}


if __name__ == "__main__":
    main.main()
