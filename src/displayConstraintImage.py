import os
import glob
import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, default='/media/yslin/SSD_DATA/research/BlenderRender/out', help='the root directory of the iamges')
    # parser.add_argument('')
    args = parser.parse_args()
    return args
def display(cfg):
    print(cfg)
    S_imgs = sorted(glob.glob(os.path.join(cfg['root_dir'], 'shadow', '*.png')))
    N_imgs = sorted(glob.glob(os.path.join(cfg['root_dir'], 'non_shadow', '*.png')))
    M_imgs = sorted(glob.glob(os.path.join(cfg['root_dir'], 'mask', '*.png')))
    
    for S_img, N_img, M_img in zip(S_imgs, N_imgs, M_imgs):
        
        M = cv2.imread(M_img, cv2.IMREAD_GRAYSCALE)
        cnt = np.bincount(M)
        print(cnt)
        # binary_M = np.zeros(M.shape, np.uint8)
        # binary_M[np.where(M > 0)] = 1
        

        print(M.shape)
        return
        # S = mpimg.imread(S_img)
        # N = mpimg.imread(N_img)
        # M = mpimg.imread(M_img)
        
        # ax = fig.add_subplot(row, col, r * col + c + 1)
            




def main():
    args = get_args()
    # constraint = 
    display(vars(args))
if __name__ == "__main__":
    main()