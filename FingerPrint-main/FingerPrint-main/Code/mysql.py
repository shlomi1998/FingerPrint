
from MongoConnection import MongoDB
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()

# Open database connection
#db = MySQLdb.connect(
try:
    db = pymysql.connect(
        host="localhost",
        user="root",
        passwd="1234",
        db="db1"
       )
except:
    while(True):
        password = input("Please insert password of DB: ")
        try:
            db = pymysql.connect(
                host="localhost",
                user="root",
                passwd=password,
                db="db1"
            )
            break
        except:
            print("Password is wrong.")

print(f"DB is: {db}")
cursor = db.cursor()



def create_table(table_name):
    f"""
    CREATE TABLE `db1`.`{table_name}` (
  `user_id` INT NOT NULL,
  `interesting_points` JSON NULL,
  `features` JSON NULL);
    """

"""

"""

"""
    CREATE TABLE `db1`.`fingerprint` (
      `IdFingerPrint` INT(11) NOT NULL AUTO_INCREMENT,
      `IdUser` INT(11) NOT NULL,
      `Hand` VARCHAR(45) NOT NULL,
      `Finger` VARCHAR(45) NOT NULL,
      `Date` DATE NOT NULL,
      `Time` TIME NOT NULL,
      `LinkImage` VARCHAR(1024) NULL DEFAULT NULL,
      `Details` JSON NOT NULL,
      `InterestingPoints` JSON NOT NULL,
      `Features` JSON NOT NULL,
      PRIMARY KEY (`IdFingerPrint`),
      UNIQUE INDEX `IdFingerPrint_UNIQUE` (`IdFingerPrint` ASC) VISIBLE)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8mb4
    COLLATE = utf8mb4_0900_ai_ci;
"""

"""
ALTER TABLE `db1`.`fingerprint` 
ADD COLUMN `Reserved1` TEXT(20) NULL DEFAULT NULL AFTER `Features`,
ADD COLUMN `Reserved2` TEXT(20) NULL DEFAULT NULL AFTER `Reserved1`,
ADD COLUMN `Reserved3` TEXT(20) NULL DEFAULT NULL AFTER `Reserved2`;

"""

"""
CREATE TABLE `db1`.`fingerprint` (
  `IdFingerPrint` INT NOT NULL,
  `Hand` VARCHAR(5) NOT NULL,
  `Finger` VARCHAR(15) NOT NULL,
  `Date` DATE NOT NULL,
  `Time` TIME NOT NULL,
  `LinkImage` VARCHAR(2083) NOT NULL,
  `Reserved1` VARCHAR(10) NULL DEFAULT NULL,
  `Reserved2` VARCHAR(10) NULL DEFAULT NULL,
  `Reserved3` VARCHAR(10) NULL DEFAULT NULL,
  PRIMARY KEY (`IdFingerPrint`),
  UNIQUE INDEX `IdFingerPrint_UNIQUE` (`IdFingerPrint` ASC) VISIBLE);

"""

def close_db():
    func_name = "close_db"
    #print(f"In {func_name}")

    global db
    db.close()


