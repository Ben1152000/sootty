# Sootty

Sootty is a graphical command-line tool for visualizing waveforms from hardware simulations, as a substitute for waveform visualizers like Verdi and GTKWave. It is designed with a focus on being lightweight and easy to use, and takes advantage of modern terminals’ capabilities to provide a clean graphical display. Current features include:
- Customizable display style
- Search and highlight events using a simple query language

And here's an example of how sootty can be used directly from the terminal:

<img width="979" alt="Screenshot of sootty in action" src="https://raw.githubusercontent.com/Ben1152000/sootty/master/image/screenshot.png">

## Getting Started

1. Install sootty using pip:

```bash
pip install sootty
```

2. Display a waveform file to the terminal:

```bash
sootty "waveform.vcd" -o > image.svg
```

Optional arguments include:
- `-s | --start FORMULA` Specify the start of the window.
- `-e | --end FORMULA` Specify the end of the window.
- `-l | --length N` Specify the number of ticks in the window (mutually exclusive with `-e`).
- `-o | --output` Print svg data to `stdout` rather than display on terminal.
- `-w | --wires LIST` Comma-separated list of wires to include in the visualization (default to all wires).
- `-b | --break FORMULA` Specify the formula for the points in time to be highlighted.
- `-r | --radix N` Display values in radix N (default 10).
- `-S | --save SAVENAME` Saves current query for future reuse.
- `-R | --reload SAVENAME` Loads a saved query. Requires query name as string.
- `--btable` Print the wire value table at breakpoints to `stdout` (`-b` is required).
- `-p` User parameter for starting time window, ending time window and visible wires to generate waveform

*Note: For more detailed information on the query language, check out [syntax.md](syntax.md)

### Examples

Below are some more examples  that take advantage of some of the features sootty has to offer:

- Display all wires starting at time 4 and ending at wire `clk`'s tenth tick:

```bash
sootty "example/example3.vcd" -s "time 4" -e "acc clk == const 10" -w "clk,rst_n,pc,inst"
```

- Display wires `Data` and `D1` for 8 units of time starting when `Data` is equal to 20:

```bash
sootty "example/example1.vcd" -l 8 -s "Data == const 20" -w "D1,Data"
```

- Saving a query for future use:

```bash
sootty "example/example2.vcd" -s "rdata && wdata == const 22" -l 10 -w "rdata, wdata" -S "save.txt"
```

- Reloading a saved query:

```bash
sootty -R "save.txt"
```

- Add breakpoints at time 9, 11, and 16 - 17 and print wire values at breakpoints:

```bash
sootty "example/example5.evcd" -b "time 9 || time 11 || after time 15 && before time 18" --btable
```

### Running with python

Sootty can also be run from within a python program:

```python
from sootty import WireTrace, Visualizer, Style
from sootty.utils import evcd2vcd

# Create wiretrace object from vcd file:
wiretrace = WireTrace.from_vcd_file("example/example1.vcd")

# Convert wiretrace to svg:
image = Visualizer(Style.Dark).to_svg(wiretrace, start=0, length=8)

# Display to stdout:
image.display()

# Manually convert EVCD file to VCD file:
with open('myevcd.evcd', 'rb') as evcd_stream:
    vcd_reader = evcd2vcd(evcd_stream)
    with open('myvcd.vcd', 'wb') as vcd_stream:
        vcd_stream.write(vcd_reader.read())
```

*Note: You can view and modify the save files for the queries in the `~/.config/sootty/save` directory.*

## Dependencies

As of the current release, Sootty can only display images in certain terminals with builtin graphics support. This currently includes the following terminal replacements:

- [iTerm2](https://iterm2.com/)
- [kitty](https://sw.kovidgoyal.net/kitty/)

The following external dependencies are also needed to properly display images within the terminal:

- [viu](https://github.com/atanunq/viu)

  ```bash
  # From source (rust package manager)
  cargo install viu
  # MacOS
  brew install viu
  # Arch Linux
  pacman -S viu
  ```
- rsvg-convert
  ```bash
  # Ubuntu
  apt install librsvg2-bin
  # MacOS
  brew install librsvg
  ```

## Contributing

If you are interested in contributing to this project, feel free to take a look at the existing issues and submit a PR. Beginners are encouraged to focus on issues with the "good first issue" label. This project has also been involved with Google Summer of Code through the [FOSSi Foundation](https://www.fossi-foundation.org/). Check out our project idea for GSoC '23: https://www.fossi-foundation.org/gsoc23-ideas#enhancing-the-sootty-terminal-based-graphical-waveform-viewer
