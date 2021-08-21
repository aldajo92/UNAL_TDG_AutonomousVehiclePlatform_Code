import numpy as np
import cv2

class Line:
    def __init__(self):
        # polynomial coefficients averaged over the last n iterations
        self.best_fit = None
        # All others not carried over between first detections
        self.reset()

    def reset(self):
        # was the line detected in the last iteration?
        self.detected = False
        # polynomial coefficients
        self.recent_fit = []
        # polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]
        # difference in fit coefficients between last and new fits
        self.diffs = np.array([0, 0, 0], dtype='float')
        # x values for detected line pixels
        self.allx = None
        # y values for detected line pixels
        self.ally = None

    def fit_line(self, x_points, y_points, first_try=True):
        try:
            n = 5
            self.current_fit = np.polyfit(y_points, x_points, 2)
            self.all_x = x_points
            self.all_y = y_points
            self.recent_fit.append(self.current_fit)
            if len(self.recent_fit) > 1:
                self.diffs = (
                    self.recent_fit[-2] - self.recent_fit[-1]) / self.recent_fit[-2]
            self.recent_fit = self.recent_fit[-n:]
            self.best_fit = np.mean(self.recent_fit, axis=0)
            line_fit = self.current_fit
            self.detected = True

            return line_fit

        except (TypeError, np.linalg.LinAlgError):
            line_fit = self.best_fit
            if first_try == True:
                self.reset()

            return line_fit

