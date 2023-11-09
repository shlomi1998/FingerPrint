
import cv2
import numpy as np
from PIL import Image
from globalFunctions import convert_pil_to_cv2, convert_numpy_to_json, convert_json_to_numpy
from MongoConnection import MongoDB
from bson.objectid import ObjectId

images_title = 'images'
ipoints_title = 'ipoints'
features_title = 'features'

mongo_connection = MongoDB()

def sep_img(img):
    sep = len(new_img)//2
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

filename = "database/1L2.tif"
new_img = cv2.imread(filename)
new_img = convert_pil_to_cv2(new_img)

seps = sep_img(new_img)
# print(seps)

ids = []

# for _sep in seps:
#     print(_sep)
#     print('----------------------')
#     json_data_im = convert_numpy_to_json(_sep, images_title)
#     print(json_data_im)
#     print('++++++++++++++++++++++')
#     idimage = mongo_connection.insert_image(json_data_im, 999)
#     ids.append(idimage)

ids = [ObjectId('64eb19c4403702f88d95af00'), ObjectId('64eb19f6403702f88d95af01')]
print(ids)

ostr = oids_to_str(ids)
print(ostr)
print(len(ostr))
stro = str_to_oids(ostr)
print(stro)


imgs = tuple()

for _id in stro:
    img = mongo_connection.get_image(_id, 999, convert_json_to_numpy, dtype=np.uint8)
    print(img)
    print('===================')
    imgs += (img, )


union = union_img(imgs)
print(union)
print(type(union))
print(len(union))
print(union.shape)


_new_img = Image.fromarray(union)
_new_img.show()
