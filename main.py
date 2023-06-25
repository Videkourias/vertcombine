import os, enum
import combine


# Enum for size units
class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


# Convert bytes to different unit
def convert_unit(size_in_bytes, unit):
    if unit == SIZE_UNIT.KB:
        return size_in_bytes / 1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes





# Update the list of images using the 'directory' directory
def getImages(directory, images):
    images.clear()
    for root, dirs, files in os.walk(directory):
        for name in files:
            images.append(os.path.join(root, name))


def main(name):
    # Directory containing images to be combined
    directory = 'Images/'
    initSize = 0

    # Check if image exists in any form
    imgname = 'Complete/' + name
    if os.path.isfile(imgname + '_vertical.jpg') or os.path.isfile(imgname + '_horizontal.jpg') or \
            os.path.isfile(imgname + '_vertical2.jpg') or os.path.isfile(imgname + '_horizontal2.jpg') or \
            os.path.isfile(imgname + '_grid.jpg') or os.path.isfile(imgname + '.pdf'):
        print("Image with that name already exists")
        exit(1)

    imagePaths = []  # Paths to image files


    # Update images array
    getImages(directory, imagePaths)
    if not imagePaths:
        print('No images to combine found in {}'.format(directory))
        exit(1)

    #print(imagePaths)

    # Combine the images
    completeNames = []
    completeNames.append(combine.sync(imagePaths, name))
    completeNames.append(combine.append(imagePaths, name, "v"))
    completeNames.append(combine.append(imagePaths, name, "h"))
    completeNames.append(combine.grid(imagePaths, name, match=True))

    # Only compare sizes if new images have been created
    if completeNames:

        # Compare size of files separately vs combined size
        for i in imagePaths:
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
