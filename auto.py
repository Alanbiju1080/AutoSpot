import tkinter as tk
from tkinter import *
import threading
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import numpy as np

Canvas = None

current_file = None

def upload_video():

    min_width_react = 80
    min_height_react = 80


    global current_file
    current_file = filedialog.askopenfilename(filetypes=[("Image files", "*.mp4; *.avi; *.mov")])
    cap = cv2.VideoCapture(current_file)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to PIL ImageTk format
        # img = Image.fromarray(frame)
        # img_tk = ImageTk.PhotoImage(img)

        # Update the canvas image
        cv2.resize(frame, (1066, 600))

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = detect_ve(img)

        canvas.image = ImageTk.PhotoImage(Image.fromarray(frame))
        canvas.create_image(400, 50, anchor="nw", image=canvas.image)


        root.update()

    cap.release()



# def capture_and_detect(canvas):
#     cap = cv2.VideoCapture(0)

#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             break

#         # Convert the frame to PIL ImageTk format
#         # img = Image.fromarray(frame)
#         # img_tk = ImageTk.PhotoImage(img)

#         # Update the canvas image
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         frame = detect_ve(frame)

#         canvas.image = ImageTk.PhotoImage(Image.fromarray(frame))
#         canvas.create_image(500, 100, anchor="nw", image=canvas.image)


#         root.update()

#     cap.release()

    # img = cv2.imread("D:\LEAP\gray.jpg")
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.resize(img, (800, 600))
    # canvas.image = ImageTk.PhotoImage(Image.fromarray(img))
    # canvas.create_image(500, 100, anchor="nw", image=canvas.image)

fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=10)

def detect_ve(frame):

    min_width_react = 80
    min_height_react = 80



    fgmask = fgbg.apply(frame)

    # Remove noise and enhance the remaining foreground regions
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("fgmask", fgmask)
    # print(1) 

    # Find contours of potential objects
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        validate_counter = (
            w >= min_width_react
            and h >= min_height_react
            and w <= 100
            and h <= 100
        )
        if not validate_counter:
            continue

        # Draw bounding box around the car
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

def clear_image():
    canvas.delete("all")

root = tk.Tk()
root.title("AutoSpot")
root.geometry("1920x1080")

# Load and display landing GIF
gif_path = "Images/AutoSpotFF.gif"
gif = Image.open(gif_path)

frames = []
for frame in range(0, gif.n_frames):
    gif.seek(frame)
    frame_image = ImageTk.PhotoImage(gif)
    frames.append(frame_image)

label = tk.Label(root)
label.pack()

def forget_label():
    label.pack_forget()
    main_window()


def animate(frame_index=0):
    if frame_index < len(frames):
        frame_image = frames[frame_index]
        label.config(image=frame_image)

        frame_index += 1
        if frame_index >= len(frames):
            label.after(1400,forget_label)  # Hide the label

        label.after(30, animate, frame_index)

animate()

def main_window():
    global canvas
    lock = threading.Lock()

    # Create canvas to display the image
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()


    capture_thread = None
    


    # Buttons
    upload_btn = PhotoImage(file="Images/Frame 1 (1).png")
    upload = tk.Button(root, image=upload_btn, borderwidth=0, command=upload_video)
    upload.image = upload_btn  # Store the image as an attribute of the button
    upload.place(x=20, y=290)

    # detect_btn = PhotoImage(file="D:\LEAP\codes\Image\Group 1.png")
    # detect = tk.Button(root, image=detect_btn, borderwidth=0, command=detect_ve)
    # detect.image = detect_btn  # Store the image as an attribute of the button
    # detect.place(x=20, y=405)

    start_button = PhotoImage(file="Images\Frame 1 (2).png")
    start = tk.Button(root, image=start_button, borderwidth=0, command=lambda: clear_image(canvas))
    start.image = start_button  # Store the image as an attribute of the button
    start.place(x=20, y=405)


root.mainloop()

















# import tkinter as tk
# from tkinter import *
# from tkinter import filedialog
# from PIL import ImageTk, Image
# import cv2
# import numpy as np






# current_file = None

