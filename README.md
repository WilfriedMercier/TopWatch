# TopWatch

## Description
A small digital clock which remains on top of other applications with a transparent background (and no window decorations with some decoration managers) built with pyQt.

# What is required to run it ?

The code is raw python except for pyQt5 which needs to be installed. You can get it with pip as follows

```bash
wilfried:~$ pip install PyQt5
```

# What does it do ?

Show time. Here is a list of what it currently does:

- [x] Show and update time every second
- [x] Transparent background and no window decorations for Linux and Mac platforms
- [x] Can be moved by left clicking and dragging the window
- [x] Can be closed by right clicking on the window
- [x] Change the text color from the Settings/Text Color menu bar (Ctrl+C)
- [x] Resize the text using the UP and DOWN arrows
- [x] Change the text font from the Settings/Change font menu bar (Ctrl+F)
- [x] Save settings into a configuration file loaded as default at next startup
- [x] Reset settings from the menu
- [x] Setup a "hide and blink sequence" (more info below) with Ctrl+b

# "Hide and blink" sequence

Instead of having the time always on screen, it is possible to hide the clock and have it blink a given amount of times at regular intervals. This can be useful if one wants to be reminded of the time say every 15 min without having constantly a clock on top of his windows, or to have a silent timer for instance.

![Blink setup](/blink_setup_example.png)

Three parameters can be set up:

- Period in format hour:min:sec. That is the amount of time the clock is hidden between two blinking sequences.
- Duration in format ms. That is the duration of a single blink.
- Blink number. That is the number of blinks in a blinking sequence.

**This piece of code has been tested on an Ubuntu 20.04.1 LTS 64 bits machine with python 3.6. The code should work on MAC OS as well, but bugs may be encountered.**
