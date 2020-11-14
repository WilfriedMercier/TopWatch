# TopWatch

## Description
A small analog clock which remains on top of other applications with a transparent background (and no window decorations with some decoration managers) built with pyQt.

# What is required to run it ?

The code is default python except for pyQt5 which needs to be installed. You can get it with pip as follows

```bash
wilfried:~$ pip install PyQt5
```

# What does it do ?

Not much... This is my first program with pyQt, coming from tkinter applications, so it is very simple. Here is a list of what is does (not) currently do:

- [x] Show and update the time
- [x] Transparent background and no window decorations for Linux and Mac platforms
- [x] Be moved by left clicking and dragging on the window
- [x] Be closed by right clicking on the window
- [x] Change the text color from the Settings/Text Color menu bar (Ctrl+C)
- [x] Resize the text using the UP and DOWN arrows
- [x] Change the text font from the Settings/Change font menu bar (Ctrl+F)
- [x] Save font  and color into a configuration file
- [x] Reset the font and color from the menu

**This piece of code has been tested on an Ubuntu 20.04.1 LTS 64 bits machine with python 3.6. The code should work on MAC OS as well, but bugs may be encountered.**
