from cx_Freeze import setup, Executable
import sys

build_exe_options = {
    "packages": ["tkinter", "pygame", "threading", "PIL"],
    "include_files": [],
    "excludes": ["test"],
    "include_msvcr": True,
    "optimize": 2,
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Таймер обратного отсчета",
    version="2.0",
    description="Таймер обратного отсчета",
    options={"build_exe": build_exe_options},
    executables=[Executable("contdown_timer.py", 
                          base=base, 
                          icon="timer_icon.ico",
                          target_name="ContdownTimer.exe")]
)