class LaneDetection:
    def __init__(self, corners):
        # self._bird_view = np.empty(1)
        self._current_frame = np.empty(0)
        self._result_segmentation = np.empty(1)

        self.width = None
        self.height = None

        self.corners = corners
        self.inv_corners = corners[::-1]
        self.src_points = np.float32(self.inv_corners)
        self._M_inv = np.empty(0)

    def _select_channel(self, bgr_img):
        hsv_img_lane = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        return hsv_img_lane[:,:,1]
    
    def _binary(self, img, thresh_min, thresh_max):
        binary = np.zeros_like(img)
        binary[(img >= thresh_min) & (img <= thresh_max)] = 1
        return binary
    
    def _bird_view(self, img):
        offset = 100 # offset for dst points
        img_size = (img.shape[1], img.shape[0])
        
        dst_points = np.float32([[offset, 0], [img_size[0]-offset, 0], 
                                    [img_size[0]-offset, img_size[1]], 
                                    [offset, img_size[1]]])
        
        M = cv2.getPerspectiveTransform(self.src_points, dst_points)
        self._M_inv = cv2.getPerspectiveTransform(dst_points, self.src_points)
        warped = cv2.warpPerspective(img, M, img_size)
        # return warped, M, self._M_inv
        return warped, M
    
    # def _detect_lines(self, binary_warped):
    #     # Check if lines were last detected; if not, re-run first_lines
    #     if self.left_line.detected == False or self.right_line.detected == False:
    #         _ = self._first_lines(binary_warped)

    #     # Set the fit as the current fit for now
    #     left_fit = self.left_line.current_fit
    #     right_fit = self.right_line.current_fit

    #     # Grab activated pixels
    #     nonzero = binary_warped.nonzero()
    #     nonzeroy = np.array(nonzero[0])
    #     nonzerox = np.array(nonzero[1])

    #     margin = 100
    #     l_lane_inds = ((nonzerox > (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] - margin))
    #                    & (nonzerox < (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] + margin)))
    #     r_lane_inds = ((nonzerox > (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] - margin))
    #                    & (nonzerox < (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] + margin)))

    #     # Extract left and right line pixel positions
    #     leftx = nonzerox[l_lane_inds]
    #     lefty = nonzeroy[l_lane_inds]
    #     rightx = nonzerox[r_lane_inds]
    #     righty = nonzeroy[r_lane_inds]

    #     # Fit new polynomials
    #     left_fit = self.left_line.fit_line(leftx, lefty, False)
    #     right_fit = self.right_line.fit_line(rightx, righty, False)

    #     # Generate x and y values for plotting
    #     fity = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0])
    #     fit_leftx = left_fit[0]*fity**2 + left_fit[1]*fity + left_fit[2]
    #     fit_rightx = right_fit[0]*fity**2 + right_fit[1]*fity + right_fit[2]

    #     # Create an image to draw on and an image to show the selection window
    #     out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
    #     window_img = np.zeros_like(out_img)

    #     # Color in left and right line pixels
    #     out_img[nonzeroy[l_lane_inds], nonzerox[l_lane_inds]] = [255, 0, 0]
    #     out_img[nonzeroy[r_lane_inds], nonzerox[r_lane_inds]] = [0, 0, 255]

    #     return out_img, left_fit, right_fit, fity, fit_leftx, fit_rightx

    def _segmentation_lane_detection(self, binary_bird_view, img_lane):
        (height, width) = img_lane.shape[:2]
        leftx, lefty, rightx, righty, out_img = self._find_lane_pixels(binary_bird_view)

        img_inv = cv2.warpPerspective(out_img, self._M_inv, (width, height)) # Inverse transformation
        result = cv2.addWeighted(img_inv, 0.8, img_lane, 1, 0)
        return result

    def _find_lane_pixels(self, binary_warped):
        # Take a histogram of the bottom half of the image
        histogram = np.sum(binary_warped[binary_warped.shape[0]//2:,:], axis=0)
        # Create an output image to draw on and visualize the result
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))
        # Find the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midpoint = np.int(histogram.shape[0]//2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

        # HYPERPARAMETERS
        # Choose the number of sliding windows
        nwindows = 4
        # Set the width of the windows +/- margin
        margin = 50
        # Set minimum number of pixels found to recenter window
        minpix = 100

        # Set height of windows - based on nwindows above and image shape
        window_height = np.int(binary_warped.shape[0]//nwindows)
        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # Current positions to be updated later for each window in nwindows
        leftx_current = leftx_base
        rightx_current = rightx_base

        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        # Step through the windows one by one
        for window in range(nwindows):
            # Identify window boundaries in x and y (and right and left)
            win_y_low = binary_warped.shape[0] - (window+1)*window_height
            win_y_high = binary_warped.shape[0] - window*window_height
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin
            
            # Draw the windows on the visualization image
    #         cv2.rectangle(out_img,(win_xleft_low,win_y_low),
    #         (win_xleft_high,win_y_high),(0,255,0), 4) 
    #         cv2.rectangle(out_img,(win_xright_low,win_y_low),
    #         (win_xright_high,win_y_high),(0,255,0), 4)
            
            # Identify the nonzero pixels in x and y within the window #
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
            (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
            (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high)).nonzero()[0]
            
            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            
            # If you found > minpix pixels, recenter next window on their mean position
            if len(good_left_inds) > minpix:
                leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:        
                rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        try:
            left_lane_inds = np.concatenate(left_lane_inds)
            right_lane_inds = np.concatenate(right_lane_inds)
        except ValueError:
            # Avoids an error if the above is not implemented fully
            pass

        # Extract left and right line pixel positions
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds] 
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

        ## color in BGR
        out_img[lefty, leftx] =   [0, 0, 255]
        out_img[righty, rightx] = [0, 255, 0]

        return leftx, lefty, rightx, righty, out_img
        
    def process_image(self, img):
        if self._current_frame.size == 0:
            self.width, self.height = img.shape[:2]
        self._current_frame = img
        s_channel = self._select_channel(img)
        binary = self._binary(s_channel, 80, 255)
        binary_bird_view, M = self._bird_view(binary)
        result = self._segmentation_lane_detection(binary_bird_view, img)
        # result2 = draw_region(img, self.corners)
        return result

def draw_region(img, vertices):
    line_color = (0, 0, 255) ## color in BGR
    thickness = 3
    
    image = np.copy(img)
    
    image = cv2.line(image, vertices[0], vertices[1], line_color, thickness)
    image = cv2.line(image, vertices[1], vertices[2], line_color, thickness)
    image = cv2.line(image, vertices[2], vertices[3], line_color, thickness)
    image = cv2.line(image, vertices[3], vertices[0], line_color, thickness)
    return image
