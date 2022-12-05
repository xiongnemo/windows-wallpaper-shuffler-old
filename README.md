# windows-wallpaper-shuffler

<!-- [![CodeFactor](https://www.codefactor.io/repository/github/xiongnemo/windows-wallpaper-shuffler/badge)](https://www.codefactor.io/repository/github/xiongnemo/windows-wallpaper-shuffler) -->

Wallpaper shuffler for Windows, implemented in Python.

## Feature

* Shuffle backgound images according to time. Use sets of image provided in dedicated path.

* Supports multi-monitor.

```reconstructedText
nemo@MARSHMALLOW-LAP > D:\temp\image_shuffler_test_dir
❯ tree
Folder PATH listing for volume ******
Volume serial number is ****-****
D:.
├───afternoon
├───dusk
├───forenoon
├───night
└───noon
```

## Usage

### Prepare Images

Create a dedicate folder for all your images.

Then, create five subfolders and copy your images into it.

### Multi-monitor config

You will need a json config file.

```json
{
    "image_base_directory": "your image's base directory",
    "per_monitor_directory": {
        "monitor_0": "override above setting for per monitor",
        "monitor_1": "...",
        ...
    },
    "dll_path": "dll path to IDesktopWallpaper::SetWallpaper's dll"
    // download from https://github.com/xiongnemo/idesktopwallpaper-dll/releases/tag/1.0.0
}
```

### Run

Slideshow time is an optional argument.

#### Single

```powershell
python ./desktop_background_shuffler.py -p "dir_to_image" -t <slideshow time>
```

or

```powershell
python ./desktop_background_shuffler.py --PATH="dir_to_image" --TIME=<slideshow time>
```

#### Multi

```powershell
python ./desktop_background_shuffler.py -m multi -c "path_to_json_config_file" -t <slideshow time>
```

### Example

#### Single

```powershell
python ./desktop_background_shuffler.py -p "D:/temp/image_shuffler_test_dir" -t 50
```

or

```powershell
python ./desktop_background_shuffler.py --PATH="D:/temp/image_shuffler_test_dir" --TIME=50
```

#### Multi

```powershell
python ./desktop_background_shuffler.py -m multi -c ./work.json -t 20
```

## Screenshots


### Multi-monitor running in single monitor mode

![](./doc/img/multi-monitor-with-sigle-monitor-mode.png)
### Multi-monitor mode

![](./doc/img/multi-monitor.png)

## Todo

- [ ] Use config file for auto configuration (time).
