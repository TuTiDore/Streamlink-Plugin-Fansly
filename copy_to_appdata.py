import os
import shutil

local_app_data = os.getenv('LOCALAPPDATA')
shutil.copyfile("fansly.py", rf"{local_app_data}\Programs\Streamlink\pkgs\streamlink\plugins\fansly.py")
