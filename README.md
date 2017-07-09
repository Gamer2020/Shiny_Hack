Shiny Hack
================

This is HackMew's Shinyzer code for Emerald extracted and thrown into a project.

Requirements
====================

DevkitARM

Python 3.5

ARMIPS

Tutorial
====================

>Originally Posted by HackMew.

 
```
setvar 0x8003 0x2
```

>In the example above, the shiny counter would be set to 0x2. This means we could give two consequent Pokémon and both would be shiny. After the second Pokémon is given, the shiny counter would reach 0x0, so the Shiny Hack would be disabled. For wild Pokémon, it's better not to set the counter anything higher than 0x1 anyway. What about trainers? The main concept is similar. The difference is that we need two setvar commands. The first one will be used as the counter, and the second will be used to tell which Pokémon needs to be shiny. Let's say we're about to battle a trainer who has 5 Pokémon. We want the second and the third Pokémon to be shiny, for example. So we would first set variable 0x8003 like this:

```
setvar 0x8003 0xYY0X
```

>where X stands for the Pokémon amount the trainer has. In our example, X is 5 therefore:

```
setvar 0x8003 0xYY05
```

>Then we need to choose the shiny Pokémon. Starting from the very first Pokémon till the last one, we write 1 if the Pokémon needs to be shiny or 0 otherwise:

```
01100
```

>In case you didn't realize, that's just a custom binary bit field. After converting it to hex we get 0xC. So:

```
setvar 0x8003 0xC05
```

>That's it.

Credits
=================

HackMew