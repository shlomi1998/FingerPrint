from Client import *
import sys
import datetime


def main():
    start_time = time.time()
    filename = OpenFile()
    [imgFilename, imgDir, imgPath, imgPrefix] = getInputImage(filename)  # convert the path into strings data
    [person, hand, finger, inStandard] = extractFingerDataFromFilename(imgPrefix)  # convert finger data and extract

    filePath = imgPath + imgFilename
    source_img = cv2.imread(filePath)  # read source file from path

    orig_stdout = sys.stdout
    file = open(f'{imgFilename[:-4]}.txt', 'a')
    sys.stdout = file


    print(f"On {datetime.date.today():%d/%m/%Y} {datetime.datetime.now():%H:%M:%S}")  # keep date and time of run

    print(f"Filename: {filePath}")  # print chosen file

    dbPath = DBpath  # get DB path from globalFunctions file

    thresh_source_img = findThreshold(source_img)  # find threshold of source image
    print(f"DB path: {dbPath}\n")  # print DB path

    match_img_list, mse_img_list = CreateMatchImgListByMSE(source_img)
    is_continue, match_img_list_len = IsContinue(match_img_list)

    if is_continue:
        if match_img_list_len < 1:
            match_img_list = CreateFullImgList()

        match_list = CreateMatchImgListByStitcher(source_img, match_img_list)
        PrintDetailsOfMatches(match_list)
    else:
        print("You asked not to continue. Run is stopped.\n")

    print("\nRun time: --- %s seconds ---" % (time.time() - start_time))
    print("\n==============================================")

    sys.stdout = orig_stdout
    file.close()

    return f'{imgFilename[:-4]}.txt', mse_img_list, match_list


if __name__ == '__main__':
    main()

