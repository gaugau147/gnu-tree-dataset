### Requirements:
 - Python3

### Features:
 - Create paths to batches (e.g. `labelled/highway/batch1`)
 - Browse for missing images of corresponded json files and print csv file in each batch
 - Copy available images to a new directory with same structure with `labelled`

### How to run

```bash
python walking_tree.py -json_root=<path_to_json_root> -jpeg_root=<path_to_jpeg_root> -save_dir=<path_to_save_dir>
```

