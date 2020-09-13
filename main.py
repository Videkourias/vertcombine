import numpy as np
import PIL, os
from PIL import Image

images = []  # Paths to image files


# Update the list of images using the 'directory' directory
def getImages(directory):
    images.clear()
    for root, dirs, files in os.walk(directory):
        for name in files:
            images.append(os.path.join(root, name))


# Combine the images present in the images array
def combineImages(name, method='v'):
    imgs = [PIL.Image.open(i) for i in images]

    # Find image with smallest size and resize others to match it
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

    m = method.lower()

    # Create image horizontal
    if 'h' in m:
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save('Complete/' + name + '.jpg')

    # Create image vertical
    if 'v' in m:
        imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save('Complete/' + name + '_vertical.jpg')


def main(name):
    directory = 'Images/'

    # Update images array
    getImages(directory)

    # Combine the images
    combineImages(name)


if __name__ == '__main__':
    main(input('Provide image name: '))
