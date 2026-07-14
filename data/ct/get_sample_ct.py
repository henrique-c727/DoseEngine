# Code used to obtain an example DICOM file included in pydicom

from pathlib import Path
from shutil import copy2

from pydicom import examples


source_path = examples.get_path("ct")

target_path = Path("data") / "ct" / "CT_small.dcm"
target_path.parent.mkdir(parents=True, exist_ok=True)

copy2(source_path, target_path)

print(f"CT scan copied to: {target_path.resolve()}")