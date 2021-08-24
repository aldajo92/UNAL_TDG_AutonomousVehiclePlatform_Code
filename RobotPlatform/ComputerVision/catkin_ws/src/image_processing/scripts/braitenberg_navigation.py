import numpy as np
import cv2

class Braitenberg:
    def __init__(self, corners_l, corners_r, activation_value):
        self.l_corners = corners_l
        self.r_corners = corners_r
        self.frame = np.empty(0)
        self.activation_value = activation_value
    
    def _select_channel(self, bgr_img):
        hsv_img_lane = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        return hsv_img_lane[:,:,1]
    
    def _binary(self, img, thresh_min, thresh_max):
        binary = np.zeros_like(img)
        binary[(img >= thresh_min) & (img <= thresh_max)] = 1
        return binary
    
    def _check_activation(self, img_region_gray, active_value):
        b_region = self._binary(img_region_gray, 80, 255)
        return b_region.sum() > active_value

    def _sense_pixels(self, img_region_gray):
        b_region = self._binary(img_region_gray, 80, 255)
        return b_region.sum()
    
    def _check_both_activation(self, img_l_gray, img_r_gray, active_value):
        activation_l = self._check_activation(img_l_gray, active_value)
        activation_r = self._check_activation(img_r_gray, active_value)
        return activation_l, activation_r
    
    def _sense_both_pixels(self, img_l_gray, img_r_gray):
        value_l = self._sense_pixels(img_l_gray)
        value_r = self._sense_pixels(img_r_gray)
        return value_l, value_r
    
    def _get_left_right_regions_color(self, image):
        corners_l = self.l_corners
        corners_r = self.r_corners
        img_l_color = image[corners_l[0][1]:corners_l[2][1], corners_l[0][0]:corners_l[2][0], :]
        img_r_color = image[corners_r[0][1]:corners_r[2][1], corners_r[0][0]:corners_r[2][0], :]
        return img_l_color, img_r_color

    def _get_left_right_regions_gray(self, image):
        corners_l = self.l_corners
        corners_r = self.r_corners
        img_l_gray = image[corners_l[0][1]:corners_l[2][1], corners_l[0][0]:corners_l[2][0]]
        img_r_gray = image[corners_r[0][1]:corners_r[2][1], corners_r[0][0]:corners_r[2][0]]
        return img_l_gray, img_r_gray
    
    def process_image(self, image):
        selected_channel = self._select_channel(image)
        img_l_gray, img_r_gray = self._get_left_right_regions_gray(selected_channel)
        activation_l, activation_r = self._check_both_activation(img_l_gray, img_r_gray, self.activation_value)
        return activation_l, activation_r
