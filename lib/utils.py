import tempfile
from subprocess import call
import sys
import numpy as np
import os

__author__ = 'yossiadi'


def generate_tmp_filename(extension="txt"):
    return tempfile._get_default_tempdir() + "/" + next(tempfile._get_candidate_names()) + "." + extension


def easy_call(command, debug_mode=False):
    try:
        # command = "time " + command
        if debug_mode:
            print >> sys.stderr, command
        call(command, shell=True)
    except Exception as exception:
        print "Error: could not execute the following"
        print ">>", command
        print type(exception)  # the exception instance
        print exception.args  # arguments stored in .args
        exit(-1)


def crop_wav(wav_path, start_trim, end_trim, output_path):
    duration = end_trim - start_trim
    cmd = 'sbin/sox %s %s trim %s %s' % (wav_path, output_path, str(start_trim), str(duration))
    easy_call(cmd)


# get the length of the wav file
def get_wav_file_length(wav_file):
    import wave
    import contextlib
    with contextlib.closing(wave.open(wav_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def normalize_to_prob(y):
    y_norm = np.copy(y)
    for i in range(len(y)):
        total = 0.0
        for j in range(len(y[i])):
            total += y[i][j]
            y_norm[i][j] = np.exp(y[i][j]) / np.sum(np.exp(y[i][j]))
    return y_norm


def concatenate_x_frames(x, y, num_of_frames, is_y=True):
    """
    Concatenate n frames before and after the current frame
    :param x: The features
    :param y: The labels
    :param num_of_frames: The number pf frames to concatenate
    :return: The new features and labels
    """
    if is_y:
        items_x = list()
        items_y = list()

        for item in range(len(x)):
            x_concat = []
            for i in range(num_of_frames, len(x[item]) - num_of_frames):
                tmp_x = None
                is_first = True
                # before the current frame
                for j in range(num_of_frames):
                    tmp_x = np.concatenate((tmp_x, x[item][i - num_of_frames + j].T)) if not is_first else x[item][
                        i - num_of_frames + j]
                    is_first = False
                tmp_x = np.concatenate((tmp_x, x[item][i].T))
                # after the current frame
                for j in range(num_of_frames):
                    tmp_x = np.concatenate((tmp_x, x[item][i + j + 1].T))
                x_concat.append(tmp_x)
            items_y.append(y[item][num_of_frames:len(x[item]) - num_of_frames])
            items_x.append(x_concat)
        return np.array(items_x), np.array(items_y)
    else:
        items_x = list()
        for item in range(len(x)):
            x_concat = []
            for i in range(num_of_frames, len(x[item]) - num_of_frames):
                tmp_x = None
                is_first = True
                # before the current frame
                for j in range(num_of_frames):
                    tmp_x = np.concatenate((tmp_x, x[item][i - num_of_frames + j].T)) if not is_first else x[item][
                        i - num_of_frames + j]
                    is_first = False
                tmp_x = np.concatenate((tmp_x, x[item][i].T))
                # after the current frame
                for j in range(num_of_frames):
                    tmp_x = np.concatenate((tmp_x, x[item][i + j + 1].T))
                x_concat.append(tmp_x)
            items_x.append(x_concat)
        return np.array(items_x)


def csv_append_row(tmp_preds, preds_filename, with_headers=True):

    if with_headers:
        skip_header = True

    all_lines = list()

    # check if the CSV file exists
    if os.path.isfile(preds_filename):
        # read it lines
        for line in open(preds_filename, 'r'):
            all_lines.append(line)
    else:
        # if the file does not exist it does not have headers and they should be copied
        skip_header = False

    # check if there is a header
    for line in open(tmp_preds, 'r'):
        if skip_header:
            skip_header = False
        else:
            all_lines.append(line)
    # now dump everything back
    with open(preds_filename, 'w') as f:
        for line in all_lines:
            f.write(line)