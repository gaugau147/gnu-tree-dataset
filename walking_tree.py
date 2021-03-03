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
            for f in sorted([f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]):
                self.create_folder_tree(os.path.join(path, f), current_depth - 1)
    
    def get_tree(self):
        current_depth = self.depth
        path = self.root
        return self.create_folder_tree(path, current_depth)

    def get_batch_list(self):
        return self.tree

    def get_children(self):
        return [f for f in os.listdir(self.root) if os.path.isdir(os.path.join(self.root, f))]


def compare_batch(jsonPath, imagePath, save_dir, writer):
    '''
    input:  jsonPath (str) 'labelled/exit/../batch1'
            imagePath(str) 'raw/../batch1'
            save_dir (str) 'test'
    '''

    jsonCams = sorted([f for f in os.listdir(jsonPath) if os.path.isdir(os.path.join(jsonPath, f))])

    for cam in jsonCams:
        json_list = []
        image_list = []
        # json_list = sorted([os.path.splitext(f)[0] for f in os.listdir(os.path.join(jsonPath, cam))])
        # image_list = sorted([os.path.splitext(f)[0] for f in os.listdir(os.path.join(imagePath, cam))])
        for f in sorted(os.listdir(os.path.join(jsonPath, cam))):
            json_list.append(os.path.splitext(f)[0])
            source_extension = os.path.splitext(f)[1]

        if cam not in os.listdir(imagePath):
            continue
            
        for f in sorted(os.listdir(os.path.join(imagePath, cam))):
            image_list.append(os.path.splitext(f)[0])
            dest_extension = os.path.splitext(f)[1]

        path_to_save = os.path.join(save_dir, os.path.join(*jsonPath.split(os.sep)[1:]), cam)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        if json_list == image_list:
            for f in json_list:
                shutil.copy(os.path.join(imagePath, cam, f + dest_extension), os.path.join(path_to_save, f + dest_extension))

        for f in json_list:
            if f not in image_list:
                writer.writerow({
                    'missing correspoding file in source': os.path.join(jsonPath, cam, f + source_extension)
                })
            else:
                shutil.copy(os.path.join(imagePath, cam, f + dest_extension), os.path.join(path_to_save, f + dest_extension))

        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-source', type=str, required=True, help='json root name')
    parser.add_argument('-dest', type=str, required=True, help='jpeg root name')
    parser.add_argument('-save_dir', type=str, default='test', help='where to save available images')
    args = parser.parse_args()

    source = Tree(args.source)
    dest = Tree(args.dest)

    # print('source paths: ', source.get_batch_list())
    # print('dest paths: ', dest.get_batch_list())

    print("source's children: ", source.get_children())

    inChildren = True
    folders = []
    while True:

        folders = input('Please specify which children folders for checking (please use comma or space): ')
        folders = folders.split()
        for c in folders:
            if c not in source.get_children():
                print("There are folders in not source's children.")
                inChildren = False
        if not inChildren:
            inChildren = True
            continue
        check = input('Checking folders: ' +  str(folders) + ', (y or n)?: ')
        
        if check in ' y Y yes Yes YES YEs ':
            break

    if os.path.exists(args.save_dir):
        shutil.rmtree(args.save_dir)
    
    os.makedirs(args.save_dir)

    if os.path.exists(os.path.join(args.source, 'results.csv')):
        os.remove(os.path.join(args.source, 'results.csv'))

    with open(os.path.join(args.source, 'results.csv'), 'w') as csvfile:
        fieldnames = ['missing correspoding file in source']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(source.get_batch_list())):
            child = source.get_batch_list()[i].split(os.sep)[1]
            # print(child)
            if child in folders:
                compare_batch(source.get_batch_list()[i], dest.get_batch_list()[i], args.save_dir, writer)
