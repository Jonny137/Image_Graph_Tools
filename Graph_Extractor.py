import cv2
import math
import argparse

origin_x, origin_y, end_x, end_y = -1, -1, -1, -1
refCounter = 0
point_data = []


# draw a circle on a double left mouse click event
# for starting and ending point of a graph
def draw_circle(event, x, y, flags, param):
    global origin_x, origin_y, end_x, end_y

    # ref counter switches values between 0 and 1
    # 0 for selecting starting point and 1 for
    # selecting ending point
    global refCounter

    if event == cv2.EVENT_LBUTTONDBLCLK and refCounter == 0:
        cv2.circle(img, (x, y), 10, (255, 191, 0), -1)
        origin_x = x
        origin_y = y
        refCounter += 1
    elif event == cv2.EVENT_LBUTTONDBLCLK and refCounter == 1:
        cv2.circle(img, (x, y), 10, (255, 191, 0), -1)
        end_x = x
        end_y = y
        refCounter -= 1


#  drawing points of interest on a graph
#  from which we want to write data into
#  a list we made for further processing
def points_of_interest(event, x, y, flags, param):
    global point_data

    # range for x and y axis
    range_x = abs(param[3] - param[2])
    range_y = abs(param[5] - param[4])

    # scaling factor for value/pix
    scale_x = param[1] / range_x
    scale_y = param[0] / range_y

    # in case of double-click event create a dot,
    # append value to a list and print it in terminal
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 10, (255, 191, 0), -1)

        # x-axis
        x_new = set_coord('x', x, scale_x, {
            'min': param[2],
            'max': param[3],
            'offset': param[6],
            'scale': param[8]
        })

        # y-axis
        y_new = set_coord('y', y, scale_y, {
            'min': param[4],
            'max': param[5],
            'offset': param[7],
            'scale': param[9]
        })

        coord = (x_new, y_new)
        point_data.append(coord)
        print(coord)


def set_coord(axis_type, axis, scale, params):
    new_coord = -1

    # mouse pointer is out of grid on the left
    if axis - params['offset'] < 0:
        new_coord = params['min']
    # mouse pointer is out of grid on the right
    elif axis - params['offset'] > width:
        new_coord = params['max']
    # mouse pointer is within the grid
    else:
        if params['scale'] == 'lin':
            # axis is certainly in negative part
            if params['max'] <= 0:
                new_coord = -(axis - params['offset']) / scale
            # axis is certainly in positive part
            elif params['min'] >= 0:
                new_coord = (axis - params['offset']) / scale + params['min']
            # axis is both in negative and positive part
            else:
                new_coord = (axis - params['offset']) / scale + params['min']
        # scale is certainly logarithmic
        else:
            new_offset = (axis - params['offset']) / width
            if axis_type == 'y':
                new_offset = (height - (axis - params['offset'])) / height
            new_coord = params['min'] * math.pow(10, (math.log10(params['max'] / params['min']) * new_offset))

    return new_coord


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to the image')
args = vars(ap.parse_args())

# read an image
img = cv2.imread(args['image'])
img_height, img_width = img.shape[:2]

# prompting user to enter minimum and maximum values for x and y
xmin = float(input('Enter Xmin Value: '))
xmax = float(input('Enter Xmax Value: '))
ymin = float(input('Enter Ymin Value: '))
ymax = float(input('Enter Ymax Value: '))

# prompting user to select scale of axes, linear or logarithmic
# if something else is entered, loop until valid value is entered
x_axis = input('x axis scale: lin or log ? ')

while x_axis != 'lin' and x_axis != 'log':
    print('Non-valid scale entry, try again!')
    x_axis = input('x axis scale: lin or log ? ')

y_axis = input('y axis scale: lin or log ? ')

while y_axis != 'lin' and y_axis != 'log':
    print('Non-valid scale entry, try again!')
    y_axis = input('y axis scale: lin or log ? ')

# display an image window and set the callback
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_circle)

# loop until esc is pressed
while 1:
    cv2.imshow('Image', img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

# calculating width and height based on start and end
# coordinates for ROI and making offset values for x and y
height = origin_y - end_y
width = end_x - origin_x

offset_x = origin_x
offset_y = end_y

# creating param list for sending additional parameters for points
# of interest function setting up a callback for points of interest
param = [height, width, xmin, xmax, ymin, ymax, offset_x, offset_y, x_axis, y_axis]
cv2.setMouseCallback('Image', points_of_interest, param)
cv2.imshow('Image', img)
cv2.waitKey(0)

# closing the windows after finishing the program
cv2.destroyAllWindows()
