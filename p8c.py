#!/usr/bin/env python3
# coding: utf-8

# p8c / pico-8 compiler by luisfl.me


import argparse
import clipboard
import os
import sys
import time


def print_welcome():
    print("\n\033[1m----------------------------------\033[0m")
    print("\033[1mp8c / pico-8 compiler by luisfl.me\033[0m")
    print("\033[1m----------------------------------\033[0m\n")


def print_error(message):
    print("\033[91m\033[1mError: " + message + "\033[0m\n")


def compose_header(directory_name, author):
    file_header = ""
    file_header += f"\n-- {directory_name}"
    if author: file_header += f"\n-- by {author}"
    file_header += "\n-- Compiled: " + time.strftime("%d/%m/%y %H:%M:%S") + "\n"
    return file_header


def main(args):
    print_welcome()
    directory = args.directory + "/" if args.directory[-1] != "/" else ""
    author = args.author

    # Change current working directory to the specified one
    try:
        os.chdir(directory)
    except:
        print_error("directory does not exist")
        sys.exit(1)

    # Compose a header for the new file result of the merge process
    directory_name = os.path.basename(os.path.dirname(directory))
    new_file_header = compose_header(directory_name, author)
    
    # Initialize a variable for holding the new file's content
    new_file_content = ""
    new_file_content += new_file_header

    # Look for files inside the "src" folder in the specified directory
    print(f"Retrieving source files from \"{directory_name}/src\"...")
    files = []
    try:
        files = os.listdir("./src")
        files = list(filter(lambda f: f[-4:] == ".lua", files))
        files.sort()
    except:
        print_error(f"\"src\" folder not found inside \"{directory}\"")
        sys.exit(1)

    # Exit if there are no source files
    if len(files) <= 0:
        print_error(f"no source files found in \"{directory_name}/src\"")
        sys.exit(1)

    # Retrieve each file's content and merge it
    for file in files:
        print(f"Merging \"{file}\" file...")
        new_file_content += f"\n-- {file}\n"
        with open("./src/" + file, "r") as open_file:
            new_file_content += "\n" + open_file.read() + "\n"

    # Write the result of the merge process to the new file
    print(f"Creating new \"{directory_name}.lua\" file...")
    with open(directory_name + ".lua", "w") as new_file:
        new_file.write(new_file_content)
        print(f"\n\033[92m\033[1mMerged all source files into \"{directory_name}.lua\" successfully!\033[0m")

    # Copy result to the clipboard if requested
    if args.clipboard:
        clipboard.copy(new_file_content)
        print("Copied the new file's content to the clipboard.")

    print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "p8c.py", description = "An utility that merges several Lua files which contain PICO-8 code into one file")
    parser.add_argument("directory", type = str, help = "directory path in which the \"src\" folder that contains the Lua files is stored")
    parser.add_argument("-a", "--author", help = "author(s) of the files", type = str)
    parser.add_argument("-c", "--clipboard", help = "copy the new file's content to the clipboard", action = "store_true")
    args = parser.parse_args()
    main(args)
