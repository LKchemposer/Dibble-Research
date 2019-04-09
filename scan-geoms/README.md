# Instructions

## Use in Windows

The "scan_geoms.py" is a Python script to extract converged geometries of a scan Gaussian output file (this script does not work with IRC output file ... yet) . To use the script in Windows,

1. Copy the "scan_geoms.py" file into the same folder as the ".log" Gaussian output scan file

2. Access the Windows command prompt: Start/Run, type "cmd", click "OK"

3. Make sure Python is installed, check by typing "python" in the command prompt (download at https://www.anaconda.com/distribution/#download-section)

4. Navigate to the folder where the files are located (https://www.digitalcitizen.life/command-prompt-how-use-basic-commands)

5. Copy and run each line:

   "C:\>set PATH=C:\Program Files\Python 3.7;%PATH%"

   "C:\>set PYTHONPATH=%PYTHONPATH%;C:\My_python_lib"

   "C:\>python"

6. Type "python scan_geoms.py input.log" (change "input.log" to the actual ".log" file)