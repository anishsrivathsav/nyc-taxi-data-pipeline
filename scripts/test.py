import os
from dotenv import load_dotenv

dot_env_path = os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..",'aws_credentials.env')))
print(dot_env_path)
# # # Get current file directory (e.g., scripts/)
# # current_dir = os.path.dirname(__file__)

# # # Go up one level to reach project root (../)
# # project_root = os.path.abspath(os.path.join(current_dir, ".."))

# # print(project_root)
# # # Build full path to the .env file in the root
# # dotenv_path = os.path.join(project_root, ".env")
# print(os.path.join(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
#     ".env"))
# load_dotenv(dotenv_path=os.path.join(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), "..",'aws_credentials.env')),
# ))
# aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
# aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
# region_name=os.getenv("AWS_DEFAULT_REGION")
# print(region_name)