def find_date(date):
    func_name = "find_date"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM users,fingerprint' \
          f' WHERE fingerprint.Date="{date}" AND users.ID=fingerprint.IdUser ;'

    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print("Could not find Date")
        else:
            print(f"Found date: {date}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def find_hand(hand):
    func_name = "find_hand"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM users,fingerprint' \
          f' WHERE fingerprint.Hand="{hand}" AND users.ID=fingerprint.IdUser ;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print("Could not find Hand")
        else:
            print(f"Found hand: {hand}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


##################################################
def find_finger(finger):
    func_name = "find_finger"
    #print(f"In {func_name}")

    global db

    sql = f'SELECT * FROM users,fingerprint' \
          f' WHERE fingerprint.Finger={finger} AND users.ID=fingerprint.IdUser ;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print("Could not find Finger")
        else:
            print(f"Found finger {finger}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def find_finger_and_hand(hand, finger):
    func_name = "find_finger_and_hand"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM users,fingerprint' \
          f' WHERE fingerprint.Finger={finger} AND fingerprint.Hand="{hand}" AND users.ID=fingerprint.IdUser ;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print("Could not find Hand and Finger")
        else:
            print(f"Found hand {hand} and finger {finger}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_full_name_by_id(id):
    func_name = "get_full_name_by_id"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT FirstName, LastName FROM users' \
          f' WHERE users.ID={id};'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()
        if res == ():
            print("Could not find user's full name")
            return None
        else:
            print(f"Found id: {id}\n")
            # print(f"Result from DB: {res}")
            db.commit()  # Commit changes to database
            return res[0][0], res[0][1]
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")

def get_user_by_id(id):
    func_name = "get_full_name_by_id"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT FirstName, LastName, Gender FROM users' \
          f' WHERE users.ID={id};'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()
        if res == ():
            print("Could not find user's full name")
            return None
        else:
            print(f"Found id: {id}\n")
            # print(f"Result from DB: {res}")
            db.commit()  # Commit changes to database
            return res[0][0], res[0][1]
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_first_name(id):
    func_name = "get_first_name"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT FirstName FROM users,fingerprint' \
          f' WHERE users.ID={id} AND fingerprint.IdUser={id};'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()
        if res == ():
            print("Could not find First name")
            return None
        else:
            print(f"Found id: {id}\n")
            # print(f"Result from DB: {res}")
            db.commit()  # Commit changes to database
            return res[0][0]
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_last_name(id):
    func_name = "get_last_name"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT LastName FROM users,fingerprint' \
          f' WHERE users.ID={id} AND fingerprint.IdUser={id};'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()
        if res == ():
            print("Could not find Last name")
            return None
        else:
            print(f"Found id {id}:\n")
            # print(f"Result from DB: {res}")
            db.commit()  # Commit changes to database
            return res[0][0]
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def find_id(id):
    func_name = "find_id"
    #print(f"In {func_name}")

    global db

    sql = f'SELECT * FROM users,fingerprint' \
          f' WHERE users.ID={id} AND fingerprint.IdUser={id};'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()
        if res == ():
            print("Could not find ID")
        else:
            print(f"Found id {id}:\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def delete_fingerprints_by_id(idfp):
    func_name = "delete_fingerprints_by_id"
    #print(f"In {func_name}")

    global db
    sql = f'DELETE FROM db1.fingerprint WHERE IdFingerPrint={idfp};'
    try:
        cursor.execute(sql)  # execute SQL command
        db.commit()  # commit changes to database
        return True
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")
        return False

def delete_from_idfp(userid):
    func_name = "delete_from_idfp"
    # print(f"In {func_name}")

    global db
    sql = f'DELETE FROM db1.idfp_idu WHERE idfp_idu.IdUser={userid};'
    try:
        cursor.execute(sql)  # execute SQL command
        print(f"user id={userid} delete")
        db.commit()  # commit changes to database
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def delete_from_idu(idfp):
    func_name = "delete_from_idfp"
    # print(f"In {func_name}")

    global db
    sql = f'DELETE FROM db1.idu_idfp WHERE idu_idfp.IdFingerPrint={idfp};'
    try:
        cursor.execute(sql)  # execute SQL command
        print(f"user id={idfp} delete")
        db.commit()  # commit changes to database
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")

def delete_from_users(idfp):
    func_name = "delete_from_idfp"
    # print(f"In {func_name}")

    global db
    sql = f'DELETE FROM db1.users WHERE users.IdFingerPrint={idfp};'
    try:
        cursor.execute(sql)  # execute SQL command
        print(f"user id={idfp} delete")
        db.commit()  # commit changes to database
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_mongodb_data_by_idfp(idfp):
    func_name = "get_interesting_points_by_id"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT IdImage, IdIpoints, IdFeatures ' \
        f'FROM db1.fingerprint ' \
          f'WHERE db1.fingerprint.IdFingerPrint={idfp};'

    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find user's mondoDB data\n")
        else:
            print(f"Found user's mongoDB data that match to idfp: {idfp}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")



def delete_data_from_mongodb_by_id(idfp):
    func_name = "delete_data_from_mongodb_by_id"
    # print(f"In {func_name}")

    mongodb_data = get_mongodb_data_by_idfp(idfp)
    print(mongodb_data)
    if mongodb_data is not None:
        mongo_connection = MongoDB()
        for id_image, id_ipoints, id_features in mongodb_data:
            print(id_image)
            print(id_ipoints)
            print(id_features)
            r1 = mongo_connection.delete_image(id_image)
            print(r1)
            r1 = mongo_connection.delete_ipoints(id_ipoints)
            print(r1)
            r1 = mongo_connection.delete_features(id_features)
            print(r1)


# delete_data_from_mongodb_by_id(7)

def create_user(idfp, first_name, last_name, gender):
    func_name = "create_user"
    #print(f"In {func_name}")

    global db
    sql = f'INSERT INTO db1.users (IdFingerPrint, FirstName, LastName, Gender) VALUES  ("{int(idfp)}","{first_name}", "{last_name}","{gender}")'

    try:
        cursor.execute(sql)  # execute SQL command
        db.commit()  # commit changes to database
        print("New user created\n")
        return True
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")
        return False


def add_fingerprint(idfp, hand, finger, date, time, idimage, idipoints, idfeatures,
                    link=None, r1=None, r2=None, r3=None):
    func_name = "add_fingerprint"
    #print(f"In {func_name}")

    global db
    sql = f'INSERT INTO db1.fingerprint (IdFingerPrint, Hand, Finger, Date, Time, ' \
        f'IdImage, IdIpoints, IdFeatures, LinkImage, Reserved1, Reserved2, Reserved3)' \
        f' VALUES ("{idfp}", "{hand}", "{finger}", "{date}", "{time}", "{idimage}", "{idipoints}", "{idfeatures}",' \
        f' "{link}", "{r1}", "{r2}", "{r3}")'

    try:
        cursor.execute(sql)  # execute SQL command
        db.commit()  # Commit changes to database
        return True
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")
        return False


def add_new_user_fp(iduser):
    func_name = "add_new_user_fp"
    #print(f"In {func_name}")

    global db
    sql = f'INSERT INTO db1.idfp_idu (IdUser) VALUES ("{iduser}")'

    try:
        cursor.execute(sql)  # execute SQL command
        index = cursor.lastrowid
        db.commit()  # Commit changes to database
        return index
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")
        return -1


def add_new_user_index(iduser, idfingerprint):
    func_name = "add_new_user_index"
    #print(f"In {func_name}")

    global db
    sql = f'INSERT INTO db1.idu_idfp (IdUser, IdFingerPrint) VALUES ("{iduser}", "{idfingerprint}")'

    try:
        cursor.execute(sql)  # execute SQL command
        db.commit()  # Commit changes to database
        return True
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")
        return False


def add_new_user(iduser):
    func_name = "add_new_user"
    # print(f"In {func_name}")

    index = add_new_user_fp(iduser)
    if index > 0:
        status = add_new_user_index(iduser, index)
        if status:
            return index
        else:
            print("Cannot add a new user with index to DB")
            return -1
    else:
        index = get_idfp_by_userid(iduser)
        if index is not None:
            return index
        print("Cannot add a new user to DB")
        return -1

def get_idfp_by_userid(userid):
    func_name = "get_idfp_by_userid"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT IdFingerPrint FROM idfp_idu' \
          f' WHERE idfp_idu.IdUser={userid};'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()
        if res == ():
            print("Could not find fingerprint id")
            return None
        else:
            print(f"Found id {userid}: {res[0][0]}\n")
            # print(f"Result from DB: {res}")
            db.commit()  # Commit changes to database
            return res[0][0]
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")
        return None

def get_userid_by_idfp(idfp):
    func_name = "get_userid_by_idfp"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT IdUser FROM idu_idfp' \
          f' WHERE idu_idfp.IdFingerPrint={idfp};'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()
        if res == ():
            print("Could not find user id")
            return None
        else:
            print(f"Found id {idfp}:\n")
            # print(f"Result from DB: {res}")
            db.commit()  # Commit changes to database
            return res[0][0]
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")



# iduser = 1234
# index = add_new_user(iduser)
# index = 1
# add_new_user_index(iduser, index)

def print_all_users():
    func_name = "print_all_users"
    #print(f"In {func_name}")

    num_row = cursor.execute('SELECT * FROM db1.users')
    print(num_row)
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        first_name = row[1]
        last_name = row[2]
        gender = row[3]
        # hand = row[4]
        # finger = row[5]
        # data = row[6]
        # time = row[7]
        # code = row[8]
        # Now print fetched result
        print(f'id ={id}, first_name={first_name}, last_name={last_name}, gender={gender}\n')
        # , hand = {hand}, finger = {finger}, data = {data}, time = {time}, code = {code}\n
        # ')


def save_tables_in_excel():
    func_name = "save_tables_in_excel"
    #print(f"In {func_name}")

    file_name = 'save_db.xlsx'

    with pd.ExcelWriter(file_name) as writer:
        sql = 'SELECT * FROM db1.users'
        df = pd.read_sql_query(sql, db)
        df.to_excel(writer, sheet_name='users')
        # ------------------------
        sql = 'SELECT * FROM db1.fingerprint'
        df = pd.read_sql_query(sql, db)
        df.to_excel(writer, sheet_name='fingerprint')
        # ------------------------
        sql = 'SELECT * FROM db1.user_relationships'
        df = pd.read_sql_query(sql, db)
        df.to_excel(writer, sheet_name='user_relationships')
        # ------------------------
        sql = 'SELECT * FROM db1.idfp_idu'
        df = pd.read_sql_query(sql, db)
        df.to_excel(writer, sheet_name='idfp_idu')
        # ------------------------
        sql = 'SELECT * FROM db1.idu_idfp'
        df = pd.read_sql_query(sql, db)
        df.to_excel(writer, sheet_name='idu_idfp')
        # ------------------------
    print("DB saved in excel")


def get_all_fingerprints():
    func_name = "get_all_fingerprints"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT IdUser, LinkImage FROM fingerprint;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find fingerprints\n")
        else:
            print("Found all fingerprints\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_userid_by_linkimage(link_image):
    func_name = "get_userid_by_linkimage"
    #print(f"In {func_name}")

    global db
    image_name = link_image.split('/')
    image_name = '/'.join(part for part in image_name)
    # print("Image name: ", image_name)
    sql = f'SELECT IdUser FROM db1.fingerprint' \
          f' WHERE fingerprint.LinkImage="{image_name}";'

    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find users' ids\n")
        else:
            print(f"Found user's id that match to {link_image}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_userid_by_hand_and_finger(hand, finger):
    func_name = "get_userid_by_hand_and_finger"
    #print(f"In {func_name}")

    global db
    #image_name = link_image.split('/')
    #image_name = '/'.join(part for part in image_name)
    #print("Image name: ", image_name)
    sql = f'SELECT IdUser, LinkImage ' \
        f'FROM db1.fingerprint ' \
          f'WHERE db1.fingerprint.Hand="{hand}" AND db1.fingerprint.Finger="{finger}";'

    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find users' ids\n")
        else:
            print(f"Found user's id that match to hand: {hand}, finger: {finger}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_interesting_points_by_hand_and_finger(hand, finger):
    func_name = "get_interesting_points_by_hand_and_finger"
    #print(f"In {func_name}")
    print(finger)

    global db
    sql = f'SELECT IdFingerPrint, IdImage, IdIpoints, IdFeatures ' \
        f'FROM db1.fingerprint ' \
          f'WHERE db1.fingerprint.Hand="{hand}" AND db1.fingerprint.Finger="{finger}";'

    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find users' ids\n")
        else:
            print(f"Found user's id that match to hand: {hand}, finger: {finger}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")

def get_ip_features_by_hand_and_finger(hand, finger):
    func_name = "get_ip_features_by_hand_and_finger"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT IdUser, Details, InterestingPoints, Features ' \
        f'FROM db1.fingerprint ' \
          f'WHERE db1.fingerprint.Hand="{hand}" AND db1.fingerprint.Finger="{finger}";'

    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find users' ids\n")
        else:
            print(f"Found user's id that match to hand: {hand}, finger: {finger}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_interesting_points_by_id(userid, hand, finger):
    func_name = "get_interesting_points_by_id"
    #print(f"In {func_name}")

    global db
    idfp = get_idfp_by_userid(userid)
    sql = f'SELECT IdImage, IdIpoints, IdFeatures ' \
        f'FROM db1.fingerprint ' \
          f'WHERE db1.fingerprint.IdFingerPrint={idfp} AND db1.fingerprint.Hand="{hand}" AND db1.fingerprint.Finger="{finger}";'

    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find user's interesting points\n")
        else:
            print(f"Found user's interesting points that match to hand: {hand}, finger: {finger}\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_all_data_fingerprint():
    func_name = "get_all_data_fingerprint"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM db1.fingerprint;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find fingerprints\n")
        else:
            print("Found all fingerprints\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_all_data_fingerprint_old():
    func_name = "get_all_data_fingerprint_old"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM fingerprint_old;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find old fingerprints\n")
        else:
            print("Found all old fingerprints\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")

def get_data_fingerprint_old201123():
    func_name = "get_data_fingerprint_old201123"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT IdUser, Hand, Finger, Date, Time, LinkImage FROM fingerprint_201123;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find old fingerprints\n")
        else:
            print("Found all old fingerprints\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_all_data_users():
    func_name = "get_all_fingerprints"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM users;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find users\n")
        else:
            print("Found all users\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")

def get_all_data_user_relationships():
    func_name = "get_all_fingerprints"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM user_relationships;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find user relationships\n")
        else:
            print("Found all user relationships\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_all_data_idu_idfp():
    func_name = "get_all_data_idu_idfp"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM db1.idu_idfp;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find user ids\n")
        else:
            print("Found all user ids\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def get_all_data_idfp_idu():
    func_name = "get_all_data_idfp_idu"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM db1.idfp_idu;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find fingerprint ids\n")
        else:
            print("Found all fingerprint ids\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")


def add_interesting_points_features(iduser, interesting_points, features):
    func_name = "add_interesting_points_features"
    #print(f"In {func_name}")

    global db
    sql = f'INSERT INTO db1.temp_table (user_id, interesting_points, features)' \
        f' VALUES ("{iduser}", %s, %s)'

    try:
        cursor.execute(sql, (interesting_points, features))  # execute SQL command
        db.commit()  # Commit changes to database
        return True
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")
        return False

def get_interesting_points_features():
    func_name = "get_interesting_points_features"
    #print(f"In {func_name}")

    global db
    sql = f'SELECT * FROM temp_table;'
    try:
        cursor.execute(sql)  # execute SQL command
        res = cursor.fetchall()

        if res == ():
            print(f"Could not find temp table\n")
        else:
            print("Found all data in temp table\n")
            # print(f"Result from DB: {res}")
        db.commit()  # commit changes to database
        return res
    except Exception as e:
        print(f"Error in {func_name}: {str(e)}")



# prepare a cursor object using cursor() method

# print(type(num_row))
# add_to_db(db,'22222222',"avi", 'levi', 'm', 'r', '4', '2019-06-04','13:10:00','333')
# add_to_db(db,'12345678', 'noa', 'levi', 'f', 'r', '4', '2019-06-04','18:10:00','222')


# create_user('55555', 'sdfg', 'levi', 'female')
# delete_user('55555')
# add_fingerprint(db,'2222','l', '1', '2019-06-04','18:10:00','','')
# find_finger(db,'4')
# find_hand(db,'r')
# find_id(db,'206221293')
# print_all_users()
# save_tabels_in_excel()
# delete_user(db,'2
# 222')
# find_hand(db,"l")
# find_finger_and_hand('r','4')
# #
# find_id("206221293")



# find_date(db,datetime.date(2019, 6, 4))

# print(datetime.date(2019, 6, 4))

# disconnect from server
# print(get_last_name('206221293'))
# print(get_last_name('111'))
#
# ids = [6, 7, 12, 15, 111, 123, 321, 999, 1000, 1001, 1002, 1234, 4321, 55555, '58082489', '58082490', '58082491', '58082492', '58082493', '58082494', '322346180']
# for id in ids:
#     delete_fingerprint(id)
#     delete_user(id)


