import argparse
import os
import sys

from lib.textgrid import *

__author__ = 'yossiadi'


def create_text_grid(label_path, wav_filename, output_textgrid_filename, length, start_extract, csv_filename):
    # defines
    msc_2_sec = 0.001

    # validation
    if not os.path.exists(label_path):
        print >> sys.stderr, "label file does not exits"
        return

    # read the label file and parse it
    fid = open(label_path)
    lines = fid.readlines()
    values = lines[0].split()
    fid.close()

    # create the TextGrid file and save it
    if len(values) == 2:
        onset = values[0]
        offset = values[1]
        text_grid = TextGrid()

        vot_tier = IntervalTier(name='word', xmin=0.0, xmax=float(length))
        vot_tier.append(Interval(0, (float(onset) * msc_2_sec + start_extract) * 10, ""))
        vot_tier.append(
            Interval((float(onset) * msc_2_sec + start_extract) * 10, (float(offset) * msc_2_sec + start_extract) * 10,
                     "word"))
        vot_tier.append(Interval((float(offset) * msc_2_sec + start_extract) * 10, float(length), ""))

        text_grid.append(vot_tier)
        text_grid.write(output_textgrid_filename)

    if csv_filename:
        with open(csv_filename, 'w') as f:
            f.write("FILE, DURATION, START_TIME, END_TIME\n")
            f.write("%s, %f, %f, %f\n" % (wav_filename, 1000.0 * (
                                              (float(offset) * msc_2_sec + start_extract) * 10 -
                                              (float(onset) * msc_2_sec + start_extract) * 10),
                                          (float(onset) * msc_2_sec + start_extract) * 10,
                                          (float(offset) * msc_2_sec + start_extract) * 10))


if __name__ == "__main__":
    # the first argument is the label file path
    # the second argument is the wav file path
    # the third argument is the output path
    # -------------MENU-------------- #
    # command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("label_filename", help="The label file")
    parser.add_argument("wav_filename", help="The wav file")
    parser.add_argument("output_textgrid", help="The output TextGrid file")
    args = parser.parse_args()

    # main function
    create_text_grid(args.label_filename, args.wav_filename, args.output_text_grid, 0.05)
