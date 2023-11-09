
import datetime
import mysql
import cv2
from PIL import Image
from MongoConnection import MongoDB
from stitch import Stitcher
from CountInterestingPoints import convert_numpy_to_json, convert_json_to_numpy
from globalFunctions import convert_pil_to_cv2
import numpy as np
import pandas as pd

data_title = 'data'
id_title = "_id"
images_title = 'images'
ipoints_title = 'ipoints'
features_title = 'features'
image_format = 'JPEG'

# global table_fingerprint
# global table_users
# global table_idu_idfp
# global table_idfp_idu
# global table_images
# global table_ipoints
# global table_features


def get_table_fingerprint():
    _table_fingerprint = mysql.get_all_data_fingerprint()
    _columns = ['idfp', 'Hand', 'Finger', 'Date', 'Time', 'IdImage', 'IdIpoints', 'IdFeatures', 'Link', 'R1',
                           'R2', 'R3']
    df = pd.DataFrame(list(_table_fingerprint), columns=_columns)
    return df


def get_table_users():
    _table_users = mysql.get_all_data_users()
    _columns = ['idfp', 'FirstName', 'LastName', 'Gender']
    df = pd.DataFrame(list(_table_users), columns=_columns)
    return df


def get_table_idu_idfp():
    _table_idu = mysql.get_all_data_idu_idfp()
    _columns = ['idu', 'idfp']
    df = pd.DataFrame(list(_table_idu), columns=_columns)
    return df


def get_table_idfp_idu():
    _table_idfp = mysql.get_all_data_idfp_idu()
    _columns = ['idfp', 'idu']
    df = pd.DataFrame(list(_table_idfp), columns=_columns)
    return df


def get_table_images(dtype=np.uint8):
    _table_images = mongo_connection.get_all_images()
    _columns = ['idfp', 'IdImage', 'ImageData']

    datalist = list()
    for _image in _table_images:
        temp_tuple = (list(_image.keys())[-1], _image['_id'], convert_json_to_numpy(_image[list(_image.keys())[-1]], images_title, dtype=dtype))
        datalist.append(temp_tuple)
    df = pd.DataFrame(datalist, columns=_columns)
    return df


def get_table_ipoints(dtype=np.uint8):
    _table_ipoints = mongo_connection.get_all_ipoints()
    _columns = ['IdIpoints', 'idfp', 'IpointsData']

    datalist = list()
    for _ipoint in _table_ipoints:
        temp_tuple = (_ipoint['_id'],
                      list(_ipoint.keys())[-1],
                      convert_json_to_numpy(_ipoint[list(_ipoint.keys())[-1]], ipoints_title, dtype=dtype))
        datalist.append(temp_tuple)
    df = pd.DataFrame(datalist, columns=_columns)
    return df


def get_table_features(dtype=np.uint8):
    _table_features = mongo_connection.get_all_features()
    _columns = ['idfp', 'IdFeatures', 'FeaturesData']

    datalist = list()
    for _feature in _table_features:
        temp_tuple = (list(_feature.keys())[-1], _feature['_id'],
                      convert_json_to_numpy(_feature[list(_feature.keys())[-1]], features_title, dtype=dtype))
        datalist.append(temp_tuple)
    df = pd.DataFrame(datalist, columns=_columns)
    return df



def add_fingerprint(uid, hand, finger, date, time, filepath, first_name, last_name, gender,
                    link=None, r1=None, r2=None, r3=None):
    status = False
    idfp = mysql.add_new_user(uid)
    ipoints, features = stitcher.get_interesting_points_by_path(filepath)
    json_data_ip = convert_numpy_to_json(ipoints, ipoints_title)
    json_data_f = convert_numpy_to_json(features, features_title)

    if idfp != -1 and json_data_ip is not None and json_data_f is not None:
        idfp_str = str(idfp)
        image_id = mongo_connection.insert_image(filepath, idfp_str)
        ipoint_id = mongo_connection.insert_ipoints(json_data_ip, idfp_str)
        feature_id = mongo_connection.insert_features(json_data_f, idfp_str)

        if image_id != -1 and ipoint_id != -1 and feature_id != -1:
            status = mysql.add_fingerprint(idfp, hand, finger, date, time, image_id, ipoint_id, feature_id,
                        link=link, r1=r1, r2=r2, r3=r3)
            mysql.create_user(idfp, first_name, last_name, gender)

    if status:
        print("New fingerprint data was saves successfully")
    else:
        print("Error occurred while saving a new fingerprint")

