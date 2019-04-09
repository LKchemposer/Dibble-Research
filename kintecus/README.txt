Instructions

To use the `analyze_nsa.py` file, create an input text file of three lines:

1. Line 1: path to the Excel file to be analyzed (case sensitive)
2. Line 2: species of interest (case insensitive)
   Options: `neutral` (default), `anions`, `cations`, `all`, `custom`
   If `custom`, give a list (space/tab-separated) of species (case insensitive)
3. Line 3: number of timestamps (case insensitive)
   Options: `last`, `all`, `int` (every `int`, 5 default)