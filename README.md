# p8c
A simple utility made in Python for merging several Lua files which contain [PICO-8](https://www.lexaloffle.com/pico-8.php) code into one file.

## Installing dependencies
```python
pip install -r requirements.txt
```

## Usage
The specified directory must have a 'src' folder which includes all the source files to merge. The result will be stored in a new file under the specified directory, and it can also be copied directly to the clipboard for easier use in the PICO-8 program.
```python
p8c.py [-h] [-a AUTHOR] [-c] directory
```
