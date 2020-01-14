import numpy as np
import pandas as pd
import cv2
import time
from matplotlib import pyplot as plt


def get_images_shared_context(images):
    final = images[0][0].copy()
    ones = np.ones(final.shape, dtype=np.uint8)
    for im1, im2 in images:
        final = final * (ones - (im1 - im2))
        final = (final * (final > 100))
    return final

def get_scoreboard_rect(im):
    ymin = xmin = ymax = xmax = 0
    MIN_INTENSE_IN_ROW_RATIO = 0.35
    MIN_INTENSE_IN_COL_RATIO = 0.55

    thresh = np.where(im > 127, 1, 0)
    y, x = im.shape

    intense_in_line_rows = MIN_INTENSE_IN_ROW_RATIO * __get_max_intense_line_intensity(thresh)
    intense_in_line_columns = MIN_INTENSE_IN_COL_RATIO * __get_max_intense_line_intensity(thresh.T)

    ymin  = __find_first_intense_row(thresh,intense_in_line_rows)
    xmin = __find_first_intense_col(thresh, intense_in_line_columns)
    ymax =__find_first_intense_row(np.flip(thresh),intense_in_line_rows)
    xmax = __find_first_intense_col(np.flip(thresh), intense_in_line_columns)

    return (xmin, ymin), (x - xmax, y - ymax)


def __find_first_intense_row(im, min_intense,margin = 5):
    for i, r in enumerate(im):
        if (np.sum(r) > min_intense):
            return max(i - margin, 0)

def __find_first_intense_col(im, min_intense,margin = 5):
    for i, r in enumerate(im.T):
        if (np.sum(r) > min_intense):
            return max(i - margin, 0)

def __get_max_intense_line_intensity(im):
    max_intence = 0
    for i, r in enumerate(im):
        max_intence = max(max_intence, np.sum(r))
    return max_intence


def __test():
    img_path = R"ScoreBoardType.jpg"

    cap = cv2.VideoCapture(R"C:\Users\Matan\Workspace\NBA\NBA\Videos\liverpool.mp4")
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
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 3)
            cv2.imshow("f", final)
            cv2.imshow("", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # cv2.destroyAllWindows()
            print(counter_frame)
    cap.release()

    im = cv2.imread(img_path)


if __name__ == '__main__':
    __test()
