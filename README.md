# How to use

The program can be installed by running the `install` bash script (optionally include `--user` to install locally)

Run:

    sootty waveform.vcs > image.svg

with a vcs file to produce an svg waveform diagram. Optional arguments include:
- `-s | --start FORMULA` Specity the start of the window.
- `-e | --end FORMULA` Specify the end of the window.
- `-l | --length N` Specify the number of ticks in the window (mutually exclusive with `-e`).
- `-d` Display the output to the terminal (requires viu).
# Dependencies:

- viu (`git clone https://github.com/atanunq/viu.git viu/ && cd viu/ && cargo install --path .`)
- pyDigitalWaveTools (`git clone https://github.com/Nic30/pyDigitalWaveTools.git pyDigitalWaveTools/ && cd pyDigitalWaveTools/ && python3 -m pip install .`)
- rsvg-convert (`brew install librsvg`)