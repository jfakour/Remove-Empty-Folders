# Remove Empty Folders v0.1

This script will help you clean your file system by collecting a list of empty folders from a root directory and removing them.
Tested on Windows. Mac or Linux has not been tested (yet).

## Usage(s)

The script can run in:

### headless mode (arg -hl)

In headless mode the script will recursively search for empty folders and remove them without a prompt.

``` python3 ./find_empty_folders -hl -dir path_to_directory_you_want_cleaned ```

### interactive mode

In normal mode the script will search for empty folders, present a list of directories about to removed, and ask for confirmation (to remove all items in the list)

``` python3 ./find_empty_folders -dir path_to_directory_you_want_cleaned ```

## Notes

If the -dir argument is not set, or the set directory cannot be found, the script will ask for a valid directory and switch to interactive mode.