def delete_user(userid):
    func_name = "delete_user"
    #print(f"In {func_name}")

    idfp = mysql.get_idfp_by_userid(userid)
    mysql.delete_from_idfp(userid)
    mysql.delete_from_idu(idfp)
    mysql.delete_from_users(idfp)
    mysql.delete_data_from_mongodb_by_id(idfp)
    mysql.delete_fingerprints_by_id(idfp)


def fill_table_using_old_data():
    old_data = mysql.get_data_fingerprint_old201123()
    for od in old_data:
        print(od)
        idu, hand, finger, date, time, link_image = od
        first_name, last_name, gender = mysql.get_user_by_id(idu)
        add_fingerprint(idu, hand, finger, date, time, link_image, first_name, last_name, gender)


def empty_tables():
    users = mysql.get_all_data_users()
    for od in users:
        print(od)
        idfp, _, _, _ = od
        uid = mysql.get_userid_by_idfp(idfp)
        delete_user(uid)


def sep_img(img):
    sep = len(img)//2
    return img[:sep], img[sep:]


def union_img(data: tuple) -> np.ndarray:
    return np.vstack(data)


def oids_to_str(oids):
    soid = ''
    for oid in oids:
        soid += str(oid) + '|'
    return soid[:-1]


def str_to_oids(oids_str):
    return oids_str.split('|')


def read_img_by_oids(oids, idfp):
    imgs = tuple()

    oids = str_to_oids(oids)

    for _id in oids:
        img = mongo_connection.get_image(_id, idfp, convert_json_to_numpy, dtype=np.uint8)
        imgs += (img, )

    union = union_img(imgs)
    return union

def get_img_by_oids(oids, idfp):
    imgs = tuple()

    oids = str_to_oids(oids)

    for _id in oids:
        print(_id)
        print(idfp)
        img = get_image(_id, idfp)
        imgs += (img, )

    union = union_img(imgs)
    return union


def insert_sep_images(img, idfp):
    seps = sep_img(img)
    ids = []

    for _sep in seps:
        json_data_im = convert_numpy_to_json(_sep, images_title)
        idimage = mongo_connection.insert_image(json_data_im, idfp)
        ids.append(idimage)

    soid = oids_to_str(ids)
    return soid


hands = {'L': ' Left', 'R': ' Right', 'l': ' Left', 'r': ' Right'}
fingers = {1: " thumb", 2: " index finger", 3: " middle finger", 4: " ring finger", 5: " little finger"}

def get_all_tables():
    global table_fingerprint
    global table_users
    global table_idu_idfp
    global table_idfp_idu
    global table_images
    global table_ipoints
    global table_features

    table_fingerprint = get_table_fingerprint()
    # table_users = get_table_users()
    # table_idu_idfp = get_table_idu_idfp()
    # table_idfp_idu = get_table_idfp_idu()
    table_images = get_table_images()
    # table_ipoints = get_table_ipoints()
    # table_features = get_table_features()


def get_interesting_points_by_hand_and_finger(hand, finger):
    func_name = "get_interesting_points_by_hand_and_finger"
    #print(f"In {func_name}")

    _rows = table_fingerprint[table_fingerprint['Hand'].str.contains(hand) & table_fingerprint['Finger'].str.contains(finger)]
    return _rows

