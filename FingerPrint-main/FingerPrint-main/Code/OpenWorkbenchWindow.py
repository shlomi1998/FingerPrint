import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import datetime
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import mysql
from tkinter import messagebox
from Server import check_existence_by_stitcher


HEIGHT = 650
WIDTH = 700

HEIGHT2 = 500
WIDTH2 = 500

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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

        id = root.id_text.get()
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
        if control_digit == int(id[-1]):  # control digit is valid
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
        # print(f"In {func_name}")

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
    def save_fingerprint(id):
        func_name = "save_fingerprint"
        # print(f"In {func_name}")

        finger = list_fingers.get()
        hand = list_hand.get()
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        link = root.save_image_name
        details = ""

        res = mysql.add_fingerprint(id, hand, finger, date, time, link, details)
        print(f'\nSave fingerprint: id: {id}, hand: {hand}, finger: {finger},'
              f' date: {date}, time: {time}, link: {link}, details: {details}')

        first_name = mysql.get_first_name(id)
        last_name = mysql.get_last_name(id)

        print(f"User's name: {first_name}, {last_name}")

        if res:  # if succeed to add new fingerprint to user
            documentation_fingerprint(first_name, last_name, id, date, time, hand, finger)
            message = f'Save fingerprint in DB:\nid: {id}\nhand: {hand}\nfinger: {finger}' \
                f'\ndate: {date}\ntime: {time}\nlink: {link}\ndetails: {details}\n'
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
        # print(f"In {func_name}")

        first_name = root.first_name_text.get()
        last_name = root.last_name_text.get()
        id = root.id_text.get()
        gender = root.list_gender.get(root.list_gender.curselection())

        res = mysql.create_user(id, first_name, last_name, gender)
        save_fingerprint(id)

        print(f'Save:\nfirst_name: {first_name}, last_name: {last_name}, id: {id}, gender: {gender}')
        date = datetime.datetime.now()
    #
        if res:
            documentation_creat_new_user(first_name, last_name, id, date, gender)
            messagebox.showwarning("Information", f"Save new user:{first_name} {last_name} {id}")
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
    def create_window_fingerprint():
        func_name = "create_window_fingerprint"
        # print(f"In {func_name}")

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

        root.img_fingerprint1 = tk.Label(frame_images, image='')
        root.img_fingerprint1.place(relx=0.15, rely=0.05, relwidth=0.3, relheight=0.9)

        root.img_fingerprint2 = tk.Label(frame_images, image='')
        root.img_fingerprint2.place(relx=0.55, rely=0.05, relwidth=0.3, relheight=0.9)

        root.text_find_match = tk.Label(frame_text, text="", font=("Arial", 40))
        root.text_find_match.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.8, anchor="n")

        root.details_user1 = tk.Label(frame_user1, text="", font=("Arial", 12), justify='left')
        root.details_user1.place(relx=0.5, rely=0, relwidth=0.8, relheight=0.8, anchor="n")

        root.details_user2 = tk.Label(frame_user2, text="", font=("Arial", 12), justify='left')
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
        # print(f"In {func_name}")

        root.window_save_user = tk.Toplevel(root)
        canvas_new_window = tk.Canvas(root.window_save_user, height=HEIGHT2, width=WIDTH2)
        canvas_new_window.pack()

        frame_title = tk.Frame(root.window_save_user)  # frame to titel
        frame_title.place(relx=0, rely=0, relwidth=1, relheight=0.15)

        frame_img = tk.Frame(root.window_save_user)  # frame to image
        frame_img.place(relx=0, rely=0.15, relwidth=1, relheight=0.2)

        frame_window = tk.Frame(root.window_save_user)
        frame_window.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        title = tk.Label(frame_title, text="Save user information in DB", font=("Arial", 16))
        title.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.8, anchor="n")

        root.save_img_label = tk.Label(frame_img, image='')
        root.save_img_label.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.95, anchor="n")

        first_name_label = tk.Label(frame_window, text="First Name")
        first_name_label.place(relx=0.2, rely=0.1, relwidth=0.2, relheight=0.1, anchor="n")

        root.first_name_text = tk.Entry(frame_window, bd=5)
        root.first_name_text.place(relx=0.35, rely=0.1, relwidth=0.3, relheight=0.1)

        last_name_label = tk.Label(frame_window, text="Last Name")
        last_name_label.place(relx=0.2, rely=0.25, relwidth=0.2, relheight=0.1, anchor="n")

        root.last_name_text = tk.Entry(frame_window, bd=5)
        root.last_name_text.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.1)

        id_label = tk.Label(frame_window, text="User ID")
        id_label.place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.1, anchor="n")

        root.id_text = tk.Entry(frame_window, bd=5)
        root.id_text.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.1)

        gender_label = tk.Label(frame_window, text="Gender")
        gender_label.place(relx=0.2, rely=0.55, relwidth=0.3, relheight=0.1, anchor="n")
        root.list_gender = tk.Listbox(frame_window)

        root.list_gender.insert(1, "male")
        root.list_gender.insert(2, "female")
        root.list_gender.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.1)

        button_save = tk.Button(frame_window, text="save new user", font=30, command=ask_check_id, bd=5)
        button_save.place(relx=0.47, rely=0.75, relwidth=0.25, relheight=0.1, anchor="n")

    '''
        def save_image_original_size():
        Brief:
            This function saves original photo.
        Input:
            No input.
        Output:
            No output.
    '''
    def save_image_original_size():
        func_name = "save_image_original_size"
        # print(f"In {func_name}")

        root.save_photo = Image.open(root.filename)
        root.save_photo = sharpness(brightness(root.save_photo, root.brightness_img),
                                    root.sharpness_img).rotate(root.nrotate)
        root.save_image_name = "results/" + root.filename.split("/")[-1]
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
    def images_fingerprint(inDB_image, image_filename, image_id):
        func_name = "images_fingerprint"
        # print(f"In {func_name}")

        # print("Print: ", type(root.save_photoimage2), type(inDB_image))
        root.img_fingerprint1.config(image=root.save_photoimage2)
        root.img_fingerprint2.config(image=inDB_image)

        text_window = "Match was found"
        text_user1 = 'Source image'
        text_user2 = 'Filename: ' + image_filename + '\nID: ' + str(image_id)

        root.text_find_match.config(text=text_window)
        root.details_user1.config(text=text_user1)
        root.details_user2.config(text=text_user2)

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
        # print(f"In {func_name}")

        linkedImages = mysql.get_all_fingerprints()
        is_match, source_image, inDB_image, linked_image_filename, linked_image_id = check_existence_by_stitcher(root.filename, linkedImages)

        if is_match:
            create_window_fingerprint()
            save_image_original_size()
            save_img = root.save_photo.resize((200, 200), Image.ANTIALIAS)
            root.save_photoimage2 = ImageTk.PhotoImage(save_img)

            #source_image = source_image.resize((200, 200), Image.ANTIALIAS)
            #source_image = ImageTk.PhotoImage(source_image)

            inDB_image = inDB_image.resize((200, 200), Image.ANTIALIAS)
            inDB_image = ImageTk.PhotoImage(inDB_image)

            images_fingerprint(inDB_image, linked_image_filename, linked_image_id)
        else:
            messagebox.showwarning("Information", "No match was found")

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
        # print(f"In {func_name}")

        is_details_filled = check_details_filled()

        if is_details_filled:
            check_match_fingerprint()

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
        # print(f"In {func_name}")
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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

        is_details_filled = check_details_filled()

        if is_details_filled:
            linked_images = mysql.get_all_fingerprints()
            is_match, source_image, in_db_image, linked_image_filename, linked_image_id = check_existence_by_stitcher(root.filename, linked_images)
            save_image_original_size()

            if is_match:  # if found match in DB
                messagebox.showwarning("Information", f"Found match to a user id {linked_image_id}")
                save_fingerprint(linked_image_id)
            else:  # if did not find match in DB, open window to creat a new user
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
        # print(f"In {func_name}")

        root.temp_img = None
        root.brightness_img = 1.0
        root.sharpness_img = 1.0
        root.nrotate = 0
        rotate_scale.set(0)
        brightness_scale.set(1.0)
        sharpness_scale.set(1.0)

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
        # print(f"In {func_name}")

        reset_parameters()
        root.open_img = root.original_img
        root.image_tk = ImageTk.PhotoImage(root.open_img)
        img_label.configure(image=root.image_tk)

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
        # print(f"In {func_name}")

        root.filename = filedialog.askopenfilename(title='Choose a fingerprint')
        if len(root.filename) > 0:
            reset_parameters()
            root.open_img = Image.open(root.filename)
            root.open_img = root.open_img.resize((200, 200), Image.ANTIALIAS)
            root.temp_img = None
            root.original_img = root.open_img  # save original image for reset
            root.image_tk = ImageTk.PhotoImage(root.open_img)

            img_label.configure(image=root.image_tk)
        else:
            pass

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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

        enhancer = ImageEnhance.Sharpness(img)
        enhance = enhancer.enhance(val)
        return enhance

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
        # print(f"In {func_name}")

        root.temp_img = sharpness(brightness(root.open_img, root.brightness_img),
                                  root.sharpness_img).rotate(root.nrotate)
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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

        root.sharpness_img = value

        update_img()

    '''
        def clean_noise_img(value=None):
        Brief:
            THIS FUNCTION DOES NOT WORK YET !!!
        Input:
            No input.
        Output:
            No output.
    '''
    def clean_noise_img(value=None):
        func_name = "clean_noise_img"
        # print(f"In {func_name}")

        messagebox.showwarning("Warning", "This function does not work yet!")

        # root.clean_noise_img = value
        # inverted_image = root.open_img.filter(ImageFilter.GaussianBlur(radius=root.clean_noise_img))
        # root.image_tk = ImageTk.PhotoImage(inverted_image)
        # img_label.configure(image=root.image_tk)
        # update_img()


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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

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
        # print(f"In {func_name}")

        if root.open_img is None and float(value) != 1.0:  # if there is no picture
            messagebox.showwarning("Warning", "no image")
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
        # print(f"In {func_name}")

        if root.open_img is None and float(value) != 1.0:  # If there is no picture
            messagebox.showwarning("Warning", "No image")
            sharpness_scale.set(1.0)
        # if this is the first time that this window is opened - do nothing
        elif root.open_img is None and float(value) == 1.0:
            return
        else:
            clean_noise_img(float(value))


    root = tk.Tk()
    root.open_img = None

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame_img = tk.Frame(root, borderwidth=1, relief='solid')  # frame to image, left side
    frame_img.place(relx=0.35, rely=0.05, relwidth=0.55, relheight=0.40)

    img_label = tk.Label(frame_img, image='')
    img_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
    root.nrotate = 0
    root.nalpha = 0
    root.brightness_img = 1.0
    root.sharpness_img = 0
    root.clean_noise_img = 0

    frame2 = tk.Frame(root)  # frame to button, right side
    frame2.place(relx=0.1, rely=0.05, relwidth=0.20, relheight=0.40)

    button_load_img = tk.Button(frame2, text="load image", font=40, command=load_img, bd=5)
    button_load_img.place(rely=0.02, relwidth=0.8, relheight=0.25)

    button2 = tk.Button(frame2, text="take a picture", font=10, command=rotate_img, bd=5)
    button2.place(rely=0.35, relwidth=0.8, relheight=0.25)

    button_reset = tk.Button(frame2, text="reset image", font=30, command=reset_image, bd=5)
    button_reset.place(rely=0.7, relwidth=0.8, relheight=0.25)

    frame3 = tk.Frame(root, bd=5,)  # frame to input finger and hands
    frame3.place(relx=0.08, rely=0.48, relwidth=0.2, relheight=0.35)

    frame4 = tk.Frame(root,)  # frame of scales
    frame4.place(relx=0.3, rely=0.45, relwidth=0.6, relheight=0.4)

    lower_frame = tk.Frame(root)  # lower frame for key buttons
    lower_frame.place(relx=0.1, rely=0.85, relwidth=0.82, relheight=0.12)

    label_hand = tk.Label(frame3, text='Finger:',)
    label_hand.place(relx=0.05, rely=0.05, relwidth=0.30, relheight=0.2)

    list_fingers = ttk.Combobox(frame3, values=[" thumb", " index finger",
                                                " middle finger", " ring finger",
                                                " little finger"])
    list_fingers.place(relx=0.4, rely=0.05, relwidth=0.60, relheight=0.2)

    label_hand = tk.Label(frame3, text='Hand:',)
    label_hand.place(relx=0.05, rely=0.5, relwidth=0.30, relheight=0.2)

    list_hand = ttk.Combobox(frame3, values=(" Right", " Left"))
    list_hand.place(relx=0.4, rely=0.5, relwidth=0.40, relheight=0.2)

    rotate_scale = tk.Scale(frame4, from_=0, to=360, orient='horizontal',
                            label="rotate image", command=update_rotate)
    rotate_scale.place(relx=0.05, rely=0.05, relwidth=0.95, relheight=0.2)

    brightness_scale = tk.Scale(frame4, from_=0.0, to=4.0, resolution=0.2, orient='horizontal', label="brightness",
                                command=update_brightness)
    brightness_scale.set(1.0)
    brightness_scale.place(relx=0.05, rely=0.29, relwidth=0.95, relheight=0.2)

    sharpness_scale = tk.Scale(frame4, from_=0.0, to=4.0, resolution=0.2, orient='horizontal', label="sharpness",
                               command=update_sharpness, )
    sharpness_scale.set(1.0)
    sharpness_scale.place(relx=0.05, rely=0.53, relwidth=0.95, relheight=0.2)
    noise_scale = tk.Scale(frame4, from_=0.0, to=3.0, resolution=0.05, orient='horizontal', label="clean noise", command=update_clean_noise)
    noise_scale.set(0.0)
    noise_scale.place(relx=0.05, rely=0.77, relwidth=0.95, relheight=0.2)

    button_save = tk.Button(lower_frame, text="save in DB", font=30, command=save_image, bd=5)
    button_save.place(relx=0.05, rely=0.1, relwidth=0.35, relheight=0.7)

    button_fingerprint = tk.Button(lower_frame, text="Find match in DB", font=30, command=match_fingerprint, bd=5)
    button_fingerprint.place(relx=0.55, rely=0.1, relwidth=0.35, relheight=0.7)

    root.mainloop()  # display


if __name__ == "__main__":
    MainApp()
