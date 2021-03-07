import os
import sys
import platform
import ctypes
import getopt
from ctypes import windll, cdll
import random
import time
import json

legal_image_suffix = ['png', 'jpg', 'jpeg', 'bmp']


# why i comment those lines
# there's no such kind of image in my image sets.
folder_name_for_config = {
    # "dawn": "dawn",
    # "morning": "morning",
    "forenoon": "forenoon",
    "noon": "noon",
    "afternoon": "afternoon",
    "dusk": "dusk",
    "night": "night",
}

# https://code.activestate.com/recipes/460509/


class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_ulong),
        ('top', ctypes.c_ulong),
        ('right', ctypes.c_ulong),
        ('bottom', ctypes.c_ulong)
    ]

    def dump(self):
        return map(int, (self.left, self.top, self.right, self.bottom))


def get_monitors():
    retval = []
    CBFUNC = ctypes.WINFUNCTYPE(
        ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)

    def cb(hMonitor, hdcMonitor, lprcMonitor, dwData):
        r = lprcMonitor.contents
        print("cb: %s %s %s %s %s %s %s %s" % (hMonitor, type(hMonitor), hdcMonitor, type(
            hdcMonitor), lprcMonitor, type(lprcMonitor), dwData, type(dwData)))
        data = [hMonitor]
        data.append(r.dump())
        retval.append(data)
        return 1
    cbfunc = CBFUNC(cb)
    temp = windll.user32.EnumDisplayMonitors(0, 0, cbfunc, 0)
    return retval


def show_help():
    print('Usage: desktop_background_shuffler.py -p <base_directory_path> -t <slideshow_time> -m <work_mode> -c <config_file_path>')
    print('   or: desktop_background_shuffler.py --PATH=<base_directory_path> --TIME=<slideshow_time> --MODE=<work_mode> --CONFIG=<config_file_path>')
    print('If working in multi-monitor mode, a config file is needed.')


def check_base_folder_availability(path: str) -> bool:
    folder_list = os.listdir(os.path.normpath(path))
    for key in folder_name_for_config:
        temp_folder_name = folder_name_for_config[key]
        if temp_folder_name not in folder_list:
            print("Missing subfolder " + '"' + temp_folder_name + '".')
            return False
        subfolder_list = os.listdir(
            os.path.normpath(path + '/' + temp_folder_name))
        if len(subfolder_list) < 1:
            print("No file in subfolder " + '"' + temp_folder_name + '".')
            return False
        vaild_image_count = 0
        for name in subfolder_list:
            image_name_splited = name.split(".")
            suffix = image_name_splited[-1].lower()
            if suffix in legal_image_suffix and len(image_name_splited) >= 2:
                vaild_image_count += 1
                continue
        if vaild_image_count == 0:
            print("No vaild image in subfolder " + '"' + temp_folder_name +
                  '". If you believe this is an error, please update "legal_image_suffix" in script.')
            return False
    return True

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfow
# function prototype:
# BOOL SystemParametersInfoW(
#   UINT  uiAction,
#   UINT  uiParam,
#   PVOID pvParam,
#   UINT  fWinIni
# );
# We will use these:
# uiAction                  uiParam     pvParam                 fWinIni
# SPI_SETDESKWALLPAPER      0           Path(for this call)     SPIF_SENDWININICHANGE
# 0x0014                    0           image_path              0x0002
# **reminder**
# fWinIni seems can be anything, at least from 0x00 to 0x03.


def change_desktop_background_with_image(image_path: str):
    SPI_SETDESKWALLPAPER = 0x0014
    SPIF_SENDWININICHANGE = 0x0002
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, SPIF_SENDWININICHANGE)


def find_available_image_within_path(folder_path: str) -> str:
    file_list = os.listdir(os.path.normpath(folder_path))
    while True:
        image_name = random.choice(file_list)
        print("found file: " + image_name)
        image_name_splited = image_name.split(".")
        suffix = image_name_splited[-1].lower()
        if suffix in legal_image_suffix and len(image_name_splited) >= 2:
            image_file_relative_path = image_name
            print("found valid image: " + image_name)
            break
    image_path = os.path.normpath(
        folder_path + "/" + image_file_relative_path)
    return image_path


