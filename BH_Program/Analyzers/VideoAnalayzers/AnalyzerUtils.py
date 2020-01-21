import numpy as np


def get_images_shared_context(images):
    final = images[0][0].copy()
    ones = np.ones(final.shape, dtype=np.uint8)
    for im1, im2 in images:
        final = final * (ones - (im1 - im2))
        final = (final * (final > 100))
    return final


def get_scoreboard_rect(im):
    MIN_INTENSE_IN_ROW_RATIO = 0.35
    MIN_INTENSE_IN_COL_RATIO = 0.55

    thresh = np.where(im > 127, 1, 0)
    y, x = im.shape

    intense_in_line_rows = MIN_INTENSE_IN_ROW_RATIO * __get_max_intense_line_intensity(thresh)
    intense_in_line_columns = MIN_INTENSE_IN_COL_RATIO * __get_max_intense_line_intensity(thresh.T)

    ymin = __find_first_intense_row(thresh, intense_in_line_rows)
    xmin = __find_first_intense_col(thresh, intense_in_line_columns)
    ymax = __find_first_intense_row(np.flip(thresh), intense_in_line_rows)
    xmax = __find_first_intense_col(np.flip(thresh), intense_in_line_columns)

    return (xmin, ymin), (x - xmax, y - ymax)


#################################################################
###############  PRIVATES   #####################################
#################################################################

def __find_first_intense_row(im, min_intense, margin=5):
    for i, r in enumerate(im):
        if (np.sum(r) > min_intense):
            return max(i - margin, 0)


def __find_first_intense_col(im, min_intense, margin=5):
    for i, r in enumerate(im.T):
        if (np.sum(r) > min_intense):
            return max(i - margin, 0)


def __get_max_intense_line_intensity(im):
    max_intence = 0
    for i, r in enumerate(im):
        max_intence = max(max_intence, np.sum(r))
    return max_intence
