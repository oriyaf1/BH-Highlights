import numpy as np
import pandas as pd
import cv2
import time
from matplotlib import pyplot as plt


def __test():
    img_path = R"ScoreBoardType.jpg"

    cap = cv2.VideoCapture(R"C:\Users\Matan\Workspace\NBA\NBA\Videos\videoplayback.mp4")
    counter_frame = 0
    first_frame = None
    frames = []
    while (cap.isOpened()):
        counter_frame += 1
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if (counter_frame % 4 == 0 and counter_frame >= 1000):
            first_frame = gray
        if ((counter_frame + 2) % 4 == 0 and counter_frame >= 1000):
            second_frame = gray
            if (len(frames) > 10):
                frames.pop()
            frames.append((first_frame, second_frame))
        if (len(frames) > 10):
            final = get_images_shared_context(frames)
            p1, p2 = get_scoreboard_rect(final)
            # backtorgb = cv2.cvtColor(final, cv2.COLOR_GRAY2RGB)
            # p = get_scoreboard(backtorgb)
            cv2.rectangle(frame, p1, p2, (0, 255, 0),3)
            # cv2.imshow("f", final)
            cv2.imshow("", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # cv2.destroyAllWindows()
            print(counter_frame)
    cap.release()

    im = cv2.imread(img_path)


def get_images_shared_context(images):
    final = images[0][0].copy()
    ones = np.ones(final.shape, dtype=np.uint8)
    for im1, im2 in images:
        final = final * (ones - (im1 - im2))
        final = (final * (final > 100))
    return final


def get_scoreboard_rect(im):
    ymin = 0
    xmin = 0
    ymax = 0
    xmax = 0
    thresh = np.where(im > 127, 1, 0)
    print (thresh.dtype)
    y, x = im.shape
    intense_in_line_rows = 0
    intense_in_line_columns = 0

    for i, r in enumerate(thresh):
        intense_in_line_rows = max(intense_in_line_rows,np.sum(r))
        intense_in_line_rows = intense_in_line_rows

    intense_in_line_rows = 0.35*intense_in_line_rows
    for i, c in enumerate(thresh.T):
        intense_in_line_columns = max(intense_in_line_columns, np.sum(c))
        intense_in_line_columns =  intense_in_line_columns
    intense_in_line_columns = 0.35*intense_in_line_columns
    print (intense_in_line_columns,intense_in_line_rows)
    for i, r in enumerate(thresh):

        if (np.sum(r) > intense_in_line_rows):
            ymin = max(i - 5, 0)
            print(i)
            break;
    for i, c in enumerate(thresh.T):
        if (np.sum(c) > intense_in_line_columns):
            xmin = max(i - 5, 0)
            print(i)
            break;
    for i, r in enumerate(np.flip(thresh)):
        if (np.sum(r) > intense_in_line_rows):
            ymax = max(i - 5, 0)
            print(i)
            break;
    for i, c in enumerate(np.flip(thresh).T):
        if (np.sum(c) > intense_in_line_columns):
            xmax = max(i - 5, 0)
            print(i)
            break;
    return (xmin, ymin), (x - xmax, y - ymax)


def get_scoreboard(im):
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)

    ## Step #1 - Detect contours using both methods on the same image
    contours1, heirarchy1 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours2, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for index, c in enumerate(contours1):
        img1 = im.copy()
        x, y, w, h = cv2.boundingRect(c)
        if (h < 20 or w < 20): continue
        cv2.drawContours(img1, contours2, index, (0, 255, 0), 3)
        cv2.imshow("b", thresh)
        cv2.imshow("", img1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(index)


if __name__ == '__main__':
    __test()
