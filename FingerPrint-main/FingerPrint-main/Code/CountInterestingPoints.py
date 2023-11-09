
#Imports:
from stitch import Stitcher
import cv2
from PIL import Image
import json
from json import JSONEncoder, JSONDecoder
import numpy as np
import mysql
from datetime import datetime as dt
from globalFunctions import *




def main():
    # pic1 = "database/1L2.tif"
    # pic2 = "database/1L2_6.tif"
    # pic3 = "database/1L2_4.tif"
    # stitcher = Stitcher()  # define a variable of Stitcher class
    #
    # source_img = cv2.imread(pic1)
    # destination_img = cv2.imread(pic2)
    #
    # result, vis, ipoints, features = stitcher.stitch([source_img, destination_img])
    # # print(result)
    # # print('\n\n\n')
    # # print(vis)
    # # print('\n\n\n')
    # # print(type(ipoints))
    # # print('\n\n\n')
    # # print(type(features))
    # # print('\n\n\n')
    #
    # json_data_ip = convert_numpy_to_json(source_img, 'details')
    # print(json_data_ip)
    # print(len(json_data_ip))
    # numpy_arr = convert_json_to_numpy(json_data_ip, 'details')
    # print(numpy_arr)
    # print(len(numpy_arr))
    #
    #
    # json_data_f = convert_numpy_to_json(features, 'features')
    # # print(json_data_f)
    # # print(len(json_data_f))
    # numpy_arr = convert_json_to_numpy(json_data_f, 'features')
    # # print(numpy_arr)
    # # print(len(numpy_arr))
    #
    # res = mysql.add_interesting_points_features(1, json_data_ip, json_data_f)
    # print(res)

    '''
    start_time = dt.now()

    new_pic = cv2.imread(pic3)
    n_ip, n_f = stitcher.get_interesting_points(new_pic)

    res = mysql.get_interesting_points_features()
    for user_id, ip, features in res:
        # print(user_id)
        try:
            numpy_ip = convert_json_to_numpy(ip, 'interesting_points')
        except:
            numpy_ip = convert_json_to_numpy(ip, 'details')
        try:
            numpy_f = convert_json_to_numpy(features, 'features')
        except:
            numpy_f = convert_json_to_numpy(features, 'interesting_points')

        M = stitcher.stitch_ips(n_ip, n_f, numpy_ip, numpy_f)
        # print(M)


    now_time = dt.now()
    print(f'start_time: {start_time}')
    print(f'now_time: {now_time}')
    print(now_time - start_time)

    start_time = dt.now()

    new_pic = cv2.imread(pic3)
    n_ip, n_f = stitcher.get_interesting_points(new_pic)

    res = mysql.get_interesting_points_features()
    for user_id, ip, features in res:
        source_img = cv2.imread(pic1)
        destination_img = cv2.imread(pic3)
        result, vis, ipoints, features = stitcher.stitch([source_img, destination_img])

    now_time = dt.now()
    print(f'start_time: {start_time}')
    print(f'now_time: {now_time}')
    print(now_time - start_time)
    '''

    # copy_db_with_ips()
    fingerprints = mysql.get_all_data_fingerprint()
    # fingerprints = mysql.get_all_fingerprints()
    print(fingerprints)

    # for _, id_user, hand, finger, date, time, link_image, details, ips, features, _, _, _ in fingerprints:
    # for i in fingerprints:
        # print(id_user, hand, finger, date, time, link_image)
        # print(i)


    # cv2.imshow("result", result)  # show result image (for check)
    # vis = Image.fromarray(vis, 'RGB')
    # destination_img = Image.fromarray(destination_img, 'RGB')
    # source_img = Image.fromarray(source_img)  # , 'RGB')
    # destination_img.show()
    # vis.show()
    # # img2 = trim(destination_img)
    # source_img.show()
    # cv2.waitKey(0)


def copy_db_with_ips():
    old_fingerprints = mysql.get_all_data_fingerprint_old()

    for _, id_user, hand, finger, date, time, link_image, _, _ in old_fingerprints:
        print(id_user, hand, finger, date, time, link_image)
        img = cv2.imread(link_image)
        interesting_points, features = stitcher.get_interesting_points_by_path(img)
        details = convert_numpy_to_json(img, details_title)
        interesting_points = convert_numpy_to_json(interesting_points, ips_title)
        features = convert_numpy_to_json(features, features_title)
        print("Data is ready")

        mysql.add_fingerprint(id_user, hand, finger, date, time, link_image, details, interesting_points, features)

    mysql.close_db()


if __name__ == '__main__':
    pass
    # main()

