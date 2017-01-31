import argparse
from lib.htkmfc import HTKFeat_read
from run_front_end import extract_single_mfcc
import numpy as np
import os
import tempfile


def generate_tmp_filename(extension="txt"):
    return tempfile._get_default_tempdir() + "/" + next(tempfile._get_candidate_names()) + "." + extension


def main(wav_path, features_path):
    # extract the features
    tmp_htk_filename = generate_tmp_filename("htk")
    extract_single_mfcc(wav_path, tmp_htk_filename)

    # convert them to .txt file
    reader = HTKFeat_read(tmp_htk_filename)
    matrix = reader.getall()

    # write them to the desired output
    f_handle = file(features_path, 'a')
    np.savetxt(f_handle, matrix)
    f_handle.close()

    # remove leftovers
    os.remove(tmp_htk_filename)


if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser(description="This script extract the mfcc features from a given audio file.")
    parser.add_argument("wav_path", help="The path to the audio files")
    parser.add_argument("features_path", help="The path to save the mfcc's and labels, the saved file will be a "
                                              "pickle file for both features and labels")
    args = parser.parse_args()

    main(args.wav_path, args.features_path)
