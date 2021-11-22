# How to use

This library can be installed from PyPi:

    python3 -m pip install sootty

To use, run:

    sootty waveform.vcd > image.svg

with a vcs file to produce an svg waveform diagram. Optional arguments include:
- `-s | --start FORMULA` Specity the start of the window.
- `-e | --end FORMULA` Specify the end of the window.
- `-l | --length N` Specify the number of ticks in the window (mutually exclusive with `-e`).
- `-d` Display the output to the terminal (requires viu).
- `-w | --wires LIST` Comma-separated list of wires to include in the visualization (default to all wires).

## Examples:

Display all wires starting at time 4 and ending at wire `clk`'s tenth tick:

    sootty example/example3.vcd -s "time 4" -e "acc clk == const 10" -w "clk,rst_n,core.pc,core.inst" -d

Display wires `Data` and `D1` for 8 units of time starting when `Data` is equal to 20:

    sootty example/example1.vcd -l 8 -s "Data == const 20" -w "D1,Data" -d

How to run in python (using the repl):

    from sootty import WireTrace, Visualizer, Style

    # Create wiretrace object from vcd file:
    wiretrace = WireTrace.from_vcd_file("example/example1.vcd")

    # Convert wiretrace to svg:
    image = Visualizer(Style.Dark).to_svg(wiretrace, start=0, length=8)
    
    # Display to stdout:
    image.display()

# Dependencies:

- viu (`git clone https://github.com/atanunq/viu.git viu/ && cd viu/ && cargo install --path .`)
- rsvg-convert (`brew install librsvg`)
