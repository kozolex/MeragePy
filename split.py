# path to original dataset
dataset_root = '/data/DataSet_Compare_1/3lata'

train_dataset_root = dataset_root + '.augmented.train'
val_dataset_root = dataset_root + '.augmented.val'
test_dataset_root = dataset_root + '.augmented.test'

import os
from random import shuffle


dirs = os.listdir(dataset_root)
dirs.sort()

print dirs

all_files = []

for i in range(len(dirs)):
    dir_path = os.path.join(dataset_root, dirs[i])
    dir_content = [os.path.join(dirs[i],f) for f in os.listdir(dir_path)]
    shuffle(dir_content)
    all_files.append(dir_content)

from sklearn.cross_validation import train_test_split

test_size = 0.2

train_files = []
val_files = []
test_files = []

for i in range(len(all_files)):
    train, val_test = train_test_split(all_files[i],test_size=test_size)    
    val, test = train_test_split(val_test,test_size=0.5)
    
    for f in train:
        train_files.append(f)

    for f in val:
        val_files.append(f)

    for f in test:
        test_files.append(f)
    

print "Train samples", len(train_files)
print "Validation samples", len(val_files)
print "Test samples", len(test_files)

def copy_dataset(file_list, src_root, dst_root):
    print "Copying files from", src_root,"to", dst_root
    for fpath in file_list:
        src_path = os.path.join(src_root,fpath)
        dst_path = os.path.join(dst_root,fpath)

        dst_dir = os.path.split(dst_path)[0]
        if not os.path.exists(dst_dir):
            print "Creating ", dst_dir
            os.makedirs(dst_dir)
        !cp $src_path $dst_path
    
!rm -R $train_dataset_root
!rm -R $val_dataset_root
!rm -R $test_dataset_root
copy_dataset(train_files, dataset_root, train_dataset_root)
copy_dataset(val_files, dataset_root, val_dataset_root)
copy_dataset(test_files, dataset_root, test_dataset_root)
print "Done."