# Description

Image-to-text. A tool that can be used to describe an image.

# Usage

```bash
usage: main.py [-h] [-v] -i some image

Describe content of an image.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i some image, --input some image
                        Path to the image

Bye
```
![Alt text](/resources/img_description.gif)


## The target image
'give_thanks.png' image can be found in the folder named 'resources'. 

![Alt text](/resources/give_thanks.png)

# Requirements

My setup is:

WIN 10 + nvidia drivers 522 + cuda 11.8 + WSL2 with Ubuntu 22.04 with cuda tools + python >=3.10

see "pyproject.toml"

```bash
poetry install
```
