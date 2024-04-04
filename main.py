import argparse
import atexit
import box
import sys
import yaml
from pathlib import Path

import logging.config
import logging.handlers

from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image


logger = logging.getLogger(__name__)

with open('configs/config.yml', 'r', encoding='utf8') as ymlfile:
    config = box.Box(yaml.safe_load(ymlfile))


def setup_logging():
    config_file = Path("configs/log_config.yml")
    with open(config_file) as log_file:
        log_config = yaml.safe_load(log_file)
    logging.config.dictConfig(log_config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def process_image(path_input: str, prompt: str = config.prompt.default_prompt) -> str:
    """Function which takes a path to an image and outputs a description of it based on a prompt.
    Default prompt = "Describe this image."

    :param prompt: Prompt.
    :param path_input: Image path.
    :returns: Description of the image.
    """
    if not Path(path_input).exists():
        logger.info(f"File not found")
        return

    model = AutoModelForCausalLM.from_pretrained(
        config.img_to_txt_model.model, trust_remote_code=True, revision=config.img_to_txt_model.revision
    )
    tokenizer = AutoTokenizer.from_pretrained(config.img_to_txt_model.model, revision=config.img_to_txt_model.revision)

    image = Image.open(f"{path_input}")
    enc_image = model.encode_image(image)

    image_description = model.answer_question(enc_image, prompt, tokenizer)

    logger.info(f"Using prompt: {prompt}. Image description is at follows: {image_description}")

    return image_description


def create_parser():
    parser = argparse.ArgumentParser(
        prog=f"{sys.argv[0]}",
        description="Describe content of an image",
    )
    parser.add_argument("-v", "--version", dest="version", action="version", version=f"%(prog)% {config.version}")

    parser.add_argument("-i", "--input", type=str, required=True, help="Path to the image", metavar="some image")

    parser.epilog = f"Bye"

    return parser


def main():
    setup_logging()
    parser = create_parser()
    args = parser.parse_args()

    if args.input:
        result = process_image(path_input=args.input)
        print(result)
    else:
        parser.print_help()


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    main()
