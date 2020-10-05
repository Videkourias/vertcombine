import numpy as np
import PIL, os, math
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


# Combine the images present in the images array, vertically or horizontally, using numpy and PIL methods
# Shrinks all images to same size as smallest image, can cause blur in resultant image
# Returns the name of the image created, image only created using 1 method (vertical by default) per call
def combineSync(name, method='v'):
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
        imgs_comb.save('Complete/' + name + '_horizontal.jpg')
        return 'Complete/' + name + 'horizontal.jpg'

    # Create image vertical
    if 'v' in m:
        imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save('Complete/' + name + '_vertical.jpg')
        return 'Complete/' + name + '_vertical.jpg'


# Combine the images present in the images array, vertically or horizontally, using PIL methods
# Creates one large image using the sum height and greatest width of all the component images
# Returns the name of the image created, image only created using 1 method (vertical by default) per call
def combineAppend(name, method='v'):
    imgs = [PIL.Image.open(i) for i in images]

    # Determine max width and sum height of images
    widths, heights = zip(*(i.size for i in imgs))

    m = method.lower()

    # Create vertical image
    if 'v' in m:
        max_width = max(widths)
        total_height = sum(heights)

        # Combined image
        combine = Image.new('RGB', (max_width, total_height), (255, 255, 255))

        # Paste old images onto new image
        y_offset = 0
        for i in imgs:
            # Centers images within vertical column
            x_offset = (max_width - i.size[0]) // 2
            combine.paste(i, (x_offset, y_offset))
            y_offset += i.size[1]

        combine.save('Complete/' + name + '_vertical2.jpg')
        return 'Complete/' + name + '_vertical2.jpg'

    # Create horizontal image
    if 'h' in m:
        total_width = sum(widths)
        max_height = max(heights)

        # Combined image
        combine = Image.new('RGB', (total_width, max_height), (255, 255, 255))

        # Paste old images onto new image
        x_offset = 0
        for i in imgs:
            # Centers image within horizontal row
            y_offset = (max_height - i.size[1]) // 2
            combine.paste(i, (x_offset, y_offset))
            x_offset += i.size[0]

        combine.save('Complete/' + name + '_horizontal2.jpg')
        return 'Complete/' + name + '_horizontal2.jpg'


# Combine the images present in the images array using PIL methods
# Creates a grid of images that have a small border surrounding them
# WIP, works best on images of identical size, ideal for large sets of images
# Returns the name of the image created
def combineGrid(name, cols=5):
    imgs = [PIL.Image.open(i) for i in images]

    width, height = imgs[0].size

    rows = math.ceil(len(imgs) / cols)

    # Determine buffer between columns and rows
    colbuffer = width // 100
    rowbuffer = height // 100

    # Combined image
    combine = Image.new('RGB', ((cols * width) + ((cols-1) * colbuffer), (rows * height) + ((rows-1) * rowbuffer)))

    # Paste old images onto new image
    y_offset = 0
    x_pos = 0
    y_pos = 0
    for i in imgs:
        # Offsets X,Y coords
        # x offset should account for some number of spaces
        x_offset = x_pos * width + (x_pos * colbuffer)

        combine.paste(i, (x_offset, y_offset))

        x_pos += 1
        if x_pos == cols:
            y_pos += 1
            y_offset += height + (y_pos * rowbuffer)
            x_pos = 0

    combine.save('Complete/' + name + '_grid.jpg')
    return 'Complete/' + name + '_grid.jpg'


def main(name):
    directory = 'Images/'
    initSize = 0

    # Check if image exists in any form
    imgname = 'Complete/' + name
    if os.path.isfile(imgname + '_vertical.jpg') or os.path.isfile(imgname + '_horizontal.jpg') or \
            os.path.isfile(imgname + '_vertical2.jpg') or os.path.isfile(imgname + '_horizontal2.jpg') or \
            os.path.isfile(imgname + '_grid.jpg'):
        print("Image with that name already exists")
        exit(1)

    # Update images array
    getImages(directory)

    # Combine the images
    completeNames = []
    completeNames.append(combineSync(name))
    completeNames.append(combineAppend(name))
    completeNames.append(combineGrid(name))

    # Only compare sizes if new images have been created
    if completeNames:

        # Compare size of files separately vs combined size
        for i in images:
            initSize += os.path.getsize(i)

        # Cycle through the created images
        for n in completeNames:
            endSize = os.path.getsize(n)

            print('===={}===='.format(n))
            print('Init size: {} MB\nEnd size: {} MB\nDifference: {} MB\n\n'.format(
                round(convert_unit(initSize, SIZE_UNIT.MB), 3),
                round(convert_unit(endSize, SIZE_UNIT.MB), 3),
                round(convert_unit(abs(endSize - initSize),
                                   SIZE_UNIT.MB), 3)))


if __name__ == '__main__':
    main(input('Provide image name: '))
