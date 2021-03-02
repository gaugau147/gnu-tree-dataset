import os
import argparse
import csv
import shutil

class Tree:
    def __init__(self, root):
        self.root = root
        self.depth = 1
        self.depth = self.get_depth()
        self.tree = []
        self.get_tree()
    
    def get_root(self):
        return self.root
    
    def find_max_depth(self, path):
        '''recursively get the max depth of a directory'''
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        if len(folders) == 0:
            return self.depth
        else:
            self.depth += 1
            return self.find_max_depth(os.path.join(path, folders[0]))

    def get_depth(self):
        '''return max depth of root'''
        return self.find_max_depth(self.root)
    
    def create_folder_tree(self, path, current_depth):
        '''recursively get the leaf directories of the GNU tree'''
        if current_depth == 2:
            self.tree.append(path)
        else:
            for f in sorted(os.listdir(path)):
                self.create_folder_tree(os.path.join(path, f), current_depth - 1)
    
    def get_tree(self):
        current_depth = self.depth
        path = self.root
        return self.create_folder_tree(path, current_depth)

    def get_batch_list(self):
        return self.tree


def compare_batch(jsonPath, imagePath, save_dir):
    '''
    input:  jsonPath (str) 'labelled/exit/batch1'
            imagePath(str) 'raw/batch1'
            save_dir (str) 'test'
    '''

    jsonCams = sorted([f for f in os.listdir(jsonPath) if os.path.isdir(os.path.join(jsonPath, f))])
    

    # path_to_save = os.path.join(save_dir, os.path.join(*imagePath.split(os.sep)[1:]))
    # if not os.path.exists(path_to_save):
    #     os.makedirs(path_to_save)

    if os.path.exists(os.path.join(jsonPath, '_'.join(jsonPath.split(os.sep)) + '.csv')):
        os.remove(os.path.join(jsonPath, '_'.join(jsonPath.split(os.sep)) + '.csv'))

    with open(os.path.join(jsonPath, '_'.join(jsonPath.split(os.sep)) + '.csv'), 'w', newline='') as csvfile:
        fieldnames = ['path', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for cam in jsonCams:
            json_list = sorted([os.path.splitext(f)[0] for f in os.listdir(os.path.join(jsonPath, cam))])
            image_list = sorted([os.path.splitext(f)[0] for f in os.listdir(os.path.join(imagePath, cam))])

            path_to_save = os.path.join(save_dir, os.path.join(*jsonPath.split(os.sep)[1:]), cam)
            if not os.path.exists(path_to_save):
                os.makedirs(path_to_save)

            if json_list == image_list:
                for f in json_list:
                    shutil.copy(os.path.join(imagePath, cam, f + '.jpeg'), os.path.join(path_to_save, f + '.jpeg'))

            for f in json_list:
                # cams = os.listdir(os.path.join(jsonPath, f))
                if f not in image_list:
                    # print('not in image folder: ', os.path.join(jsonPath, f))
                    writer.writerow({
                        'path': os.path.join(jsonPath, cam, f + '.json'),
                        'status': 'missing image'
                    })
                else:
                    shutil.copy(os.path.join(imagePath, cam, f + '.jpeg'), os.path.join(path_to_save, f + '.jpeg'))

        


if __name__ == "__main__":
    # dirs = [d for d in os.listdir('.' if os.path.isdir(x))]
    parser = argparse.ArgumentParser()
    parser.add_argument('-json_root', type=str, required=True, help='json root name')
    parser.add_argument('-jpeg_root', type=str, required=True, help='jpeg root name')
    parser.add_argument('-save_dir', type=str, default='test', help='where to save available images')
    args = parser.parse_args()

    json = Tree(args.json_root)
    jpeg = Tree(args.jpeg_root)

    print('json tree: ', json.get_batch_list())
    print('jpeg tree: ', jpeg.get_batch_list())

    if os.path.exists(args.save_dir):
        shutil.rmtree(args.save_dir)
    
    os.makedirs(args.save_dir)

    
    for i in range(len(json.get_batch_list())):
        compare_batch(json.get_batch_list()[i], jpeg.get_batch_list()[i], args.save_dir)
        # pass
