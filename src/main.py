from nicegui import ui
from PIL import Image
import cv2 as cv2
import numpy as np

# image_frame_path = "./images/24-colour-patches.png"
image_frame_path = "./images/colour_wheel.png"
img_frame_RGB = cv2.cvtColor(cv2.imread(filename=image_frame_path), cv2.COLOR_BGR2RGB)
img_frame_LAB = cv2.cvtColor(img_frame_RGB, cv2.COLOR_RGB2Lab)
img_frame_HSV = cv2.cvtColor(img_frame_RGB, cv2.COLOR_RGB2HSV)


min_thres_R = 0
max_thres_R = 255
min_thres_G = 0
max_thres_G = 255
min_thres_B = 0
max_thres_B = 255

min_thres_H = 0
max_thres_H = 255
min_thres_S = 0
max_thres_S = 255
min_thres_V = 0
max_thres_V = 255


min_thres_L  = 0
max_thres_L  = 255
min_thres_A = 0
max_thres_A = 255
min_thres_b = 0
max_thres_b = 255

def mask_image():
    global RGB_Img, HSV_Img, LAB_Img
    # RGB Mask
    lower_bound = np.array([min_thres_R, min_thres_G, min_thres_B], dtype=np.uint8)
    upper_bound = np.array([max_thres_R, max_thres_G, max_thres_B], dtype=np.uint8)
    
    mask = cv2.inRange(img_frame_RGB, lower_bound, upper_bound)
    new_img_frame_RGB = cv2.bitwise_and(img_frame_RGB, img_frame_RGB, mask=mask)
    RGB_Img.set_source(Image.fromarray(new_img_frame_RGB, 'RGB'))

    # HSV Mask
    lower_bound = np.array([min_thres_H, min_thres_S, min_thres_V], dtype=np.uint8)
    upper_bound = np.array([max_thres_H, max_thres_S, max_thres_V], dtype=np.uint8)
    
    mask = cv2.inRange(img_frame_HSV, lower_bound, upper_bound)
    new_img_frame_HSV = cv2.bitwise_and(img_frame_HSV, img_frame_HSV, mask=mask)
    HSV_Img.set_source(Image.fromarray(cv2.cvtColor(new_img_frame_HSV, cv2.COLOR_HSV2RGB), 'RGB'))

    # YCC Mask
    lower_bound = np.array([min_thres_L, min_thres_A, min_thres_b], dtype=np.uint8)
    upper_bound = np.array([max_thres_L, max_thres_A, max_thres_b], dtype=np.uint8)
    
    mask = cv2.inRange(img_frame_LAB, lower_bound, upper_bound)
    new_img_frame_LAB = cv2.bitwise_and(img_frame_LAB, img_frame_LAB, mask=mask)
    LAB_Img.set_source(Image.fromarray(cv2.cvtColor(new_img_frame_LAB, cv2.COLOR_LAB2RGB), 'RGB'))

    

def labeled_slider(bound_min_var_name, bound_max_var_name, label_text="text", slider_min=0, slider_max=255, slider_step=1):
    with ui.row().classes("no-wrap w-full items-center"):
        ui.label(label_text).classes("ml-3")
        with ui.range(min=slider_min, max=slider_max, step=slider_step, value={'min': slider_min, 'max': slider_max}) as range:
            range.props('label-always') \
            .classes("pr-5 pl-5 pt-4 w-full")\
            .bind_value_to(globals(), bound_min_var_name, forward=lambda x: x["min"]) \
            .bind_value_to(globals(), bound_max_var_name, forward=lambda x: x["max"]) \
            .on_value_change(callback=mask_image) \

with ui.grid(columns=3).classes("w-full items-center"):
        ui.label("RGB Image").classes("text-center")
        ui.label("HSV Image").classes("text-center")
        ui.label("LAB Image").classes("text-center")

        ui.separator()
        ui.separator()
        ui.separator()

        labeled_slider(label_text="R",  bound_min_var_name="min_thres_R", bound_max_var_name="max_thres_R")
        labeled_slider(label_text="H",  bound_min_var_name="min_thres_H", bound_max_var_name="max_thres_H", slider_max=180)
        labeled_slider(label_text="L",  bound_min_var_name="min_thres_L", bound_max_var_name="max_thres_L")

        labeled_slider(label_text="G",  bound_min_var_name="min_thres_G", bound_max_var_name="max_thres_G")
        labeled_slider(label_text="S",  bound_min_var_name="min_thres_S", bound_max_var_name="max_thres_S")
        labeled_slider(label_text="A", bound_min_var_name="min_thres_A", bound_max_var_name="max_thres_A")
        
        labeled_slider(label_text="B",  bound_min_var_name="min_thres_B", bound_max_var_name="max_thres_B")
        labeled_slider(label_text="V",  bound_min_var_name="min_thres_V", bound_max_var_name="max_thres_V")
        labeled_slider(label_text="B", bound_min_var_name="min_thres_b", bound_max_var_name="max_thres_b")

        RGB_Img = ui.image(Image.fromarray(img_frame_RGB, 'RGB'))
        HSV_Img = ui.image(Image.fromarray(cv2.cvtColor(img_frame_HSV, cv2.COLOR_HSV2RGB), 'RGB'))
        LAB_Img = ui.image(Image.fromarray(cv2.cvtColor(img_frame_LAB, cv2.COLOR_LAB2RGB), 'RGB'))

ui.run()