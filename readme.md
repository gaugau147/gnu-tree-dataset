### Requirements:
 - Python3

### Features:
 - Create paths to batches (e.g. `labelled/highway/batch1`)
 - Browse for missing images of corresponded json files and print to csv file
 - Copy file from `dest` to a new directory with same structure with `source`

### How to run
```bash
python walking_tree.py -source=<path_to_json_root> -dest=<path_to_jpeg_root> -save_dir=<path_to_save_dir>
```

