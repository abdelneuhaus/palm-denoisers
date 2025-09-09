import subprocess
from pathlib import Path

care_venv = Path(__file__).parent.parent.parent / "venv_care" / "Scripts" / "python.exe"
print(care_venv)
sub1 = subprocess.run([care_venv, str(Path(__file__).parent / "data_processing.py")])
