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

- [x] Print and update the time
- [x] Transparent background and no window decorations for some platforms and window managers
- [x] Be moved by left clicking and dragging on the window
- [x] Be closed by right clicking on the window
- [x] Change the text color from the Settings/Text Color menu bar (Ctrl+C)
- [ ] Resize the text
- [ ] Change the text font
- [ ] Save font, size and color into a configuration file

**This piece of code has only been tested on an Ubuntu 20.04.1 LTS 64 bits with python 3.6.**
