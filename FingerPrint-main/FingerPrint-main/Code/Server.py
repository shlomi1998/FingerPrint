
from stitch import Stitcher
import mysql
import PIL
from Client import *
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy
from matplotlib import cm

def findMatchByMSE_Threshold(source_img, dbPath=DBpath):
    kernel = np.ones((5, 5), np.uint8)
    i = ZERO
    is_continue = False

    match_img_list = []

    thresh_source_img = findThreshold(source_img)  # find threshold of source image

    print("Path: " + dbPath)

    for filename in glob.glob(os.path.join(dbPath, STAR + IMG_TIF_TYPE)):
        print("Filename: ", filename)
        dest_img = cv2.imread(filename)  # read a new image
        ###dest_img = cv2.morphologyEx(dest_img, cv2.MORPH_CLOSE, kernel)  # clean image by morphology method
        mse_before_threshold = mse(source_img, dest_img)  # calculate MSE function
        print("MSE before threshold: ", mse_before_threshold)

        thresh_dest_img = findThreshold(dest_img)  # find threshold of current image in DB
        mse_after_threshold = mse(thresh_source_img, thresh_dest_img)  # calculate MSE function
        print("MSE after threshold: ", mse_after_threshold)

        print("index: ", i, "\n")
        i += 1
        #if i > 6:  # if condition to break loop due to runtime
        #    break
        print("----------------------------------------------")

        if mse_before_threshold < constants.THRESHOLD:
            match_img_list.append((filename, dest_img))  # thresh_dest_img

        continue  # break current iteration -prevents error of open-cv

    is_continue = True
    is_empty = False
    ###This if-else loop should be fixed!!!
    if len(match_img_list) < 1:  # if there is no match
        is_empty = True
        is_continue = bool(int(input("No match was found by MSE, do you want to continue?\n1 = Yes, 0 = No\n")))
    ###else:  # if found at least one image that may be matches

    if is_continue:
        if is_empty:
            database_files = glob.glob(os.path.join(DBpath, STAR + IMG_TIF_TYPE))
            database_files = database_files[:3]
            read_files = [cv2.imread(database_file) for database_file in database_files]
            match_img_list = list(zip(database_files, read_files))

        match_list = []  # define a list for matches
        stitcher = Stitcher()  # define a variable of Stitcher class

        i = 0

        for match_img in match_img_list:
            img_name, img_data = match_img
            imagesList = [source_img, img_data]  # thresh_source_img  # define a list of source and destination images to stitch
            # if mse_after_threshold-mse_before_threshold <= 0:
            # stitch the images together to create a panorama
            (result, vis) = stitcher.stitch(imagesList, showMatches=True)
            # else:
            #    result = None

            if not (result is None):  # if succeed to find matches between the two images
                print("Match was found.")
                # cv2.imshow("VIS", vis)
                scipy.misc.imsave(f'vis_{i}' + IMG_TYPE, vis)

                i += 1
                # cv2.imshow("result", result)  # show result image (for check)
                img = Image.fromarray(result, 'RGB')
                # img.show()
                img2 = trim(img)
                # img2.show()
                # cv2.waitKey(0)
                match_list.append(img_name)  # add filename to matches list
            else:
                print("There are not enough matches.")

        print(f"\nFound {len(match_list)} matches as follow:")
        for img_name in match_list:
            print(img_name)







def check_existance_by_stitcher(image, linkImages):
    stitcher = Stitcher()  # define a variable of Stitcher class
    source_img = cv2.imread(image)

    for linkId, linkImage_filename in linkImages:
        img = cv2.imread(linkImage_filename)  # read linked image from path
        #linkImage = numpy.empty_like(linkImage[0])
        #image = numpy.array(image)
        #print("Linked: ", linkImage, type(linkImage), type(image))
        imagesList = [source_img,
                      img]  # thresh_source_img  # define a list of source and destination images to stitch
        # if mse_after_threshold-mse_before_threshold <= 0:
        # stitch the images together to create a panorama
        (result, vis) = stitcher.stitch(imagesList, showMatches=True)
        # else:
        #    result = None

        if not (result is None):  # if succeed to find matches between the two images
            print("Match was found.")
            # cv2.imshow("VIS", vis)

            # cv2.imshow("result", result)  # show result image (for check)
            img = Image.fromarray(img, 'RGB')
            source_img = Image.fromarray(source_img)#, 'RGB')
            # img.show()
            #img2 = trim(img)
            # img2.show()
            # cv2.waitKey(0)
            return True, source_img, img, linkImage_filename, linkId
    #    else:
    #        print("There are not enough matches.")
    print("There are not enough matches.")
    return False, None, None, None, None




def opening(image, k_value):
    #k_value = 3
    kernel = np.ones((k_value, k_value), np.uint8)
    opening_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    opening_image = cv2.resize(opening_image, (480, 560))
    cv2.imshow("Opening", opening_image)
    return opening_image


def dilation(image, k_value):
    #k_value = 3
    kernel = np.ones((k_value, k_value), np.uint8)
    dilation_image = cv2.dilate(image, kernel, iterations=2)
    dilation_image = cv2.resize(dilation_image, (480, 560))
    cv2.imshow("Dilation", dilation_image)
    return dilation_image


def convert_cv2_to_pil(img):
    # convert cv2 image to pil
    converted_img = Image.fromarray(np.uint8(img))
    return converted_img


def convert_pil_to_cv2(img):
    # convert pil image to cv2
    converted_img = np.array(img)
    return converted_img


def brightness(img, val):
    func_name = "brightness"
    #print(f"In {func_name}")

    enhancer = ImageEnhance.Brightness(img)
    enhance = enhancer.enhance(val)
    return enhance


def clean_noise(img, val):
    func_name = "clean_noise"
    #print(f"In {func_name}")

    # convert pil image to cv2
    pix = np.array(img)
    converted_img = cv2.cvtColor(pix, cv2.COLOR_GRAY2BGR)
    val = int(val)
    inverted_image = cv2.fastNlMeansDenoisingColored(converted_img, None, 5 * val, 5 * val, 3 * val,
                                                     10 * val)
    # convert cv2 image to pil
    #cleaned = ImageTk.PhotoImage(Image.fromarray(inverted_image.astype(np.uint8)))
    cleaned = Image.fromarray(np.uint8(inverted_image))
    return cleaned



def clean_img(image, k_value):
    kernel = (k_value, k_value)  # the dimension of the x and y axis of the kernel.
    cleaned_image = cv2.blur(image, kernel)
    return cleaned_image







# Open image and basic actions
filename = filedialog.askopenfilename(title='Choose a fingerprint')
img = cv2.imread(filename)

img = cv2.resize(img, (480, 560))
dst = cv2.fastNlMeansDenoisingColored(img, None, 15, 15, 11, 32)

pil_img = convert_cv2_to_pil(dst)
bright_img = brightness(pil_img, 1.4)
bright_img.show()

cv2_img = convert_pil_to_cv2(bright_img)
_, mask = cv2.threshold(cv2_img, 100, 255, cv2.THRESH_BINARY_INV)
dilation_image = dilation(mask, 7)


# Clean image
cleaned_img = clean_img(img, 5)
cv2.imshow("Cleaned", cleaned_img)


# MASK
mask_img = dilation_image
print(type(dilation_image))

mask = (mask_img == 0)
new_array = np.copy(cleaned_img)
new_array[mask] = img[mask]
cv2.imshow("New", new_array)
cv2.waitKey(30000)

