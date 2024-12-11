from os import environ
from os.path import dirname as path_dirname, join as path_join

from src.utils import load_json_file


src_dir = path_dirname(__file__)
app_dir = path_dirname(src_dir)
env_file_path = path_join(app_dir, ".env")
model_requirements_file_path = path_join(app_dir, "modelRequirements.json")



TRITON_HTTP_URL = "http://lipikar.cse.iitd.ac.in:8020"
APP_MODE = 'DEVELOPMENT'
DEVLOPMENT_HOST = "0.0.0.0"
DEVLOPMENT_PORT = 8020

model_requirements_map = load_json_file(model_requirements_file_path)
print("model_requirements_map loaded")

# from os import environ
# from os.path import dirname as path_dirname, join as path_join

# from dotenv import load_dotenv


# APP_MODE = environ.get('APP_MODE', 'DEVELOPMENT')

# if APP_MODE == "DEVELOPMENT":
#     src_dir = path_dirname(__file__)
#     app_dir = path_dirname(src_dir)
#     env_file_path = path_join(app_dir, ".env")

#     load_dotenv()

# ORTHANC_BASE_URL = environ.get('ORTHANC_BASE_URL', None)
# TRITON_HTTP_URL = environ.get('TRITON_HTTP_URL', None)
# DEVLOPMENT_PORT = environ.get('DEVLOPMENT_PORT', None)

# if ORTHANC_BASE_URL is None:
#     raise RuntimeError(f"The environment variable ORTHANC_BASE_URL is not defined.")
# if TRITON_HTTP_URL is None:
#     raise RuntimeError(f"The environment variable TRITON_HTTP_URL is not defined.")
# if APP_MODE == "DEVELOPMENT" and DEVLOPMENT_PORT is None:
#     raise RuntimeError(f"The environment variable DEVLOPMENT_PORT is not defined.")

# if APP_MODE == "DEVELOPMENT":
#     DEVLOPMENT_PORT = int(DEVLOPMENT_PORT)