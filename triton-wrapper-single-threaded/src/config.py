from json import dumps as json_dumps
from os import environ
from os.path import dirname as path_dirname, join as path_join

from dotenv import load_dotenv

from src.utils import load_json_file


APP_MODE = environ.get('APP_MODE', 'DEVELOPMENT')

if APP_MODE == "DEVELOPMENT":
    src_dir = path_dirname(__file__)
    app_dir = path_dirname(src_dir)
    env_file_path = path_join(app_dir, ".env")

    load_dotenv()

TRITON_HTTP_URL = environ.get('TRITON_HTTP_URL', None)
DEVLOPMENT_HOST = environ.get('DEVLOPMENT_HOST', None)
DEVLOPMENT_PORT = environ.get('DEVLOPMENT_PORT', None)

if TRITON_HTTP_URL is None:
    raise RuntimeError(f"The environment variable TRITON_HTTP_URL is not defined.")
if APP_MODE == "DEVELOPMENT":
    if DEVLOPMENT_HOST is None:
        raise RuntimeError(f"The environment variable DEVLOPMENT_HOST is not defined.")
    if DEVLOPMENT_PORT is None:
        raise RuntimeError(f"The environment variable DEVLOPMENT_PORT is not defined.")

    DEVLOPMENT_PORT = int(DEVLOPMENT_PORT)

print("Loaded environment variables:")
print(f"  APP_MODE = {APP_MODE}")
print(f"  TRITON_HTTP_URL = {TRITON_HTTP_URL}")
print(f"  DEVLOPMENT_HOST = {DEVLOPMENT_HOST}")
print(f"  DEVLOPMENT_PORT = {DEVLOPMENT_PORT}")
print("")

src_dir = path_dirname(__file__)
app_dir = path_dirname(src_dir)
env_file_path = path_join(app_dir, ".env")
model_requirements_file_path = path_join(app_dir, "modelRequirements.json")

print(f"Loading model requirements map from {model_requirements_file_path} ...")
model_requirements_map = load_json_file(model_requirements_file_path)
print("    ... model_requirements_map loaded:- ")
print(json_dumps(model_requirements_map, indent=4))
print("")
