import os
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk

# Set the directory path
dir_path = "D:\Diploma\cpu\openpose\examples\media"

def parse_coordinates(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    points = []

    for line in lines:
        x, y = line.split()

        x = float(x)
        y = float(y)
        points.append((x, y))

    return points


def normalize_points(points):
    chest_number = 1

    relative_coords = [(0.0,0.0)] * 25
    max_axial_deviation = 0
    for i in range(len(points)):
        relative_coords[i] = (points[i][0] - points[chest_number][0], points[i][1] - points[chest_number][1])

        max_axial_deviation = max(max_axial_deviation, abs(relative_coords[i][0]), abs(relative_coords[i][1]))

    normalization_koeff = 2 * max_axial_deviation
    for i in range(len(points)):
        relative_coords[i] = (relative_coords[i][0] / normalization_koeff, relative_coords[i][1] / normalization_koeff)

    new_points = [(0.0,0.0)]*25
    for i in range(len(points)):
        new_points[i] = (0.5 + relative_coords[i][0], 0.5 + relative_coords[i][1])

    return new_points


def draw_points(file_path):
    colors = {
        0: "green",
        1: "red",
        2: "blue",
        3: "yellow",
        4: "purple",
        5: "orange",
        6: "pink",
        7: "teal",
        8: "magenta",
        9: "lime",
        10: "cyan",
        11: "maroon",
        12: "navy",
        13: "olive",
        14: "gray",
        15: "silver",
        16: "black",
        17: "white",
        18: "indigo",
        19: "turquoise",
        20: "violet",
        21: "chartreuse",
        22: "beige",
        23: "lavender",
        24: "brown"
    }

    draw = ImageDraw.Draw(current_image)
    radius = 5

    coordinates = parse_coordinates(file_path + ".pose")
    #print(coordinates)
    #print(normalize_points(coordinates))
    for i in range(len(coordinates)):
        coord = coordinates[i]
        bbox = (coord[0] - radius, coord[1] - radius, coord[0] + radius, coord[1] + radius)

        draw.ellipse(bbox, fill=colors[i])


# Get all the image files in the directory
image_files = [f for f in os.listdir(dir_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]

# Create a Tkinter window
root = tk.Tk()
root.title("Photo Viewer")

# Load the first image in the directory and resize it to fit inside the window
current_index = 0
file_path = os.path.join(dir_path, image_files[current_index])
current_image = Image.open(file_path)
draw_points(file_path)

window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
width_ratio = window_width / current_image.width
height_ratio = window_height / current_image.height
scale_ratio = min(width_ratio, height_ratio)
new_width = int(current_image.width * scale_ratio)
new_height = int(current_image.height * scale_ratio)
current_image = current_image.resize((new_width, new_height))
image_tk = ImageTk.PhotoImage(current_image)
image_label = tk.Label(root, image=image_tk)
image_label.pack()


# Function to switch to the next image
def next_image(event):
    global current_index, current_image, image_tk, image_label
    if current_index < len(image_files) - 1:
        current_index += 1
    else:
        current_index = 0

    file_path = os.path.join(dir_path, image_files[current_index])
    current_image = Image.open(file_path)

    draw_points(file_path)

    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    width_ratio = window_width / current_image.width
    height_ratio = window_height / current_image.height
    scale_ratio = min(width_ratio, height_ratio)
    new_width = int(current_image.width * scale_ratio)
    new_height = int(current_image.height * scale_ratio)
    current_image = current_image.resize((new_width, new_height))
    image_tk = ImageTk.PhotoImage(current_image)
    image_label.configure(image=image_tk)

# Function to switch to the previous image
def prev_image(event):
    global current_index, current_image, image_tk, image_label
    if current_index > 0:
        current_index -= 1
    else:
        current_index = len(image_files) - 1

    file_path = os.path.join(dir_path, image_files[current_index])
    current_image = Image.open(file_path)
    draw_points(file_path)

    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    width_ratio = window_width / current_image.width
    height_ratio = window_height / current_image.height
    scale_ratio = min(width_ratio, height_ratio)
    new_width = int(current_image.width * scale_ratio)
    new_height = int(current_image.height * scale_ratio)
    current_image = current_image.resize((new_width, new_height))
    image_tk = ImageTk.PhotoImage(current_image)
    image_label.configure(image=image_tk)

# Bind arrow keys to switch between images
root.bind("<Left>", prev_image)
root.bind("<Right>", next_image)

root.mainloop()
