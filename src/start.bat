set PYTHONPATH=%CD%
if EXIST installed (
    start pythonw main.py
    exit
) else (
    start python main.py
)