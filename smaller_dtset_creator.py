from logging import root
import os
from re import sub
# import splitfolders
import numpy as np
import shutil

root_dir = "/Users/zoetzikra/Documents/2022-2023/BSc_Project/50_artists_dtset/images"
# training = os.makedirs(root_dir +'/train(sampled)')
# validation = os.makedirs(root_dir +'/val(sampled)')
sampled_source = os.makedirs(root_dir +'/src(sampled)')


counter_tr = 0
counter_val = 0


for subdir, dirs, files in os.walk(root_dir+"/source"):
    for dir in dirs:
        # if (dir == root_dir +'/train' or dir == root_dir +'/val'):
        #     continue
        # folder to copy the images from
        src = dir

        # get the file names in the current directory
        directoryFileNames = os.listdir(root_dir+"/source/" + src)
        # print("directoryFileNames: ", directoryFileNames)
        np.random.shuffle(directoryFileNames)

        # divide the data
        data_we_keep, data_we_throw = np.split(np.array(directoryFileNames), [int(len(directoryFileNames) * (0.25))])

        # turn to list so you can iterate more easily
        # data_we_keep = [src+'/'+ file for file in data_we_keep.tolist()]
        # data_we_throw = [src+'/' + file for file in data_we_throw.tolist()]
        # print('Total images: ', len(directoryFileNames))
        # print('data_we_keep: ', len(data_we_keep))
        # counter_tr += len(data_we_keep)
        # print('data_we_throw: ', len(data_we_throw))


        # divide the data
        train_FileNamesDir, val_FileNamesDir = np.split(np.array(data_we_keep), [int(len(data_we_keep) * (0.8))])

        # turn to list so you can iterate more easily
        train_FileNamesDir = [src+'/'+ file for file in train_FileNamesDir.tolist()]
        val_FileNamesDir = [src+'/' + file for file in val_FileNamesDir.tolist()]

        print('Total images: ', len(directoryFileNames))
        print('Training: ', len(train_FileNamesDir))
        print('Validation: ', len(val_FileNamesDir))
        
        # print("train_FileNamesDir ", train_FileNamesDir)

        destination_folder = os.makedirs(root_dir +'/src(sampled)/'+ dir)
        for file in train_FileNamesDir:
            shutil.copy(root_dir+'/source/'+file, root_dir +'/src(sampled)/'+ dir)
            counter_tr +=1
        for file in val_FileNamesDir:
            shutil.copy(root_dir+"/source/"+file, root_dir +'/src(sampled)/'+ dir)
            counter_val +=1


        # destination_folder_train = os.makedirs(root_dir +'/train/'+ dir)
        # destination_folder_val = os.makedirs(root_dir +'/val/'+ dir)
        # Copy-pasting images
        # for file in train_FileNamesDir:
        #     shutil.copy(root_dir+'/source/'+file, root_dir +'/train/'+ dir)
        #     counter_tr +=1

        # for file in val_FileNamesDir:
        #     shutil.copy(root_dir+"/source/"+file, root_dir +'/val/'+ dir)
        #     counter_val +=1

        print("done")
            
print(counter_tr)
print(counter_val)

    #print(subdir)
        
    # for file in files:
    #     # print(os.path.join(subdir, file))
    #     # counter += 1 #it prints one more than it should aka the subdir 1
        
    #     src = subdir
    #     allFileNames = os.listdir(src)

        
    #     np.random.shuffle(allFileNames)
    #     train_FileNames, val_FileNames = np.split(np.array(allFileNames),[int(len(allFileNames)*0.8), int(len(allFileNames)*0.2)])

    #     train_FileNames = [src+'/'+ name for name in train_FileNames.tolist()]
    #     val_FileNames = [src+'/' + name for name in val_FileNames.tolist()]

    #     print('Total images: ', len(allFileNames))
    #     print('Training: ', len(train_FileNames))
    #     print('Validation: ', len(val_FileNames))


    #     # Copy-pasting images
    #     for name in train_FileNames:
    #         shutil.copy(name, root_dir+"/train"+ src)

    #     for name in val_FileNames:
    #         shutil.copy(name, root_dir+"/val"+ src)

    #     #print(src)