def get_ipoints(id_ipoints, idfp):
    _ipoints = table_ipoints[
        table_ipoints['IdIpoints'].astype(str).str.contains(id_ipoints) & table_ipoints['idfp'].astype(str).str.contains(idfp)].loc[0]['IpointsData']
    return _ipoints

def get_features(id_ipoints, idfp):
    _features = table_features[
        table_features['IdFeatures'].astype(str).str.contains(id_ipoints) & table_features['idfp'].astype(str).str.contains(idfp)].loc[0]['FeaturesData']
    return _features


def get_image(oid, idfp):
    _image = table_images[
        table_images['IdImage'].astype(str).str.contains(oid) & table_images['idfp'].astype(
            str).str.contains(idfp)].loc[0]['ImageData']
    return _image


def run_system_by_db():
    while True:
        filename = input("Pls insert filename: ")
        hand = input('Choose hand(R/L): ')
        finger = int(input('Choose finger(1-5): '))
        is_there_match = False
        match_to = None
        if hand in hands.keys() and finger in fingers.keys():
            new_img = cv2.imread(filename)
            new_img = convert_pil_to_cv2(new_img)
            hand = hands[hand]
            finger = fingers[finger]
            kpsA, featuresA = stitcher.get_interesting_points_by_img(new_img)

            # json_data_im = convert_numpy_to_json(new_img, images_title)
            json_data_ip = convert_numpy_to_json(kpsA, ipoints_title)
            json_data_f = convert_numpy_to_json(featuresA, features_title)

            all_in_db = mysql.get_interesting_points_by_hand_and_finger(hand, finger)
            for fp in all_in_db:
                idfp, id_image, id_ipoints, id_features = fp
                # img = mongo_connection.get_image(id_image, idfp, convert_json_to_numpy)
                kpsB = mongo_connection.get_ipoints(id_ipoints, idfp, convert_json_to_numpy)
                featuresB = mongo_connection.get_features(id_features, idfp, convert_json_to_numpy)
                M = stitcher.stitch_ips(kpsA, featuresA, kpsB, featuresB)

                if M is not None:
                    if match_to is None:
                        match_to = idfp
                    elif match_to != idfp:
                        match_to = -1
                    matches, H, status = M

                    img = read_img_by_oids(id_image, idfp)

                    # print(type(new_img))
                    # print(new_img.shape)
                    # print(type(img))
                    # print(img.shape)
                    #
                    # shape = new_img.shape
                    # strides = new_img.strides
                    # img = np.lib.stride_tricks.as_strided(img, shape, strides)
                    # print(img.shape)

                    result = stitcher.get_result(new_img, img, H)
                    # result = stitcher.get_result(img, img, H)
                    vis = stitcher.get_vis(new_img, img, kpsA, kpsB, matches, status)
                    # vis = stitcher.get_vis(img, img, kpsA, kpsB, matches, status)

                    # _result = Image.fromarray(result, 'RGB')
                    _vis = Image.fromarray(vis, 'RGB')
                    # _img = Image.fromarray(img, 'RGB')
                    # _new_img = Image.fromarray(new_img)

                    # vis = vis.resize((500, 250), Image.ANTIALIAS)
                    # _result.show()
                    _vis.show()
                    # _img.show()
                    # _new_img.show()

            if match_to is not None and match_to > 0:
                is_there_match = True
            if is_there_match:
                print(f"Match was found to idfp: {match_to}.")
                is_add = input('Do you want to add the new image to this user? (Y/N)')

                if is_add == 'Y' or is_add == 'y':
                    date = datetime.datetime.now().date()
                    time = datetime.datetime.now().time()
                    # idimage = mongo_connection.insert_image(filename, match_to)
                    # idimage = mongo_connection.insert_image(json_data_im, match_to)
                    idimage = insert_sep_images(new_img, match_to)
                    idipoints = mongo_connection.insert_ipoints(json_data_ip, match_to)
                    idfeatures = mongo_connection.insert_features(json_data_f, match_to)
                    status = mysql.add_fingerprint(match_to, hand, finger, date, time, idimage, idipoints, idfeatures)
                    if status:
                        print("The image was saved successfully")
                    else:
                        print("The image was not saved")
                else:
                    print("Ok the image won't be saved")
            else:
                print(f"No match was found.")
                is_add = input('Do you want to add the new image to the DB? (Y/N)')

                if is_add == 'Y' or is_add == 'y':
                    uid = input("Please insert user ID: ")
                    first_name = input("First name: ")
                    last_name = input("Last name: ")
                    gender = input("Gender: (male/female)")
                    idfp = mysql.add_new_user(uid)
                    if idfp > 0:
                        mysql.create_user(idfp, first_name, last_name, gender)
                        date = datetime.datetime.now().date()
                        time = datetime.datetime.now().time()
                        # idimage = mongo_connection.insert_image(filename, idfp)
                        # idimage = mongo_connection.insert_image(json_data_im, idfp)
                        idimage = insert_sep_images(new_img, idfp)
                        idipoints = mongo_connection.insert_ipoints(json_data_ip, idfp)
                        idfeatures = mongo_connection.insert_features(json_data_f, idfp)
                        status = mysql.add_fingerprint(idfp, hand, finger, date, time, idimage, idipoints,
                                                       idfeatures)
                        if status:
                            print("The image was saved successfully")
                        else:
                            print("The image was not saved")
                    else:
                        print("Couldn't add a new user to DB")
                else:
                    print("Ok the image won't be saved")


        else:
            print('Any of hand or finger is not valid. PLease try again.')


