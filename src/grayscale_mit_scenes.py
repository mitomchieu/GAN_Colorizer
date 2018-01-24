import numpy as np
import pickle
from PIL import Image
from skimage import color, io
import matplotlib.pyplot as plt
from glob import glob

def un_scale(image):
    """
    Unscale L spectrum. Only used to doublecheck conversion from RGB to L.
    """
    image = np.squeeze(image)
    image = image * 100
    return image

def rgb_to_lab(image, l=False, ab=False):
    """
    Input: image in RGB format with full values for pixels. (0-255)
    Output: image in LAB format and with all values between -1 and 1.
    """
    lab = color.rgb2lab(image)
    if l: l_layer = np.zeros((256,256,1))
    else: ab_layers = np.zeros((256,256,2))
    for i in range(len(lab)):
        for j in range(len(lab[i])):
            p = lab[i,j]
            # new_img[i,j] = [p[0]/100,(p[1] + 128)/255,(p[2] + 128)/255]
            if ab: ab_layers[i,j] = [(p[1] + 127)/255 * 2 - 1,(p[2] + 128)/255 * 2 -1]
            else: l_layer[i,j] = [p[0]/50 - 1]
    if l: return l_layer
    else: return ab_layers

def lab_to_rgb(image):
    """
    Input: image in LAB format and with all values between -1 and 1.
    Output: image in RGB format with full values for pixels. (0-255)
    """
    new_img = np.zeros((256,256,3))
    for i in range(len(image)):
        for j in range(len(image[i])):
            p = image[i,j]
            new_img[i,j] = [(p[0] + 1) * 50,(p[1] +1) / 2 * 255 - 127,(p[2] +1) / 2 * 255 - 128]
    new_img = color.lab2rgb(new_img) * 255
    new_img = new_img.astype('uint8')
    return new_img

if __name__ == '__main__':
    file_paths = glob('../data/forest/*.jpg')
    X_train = np.array([np.array(Image.open(f).getdata()).reshape(256,256,3).astype('uint8') for f in file_paths])
    print(len(X_train),'images imported...')

    np.random.shuffle(X_train)
    X_test = X_train[:25]
    X_train = X_train[25:]
    print('Train/Test Split Done..')
    print(len(X_test), 'train images')
    print(len(X_train), 'test images')

    X_train_L = np.array([rgb_to_lab(image, l=True) for image in X_train])
    print('X_train L layer done...')
    X_train_AB = np.array([rgb_to_lab(image, ab=True) for image in X_train])
    print('X_train a*b* layers done...')
    X_train = (X_train_L, X_train_AB)
    with open('../data/X_train.p','wb') as f:
        pickle.dump(X_train,f)
    print('X_train done...')

    X_test_L = np.array([rgb_to_lab(image,l=True) for image in X_test])
    print('X_test L layer done...')
    X_test_AB = np.array([rgb_to_lab(image, ab=True) for image in X_test])
    print('X_test a*b* layers done...')
    X_test = (X_test_L, X_test_AB)
    with open('../data/X_test.p','wb') as f:
        pickle.dump(X_test,f)
    print('X_test done...')
