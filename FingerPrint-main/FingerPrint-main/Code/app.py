
# Imports:
import os, glob
import mysql
from globalFunctions import check_existence_by_stitcher, check_existence_by_ipoints, check_existence_by_c2c, convert_json_to_numpy, convert_numpy_to_json, Titles
from Constants import *
from MongoConnection import MongoDB

'''
The MainApp() function is the main function of the project.
In this function, we define sub-functions that all work together and make the project work. 
'''
def MainApp():
    '''
    def documentation_creat_new_user(first_name, last_name, id, date, gender):
    Brief:
        This function documents new created user into a text file.
    Input:
        -first_name: first name of user.
        -last_name: last name of user.
        -id: ID of user.
        -date: date of taking image.
        -gender: gender of user.
    Output:
        No output.
    '''
    def documentation_creat_new_user(first_name, last_name, id, date, gender):
        func_name = "documentation_creat_new_user"
        #print(f"In {func_name}")

        file_name = "documentation.txt"
        with open(file_name, "a") as text_file:
            text_file.write(f'Creat new user on: {date} \n:'
                            f'First name: {first_name}\n'
                            f'Last name: {last_name}\n'
                            f'ID: {id}\n'
                            f'Gender: {gender}\n'
                            f'------------------------------------------------------------------------\n')
        print(f'Documentation was saved in file name {file_name}')

    '''
        def documentation_fingerprint(first_name, last_name, id, date, time, hand, finger):
        Brief:
            This function documents fingerprint of exists user into a text file.
        Input:
            -first_name: first name of user.
            -last_name: last name of user.
            -id: ID of user.
            -date: date of taking image.
            -time: time of taking image.
            -hand: hand of user which was taken.
            -finger: finger of user which was taken.
        Output:
            No output.
        '''
    def documentation_fingerprint(first_name, last_name, id, date, time, hand, finger):
        func_name = "documentation_fingerprint"
        #print(f"In {func_name}")

        img = root.save_image_name
        file_name = "documentation.txt"

        with open(file_name, "a") as text_file:
            text_file.write(f'Name: {first_name} {last_name} ID: {id}\n'
                            f'Date: {date} Time: {time}\n'
                            f'Image: {img} \n'
                            f'Match to: \n'
                            f'Hand: {hand}, finger:{finger}\n'
                            f'------------------------------------------------------------------------\n')
        print(f'Documentation was saved in file name {file_name}')

    '''
        def check_id_valid():
        Brief:
            This function checks if user's ID is valid.
        Algorithm:
            -Multiply each digit except the last by 1,2,1,2,... Alternately.
            -If multiplication exceeds 10 - sum digits.
            -Sum up all the results of the multiplication.
            -Examine the complement to a multiplication of 10.
        Input:
            No input.
        Output:
            -True: if user's ID is valid.
            -False: if user's ID is not valid.
    '''
    def check_id_valid():
        func_name = "check_id_valid"
        #print(f"In {func_name}")

        id = root.id_text.get()
        id = id.zfill(9)
        _sum = 0
        #
        for i in range(len(id) - 1):
            if i % 2 == 0:  # multiply by 1
                _sum += int(id[i])
            else:  # multiply by 2
                num = int(id[i]) * 2
                if num >= 10:  # if multiplication exceeds 10 - sum digits
                    _sum += num % 10 + num // 10
                else:
                    _sum += num

        # Completion of multiplication 10
        multiplication10 = (_sum // 10 + 1) * 10
        control_digit = multiplication10 - _sum
        if control_digit == int(id[-1]) or (control_digit == 10 and int(id[-1]) == 0):  # control digit is valid
            return True
        else:
            return False  # control digit is NOT valid

    '''
        def ask_check_id():
        Brief:
            This function asks user if he wants to check validation of ID number.
        Input:
            No input.
        Output:
            No output.
    '''
    def ask_check_id():
        func_name = "ask_check_id"
        #print(f"In {func_name}")

        answer = tk.messagebox.askquestion("Check ID", "Do you want to check if ID number is valid??", icon='warning')

        if answer == 'yes':  # if user wants to check ID number
            is_valid_id = check_id_valid()
            if is_valid_id:  # id ID number is valid - save user
                save_user()
            else:
                messagebox.showwarning("Warning", "Invalid ID number, Please enter a valid ID")
                root.window_save_user.lift()
        else:
            save_user()

    '''
        def save_fingerprint(id):
        Brief:
            This function saves new fingerprint in DB to an exists user by ID.
        Input:
            -id: user's ID number.
        Output:
            No output.
    '''
    def save_fingerprint(id, img_pix='', kps='', features=''):
        func_name = "save_fingerprint"
        #print(f"In {func_name}")

        finger = list_fingers.get()
        hand = list_hand.get()
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        link = root.save_image_name
        details = img_pix
        interesting_points = (kps, features)

        res = mysql.add_fingerprint(id, hand, finger, date, time, link, details, interesting_points)
        # print(f'\nSave fingerprint: id: {id}, hand: {hand}, finger: {finger},'
        #       f' date: {date}, time: {time}, link: {link},'
        #       f' details: {details}, interesting points: {interesting_points}')

        first_name = mysql.get_first_name(id)
        last_name = mysql.get_last_name(id)

        # print(f"User's name: {first_name}, {last_name}")

        if res:  # if succeed to add new fingerprint to user
            documentation_fingerprint(first_name, last_name, id, date, time, hand, finger)
            message = f'Save fingerprint in DB:\nid: {id}\nhand: {hand}\nfinger: {finger}' \
                f'\ndate: {date}\ntime: {time}\nlink: {link}' \
                f'\ndetails: {details}\ninteresting points: {interesting_points}'
            messagebox.showwarning("Information", message)
        else:
            messagebox.showwarning("Information", "Error occurred while saving fingerprint in FingerPrint table")

    '''
        def save_user():
        Brief:
            This function saves new user in DB.
        Input:
            No input.
        Output:
            No output.
    '''
    def save_user():
        func_name = "save_user"
        #print(f"In {func_name}")

        first_name = root.first_name_text.get()
        last_name = root.last_name_text.get()
        id = root.id_text.get()
        gender = root.list_gender.get(root.list_gender.curselection())

        res = mysql.create_user(id, first_name, last_name, gender)
        save_fingerprint(id)

        # print(f'Save:\nfirst_name: {first_name}, last_name: {last_name}, id: {id}, gender: {gender}')
        date = datetime.datetime.now()
    #
        if res:
            documentation_creat_new_user(first_name, last_name, id, date, gender)
            messagebox.showwarning("Information", f"Save new user:\nFirst name: {first_name}\nLast name: {last_name}\nID: {id}")
            root.window_save_user.destroy()
        else:
            messagebox.showwarning("Information", "Error occurred while saving user in Users table")
            root.window_save_user.destroy()

    '''
        def create_window_fingerprint():
        Brief:
            This function creates a window for match fingerprints.
        Input:
            No input.
        Output:
            No output.
    '''
    def create_window_fingerprint(first_name, last_name, uid, vis):
        func_name = "create_window_fingerprint"
        #print(f"In {func_name}")

        root.window_fingerprint = tk.Toplevel(root)
        canvas_window_fingerprint = tk.Canvas(root.window_fingerprint, height=HEIGHT, width=WIDTH)
        canvas_window_fingerprint.pack()

        frame_text = tk.Frame(root.window_fingerprint)  # frame to image, left side
        frame_text.place(relx=0, rely=0, relwidth=1, relheight=0.15)

        frame_images = tk.Frame(root.window_fingerprint)  # frame to image, left side
        frame_images.place(relx=0, rely=0.15, relwidth=1, relheight=0.4)

        frame_details = tk.Frame(root.window_fingerprint)  # frame to image, left side
        frame_details.place(relx=0, rely=0.55, relwidth=1, relheight=0.45)

        frame_user1 = tk.Frame(frame_details)  # frame to image, left side
        frame_user1.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        frame_user2 = tk.Frame(frame_details)  # frame to image, left side
        frame_user2.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        vis = vis.resize((500, 250), Image.ANTIALIAS)
        visimage = ImageTk.PhotoImage(vis)

        text_window = "Match has been found"
        text_user = f'User name: {first_name} {last_name}\nID: {uid}\n'
        text_filename = f'Filename: None'

        root.img_vis = tk.Label(frame_images, image=visimage)
        root.img_vis.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        root.img_vis.image = visimage

        root.text_find_match = tk.Label(frame_text, text=text_window, font=("Arial", 40))
        root.text_find_match.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.8, anchor="n")

        root.details_user = tk.Label(frame_user1, text=text_user, font=("Arial", 12), justify='left')
        root.details_user.place(relx=0.5, rely=0, relwidth=0.9, relheight=0.9, anchor="n")

        root.details_user2 = tk.Label(frame_user2, text=text_filename, font=("Arial", 12), justify='left')
        root.details_user2.place(relx=0.5, rely=0, relwidth=0.8, relheight=0.8, anchor="n")

    '''
        def create_window_save_user():
        Brief:
            This function creates a window for saving new user.
        Input:
            No input.
        Output:
            No output.
    '''
    def create_window_save_user():
        func_name = "create_window_save_user"
        #print(f"In {func_name}")

        root.window_save_user = tk.Toplevel(root)
        canvas_new_window = tk.Canvas(root.window_save_user, height=HEIGHT2, width=WIDTH2)
        canvas_new_window.pack()

        frame_title = tk.Frame(root.window_save_user)  # a frame for the title
        frame_title.place(relx=0, rely=0, relwidth=1, relheight=0.15)

        frame_img = tk.Frame(root.window_save_user)  # a frame for an image
        frame_img.place(relx=0, rely=0.15, relwidth=1, relheight=0.2)

        frame_window = tk.Frame(root.window_save_user)  # a frame for the texts on current window
        frame_window.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        title = tk.Label(frame_title, text="Save user information in DB", font=("Arial", 16))  # the title of the frame
        title.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.8, anchor="n")

        root.save_img_label = tk.Label(frame_img, image='')
        root.save_img_label.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.95, anchor="n")

        # texts on current window
        first_name_label = tk.Label(frame_window, text="First Name")
        first_name_label.place(relx=0.2, rely=0.1, relwidth=0.2, relheight=0.1, anchor="n")

        root.first_name_text = tk.Entry(frame_window, bd=5)  # an entry for first name
        root.first_name_text.place(relx=0.35, rely=0.1, relwidth=0.3, relheight=0.1)

        last_name_label = tk.Label(frame_window, text="Last Name")
        last_name_label.place(relx=0.2, rely=0.25, relwidth=0.2, relheight=0.1, anchor="n")

        root.last_name_text = tk.Entry(frame_window, bd=5)  # an entry for last name
        root.last_name_text.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.1)

        id_label = tk.Label(frame_window, text="User ID")
        id_label.place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.1, anchor="n")

        root.id_text = tk.Entry(frame_window, bd=5)  # an entry for id
        root.id_text.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.1)

        gender_label = tk.Label(frame_window, text="Gender")
        gender_label.place(relx=0.2, rely=0.55, relwidth=0.3, relheight=0.1, anchor="n")
        root.list_gender = tk.Listbox(frame_window)

        root.list_gender.insert(1, "male")
        root.list_gender.insert(2, "female")
        root.list_gender.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.1)

        button_save = tk.Button(frame_window, text="Save", font=30, command=ask_check_id, bd=5)
        button_save.place(relx=0.47, rely=0.75, relwidth=0.25, relheight=0.1, anchor="n")

    '''
        def save_image_original_size():
        Brief:
            This function saves the image with effects changes original size.
        Input:
            No input.
        Output:
            No output.
    '''
    def save_image_original_size(is_exists=False):
        func_name = "save_image_original_size"
        #print(f"In {func_name}")

        root.save_photo = Image.open(root.filename)
        root.save_photo = sharpness(brightness(root.save_photo, root.brightness_img),
                                    root.sharpness_img).rotate(root.nrotate)
        full_filename = root.filename.split("/")[-1]

        if is_exists:
            filename, suffix = full_filename.split('.')
            if full_filename in os.listdir(save_path):
                dir_files = glob.glob(save_path + filename.split('.')[0] + '*')
                indexes = [int(x.split('_')[-1].split('.')[0]) for x in dir_files if '_' in x]

                if len(indexes) == 0:
                    index = '1'
                else:
                    index = str(max(indexes) + 1)
                end_filename = filename + '_' + index + '.' + suffix
            else:
                end_filename = filename + '_0.' + suffix
            root.save_image_name = save_path + end_filename
        else:
            root.save_image_name = save_path + full_filename
        root.save_photo.save(root.save_image_name)

    '''
        def images_fingerprint(inDB_image, image_filename, image_id):
        Brief:
            This function shows two images that were found as match one to the other.
        Input:
            -inDB_image: image in DB that was found as match to current input image.
            -image_filename: filename of image from DB.
            -image_id: ID of user from DB his image was found as match to current image.
        Output:
            No output.
    '''
    def images_fingerprint(first_name, last_name, image_id, filename, vis):
        func_name = "images_fingerprint"
        #print(f"In {func_name}")

        vis = vis.resize((500, 250), Image.ANTIALIAS)
        root._visimage = ImageTk.PhotoImage(vis)
        root.img_vis.config(image=root._visimage)

        text_window = "Match has been found"
        text_user = f'User name: {first_name} {last_name}\nID: {image_id}\n'
        text_filename = f'Filename: {filename}'

        root.text_find_match.config(text=text_window)
        root.details_user.config(text=text_user + text_filename)

    '''
        def check_match_fingerprint():
        Brief:
            This function checks if there is any match image to current one in DB.
        Input:
            No input.
        Output:
            No output.
    '''
    def check_match_fingerprint():
        func_name = "check_match_fingerprint"

        finger = list_fingers.get()
        hand = list_hand.get()
        accuracy_level = list_accuracy.get()
        # print(f"Hand={hand}, Finger={finger}, Accuracy={accuracy_level}")
        # linked_images = mysql.get_userid_by_hand_and_finger(hand, finger)
        linked_images = mysql.get_interesting_points_by_hand_and_finger(hand, finger)

        if linked_images == ():
            messagebox.showwarning("Information", "Could not find users' ids")

        else:
            exists_images = check_existence_by_ipoints(root.filename, linked_images, accuracy_level)
            if len(exists_images) == 0:
                messagebox.showwarning("Information", "Match has not been found")
            else:
                id = None
                ipoints = None
                for e_img in exists_images:
                    linked_filename, kps, features, vis, linked_image_id = e_img
                    # print(f'Data from DB: {linked_filename}, {linked_image_id}')

                    first_name, last_name = mysql.get_full_name_by_id(linked_image_id)
                    # print("User name: ", first_name, last_name)

                    if id is None:
                        id = linked_image_id
                        ipoints = kps, features
                    elif id != linked_image_id:
                        id = -1
                    create_window_fingerprint(first_name, last_name, linked_image_id, linked_filename, vis)

                if id is not None and id != -1:
                    answer = tk.messagebox.askquestion("Add fingerprint", f"Do you want to add the new fingerprint to user id {id}?",
                                                       icon='warning')

                    if answer == 'yes':  # if user wants to check ID number
                        save_image_original_size(True)
                        date = datetime.datetime.now().date()
                        time = datetime.datetime.now().time()
                        link = root.save_image_name
                        img_pix = np.array(root.save_photo)
                        res = mysql.add_fingerprint(id, hand, finger, date, time, link, img_pix, ipoints)

                        # print(f'\nSave fingerprint: id: {id}, hand: {hand}, finger: {finger},'
                        #       f' date: {date}, time: {time}, link: {link},'
                        #       f' details: {img_pix}, interesting points: {ipoints}')

                        if res:  # if succeed to add new fingerprint to user
                            message = f'Save fingerprint in DB:\nid: {id}\nhand: {hand}\nfinger: {finger}' \
                                f'\ndate: {date}\ntime: {time}\nlink: {link}' \
                                f'\ndetails: {img_pix}\ninteresting points: {ipoints}'
                            messagebox.showwarning("Information", message)
                        else:
                            messagebox.showwarning("Information",
                                                   "Error occurred while saving fingerprint in FingerPrint table")

    '''
        def check_match_fingerprint_ip():
        Brief:
            This function checks if there is any match image to current one in DB, based on saved interesting points.
        Input:
            No input.
        Output:
            No output.
    '''
    def check_match_fingerprint_ip():
        func_name = "check_match_fingerprint_ip"

        finger = list_fingers.get()
        hand = list_hand.get()
        accuracy_level = list_accuracy.get()
        # print(f"Hand={hand}, Finger={finger}, Accuracy={accuracy_level}")
        # linked_images = mysql.get_userid_by_hand_and_finger(hand, finger)
        user_data = mysql.get_ip_features_by_hand_and_finger(hand, finger)

        if user_data == ():
            messagebox.showwarning("Information", "Could not find users' ids")

        else:
            exists_images = check_existence_by_ipoints(root.filename, linked_images, accuracy_level)
            if len(exists_images) == 0:
                messagebox.showwarning("Information", "Match has not been found")
            else:
                id = None
                ipoints = None
                for e_img in exists_images:
                    linked_filename, kps, features, vis, linked_image_id = e_img
                    # print(f'Data from DB: {linked_filename}, {linked_image_id}')

                    first_name, last_name = mysql.get_full_name_by_id(linked_image_id)
                    # print("User name: ", first_name, last_name)

                    if id is None:
                        id = linked_image_id
                        ipoints = kps, features
                    elif id != linked_image_id:
                        id = -1
                    create_window_fingerprint(first_name, last_name, linked_image_id, vis)

                if id is not None and id != -1:
                    answer = tk.messagebox.askquestion("Add fingerprint",
                                                       f"Do you want to add the new fingerprint to user id {id}?",
                                                       icon='warning')

                    if answer == 'yes':  # if user wants to check ID number
                        save_image_original_size(True)
                        date = datetime.datetime.now().date()
                        time = datetime.datetime.now().time()
                        link = root.save_image_name
                        img_pix = np.array(root.save_photo)
                        res = mysql.add_fingerprint(id, hand, finger, date, time, link, img_pix, ipoints)

                        # print(f'\nSave fingerprint: id: {id}, hand: {hand}, finger: {finger},'
                        #       f' date: {date}, time: {time}, link: {link},'
                        #       f' details: {img_pix}, interesting points: {ipoints}')

                        if res:  # if succeed to add new fingerprint to user
                            message = f'Save fingerprint in DB:\nid: {id}\nhand: {hand}\nfinger: {finger}' \
                                f'\ndate: {date}\ntime: {time}\nlink: {link}' \
                                f'\ndetails: {img_pix}\ninteresting points: {ipoints}'
                            messagebox.showwarning("Information", message)
                        else:
                            messagebox.showwarning("Information",
                                                   "Error occurred while saving fingerprint in FingerPrint table")


    def check_match_c2c():
        func_name = "check_match_c2c"

        finger = list_fingers.get()
        hand = list_hand.get()
        accuracy_level = list_accuracy.get()
        # print(f"Hand={hand}, Finger={finger}, Accuracy={accuracy_level}")
        # linked_images = mysql.get_userid_by_hand_and_finger(hand, finger)
        linked_images = mysql.get_interesting_points_by_hand_and_finger(hand, finger)
        print(linked_images)
        # linked_images = set(linked_images)

        kernel = int(root.mat_clean_scale.get())
        # print(f"Kernel: {kernel}")
        val = root.clean_fingerprint_img
        # print(f"Val: {val}")
        exists_images = check_existence_by_c2c(root.filename, linked_images, accuracy_level, val, kernel)

        if len(exists_images) == 0:
            messagebox.showwarning("Information", "Match has not been found")
        else:
            id = None
            ipoints = None
            _idfp = None
            for e_img in exists_images:
                idfp, kps, features, vis = e_img
                # print(f'Data from DB: {linked_filename}, {linked_image_id}')
                uid = mysql.get_userid_by_idfp(idfp)

                first_name, last_name = mysql.get_full_name_by_id(uid)
                # print("User name: ", first_name, last_name)

                if id is None:
                    id = uid
                    ipoints = kps, features
                    _idfp = idfp
                elif id != uid:
                    id = -1
                create_window_fingerprint(first_name, last_name, uid, vis)

            if id is not None and id != -1:
                answer = tk.messagebox.askquestion("Add fingerprint",
                                                   f"Do you want to add the new fingerprint to user id {id}?",
                                                   icon='warning')

                if answer == 'yes':  # if user wants to check ID number
                    save_image_original_size(True)
                    date = datetime.datetime.now().date()
                    time = datetime.datetime.now().time()
                    link = root.save_image_name
                    img_pix = np.array(root.save_photo)
                    idipoints, idfeatures = ipoints
                    idipoints = convert_numpy_to_json(idipoints, Titles.ipoints_title)
                    idfeatures = convert_numpy_to_json(idfeatures, Titles.features_title)

                    idfp_str = _idfp

                    image_id = mongodb.insert_image(root.filename, idfp_str)
                    ipoint_id = mongodb.insert_ipoints(idipoints, idfp_str)
                    feature_id = mongodb.insert_features(idfeatures, idfp_str)

                    res = mysql.add_fingerprint(_idfp, hand, finger, date, time, image_id, ipoint_id, feature_id)

                    # print(f'\nSave fingerprint: id: {id}, hand: {hand}, finger: {finger},'
                    #       f' date: {date}, time: {time}, link: {link},'
                    #       f' details: {img_pix}, interesting points: {ipoints}')

                    if res:  # if succeed to add new fingerprint to user
                        message = f'Save fingerprint in DB:\nid: {id}\nhand: {hand}\nfinger: {finger}' \
                            f'\ndate: {date}\ntime: {time}\nImage: {image_id}' \
                            f'\nInteresting points: {ipoint_id}\nFeatures: {feature_id}'
                        messagebox.showwarning("Information", message)
                    else:
                        messagebox.showwarning("Information",
                                               "Error occurred while saving fingerprint in FingerPrint table")


    '''
        def match_fingerprint():
        Brief:
            This function calls to function that checks if there is any match in DB.
        Input:
            No input.
        Output:
            No output.
    '''
    def match_fingerprint():
        func_name = "match_fingerprint"
        #print(f"In {func_name}")

        is_details_filled = check_details_filled()

        if is_details_filled:
            check_match_fingerprint()



    def match_c2c():
        func_name = "match_c2c"
        #print(f"In {func_name}")

        is_details_filled = check_details_filled()

        if is_details_filled:
            check_match_c2c()




    '''
        def check_user_exists():
        Brief:
            THIS FUNCTION DOES NOTHING YET !!!
        Input:
            No input.
        Output:
            No output.
    '''
    def check_user_exists():
        func_name = "check_user_exists"
        #print(f"In {func_name}")
        pass

    '''
        def new_user():
        Brief:
            This function opens new window to create new user and keeps his image information.
        Input:
            No input.
        Output:
            No output.
    '''
    def new_user():
        func_name = "new_user"
        #print(f"In {func_name}")

        create_window_save_user()

        save_img = root.save_photo.resize((100, 100), Image.ANTIALIAS)
        root.save_photoimage = ImageTk.PhotoImage(save_img)
        root.save_img_label.config(image=root.save_photoimage)

    '''
        def fingerprint_id_match():
        Brief:
            THIS FUNCTION DOES NOTHING YET !!!
        Input:
            No input.
        Output:
            No output.
    '''
    def fingerprint_id_match():
        func_name = "fingerprint_id_match"
        #print(f"In {func_name}")

        return None

    '''
        def check_details_filled():
        Brief:
            This function checks if user filled out his details.
        Input:
            No input.
        Output:
            -True: if there is an image and Finger and Hand were selected.
            -False: otherwise.
    '''
    def check_details_filled():
        func_name = "check_details_filled"
        #print(f"In {func_name}")

        if root.open_img is None:  # If there is no picture, show error message
            messagebox.showwarning("Warning", "No image")
            return False
        elif list_fingers.current() == -1:
            messagebox.showwarning("Warning", "No finger was selected")
            return False
        elif list_hand.current() == -1:
            messagebox.showwarning("Warning", "No hand was selected")
            return False
        else:
            return True

    '''
        def save_image():
        Brief:
            This function saves new image or new user in DB.
        Input:
            No input.
        Output:
            No output.
    '''
    def save_image():
        func_name = "save_image"
        #print(f"In {func_name}")

        is_details_filled = check_details_filled()

        if is_details_filled:
            finger = list_fingers.get()
            hand = list_hand.get()
            accuracy_level = list_accuracy.get()
            linked_images = mysql.get_interesting_points_by_hand_and_finger(hand, finger)

            if linked_images == ():
                save_image_original_size()
                new_user()

            else:
                exists_images = check_existence_by_ipoints(root.filename, linked_images, accuracy_level)
                if len(exists_images) > 0:
                    id = None
                    _kps, _features = None, None
                    for e_img in exists_images:
                        linked_filename, kps, features, vis, linked_image_id = e_img

                        if id is None:
                            id = linked_image_id
                            _kps, _features = kps, features
                        elif id != linked_image_id:
                            id = -1

                    if id is not None and id != -1:
                        answer = tk.messagebox.askquestion("Add fingerprint",
                                                           f"Found match to a user id {id}.\n"
                                                           f"Do you want to add the new fingerprint to user id {id}?",
                                                           icon='warning')

                        if answer == 'yes':  # if user wants to check ID number
                            save_image_original_size(True)
                            img_pix = np.array(root.save_photo)
                            save_fingerprint(id, img_pix, _kps, _features)
                else:  # if did not find match in DB, open window to create a new user
                    save_image_original_size()
                    new_user()




    '''
        def reset_parameters():
        Brief:
            This function resets parameters of image.
        Input:
            No input.
        Output:
            No output.
    '''
    def reset_parameters():
        func_name = "reset_parameters"
        #print(f"In {func_name}")

        root.temp_img = root.original_img
        root.brightness_img = 1.0
        root.sharpness_img = 1.0
        root.nrotate = 0
        rotate_scale.set(0)
        brightness_scale.set(1.0)
        sharpness_scale.set(1.0)
        clean_scale.set(0.0)
        noise_scale.set(0.0)
        root.mat_clean_scale.set(0.0)

    '''
        def reset_image():
        Brief:
            This function resets image.
        Input:
            No input.
        Output:
            No output.
    '''
    def reset_image():
        func_name = "reset_image"
        #print(f"In {func_name}")

        reset_parameters()
        root.open_img = root.original_img
        root.image_tk = ImageTk.PhotoImage(root.open_img)
        img_label.configure(image=root.image_tk)


    def take_image():
        messagebox.showwarning("Warning", "This function does not work yet!\n"
                                          "You are moved to load image function")
        load_img()

    '''
        def load_img():
        Brief:
            This function loads an image.
        Input:
            No input.
        Output:
            No output.
    '''
    def load_img():
        func_name = "load_img"
        #print(f"In {func_name}")

        temp_filename = filedialog.askopenfilename(title='Choose a fingerprint')

        if len(temp_filename) > 0:
            root.filename = temp_filename
            root.open_img = Image.open(root.filename)
            root.open_img = root.open_img.resize((200, 200), Image.ANTIALIAS)
            root.temp_img = None
            root.original_img = root.open_img  # save original image for reset
            reset_parameters()
            root.image_tk = ImageTk.PhotoImage(root.open_img)
            # print("Image len: ", root.open_img.size)

            img_label.configure(image=root.image_tk)
            img_label_txt.configure(text=f"Filepath: {root.filename}")
        else:
            try:
                root.filename
            except:
                messagebox.showwarning("Warning", "You must choose a file to start")
                load_img()


    '''
        def brightness(img, val):
        Brief:
            This function changes the brightness of image by value.
        Input:
            -img: current input image.
            -val: value of brightness to change.
        Output:
            -enhance: img after brightness.
    '''
    def brightness(img, val):
        func_name = "brightness"
        #print(f"In {func_name}")

        enhancer = ImageEnhance.Brightness(img)
        enhance = enhancer.enhance(val)
        return enhance

    '''
        def sharpness(img, val):
        Brief:
            This function changes the sharpness of image by value.
        Input:
            -img: current input image.
            -val: value of sharpness to change.
        Output:
            -enhance: img after brightness.
    '''
    def sharpness(img, val):
        func_name = "sharpness"
        #print(f"In {func_name}")

        enhancer = ImageEnhance.Sharpness(img)
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

    def clean_fingerprint(img, val, k_value):
        func_name = "clean_fingerprint"
        #print(f"In {func_name}")

        # convert pil image to cv2
        img = np.array(img)
        #converted_img = cv2.cvtColor(pix, cv2.COLOR_GRAY2BGR)
        inverted_image = cv2.fastNlMeansDenoisingColored(img, None, 15, 15, 11, 32)

        pil_img = convert_cv2_to_pil(inverted_image)
        bright_img = brightness(pil_img, 1.4)

        cv2_img = convert_pil_to_cv2(bright_img)
        _, mask = cv2.threshold(cv2_img, 100, 255, cv2.THRESH_BINARY_INV)
        dilation_image = dilation(mask, val)
        kernel = k_value
        cleaned_img = clean_img(img, kernel)

        mask_img = dilation_image  # mask
        mask = (mask_img == 0)
        cleaned_fingerprint = np.copy(cleaned_img)
        cleaned_fingerprint[mask] = img[mask]

        # convert cv2 image to pil
        converted_img = convert_cv2_to_pil(cleaned_fingerprint)
        return converted_img

    '''
        def update_img():
        Brief:
            This function updates all changes to the image:
            rotate, sharpness, brightness, clean noises.
        Input:
            No input.
        Output:
            No output.
    '''
    def update_img():
        func_name = "update_img"
        #print(f"In {func_name}")

        root.temp_img = sharpness(brightness(root.open_img, root.brightness_img),
                                  root.sharpness_img).rotate(root.nrotate)
        root.temp_img = clean_noise(root.temp_img, root.clean_noise_img)
        kernel = int(root.mat_clean_scale.get())
        root.temp_img = clean_fingerprint(root.temp_img, root.clean_fingerprint_img, kernel)
        root.image_tk = ImageTk.PhotoImage(root.temp_img)
        img_label.configure(image=root.image_tk)

    '''
        def rotate_img(value=None):
        Brief:
            This function rotates an image by value.
        Input:
            -value: value to rotate image.
        Output:
            No output.
    '''
    def rotate_img(value=None):
        func_name = "rotate_img"
        #print(f"In {func_name}")

        if value is None:
            messagebox.showwarning("Warning", "This function does not work yet!")
        else:
            root.nrotate = value
            update_img()

    '''
        def brightness__img(value):
        Brief:
            This function defines change of brightness to image.
        Input:
            -value: value to change brightness of image.
        Output:
            No output.
    '''
    def brightness__img(value):
        func_name = "brightness__img"
        #print(f"In {func_name}")

        root.brightness_img = value
        update_img()

    '''
        def sharpness_img(value):
        Brief:
            This function defines change of sharpness to image.
        Input:
            -value: value to change sharpness of image.
        Output:
            No output.
    '''
    def sharpness_img(value):
        func_name = "sharpness_img"
        #print(f"In {func_name}")

        root.sharpness_img = value

        update_img()

    '''
        def clean_noise_img(value=None):
        Brief:
            This function cleans noises from the whole image.
        Input:
            No input.
        Output:
            No output.
    '''
    def clean_noise_img(value=None):
        func_name = "clean_noise_img"
        #print(f"In {func_name}")

        root.clean_noise_img = value
        print("--------------------CLEAN---------------------")
        update_img()


    '''
        def update_rotate(value):
        Brief:
            This function updates rotation by value.
        Input:
            -value: value to rotate by.
        Output:
            No output.
    '''
    def update_rotate(value):
        func_name = "update_rotate"
        #print(f"In {func_name}")

        if root.open_img is None:
            messagebox.showwarning("Warning", "No image")
            rotate_scale.set(0)
        else:
            rotate_img(int(value))

    '''
        def update_brightness(value):
        Brief:
            This function updates brightness by value.
        Input:
            -value: value to bright by.
        Output:
            No output.
    '''
    def update_brightness(value):
        func_name = "update_brightness"
        #print(f"In {func_name}")

        if root.open_img is None and float(value) != 1.0:  # if there is no picture
            messagebox.showwarning("Warning", "No image")
            brightness_scale.set(1.0)
        # if this is the first time that this window is opened - do nothing
        elif root.open_img is None and float(value) == 1.0:
            return
        else:
             brightness__img(float(value))

    '''
        def update_sharpness(value):
        Brief:
            This function updates sharpness by value.
        Input:
            -value: value to sharp by.
        Output:
            No output.
    '''
    def update_sharpness(value):
        func_name = "update_sharpness"
        #print(f"In {func_name}")

        if root.open_img is None and float(value) != 1.0:  # if there is no picture
            messagebox.showwarning("Warning", "No image")
            sharpness_scale.set(1.0)
        # if this is the first time that this window is opened - do nothing
        elif root.open_img is None and float(value) == 1.0:
            return
        else:
            sharpness_img(float(value))

    '''
        def update_clean_noise(value):
        Brief:
            This function updates noise cleaning by value.
        Input:
            -value: value to clean noises by.
        Output:
            No output.
    '''
    def update_clean_noise(value):
        func_name = "update_clean_noise"
        #print(f"In {func_name}")

        if root.open_img is None and float(value) != 0.00:  # If there is no picture
            messagebox.showwarning("Warning", "No image")
            clean_noise_img(0.0)
        # if this is the first time that this window is opened - do nothing
        elif root.open_img is None and float(value) == 0.00:
            return
        else:
            clean_noise_img(float(value))

    '''
            def update_clean_fingerprint(value):
            Brief:
                This function updates noise cleaning by value.
            Input:
                -value: value to clean noises by.
            Output:
                No output.
        '''

    def update_clean_fingerprint(value):
        func_name = "update_clean_fingerprint"
        # print(f"In {func_name}")

        if root.open_img is None and float(value) != 0.00:  # If there is no picture
            messagebox.showwarning("Warning", "No image")
            clean_noise_img(0.0)
        # if this is the first time that this window is opened - do nothing
        elif root.open_img is None and float(value) == 0.00:
            return
        else:
            #clean_noise_img(float(value))
            root.clean_fingerprint_img = clean_scale.get()
            update_img()
            #clean_fingerprint(root.open_img, value)
            #dst = cv2.fastNlMeansDenoisingColored(root.open_img, None, 15, 15, 11, 32)









    '''
            def update_sharpness(value):
            Brief:
                This function updates sharpness by value.
            Input:
                -value: value to sharp by.
            Output:
                No output.
        '''

    def update_matrix(value):
        func_name = "update_matrix"
        # print(f"In {func_name}")

        if root.open_img is None and float(value) != 1.0:  # if there is no picture
            messagebox.showwarning("Warning", "No image")
            root.mat_clean_scale.set(3)
        # if this is the first time that this window is opened - do nothing
        elif root.open_img is None and float(value) == 1.0:
            return
        else:
            #root.mat_clean_scale.set(11 if int(value) == 10 else value)
            global past
            n = int(value)
            if not n % 2:
                root.mat_clean_scale.set(n + 1 if n > past else n - 1)
                past = root.mat_clean_scale.get()

    def opening():
        img = cv2.imread(root.filename, cv2.IMREAD_GRAYSCALE)
        _, mask = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY_INV)
        k_value = int(root.mat_clean_scale.get())
        kernal = np.ones((k_value, k_value), np.uint8)
        root.opening_image = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
        cv2.imshow("Opening", root.opening_image)

    def closing():
        img = cv2.imread(root.filename, cv2.IMREAD_GRAYSCALE)
        _, mask = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY_INV)
        k_value = int(root.mat_clean_scale.get()) + 6
        kernal = np.ones((k_value, k_value), np.uint8)
        closing_image = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
        cv2.imshow("Closing", closing_image)

    def clean_img(image, k_value):
        kernel = (k_value, k_value)  # the dimension of the x and y axis of the kernel.
        cleaned_image = cv2.blur(image, kernel)
        return cleaned_image

    def convert_cv2_to_pil(img):
        # convert cv2 image to pil
        converted_img = Image.fromarray(np.uint8(img))
        return converted_img

    def convert_pil_to_cv2(img):
        # convert pil image to cv2
        converted_img = np.array(img)
        return converted_img

    def dilation(image, k_value):
        # k_value = 3
        kernel = np.ones((k_value, k_value), np.uint8)
        dilation_image = cv2.dilate(image, kernel, iterations=2)
        return dilation_image

    def erosion():
        img = cv2.imread(root.filename, cv2.IMREAD_GRAYSCALE)
        _, mask = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY_INV)
        k_value = int(root.mat_clean_scale.get()) + 6
        kernal = np.ones((k_value, k_value), np.uint8)
        erosion_image = cv2.erode(mask, kernal, iterations=1)
        cv2.imshow("Erosion", erosion_image)


    root = tk.Tk()
    root.open_img = None
    root.iconbitmap("icon.ico")

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame_img = tk.Frame(root, borderwidth=1, relief='solid')  # frame to image, left side
    frame_img.place(relx=0.35, rely=0.05, relwidth=0.55, relheight=0.40)

    img_label = tk.Label(frame_img, image='')
    img_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    img_label_txt = tk.Label(frame_img, text='')
    img_label_txt.place(relx=0.01, rely=0.01, relwidth=0.99, relheight=0.2)

    root.nrotate = 0
    root.nalpha = 0
    root.brightness_img = 1.0
    root.sharpness_img = 0
    root.clean_noise_img = 0
    root.clean_fingerprint_img = 0

    frame2 = tk.Frame(root)  # frame to button, right side
    frame2.place(relx=0.1, rely=0.05, relwidth=0.20, relheight=0.40)

    button_load_img = tk.Button(frame2, text="Load image", font=40, command=load_img, bd=5)
    button_load_img.place(rely=0.02, relwidth=0.8, relheight=0.25)

    button2 = tk.Button(frame2, text="Take a picture", font=10, command=take_image, bd=5)
    button2.place(rely=0.35, relwidth=0.8, relheight=0.25)

    button_reset = tk.Button(frame2, text="Reset image", font=30, command=reset_image, bd=5)
    button_reset.place(rely=0.7, relwidth=0.8, relheight=0.25)

    frame3 = tk.Frame(root, bd=5,)  # frame to input finger and hands
    frame3.place(relx=0.03, rely=0.48, relwidth=0.22, relheight=0.35)

    frame4 = tk.Frame(root,)  # frame of scales
    frame4.place(relx=0.3, rely=0.45, relwidth=0.6, relheight=0.4)

    lower_frame = tk.Frame(root)  # lower frame for key buttons
    lower_frame.place(relx=0.05, rely=0.85, relwidth=0.95, relheight=0.12)

    label_finger = tk.Label(frame3, text='Finger:',)
    label_finger.place(relx=0.05, rely=0.05, relwidth=0.30, relheight=0.2)

    list_fingers = ttk.Combobox(frame3, values=[" thumb", " index finger",
                                                " middle finger", " ring finger",
                                                " little finger"])
    list_fingers.place(relx=0.45, rely=0.05, relwidth=0.55, relheight=0.2)

    label_hand = tk.Label(frame3, text='Hand:',)
    label_hand.place(relx=0.05, rely=0.35, relwidth=0.30, relheight=0.2)

    list_hand = ttk.Combobox(frame3, values=(" Right", " Left"))
    list_hand.place(relx=0.45, rely=0.35, relwidth=0.55, relheight=0.2)

    label_accuracy = tk.Label(frame3, text='Accuracy\nlevel (%):', )
    label_accuracy.place(relx=0.01, rely=0.65, relwidth=0.40, relheight=0.2)

    list_accuracy = ttk.Combobox(frame3, values=[i for i in range(1, 101)])
    list_accuracy.place(relx=0.45, rely=0.65, relwidth=0.55, relheight=0.2)

    label_rotate = tk.Label(frame4, text="Rotate image",)
    label_rotate.place(relx=0.01, rely=0.00, relwidth=0.30, relheight=0.2)
    rotate_scale = tk.Scale(frame4, from_=0, to=360, orient='horizontal', command=update_rotate)
    rotate_scale.place(relx=0.30, rely=0.00, relwidth=0.70, relheight=0.2)

    label_brightness = tk.Label(frame4, text="Brightness",)
    label_brightness.place(relx=0.01, rely=0.15, relwidth=0.30, relheight=0.2)
    brightness_scale = tk.Scale(frame4, from_=0.0, to=4.0, resolution=0.2, orient='horizontal',
                                command=update_brightness)
    brightness_scale.set(1.0)
    brightness_scale.place(relx=0.30, rely=0.15, relwidth=0.70, relheight=0.2)

    label_sharpness = tk.Label(frame4, text="Sharpness",)
    label_sharpness.place(relx=0.01, rely=0.30, relwidth=0.30, relheight=0.2)
    sharpness_scale = tk.Scale(frame4, from_=0.0, to=4.0, resolution=0.2, orient='horizontal',
                               command=update_sharpness, )
    sharpness_scale.set(1.0)
    sharpness_scale.place(relx=0.30, rely=0.30, relwidth=0.70, relheight=0.2)

    label_noise = tk.Label(frame4, text="Clean noise",)
    label_noise.place(relx=0.01, rely=0.45, relwidth=0.30, relheight=0.2)
    noise_scale = tk.Scale(frame4, from_=1.0, to=5.0, resolution=1.0, orient='horizontal', command=update_clean_noise)
    noise_scale.set(0.0)
    noise_scale.place(relx=0.30, rely=0.45, relwidth=0.70, relheight=0.2)

    label_clean = tk.Label(frame4, text='Clean fingerprint:',)
    label_clean.place(relx=0.01, rely=0.60, relwidth=0.30, relheight=0.2)
    clean_scale = tk.Scale(frame4, from_=1.0, to=11.0, resolution=1.0, orient='horizontal',
                           command=update_clean_fingerprint)
    clean_scale.set(0.0)
    clean_scale.place(relx=0.30, rely=0.60, relwidth=0.70, relheight=0.2)

    label_clean = tk.Label(frame4, text='Matrix size:', )
    label_clean.place(relx=0.01, rely=0.75, relwidth=0.30, relheight=0.2)
    root.mat_clean_scale = tk.Scale(frame4, from_=3.0, to=11.0, orient='horizontal',
                           command=update_matrix)
    root.mat_clean_scale.set(0.0)
    root.mat_clean_scale.place(relx=0.30, rely=0.75, relwidth=0.70, relheight=0.2)

    button_save = tk.Button(lower_frame, text="Save in DB", font=30, command=save_image, bd=5)
    button_save.place(relx=0.05, rely=0.1, relwidth=0.22, relheight=0.7)

    button_fingerprint = tk.Button(lower_frame, text="Find match in DB", font=30, command=match_fingerprint, bd=5)
    button_fingerprint.place(relx=0.35, rely=0.1, relwidth=0.22, relheight=0.7)

    button_c2c = tk.Button(lower_frame, text="C2C", font=30, command=match_c2c, bd=5)
    button_c2c.place(relx=0.65, rely=0.1, relwidth=0.22, relheight=0.7)

    mongodb = MongoDB()
    root.title("Workbench")
    root.mainloop()  # display
    mysql.close_db()


if __name__ == "__main__":
    MainApp()
