import numpy as np
import random
import os
from glob import glob
from skimage import io
from sklearn.feature_extraction.image import extract_patches_2d

np.random.seed(5)
train_files = glob('Patches_Train/**')

def find_patches(training_images, class_num, num_samples, patch_size=(65,65)):
    '''
    INPUT:  (1) list 'training_images': all training images to select from
            (2) int 'class_num': class to sample from choice of {0, 1, 2, 3, 4}.
            (3) tuple 'patch_size': dimensions of patches to be generated defaults to 65 x 65
    OUTPUT: (1) num_samples patches from class 'class_num' randomly selected. note- if class_num is 0, will choose patches randomly, not exclusively 0s.
    '''
    ct = 0
    patches, l = [], [] #list of all patches and associated labels
    if class_num == 0:
        while ct < num_samples:
            im_path = random.choice(training_images)
            patch, label = random_patches(im_path, patch_size = patch_size)
            patches.append(patch)
            l.append(label)
            ct += 1
        return zip(patches, l)

    h,w = patch_size[0], patch_size[1]
    while ct < num_samples:
        im_path = random.choice(training_images) # select image to sample from
        fn = os.path.basename(im_path)
        label = io.imread('Labels/' + fn[:-4] + 'L.png')
        if class_num not in np.unique(label): # no pixel label class_num in img
            continue
        img = io.imread(im_path).reshape(5, 240, 240)[:-1] # exclude label slice
        p = random.choice(np.argwhere(label == class_num)) # center pixel
        while p[0] < h/2 or p[1] < h/2: # if patch won't fit
            p = random.choice(np.argwhere(label == class_num))

        p_ix = (p[0]-(h/2), p[0]+((h+1)/2), p[1]-(w/2), p[1]+((w+1)/2)) # patch index
        patch = np.array([i[p_ix[0]:p_ix[1], p_ix[2]:p_ix[3]] for i in img])
        l.append(label[p_ix[0]:p_ix[1], p_ix[2]:p_ix[3]])
        patches.append(patch) # patch = (n_chan, h, w)
        ct += 1
    return zip(patches, l)

def random_patches(im_path, patch_size = (65,65)):
    fn = os.path.basename(im_path)
    patch_lst = []
    label = io.imread('Labels/' + fn[:-4] + 'L.png')
    imgs = (io.imread(im_path).reshape(5, 240, 240))
    imgs[4] = label
    for img in imgs:
        patch_lst.append(extract_patches_2d(img, patch_size, max_patches = 1, random_state=5)) #set rs for same patch ix among modes
    patches = np.array(zip(patch_lst[0], patch_lst[1], patch_lst[2], patch_lst[3])[0])
    patch_label = np.array(patch_lst[-1][0])
    return patches, patch_label

def make_training_patches(training_images, num_total, balanced_classes = True):
    per_class = num_total / 5
    patches = [] # list of tuples (patche, label)
    class_0 = find_patches(training_images, 0, per_class)
    class_1 = find_patches(training_images, 1, per_class)
    class_2 = find_patches(training_images, 2, per_class)
    class_3 = find_patches(training_images, 3, per_class)
    class_4 = find_patches(training_images, 4, per_class)


# def generate_patches(img_path, patch_size=(65,65), num_patches = 10):
#     '''
#     Generates patches (num_chan, patch_h, patch_w) for an input image
#     INPUT:  (1) string 'img_path': path to imput image (png, strip of slices)
#             (2) tuple 'patch_size': dimensions of patches to be used in net
#             (3) int 'num_patches': number of patches to be generated per slice.
#     OUTPUT: (1) list of scan patches: (num_slices * num_patches, num_channels, patch_h, patch_w)
#             (2) list of label patches: (num_slices * num_patches, patch_h, patch_w)
#     '''
#     patch_lst = [] # list of lists: patches for each slice (same idxs)
#     patch_labels = []
#     fn = os.path.basename(im_path)
#     label = io.imread('Labels/' + fn[:-4] + 'L.png')
#     slices = io.imread(img_path).reshape(5,240,240)[:-1] # (chan + gt, h, w)
#     slices = slices.append(label)
#     for img in slices:
#         patch_lst.append(extract_patches_2d(img, patch_size, max_patches = num_patches, random_state=5)) #set rs for same patch ix among modes
#     patches = np.array(zip(patch_lst[0], patch_lst[1], patch_lst[2], patch_lst[3]))
#     patch_labels = np.array([i[patch_size[0] / 2][patch_size[1]/2] for i in patch_lst[-1]])
#     return patches, patch_labels

    # for slice_strip in self.normed_slices: # slice = strip of 5 images
    #     slices = slice_strip.reshape(5,240,240)
        # for img in slices:
        #     # get list of patches corresponding to each image in slices
        #     patch_list.append(extract_patches_2d(img, patch_size, max_patches = num_patches, random_state=5)) #set rs for same patch ix among modes
        # self.patches.append(zip(patch_list[0], patch_list[1], patch_list[2], patch_list[3]))
        # self.patch_labels.append(patch_list[-1])
