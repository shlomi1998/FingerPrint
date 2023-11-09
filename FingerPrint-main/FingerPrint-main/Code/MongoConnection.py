
# Username: ayatech100
# Password: NqZr7paYpoVpC3xM


# Public Key: cxpoescz
# Private Key: 7d775765-cc96-4edb-a387-9ad601faf5c9

from pymongo import MongoClient
from PIL import Image
import io
import matplotlib.pyplot as plt
from stitch import *
from globalFunctions import convert_numpy_to_json, convert_json_to_numpy
from bson.objectid import ObjectId
from globalFunctions import convert_pil_to_cv2

data_title = 'data'
id_title = "_id"
images_title = 'images'
ipoints_title = 'ipoints'
features_title = 'features'
image_format = 'JPEG'


class MongoDB:
    def __init__(self):
        try:
            self.URI = 'mongodb+srv://ayatech100:NqZr7paYpoVpC3xM@fingerprints.us44mnq.mongodb.net/?retryWrites=true&w=majority'
            self.client = MongoClient(self.URI)
        except:
            while(True):
                username = input("Please insert username of DB: ")
                password = input("Please insert password of DB: ")
                try:
                    self.URI = f'mongodb+srv://{username}:{password}@fingerprints.us44mnq.mongodb.net/?retryWrites=true&w=majority'
                    self.client = MongoClient(self.URI)
                    break
                except:
                    print("Password is wrong.")

        print(f"MongoDB is connected successfully")
        self.db = None
        self.images = None
        self.ipoints = None
        self.features = None

        self.connections()

    def connections(self):
        self.connect_db()
        self.connect_collections()

    def connect_db(self):
        self.db = self.client.db2

    def connect_collections(self):
        self.images = self.db.images
        self.ipoints = self.db.ipoints
        self.features = self.db.features

    def close_session(self):
        self.client.close()

    def insert_image(self, image_data, id_fingerprint):
        try:
            id_fingerprint = str(id_fingerprint)

            image = {
                id_fingerprint: image_data
            }

            image_id = self.images.insert_one(image).inserted_id
            return image_id
        except Exception as e:
            print(f"Error occurred in function insert_image: {e}")
            return -1

    def insert_image_source(self, filepath, id_fingerprint):
        try:
            id_fingerprint = str(id_fingerprint)
            im = Image.open(filepath)

            image_bytes = io.BytesIO()
            im.save(image_bytes, format=image_format)

            image = {
                id_fingerprint: image_bytes.getvalue()
            }

            image_id = self.images.insert_one(image).inserted_id
            return image_id
        except Exception as e:
            print(f"Error occurred in function insert_image: {e}")
            return -1

    def get_image(self, oid, idfp, convert_json_to_numpy, dtype=np.uint8):
        oid = ObjectId(oid)
        idfp = str(idfp)
        _images = [i for i in self.images.find({id_title: oid})]

        if len(_images) > 0:
            numpy_arr = [convert_json_to_numpy(image[idfp], images_title, dtype=dtype) for image in _images]
            return numpy_arr[0]
        return None

    def get_all_images(self):
        _images = [i for i in self.images.find({})]

        return _images

        # print(_images[0].keys())
        #
        # if len(_images) > 0:
        #     numpy_arr = [convert_json_to_numpy(image[image.keys()[-1]], images_title, dtype=dtype) for image in _images]
        #     return numpy_arr
        # return None

    def get_image_source(self, oid, idfp):
        oid = ObjectId(oid)
        idfp = str(idfp)
        _images = [i for i in self.images.find({id_title: oid})]
        pil_img = None

        for _image in _images:
            pil_img = Image.open(io.BytesIO(_image[idfp]))
            plt.imshow(pil_img)
        plt.show()

        # np_data = np.frombuffer(_images[0][idfp])
        if pil_img is not None:
            np_data = convert_pil_to_cv2(pil_img)
            print('from requests', np_data)
            return np_data
        return None

    def delete_image(self, oid):
        try:
            result = self.images.delete_one(
                {
                    id_title: ObjectId(oid)
                })
            return result
        except:
            print(f"Could not delete image of object ID {oid}")

    def delete_all_images(self):
        try:
            result = self.images.delete_many({})
            return result
        except:
            print(f"Could not delete images from MongoDB")

    def insert_ipoints(self, ipoints_data, id_fingerprint):
        try:
            id_fingerprint = str(id_fingerprint)
            ipoint = {
                id_fingerprint: ipoints_data
            }

            ipoint_id = self.ipoints.insert_one(ipoint).inserted_id
            return ipoint_id
        except Exception as e:
            print(f"Error occurred in function insert_ipoints: {e}")
            return -1

    def get_ipoints(self, oid, idfp, convert_json_to_numpy):
        oid = ObjectId(oid)
        idfp = str(idfp)
        _ipoints = [i for i in self.ipoints.find({id_title: oid})]

        if len(_ipoints) > 0:
            numpy_arr = [convert_json_to_numpy(ipoint[idfp], ipoints_title) for ipoint in _ipoints]
            return numpy_arr[0]
        return None

    def get_all_ipoints(self):
        _ipoints = [i for i in self.ipoints.find({})]

        return _ipoints

        # if len(_ipoints) > 0:
        #     numpy_arr = [convert_json_to_numpy(ipoint[idfp], ipoints_title) for ipoint in _ipoints]
        #     return numpy_arr[0]
        # return None

    def delete_ipoints(self, oid):
        try:
            result = self.ipoints.delete_one(
                {
                    id_title: ObjectId(oid)
                })
            return result
        except:
            print(f"Could not delete image of object ID {oid}")


    def delete_all_ipoints(self):
        try:
            result = self.ipoints.delete_many({})
            return result
        except:
            print(f"Could not delete interesting points from MongoDB")

    def insert_features(self, features_data, id_fingerprint):
        try:
            id_fingerprint = str(id_fingerprint)
            feature = {
                id_fingerprint: features_data
            }

            feature_id = self.features.insert_one(feature).inserted_id
            return feature_id
        except Exception as e:
            print(f"Error occurred in function insert_features: {e}")
            return -1

    def get_features(self, oid, idfp, convert_json_to_numpy):
        oid = ObjectId(oid)
        idfp = str(idfp)
        _features = [i for i in self.features.find({id_title: oid})]

        if len(_features) > 0:
            numpy_arr = [convert_json_to_numpy(feature[idfp], features_title) for feature in _features]
            return numpy_arr[0]
        return None

    def get_all_features(self):
        _features = [i for i in self.features.find({})]

        return _features

        # if len(_features) > 0:
        #     numpy_arr = [convert_json_to_numpy(feature[idfp], features_title) for feature in _features]
        #     return numpy_arr[0]
        # return None

    def delete_features(self, oid):
        try:
            result = self.features.delete_one(
                {
                    id_title: ObjectId(oid)
                })
            return result
        except:
            print(f"Could not delete image of object ID {oid}")

    def delete_all_features(self):
        try:
            result = self.features.delete_many({})
            return result
        except:
            print(f"Could not delete features from MongoDB")


