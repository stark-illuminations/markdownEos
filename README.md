# markdownEos

A simple Python script to convert Markdown (.md) files to Eos cuelists.

The script finds a table in a markdown file, gets indexes for important cue information, and sends a series of OSC commands to Eos to record each cue and set things like timing, labels, notes, and scenes.

## Installation
This script requires Python-OSC to run. Find it [https://pypi.org/project/python-osc/](here).

## Usage
This is currently a command line tool, but a GUI isn't out of the question for future versions. 

**It is strongly recommended that you start with a blank cuelist/showfile, or or back up your showfile prior to running this script.**

Usage is as follows:

`$ python mdToEos.py -md [path/to/markdown/file] -ip [Console IP] -port [Console Port] -q ["Cue Column Header"]`

Optional arguments are:

    --i ["Timing Column Header"]
    --l ["Label Column Header"]
    --n ["Notes Column Header"]
    --s ["Scene Column Header"]
    --m ["Mark Column Header"]
    --b ["Block Column Header"]
    --f ["Follow Column Header"]
    --x ["Execute Column Header"]
