# run system commands
from subprocess import call
import tempfile
import os


def easy_call(command):
    try:
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


def get_wav_file_length(wav_file):
    import wave
    import contextlib
    with contextlib.closing(wave.open(wav_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration


def generate_tmp_filename(extension="txt"):
    return tempfile._get_default_tempdir() + "/" + next(tempfile._get_candidate_names()) + "." + extension


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