def run_system_by_system():
    while True:
        filename = input("Pls insert filename: ")
        hand = input('Choose hand(R/L): ')
        finger = int(input('Choose finger(1-5): '))
        is_there_match = False
        match_to = None
        if hand in hands.keys() and finger in fingers.keys():
            new_img = cv2.imread(filename)
            new_img = convert_pil_to_cv2(new_img)
            hand = hands[hand]
            finger = fingers[finger]
            kpsA, featuresA = stitcher.get_interesting_points_by_img(new_img)

            # json_data_im = convert_numpy_to_json(new_img, images_title)
            json_data_ip = convert_numpy_to_json(kpsA, ipoints_title)
            json_data_f = convert_numpy_to_json(featuresA, features_title)

            all_in_db = get_interesting_points_by_hand_and_finger(hand, finger)
            for fp in all_in_db:
                idfp, id_image, id_ipoints, id_features = fp
                kpsB = get_ipoints(id_ipoints, idfp)
                featuresB = get_features(id_features, idfp)
                M = stitcher.stitch_ips(kpsA, featuresA, kpsB, featuresB)

                if M is not None:
                    if match_to is None:
                        match_to = idfp
                    elif match_to != idfp:
                        match_to = -1
                    matches, H, status = M

                    img = read_img_by_oids(id_image, idfp)

                    # print(type(new_img))
                    # print(new_img.shape)
                    # print(type(img))
                    # print(img.shape)
                    #
                    # shape = new_img.shape
                    # strides = new_img.strides
                    # img = np.lib.stride_tricks.as_strided(img, shape, strides)
                    # print(img.shape)

                    result = stitcher.get_result(new_img, img, H)
                    # result = stitcher.get_result(img, img, H)
                    vis = stitcher.get_vis(new_img, img, kpsA, kpsB, matches, status)
                    # vis = stitcher.get_vis(img, img, kpsA, kpsB, matches, status)

                    # _result = Image.fromarray(result, 'RGB')
                    _vis = Image.fromarray(vis, 'RGB')
                    # _img = Image.fromarray(img, 'RGB')
                    # _new_img = Image.fromarray(new_img)

                    # vis = vis.resize((500, 250), Image.ANTIALIAS)
                    # _result.show()
                    _vis.show()
                    # _img.show()
                    # _new_img.show()

            if match_to is not None and match_to > 0:
                is_there_match = True
            if is_there_match:
                print(f"Match was found to idfp: {match_to}.")
                is_add = input('Do you want to add the new image to this user? (Y/N)')

                if is_add == 'Y' or is_add == 'y':
                    date = datetime.datetime.now().date()
                    time = datetime.datetime.now().time()
                    # idimage = mongo_connection.insert_image(filename, match_to)
                    # idimage = mongo_connection.insert_image(json_data_im, match_to)
                    idimage = insert_sep_images(new_img, match_to)
                    idipoints = mongo_connection.insert_ipoints(json_data_ip, match_to)
                    idfeatures = mongo_connection.insert_features(json_data_f, match_to)
                    status = mysql.add_fingerprint(match_to, hand, finger, date, time, idimage, idipoints, idfeatures)
                    if status:
                        print("The image was saved successfully")
                    else:
                        print("The image was not saved")
                else:
                    print("Ok the image won't be saved")
            else:
                print(f"No match was found.")
                is_add = input('Do you want to add the new image to the DB? (Y/N)')

                if is_add == 'Y' or is_add == 'y':
                    uid = input("Please insert user ID: ")
                    first_name = input("First name: ")
                    last_name = input("Last name: ")
                    gender = input("Gender: (male/female)")
                    idfp = mysql.add_new_user(uid)
                    if idfp > 0:
                        mysql.create_user(idfp, first_name, last_name, gender)
                        date = datetime.datetime.now().date()
                        time = datetime.datetime.now().time()
                        # idimage = mongo_connection.insert_image(filename, idfp)
                        # idimage = mongo_connection.insert_image(json_data_im, idfp)
                        idimage = insert_sep_images(new_img, idfp)
                        idipoints = mongo_connection.insert_ipoints(json_data_ip, idfp)
                        idfeatures = mongo_connection.insert_features(json_data_f, idfp)
                        status = mysql.add_fingerprint(idfp, hand, finger, date, time, idimage, idipoints,
                                                       idfeatures)
                        if status:
                            print("The image was saved successfully")
                        else:
                            print("The image was not saved")
                    else:
                        print("Couldn't add a new user to DB")
                else:
                    print("Ok the image won't be saved")


        else:
            print('Any of hand or finger is not valid. PLease try again.')




