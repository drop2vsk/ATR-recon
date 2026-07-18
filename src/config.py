from pathlib import Path
import pandas as pd


class FileGather:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.resources_dir = self.root_dir / "resources"
        self.sources_file = self.resources_dir / "source_files"
        self.targets_file = self.resources_dir / "target_files"


obj = FileGather()
print(obj.root_dir)
print(obj.resources_dir)
print(obj.sources_file)
print(obj.targets_file)