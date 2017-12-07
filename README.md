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
- Use RL to build a bot for all classes
- Visual system to recognize mobs, drops, exp/mesos/drops gained
- Multi-bot grinding that can cover larger maps
- Intercept game packets so that no need to get vision working.

To-dos:
- (Check √) Complete image layer for screen capturing/pixel accessing in macOS. Thanks SO!
- Design a character info layer to read character info (max HP/MP, pot rate and keys, attack skill keys and delays, etc) from a text file.
- Design a character control layer to do the grinding. Perhaps on the highest level will use a subsumption architecture. Behaviors and their relative hierarchy: recast skill -> loot -> npc -> switch platform -> grind. Lower level need not use the same architecture.
- Design a map-info layer that stores (or reads from a file?) the geography of the current map. If possible can also let the game bot to explore the map and figure out the geography by itself, but seems pretty hard given my current knowledge. Four types of geography: floor, slope, rope, and door. A grinding- and moving-style is associated with each instance of geography. Each instance also records the pixel range in the mini map, so can know the current position of the player.