# flying-robots, a (kind of) three-dimensional clone of the classing BSD Robots game.

flying-robots is a simple game inspired by the classic [BSD Robots](https://man.openbsd.org/robots) game. You are
being chased by robots, and the only way to kill them is to make them crash. Whereas in the classic Robots game you
could move along the x and y axes, flying-robots allows you to also move along the z axis (ie, perpendicular to the
screen). While movement is in three dimensions, the 2D view of the classic robots game is retained, with the player able
to view one z-level at a time.

It is written in Python 3. It has a cross-platform graphical interface, written using Tkinter, and a textual interface,
which uses the curses library (Unix-like systems only).

## Dependencies

The game depends on Python 3 and Tk. On Unix-like systems, you can use the curses interface if you don't have Tk
installed, or if you would rather play in the terminal.

## Installation

You can clone the git repository and install using `pip`.

```bash
git clone https://github.com/bunburya/flying-robots.git
cd flying-robots
pip install -e .
```

If you use ArchLinux, you can also install the [`flying-robots`](https://aur.archlinux.org/packages/flying-robots/)
package from the AUR. If you enjoy the game, please consider voting for it on the AUR page.

## Options

You can customise the way flying-robots runs by providing one or more command line options to it. Run
`flying-robots --help` to see all available options. 

## License

flying-robots is published under the permissive MIT license.
