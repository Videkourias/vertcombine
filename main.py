import numpy as np
import PIL, os
from PIL import Image

images = [] # Paths to image files


# Update the list of images using the 'directory' directory
def getImages(directory):
    for root, dirs, files in os.walk(directory):
        for name in files:
            images.append(os.path.join(root, name))


'''
list_im = ['Test1.jpg', 'Test2.jpg', 'Test3.jpg']
imgs    = [ PIL.Image.open(i) for i in list_im ]
# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

# save that beautiful picture
imgs_comb = PIL.Image.fromarray( imgs_comb)
imgs_comb.save( 'Trifecta.jpg' )

# for a vertical stacking it is simple: use vstack
imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
imgs_comb = PIL.Image.fromarray( imgs_comb)
imgs_comb.save( 'Trifecta_vertical.jpg' )
'''


def main():
    directory = 'Images'

    # Update images array
    getImages(directory)
    print(images)


if __name__ == '__main__':
    main()