if __name__ == '__main__':
    stitcher = Stitcher()
    mongo_connection = MongoDB()
    # empty_tables()
    # fill_table_using_old_data()
    # delete_user(1)
    # mysql.delete_fingerprints_by_id(207)
    # mongo_connection.delete_all_images()
    # run_system_by_system()


    get_all_tables()
    print(table_fingerprint)
    # print(table_users)
    # print(table_idu_idfp)
    # print(table_idfp_idu)
    print(table_images)
    # print(table_ipoints)
    # print(table_features)
    # hand, finger = ' Left', ' index finger'
    # print(get_interesting_points_by_hand_and_finger(hand, finger))
    # idipoints, idfp = '64eb30d027e36817c2d6a0b6', '212'
    # print(get_ipoints(idipoints, idfp))
    # idfeatures, idfp = '64eb30d227e36817c2d6a0b7', '212'
    # print(get_features(idfeatures, idfp))

    idimage, idfp = '64eb305127e36817c2d6a0b4|64eb309d27e36817c2d6a0b5', '212'
    img = get_img_by_oids(idimage, idfp)
    _img = Image.fromarray(img, 'RGB')
    _img.show()

    # oid = '64e1fc6411e5fbe68be55962'
    # idfp = 210
    # print(type(mongo_connection.get_image(oid, idfp)))

# Run stopped here:
# (13, ' Left', ' thumb', datetime.date(2023, 2, 21), datetime.timedelta(seconds=54790), 'results/ACL1.tif')
# Error occurred in function insert_image: you are over your space quota, using 513 MB of 512 MB, full error: {'ok': 0, 'errmsg': 'you are over your space quota, using 513 MB of 512 MB', 'code': 8000, 'codeName': 'AtlasError'}
# Row number 143 in old db