def main(idfp):
#     filepath = "database/1L1.tif"
#     pic1 = "database/1L2.tif"
#     pic2 = "database/1L2_6.tif"
#     pic3 = "database/1L2_4.tif"
#     stitcher = Stitcher()  # define a variable of Stitcher class
#
#     source_img = cv2.imread(pic1)
#     destination_img = cv2.imread(pic2)
#
#     result, vis, ipoints, features = stitcher.stitch([source_img, destination_img])
#
#     json_data_ip = convert_numpy_to_json(ipoints, ipoints_title)
#
#     json_data_f = convert_numpy_to_json(features, features_title)
#
    mongo_connection = MongoDB()

    mongo_connection.get_all_images(convert_json_to_numpy)
#
#     # image_id = mongo_connection.insert_image(filepath, idfp)
#     # print(f"Image id is: {image_id}")
#     # # print(f"Image id len is: {len(image_id)}")
#     # print(f"Image id type is: {type(image_id)}")
#     # sid = str(image_id)
#     # # sid = "64b69c4b01daa286c5355f32"
#     # oid2 = ObjectId(sid)
#     #
#     # ipoint_id = mongo_connection.insert_ipoints(json_data_ip, idfp)
#     # print(f"Ipoint id is: {ipoint_id}")
#     # # print(f"Ipoint id len is: {len(ipoint_id)}")
#     # print(f"Ipoint id type is: {type(ipoint_id)}")
#     #
#     # feature_id = mongo_connection.insert_features(json_data_f, idfp)
#     # print(f"Feature id is: {feature_id}")
#     # # print(f"Feature id len is: {len(feature_id)}")
#     # print(f"Feature id type is: {type(feature_id)}")
#     #
#     # print(mongo_connection.get_image(oid2))
#     # print(mongo_connection.get_ipoints(ipoint_id, idfp))
#     # print(mongo_connection.get_features(feature_id, idfp))
#     #
#     #
#     # mongo_connection.delete_features(feature_id)
#     # print(mongo_connection.get_features(feature_id, idfp))
#     #
#     # mongo_connection.close_session()
#
#
if __name__ == '__main__':
    idfp = str(22)
    main(idfp)
#
#     pass

