# Instructions

## Input file

To use the "analyze_nsa.py" file, create an input text file of exactly three lines:

1. **Line 1:** path to the Excel file to be analyzed (case sensitive)

2. **Line 2:** species of interest (case insensitive)

   Options: "neutral" (default), "anions", "cations", "all", "custom"
   If "custom" is used, give a list (space/tab-separated) of species (case insensitive)

3. **Line 3:** number of timestamps (case insensitive)
   Options: "last", "all", `int`  (every `int` timestamps, 5 default)

See [sample input file](./input.txt) for example.

## Use in Windows

1. Create the input file (can be in ".txt" or any text file extension)
2. Copy the "scan_geoms.py" file into the same folder as the input file
3. Access the Windows command prompt: Start/Run, type "cmd", click "OK"
4. Make sure Python is installed, check by typing "python" in the command prompt (download at https://www.anaconda.com/distribution/#download-section)
5. Navigate to the folder where the files are located (https://www.digitalcitizen.life/command-prompt-how-use-basic-commands)
6. Copy and run each line:
   "C:\>set PATH=C:\Program Files\Python 3.7;%PATH%"
   "C:\>set PYTHONPATH=%PYTHONPATH%;C:\My_python_lib"
   "C:\>python"
7. Type "python analyze_nsa.py input.txt" (change "input.txt" to the actual input filename)