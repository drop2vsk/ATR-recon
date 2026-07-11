from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SRC_FOLDER = BASE_DIR / "src"
RESOURCE_FOLDER = BASE_DIR / "resouce"
SOURCE_FILE = RESOURCE_FOLDER / "source/source_data.xlsx"
TARGET_FILE = RESOURCE_FOLDER / "target/target_data.xlsx"

DRIVER_CONFIG = RESOURCE_FOLDER / "driverconfig.xlsx"

print(BASE_DIR)
print(SRC_FOLDER)
print(RESOURCE_FOLDER)
print(SOURCE_FILE)
print(TARGET_FILE)
print(DRIVER_CONFIG)
