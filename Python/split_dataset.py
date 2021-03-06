# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 17:37:26 2020

@author: johan
"""



import os
import shutil
import utils
import constants
import progressbar



def get_data_sets(images_folder):
    
    import random as rand
    all_image_paths = utils.get_all_image_paths_in_folder(images_folder)
    test_image_paths = []
    val_image_paths = []
    train_image_paths = []
    for src_dir_index in range(0,len(constants.data_source_folders)):
        images_in_current_folder = []
        for image_path in all_image_paths:
            if "_srcdir" + str(src_dir_index) in image_path:
                images_in_current_folder.append(image_path)
        rand.shuffle(images_in_current_folder)    

        for i,path in enumerate(images_in_current_folder):
            if i < constants.val_splits[src_dir_index]*len(images_in_current_folder):
                val_image_paths.append(path)
            elif i < (constants.val_splits[src_dir_index]+constants.test_splits[src_dir_index])*len(images_in_current_folder):
                test_image_paths.append(path)
            else:
                train_image_paths.append(path)
        
        
    
    return [train_image_paths,val_image_paths,test_image_paths] 

def make_folders(project_dir):
    training_data_dir = os.path.join(project_dir,"training_data")
    

    folders = ['train_frames/0', 'train_masks/0', 'val_frames/0', 'val_masks/0', 'test_frames/0', 'test_masks/0']
    
    full_folder_paths = []
    
    for folder in folders:
        full_folder_path = os.path.join(training_data_dir,folder)
        os.makedirs(full_folder_path,exist_ok=True)
        utils.delete_folder_contents(full_folder_path)
        full_folder_paths.append(full_folder_path)
    
    return full_folder_paths


def split_into_train_val_and_test_sets(working_dir):
        
    print("Preparing folders...",flush=True)
    [train_frames_dir,train_masks_dir,val_frames_dir,val_masks_dir,test_frames_dir,test_masks_dir] = make_folders(working_dir)
    
    training_data_dir = os.path.join(working_dir,"training_data")
    image_tiles_dir = os.path.join(training_data_dir,"images")

    [train_image_paths,val_image_paths,test_image_paths] = get_data_sets(image_tiles_dir)
    
    print("Copying training images...",flush=True)
    for image_path in progressbar.progressbar(train_image_paths):
        shutil.copyfile(image_path,os.path.join(train_frames_dir,os.path.basename(image_path)))
        shutil.copyfile(image_path.replace("images","masks"),os.path.join(train_masks_dir,os.path.basename(image_path)))
    
    print("Copying validation images...",flush=True)
    for image_path in progressbar.progressbar(val_image_paths):
        shutil.copyfile(image_path,os.path.join(val_frames_dir,os.path.basename(image_path)))
        shutil.copyfile(image_path.replace("images","masks"),os.path.join(val_masks_dir,os.path.basename(image_path)))

    print("Copying testing images...",flush=True)
    for image_path in progressbar.progressbar(test_image_paths):
        shutil.copyfile(image_path,os.path.join(test_frames_dir,os.path.basename(image_path)))
        shutil.copyfile(image_path.replace("images","masks"),os.path.join(test_masks_dir,os.path.basename(image_path)))

        
        
        
if __name__ == '__main__':
    split_into_train_val_and_test_sets(constants.working_dir)

        
        
        
        