def get_image_path_with_current_time_and_image_base_directory(image_base_directory: str) -> str:
    year, month, day, hour, minute = map(
        int, time.strftime("%Y %m %d %H %M").split())
    current_hour = hour
    current_min = minute
    current_time = 100 * hour + minute
    print("Time: " + str(current_time))
    if current_time < 600:
        return find_available_image_within_path(
            image_base_directory + "/" + folder_name_for_config["night"])
    if current_time < 1120:
        return find_available_image_within_path(
            image_base_directory + "/" + folder_name_for_config["forenoon"])
    if current_time < 1330:
        return find_available_image_within_path(
            image_base_directory + "/" + folder_name_for_config["noon"])
    if current_time < 1700:
        return find_available_image_within_path(
            image_base_directory + "/" + folder_name_for_config["afternoon"])
    if current_time < 1930:
        return find_available_image_within_path(
            image_base_directory + "/" + folder_name_for_config["dusk"])
    else:
        return find_available_image_within_path(
            image_base_directory + "/" + folder_name_for_config["night"])


def single_monitor_loop(image_base_directory: str, slideshow_time: int):
    if image_base_directory == "":
        print("Missing options.")
        show_help()
        exit(3)

    if not check_base_folder_availability(image_base_directory):
        print("Base directory doesn't meet requirements.")
        exit(4)

    folder_list = os.listdir(image_base_directory)
    while True:
        image_path = get_image_path_with_current_time_and_image_base_directory(
            image_base_directory)
        change_desktop_background_with_image(image_path)
        time.sleep(slideshow_time)


def multiple_monitor_loop(config_file_path: str, slideshow_time: int):
    with open(config_file_path, "r", encoding="utf-8") as raw_config:
        config_dict = json.loads(raw_config.read())
    lib = cdll.LoadLibrary(config_dict["dll_path"])
    monitor_count = len(get_monitors())
    monitor_specified_base_directory = []
    print(f"monitor count: {monitor_count}")
    image_base_directory = config_dict["image_base_directory"]
    if not check_base_folder_availability(image_base_directory):
        print("Base directory doesn't meet requirements.")
        exit(4)
    for monitor_index in range(0, monitor_count):
        temp = ""
        try:
            temp = config_dict["per_monitor_directory"][f"monitor_{monitor_index}"]
            if not check_base_folder_availability(temp):
                print(
                    f"Per monitor's (#{monitor_index}) base directory doesn't meet requirements. Falling back to default.")
                temp = config_dict["image_base_directory"]
        except KeyError:
            print(
                f"Per monitor's (#{monitor_index}) base directory not found. Falling back to default.")
            temp = config_dict["image_base_directory"]
        monitor_specified_base_directory.append(temp)

    while True:
        for monitor_index in range(0, monitor_count):
            image_path = get_image_path_with_current_time_and_image_base_directory(
                monitor_specified_base_directory[monitor_index])
            lib.SetWallpaper(monitor_index, image_path)
        time.sleep(slideshow_time)


def main(argv):

    if platform.system() != "Windows":
        print("Unfortunately, the script is for Windows only.")
        exit(1)

    image_base_directory = ""
    slideshow_time = 60
    working_mode = ""
    config_file_path = ""

    try:
        opts, args = getopt.getopt(
            argv, "h:p:t:m:c:v:", ["help", "PATH=", "TIME=", "MODE=", "CONFIG="])
    except getopt.GetoptError:
        print("getopt failed to get options.")
        show_help()
        exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit(0)
        elif opt in ("-p", "--PATH"):
            image_base_directory = arg
        elif opt in ("-t", "--TIME"):
            slideshow_time = int(arg)
        elif opt in ("-m", "--MODE"):
            working_mode = arg
        elif opt in ("-c", "--CONFIG"):
            config_file_path = arg

    if working_mode != "multi":
        single_monitor_loop(image_base_directory, slideshow_time)

    multiple_monitor_loop(config_file_path, slideshow_time)


if __name__ == "__main__":
    main(sys.argv[1:])
