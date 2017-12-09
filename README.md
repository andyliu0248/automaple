# automaple

A simple automator for a ms private server.

Goals:
- Auto grinding in the whole map, specifically for 4th-job mage classes with global skills.
- Meso-looting before they expire.
- NPC drops to clear items in the backpack.
- Auto cc if other players are found.

Grander goals:
- Recharge pot if they run out.
- Re-login if dc'ed
- Re-spawn and return to grinding map if died.

Grandiest goals:
- Use [RL][RL] to build a bot for all classes, like [this][RL1], [this][RL2], and [this][RL3]
- Visual system to recognize mobs, drops, exp/mesos/drops gained
- Multi-bot grinding that can cover larger maps
- [Intercept game packets] so that no need to get vision working.

To-dos:
- (Check √) Image layer for screen capturing/pixel accessing in macOS. Thanks [StackOverflow]!
- Character info layer to read character info (max HP/MP, pot rate and keys, attack skill keys and delays, etc) from a text file.
- Character control layer to do the grinding. Perhaps on the highest level will use a subsumption architecture. Behaviors and their relative hierarchy: recast skill -> loot -> npc -> switch platform -> grind. Lower level need not use the same architecture.
- Geography class to specify properties of each geography, as well as possible transitions between them.
- Map-info layer that records (or reads from a file?) the geography of the current map.
    - If possible can also let the game bot to explore the map and figure out the geography by itself, but seems pretty hard given my current knowledge. (Update: actually implemented a function that outputs the position of the character continuously. Only need a working Geography class so that can record geography)
    - Four types of geography: floor, slope, rope, and door. A grinding- and moving-style is associated with each instance of geography. Each instance also records the pixel range in the mini map, so can know the current position of the player.


[StackOverflow]: http://neverfear.org/blog/view/156/OS_X_Screen_capture_from_Python_PyObjC
[Intercept game packets]: http://calebfenton.github.io/2017/05/27/monitoring-https-of-a-single-app-on-osx/
[RL]: https://www.wikiwand.com/en/Reinforcement_learning
[RL1]: https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/
[RL2]: www.cs.cmu.edu/~dchaplot/papers/aaai17_fps_games.pdf
[RL3]: https://medium.freecodecamp.org/how-to-build-an-ai-game-bot-using-openai-gym-and-universe-f2eb9bfbb40a?gi=1e80ca59e4a3
