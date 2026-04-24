import main, arcade

npc_dialogues_dict = {
    "wizard": {
        "name": "Krabouille",
        "position": (None, None),
        "completed": False,
        "place": "castle",
        "actions": {
            "first_encounter": [
                {
                    "type": "dialogue",
                    "content": "Je suis Krabouille le sorcier."
                },
                {
                    "type": "dialogue",
                    "content": "..."
                },
                {
                    "type": "dialogue",
                    "content": "Quoi? Mon nom te fait rire?"
                },
                {
                    "type": "dialogue",
                    "content": "On va voir si tu vas rigoler encore longtemps."
                },
                {
                    "type": "dialogue",
                    "content": "J'ai kidnappé ta famille."
                },
                {
                    "type": "dialogue",
                    "content": "Si tu veux la revoir, ramène moi une nouvelle baguette magique qui se trouve dans le château."
                },
                {
                    "type": "target",
                    "position": (350, 205)
                },
                {
                    "type": "dialogue",
                    "content": "Donne moi la clé et j'ouvrirai la porte."
                },
                {
                    "type": "dialogue",
                    "content": "Va, et explore ce vaste monde, rencontre les personnages non joueurs!"
                },
                {
                    "type": "dialogue",
                    "content": "MOUAHAHAHA"
                }
            ],
            "others": [
                {
                    "type": "dialogue",
                    "content": "Donne-moi la clé, si tu l'as"
                },
                {
                    "type": "item_wait",
                    "id": "cle",
                    "name": "Intentional Game Design",
                    "content": "Vous donnez la clé. Vous pouvez désormais entrer dans le château.",
                    "item_given": "castle_doors"
                },
                {
                    "type": "dialogue",
                    "content": "Bonne chance, ramène moi ma baguette magique et tu reverras ta famille..."
                },
                {
                    "type": "finish",
                    "action": None
                }
            ],
                "completed": [
                    {
                        "type": "dialogue",
                        "content": "Ma baguette?"
                    },
                    {
                        "type": "item_wait",
                        "id": "baguette_magique",
                        "name": "Krabouille",
                        "content": "Bien. Voilà ta famille...",
                        "item_given": None
                    },
                    {
                        "type": "item_give",
                        "id": "family"
                    }
            ]
        }
    },
    "ghost": {
        "name": "Le fantôme",
        "position": (None, None),
        "completed": False,
        "place": "torch_trial",
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
                    "content": "Je suis désolé... Pour me faire pardonner je vais t'offrir une clé qui ouvre la porte du château."
                },{
                    "type": "dialogue",
                    "content": "En echange de quelque chose bien sûr! Une statue! Elle se trouve ici:"
                },
                {
                    "type": "target",
                    "position": (162, 104)
                },
                {
                    "type": "dialogue",
                    "content": "Par contre, il te faudra un briquet. Il me semble que le cactus en a un."
                }
            ],
            "others": [
                {
                    "type": "dialogue",
                    "content": "Rapporte-moi une statue."
                },
                {
                    "type": "item_wait",
                    "id": "statue",
                    "name": "Intentional Game Design",
                    "content": "Vous obtenez une clé! Vous pouvez ouvrir la porte du château.",
                    "item_given": "cle"
                },
                {
                    "type": "dialogue",
                    "content": "Prends la clé et laisse-moi reposer en paix."
                },
                {
                    "type": "finish",
                    "action": None
                }
            ],
                "completed": [
                    {
                        "type": "dialogue",
                        "content": "Tu es sourd? Laisse moi reposer en paix!"
                    }
                ]
        }
    },
    "cactus": {
        "name": "Cactus",
        "position": (None, None),
        "completed": False,
        "place": "maze_trial",
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
                        "content": "Bref, peux-tu me ramener une potion rouge? Il me la faut pour pouvoir me substenter des mes besoins."
                    },
                    {
                        "type": "dialogue",
                        "content": "Elle se trouve ici"
                    },
                    {
                        "type": "target",
                        "position": (168, 375)
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
                        "id": "potion_rouge",
                        "name": "Intentional Game Design",
                        "content": "Vous obtenez un briquet!",
                        "item_given": "briquet"
                    },
                    {
                        "type": "dialogue",
                        "content": "Merci! En échange, voilà mon briquet. Je n'en ai plus besoin."
                    },
                    {
                        "type": "finish",
                        "action": None
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
        "completed": False,
        "place": None,
        "actions": {
            "others": [
                {
                    "type": "dialogue",
                    "content": "Qu'est-ce qu'il y a dans le coffre? Demande à l'autre gardien, il te dira la vérité."
                },
                {
                    "type": "dialogue",
                    "content": "Va le voir."
                },
                {
                    "type": "finish",
                    "action": None
                }
            ],
            "completed": [
                {
                    "type": "dialogue",
                    "content": "Alors, qu'est-ce qu'il t'a dit?"
                }
            ]
        }
    },
    "guard_r": {
        "name": "Gardien",
        "position": (None, None),
        "completed": False,
        "place": None,
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
                },
                {
                    "type": "finish",
                    "action": None
                }
            ],
            "completed": [
                {
                    "type": "dialogue",
                    "content": "..."
                }
            ]
        }
    },
    "reset_guard": {
            "name": "Gardien",
            "position": (None, None),
            "completed": False,
            "place": None,
            "actions": {
                "others": [
                    {
                        "type": "dialogue",
                        "content": "..."
                    },
                    {
                        "type": "dialogue",
                        "content": "Quoi? Tu veux la baguette magique?"
                    },
                    {
                        "type": "dialogue",
                        "content": "Résous ce puzzle et le coffre s'ouvrira, avec la baguette magique dedans."
                    },
                    {
                        "type": "dialogue",
                        "content": "Replace les tuiles au bon endroit en les poussant pour relier le point et la croix."
                    },
                    {
                        "type": "dialogue",
                        "content": "Demande-moi si tu veux réinitialiser le puzzle."
                    },
                    {
                        "type": "finish",
                        "action": "show_puzzle"
                    }
                ],
                "completed": [
                    {
                        "type": "dialogue",
                        "content": "Veux-tu réinitialiser le puzzle?"
                    },
                    {
                        "type": "key_wait",
                        "content": "Appuyez sur Y pour réinitialiser.",
                        "id": arcade.key.Y,
                        "action": "puzzle_reset"
                    }
                ]
            }
        }
}


if __name__ == "__main__":
    main.main()
