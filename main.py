import numpy as np
import PIL, os
from PIL import Image
import enum


# Enum for size units
class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def convert_unit(size_in_bytes, unit):
    if unit == SIZE_UNIT.KB:
        return size_in_bytes / 1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes


images = []  # Paths to image files


# Update the list of images using the 'directory' directory
def getImages(directory):
    images.clear()
    for root, dirs, files in os.walk(directory):
        for name in files:
            images.append(os.path.join(root, name))


# Combine the images present in the images array using numpy and PIL methods
# Shrinks all images to same size as smallest image, can cause blur in resultant image
def combineImages1(name, method='v'):
    imgs = [PIL.Image.open(i) for i in images]

    # Convert all images to type RGB, should retain colour and ensure image mode consistency
    for i in range(len(imgs)):
        imgs[i] = imgs[i].convert('RGB')

    # Find image with smallest size and resize others to match it
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

    m = method.lower()

    # Create image horizontal
    if 'h' in m:
        imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save('Complete/' + name + '.jpg')

    # Create image vertical
    if 'v' in m:
        imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save('Complete/' + name + '_vertical.jpg')

# Combine the images present in the images array using PIL methods
# Creates one large image using the sum height and greatest width of all the component images
def combineImages2(name):
    imgs = [PIL.Image.open(i) for i in images]

    # Determine max width and sum height of images
    widths, heights = zip(*(i.size for i in imgs))
    max_width = max(widths)
    total_height = sum(heights)

    # Combined image
    combine = Image.new('RGB', (max_width, total_height), (255, 255, 255))

    # Paste old images onto new image
    y_offset = 0
    for i in imgs:
        x_offset = (max_width - i.size[0])//2
        combine.paste(i, (x_offset, y_offset))
        y_offset += i.size[1]

    combine.save('Complete/' + name + '_vertical.jpg')

def main(name):
    directory = 'Images/'
    initSize = 0

    # Update images array
    getImages(directory)

    # Combine the images
    combineImages2(name)

    # Compare size of files separately vs combined size
    # for i in images:
    #    initSize += os.path.getsize(i)
    # endSize = os.path.getsize('Complete/' + name + '.jpg') if 'h' in name else os.path.getsize('Complete/' + name + '_vertical.jpg')

    # print('Init size: {} MB\nEnd size: {} MB\nDifference: {} MB'.format(round(convert_unit(initSize, SIZE_UNIT.MB), 3),
    #                                                                    round(convert_unit(endSize, SIZE_UNIT.MB), 3),
    #                                                    round(convert_unit(abs(endSize - initSize), SIZE_UNIT.MB), 3)))


if __name__ == '__main__':
    main(input('Provide image name: '))
