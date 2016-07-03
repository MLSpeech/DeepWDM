
import argparse
import sys
from label2textgrid import create_text_grid
from lib import utils
from post_process import post_process
from lib.utils import *
import front_end.predict_single_file as fe
import os

def predict(input_path, output_path, model, csv_filename):

    if not os.path.exists(input_path):
        print >> sys.stderr, "%s file does not exits" % input_path
        return

    t_model = model.upper()    
    if t_model == 'RNN':
        model_path = 'results/1_layer_model.net'
        print '==> using single layer RNN'
    elif t_model == '2RNN':
        model_path = 'results/2_layer_model.net'
        print '==> using 2 stacked layers RNN'
    elif t_model == 'BIRNN':
        model_path = 'results/bi_model.net'
        print '==> using bi-directional RNN'
    else:
        model_path = 'results/1_layer_model.net'
        print '==> unknown model, using default model: single RNN'

    length = utils.get_wav_file_length(input_path)

    feature_file = generate_tmp_filename('features')
    prob_file = generate_tmp_filename('prob')
    predict_file = generate_tmp_filename('prediction')
    dur_file = generate_tmp_filename('dur')

    print '\n1) Extracting features and classifying ...'
    os.chdir("front_end/")
    fe.main(os.path.abspath(os.path.abspath(input_path)), feature_file)
    os.chdir("..")

    print '\n2) Model predictions ...'
    cmd = 'th classify.lua -x_filename %s -class_path %s -prob_path %s -model_path %s' % (
        feature_file, predict_file, prob_file, model_path)
    os.chdir("back_end/")
    utils.easy_call(cmd)
    os.chdir("..")

    print '\n3) Extracting duration'
    post_process(os.path.abspath(predict_file), dur_file)

    print '\n4) Writing TextGrid file to %s ...' % output_path
    create_text_grid(dur_file, input_path, output_path, length, float(0.0), csv_filename)

    # remove leftovers
    os.remove(feature_file)
    os.remove(prob_file)
    os.remove(predict_file)
    os.remove(dur_file)


if __name__ == "__main__":
    # -------------MENU-------------- #
    # command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="The path to the wav file")    
    parser.add_argument("output_path", help="The path to save new text-grid file")
    parser.add_argument("model", help="The type pf model: rnn | 2rnn | birnn")
    parser.add_argument("--csv_output", help="Output results to a CSV file")
    args = parser.parse_args()

    # main function
    predict(args.input_path, args.output_path, args.model, args.csv_output)
