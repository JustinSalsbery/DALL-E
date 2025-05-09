#! python3

import sys
import argparse
import base64

from openai import OpenAI
from PIL import Image
from io import BytesIO


# simplifies the default help format
class CustomHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        pass

    def _format_action_invocation(self, action):
        if action.option_strings:
            return ', '.join(action.option_strings)
        return super()._format_action_invocation(action)


# set up argument parser
parser = argparse.ArgumentParser(description="generate an image using DALL-E", 
                                 formatter_class=CustomHelpFormatter)

parser.add_argument("prompt", nargs="?",
                    help="image prompt, e.g., 'A horse on the moon.'")
parser.add_argument("-v", "--version", action="version", version='%(prog)s 1.2.1', 
                    help="show version number and exit")
parser.add_argument("-s", "--size", choices=["default", "wide", "tall"], default="default", 
                    help="{default, wide, tall} aspect ratio")
parser.add_argument("-q", "--quality", choices=["standard", "hd"], default="standard", 
                    help="{standard, hd} detailing")
parser.add_argument("-t", "--type", choices=["natural", "vivid"], default="vivid", 
                    help="{natural, vivid} style")

# parse command line arguments
args = parser.parse_args()

if not sys.stdin.isatty():
    args.prompt = sys.stdin.read()

# check if prompt is provided
if len(sys.argv) == 1 and args.prompt is None:
    print("imagine --help\n")
    print('examples:')
    print('  imagine "A horse on the moon."')
    print('  imagine "$(chat \'Write a prompt for DALL-E.\')"')
    sys.exit(0)

# map size arguments to actual dimensions
size_mapping = {
    "default": "1024x1024",
    "wide": "1792x1024",
    "tall": "1024x1792"
}

size = size_mapping[args.size]

# generate image
openai = OpenAI()
response = openai.images.generate(
    model="dall-e-3",
    response_format="b64_json",
    prompt=args.prompt,
    quality=args.quality,
    style=args.type,
    size=size
).data[0].b64_json

# decode the Base64 image and open it as a .png file
photo = base64.b64decode(response)
Image.open(BytesIO(photo)).show()
