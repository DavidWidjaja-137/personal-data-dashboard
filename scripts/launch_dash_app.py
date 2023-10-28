import os

# get the root folder

root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

os.environ["PYTHONPATH"] = os.path.join(root_dir, "src")

app_dir = os.path.join(root_dir, "src", "dash_app")

os.chdir(app_dir)

os.system(f"python index.py")