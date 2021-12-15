"""
Takes the dogs and cats dataset and modifies the labels
"""
import argparse
import os
import math
import pathlib
import shutil
from random import sample

DIR_VAR = 'DATA_DIR'
PARTITION = ['training_set', 'test_set']
TRUE_LABEL = ['cats', 'dogs']


def overwrite_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def make_dirs(top_path):
    overwrite_dir(top_path)
    for part in PARTITION:
        part_path = '{}/{}'.format(top_path, part)
        overwrite_dir(part_path)
        for lab in TRUE_LABEL:
            lab_path = '{}/{}'.format(part_path, lab)
            overwrite_dir(lab_path)


def permute(frac, shrink):
    org_path = os.environ['DATA_DIR']
    print(org_path)
    dataset_name = 'noise_{}_size_{}'.format(int(frac*100), int(shrink*100))
    new_path = '{}/{}'.format(pathlib.Path(org_path).parent, dataset_name)
    print('NEW PATH: %s' % new_path)
    make_dirs(new_path)
    # iterate over training and test
    for part in PARTITION:
        # get important image counts (total size of partition, number we'll keep, number we'll permute)
        part_dir = '{}/{}'.format(new_path, part)
        part_img_count = len(os.listdir('{}/{}/{}'.format(org_path, part, TRUE_LABEL[0])))
        save_img_count = int(math.floor(part_img_count * shrink))
        permute_img_count = int(math.floor(save_img_count * frac))
        print('%s SAVE COUNT: %s' % (part, save_img_count))
        print('%s PERMUTE COUNT: %s' % (part, permute_img_count))
        # set first index based on training or test
        first_index = 1 if part_img_count == 4000 else 4001
        all_idx = list(range(first_index, first_index + save_img_count))
        permute_idx = sample(all_idx, permute_img_count)
        print('PERMUTING: %s' % permute_idx)
        # iterate over the dog and cat images
        for i in range(len(TRUE_LABEL)):
            true_lab = TRUE_LABEL[i]
            false_lab = TRUE_LABEL[i - 1] if i == 1 else TRUE_LABEL[i + 1]
            true_img_name = true_lab[:len(true_lab) - 1] # drop the 's'
            false_img_name = false_lab[:len(true_lab) - 1]
            true_dir = '{}/{}'.format(part_dir, true_lab)
            false_dir = '{}/{}'.format(part_dir, false_lab)
            for curr_idx in all_idx:
                src = '{}/{}/{}/{}.{}.jpg'.format(org_path, part, true_lab, true_img_name, curr_idx)
                if curr_idx in permute_idx:
                    targ = '{}/{}.{}.jpg'.format(false_dir, false_img_name, curr_idx)
                else:
                    targ = '{}/{}.{}.jpg'.format(true_dir, true_img_name, curr_idx)
                shutil.copy(src, targ)
    archive_name = '{}/{}'.format(pathlib.Path(org_path).parent, dataset_name)
    shutil.make_archive(archive_name, 'zip', root_dir=new_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--noise', '-n', type=float, default=.15)
    parser.add_argument('--shrink', '-s', type=float, default=.20)
    args = parser.parse_args()
    permute(args.noise, args.shrink)