# def upload_image():
#     global current_file
#     current_file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg; *.jpeg; *.png")])
#     img = cv2.imread(current_file)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = cv2.resize(img, (800, 600))
#     canvas.image = ImageTk.PhotoImage(Image.fromarray(img))
#     canvas.create_image(500, 100, anchor="nw", image=canvas.image)



# def clear_image():
#     canvas.delete("all")


# def detect_ve(current_file):

#     image = cv2.imread(current_file)

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply Gaussian blur to reduce noise
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)

#     # Perform edge detection using Canny edge detection
#     edges = cv2.Canny(blurred, 50, 150)

#     thresholded_image = cv2.threshold(edges, 150, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]


#     # Perform dilation to close gaps in between object edges
#     dilated = cv2.dilate(thresholded_image, None, iterations=1)

#     # Find contours of objects in the image
#     contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Filter the contours based on area and aspect ratio to extract potential vehicle regions
#     min_area = 2815
#     max_area =30000                  # Minimum area of a contour to be considered as a vehicle
#     min_aspect_ratio = 0.995  # Maximum aspect ratio of a contour to be considered as a vehicle
#     max_aspect_ratio = 2.6  # Minimum aspect ratio of a contour to be considered as a vehicle

#     # min_area = 900
#     # min_aspect_ratio = 0.3


#     vehicle_contours = []
#     for contour in contours:
#         area = cv2.contourArea(contour)
#         x, y, w, h = cv2.boundingRect(contour)
#         aspect_ratio = w / float(h)
            
#         if area > min_area and area < max_area  and aspect_ratio > min_aspect_ratio and aspect_ratio < max_aspect_ratio:
#           vehicle_contours.append(contour)

#     # Draw bounding boxes around the detected vehicle regions
#     for contour in vehicle_contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image = cv2.resize(image, (800, 600))
#     canvas.image = ImageTk.PhotoImage(Image.fromarray(image))
#     canvas.create_image(500, 100, anchor="nw", image=canvas.image)
#     return image
    
    
# root = tk.Tk()
# root.title("AutoSpot")


# # Create canvas to display the image
# canvas = tk.Canvas(root, width=1920, height=1080)
# canvas.pack()

# # select_text = tk.StringVar()
# # upload = tk.Button(root, textvariable = select_text,font = "Raleway",bg = "#4361EE", fg = "white", height = 2, width=15 ,command = lambda:upload_image())
# # select_text.set("Upload")

# login_btn = PhotoImage(file = "D:\LEAP\codes\Image\Frame 1 (1).png")
#   # Create button and image
# upload = tk.Button(root, image = login_btn,
#              borderwidth = 0, command=upload_image)
# upload.place(x =20,y = 260 )

# # select_text = tk.StringVar()
# # detect = tk.Button(root, textvariable = select_text,font = "Raleway",bg = "#4361EE", fg = "white", height = 2, width=15,command = lambda:detect_ve(current_file) )
# # select_text.set("Detect")
# detect_btn = PhotoImage(file = "D:\LEAP\codes\Image\Frame 1 (3).png")
#   # Create button and image
# detect = tk.Button(root, image = detect_btn,
#              borderwidth = 0, command=lambda:detect_ve(current_file))
# detect.place(x=20, y = 375)


# # select_text = tk.StringVar()
# # histo = tk.Button(root, textvariable = select_text,font = "Raleway",bg = "#4361EE", fg = "white", height = 2, width=15 ,command=lambda:histogram())
# # select_text.set("Histogram")
# # histo.place(x=20, y = 420)



# # select_text = tk.StringVar()
# # clear = tk.Button(root, textvariable = select_text,font = "Raleway",bg = "#4361EE", fg = "white", height = 2, width=15,command = lambda:clear_image() )
# # select_text.set("Clear")
# clr_btn = PhotoImage(file = "D:\LEAP\codes\Image\Frame 1 (2).png")
#   # Create button and image
# clear = tk.Button(root, image = clr_btn,
#              borderwidth = 0, command=lambda:clear_image())
# clear.place(x=20, y = 490)

# root.mainloop()