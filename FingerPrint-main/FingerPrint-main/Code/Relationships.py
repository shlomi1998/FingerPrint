from Client import *
import sys
import datetime
from Main import main as Main


def main():
    filename, mse_img_list, stitch_img_list = Main()

    print(filename)
    print(mse_img_list)
    mse_img_list.sort(key=lambda x: x[1])
    print(mse_img_list)
    print(stitch_img_list)





    is_check = False
    items_to_check = ["HH", "YH", "CH", "AH", "ym", "dmrm", "ZM"]
    titles = ["Filename: ", "MSE before threshold: "]

    if any(item in filename for item in items_to_check):
            is_check = True

    if is_check:
        with open(filename, "tr") as file:
            file_lines = reversed(file.readlines())
            is_keep = False

            for line in file_lines:
                if line == "Start":
                    is_keep = False
                    break
                elif line == "End":
                    is_keep = True
                elif is_keep:
                    if titles[0] in line:
                        current_filename = line.split("\\")[-1]
                        if any(item in current_filename for item in items_to_check):
                            pass








if __name__ == '__main__':
    main()


