import os

# get the root folder

root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

os.environ["PYTHONPATH"] = os.path.join(root_dir, "src")

notebook_dir = os.path.join(root_dir,"notebooks")
os.system(f"jupyter lab --notebook-dir={notebook_dir}")
