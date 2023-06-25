import numpy as np
import PIL, math
from PIL import Image


# Combine the images present in the images array, vertically or horizontally, using numpy and PIL methods
# Shrinks all images to same size as smallest image, can cause blur in resultant image
# Returns the name of the image created, image only created using 1 method (vertical by default) per call
def sync(images, name, method='v'):
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
        imgs_comb = np.vstack(list(np.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save('Complete/' + name + '_vertical.jpg')
        return 'Complete/' + name + '_vertical.jpg'


# Combine the images present in the images array, vertically or horizontally, using PIL methods
# Creates one large image using the sum height and greatest width of all the component images
# Returns the name of the image created, image only created using 1 method (vertical by default) per call
def append(images, name, method='v'):
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
# Works best on images of identical size, ideal for large sets of images. Works to an extent for varying image sizes
# Returns the name of the image created
def grid(images, name, cols=6, match=False):
    imgs = [PIL.Image.open(i) for i in images]

    # Width, height of largest image, or first image
    if match:
        width = max(i.size[0] for i in imgs)
        height = max(i.size[1] for i in imgs)
    else:
        width, height = imgs[0].size

    rows = math.ceil(len(imgs) / cols)

    # Determine buffer between columns and rows
    colbuffer = width // 50
    rowbuffer = height // 50

    # Combined image
    combine = Image.new('RGB', ((cols * width) + ((cols-1) * colbuffer), (rows * height) + ((rows-1) * rowbuffer)))

    # Paste old images onto new image
    y_offset = 0
    x_pos = 0
    for i in imgs:
        # Offsets X,Y coords
        # x offset should account for some number of spaces
        x_offset = x_pos * width + (x_pos * colbuffer)

        # Centers image within space of largest image in img list
        if match:
            combine.paste(i, (x_offset + (width - i.size[0])//2, y_offset + (height - i.size[1])//2))
        else:
            combine.paste(i, (x_offset, y_offset))

        x_pos += 1
        if x_pos == cols:
            y_offset += height + rowbuffer
            x_pos = 0

    combine.save('Complete/' + name + '_grid.jpg')
    return 'Complete/' + name + '_grid.jpg'