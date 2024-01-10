from lib.config import get_config
import argparse

def get_args():
    default_tags = get_config()["text_gen"]["default_tags"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--tags", default=default_tags, help="comma separated tags for generation prompt")
    parser.add_argument("--mode", default="gen_only", choices=["gen_only","gen_and_upload"])
    args, unknown = parser.parse_known_args()
    return args

# TODO: add a scheduled upload, can include in youtube API payload
