import main

npc_dialogues_dict = {
    "wizard": {
        "name": "Sorcier",
        "position": (None, None),
        "nb_encounters": 0,
        "completed": False,
        "actions": [
            {
                "type": "dialogue",
                "content": "I'm the evil wizard"
            },
            {
                "type": "dialogue",
                "content": "I kidnapped your family, bring me 5€ if you want to see them again."
            }
        ]
    },
    "ghost": {
        "name": "Le fantôme",
        "position": (None, None),
        "nb_encounters": 0,
        "completed": False,
        "actions": [
            {
                "type": "dialogue",
                "content": "I'm the ghost!"
            },
            {
                "type": "target",
                "position": (240, 214)
            }
        ]
    },
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
                        "content": "Bref, peux-tu me ramener une potion rouge? J'en ai besoin pour me substenter des mes bsoins."
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
                        "name": "briquet"
                    },
                    {
                        "type": "dialogue",
                        "content": "Merci! En échange, voilà mon briquet. Je n'en ai plus besoin."
                    }
                ],
                "completed": [
                    "Merci pour la potion. Maintenant, va découvrir le monde!"
                ]
        }
    },
    "guard_l": {
        "name": "Gardien",
        "position": (None, None),
        "nb_encounters": 0,
        "completed": None,
        "actions": [
            {
                "type": "dialogue",
                "content": "Qu'est-ce qu'il y a dans le coffre? Demande à l'autre gardien, il te dira la vérité."
            },
            {
                "type": "dialogue",
                "content": "Va le voir."
            }
        ]
    },
    "guard_r": {
        "name": "Gardien",
        "position": (None, None),
        "nb_encounters": 0,
        "completed": None,
        "actions": [
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


if __name__ == "__main__":
    main.main()