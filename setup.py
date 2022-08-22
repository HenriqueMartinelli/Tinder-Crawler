import sys
from cx_Freeze import setup, Executable


base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

executables = [
        Executable("main.py", base=base)
]

buildOptions = dict(
        packages = ['pandas', 'requests', 'logging', 'os', 'json', 'sys', 'datetime', 'logging.handlers'],
        includes = [],
        include_files = ['map.json', 'interesses.json'],
        excludes = []
)




setup(
    name = "Tinder bot",
    version = "2.0",
    description = "Crawler Tinder",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
