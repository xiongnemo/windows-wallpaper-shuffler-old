# windows-wallpaper-shuffler

Wallpaper shuffler for Windows, implemented in Python.

## Feature

Shuffle backgound images according to time. Use sets of image provided in dedicated path.

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

### Run

Slideshow time is an optional argument.

```powershell
python ./desktop_background_shuffler.py -p "dir_to_image" -t <slideshow time>
```

or

```powershell
python ./desktop_background_shuffler.py --PATH="dir_to_image" --TIME=<slideshow time>
```

### Example

```powershell
python ./desktop_background_shuffler.py -p "D:/temp/image_shuffler_test_dir" -t 50
```

or

```powershell
python python ./desktop_background_shuffler.py --PATH="D:/temp/image_shuffler_test_dir" --TIME=50
```

## Todo

- [ ] Use config file for auto configuration.
