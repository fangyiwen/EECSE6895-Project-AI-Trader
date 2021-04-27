import numpy as np
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()
import pandas as pd
import math
import os
import json


def run_lstm_model(stockcode, invoke_from_http=True):
    root_path = "./aitrader/myfolder/lstm/"
    number_of_iterations = 200
    # number_of_iterations = 5

    if not invoke_from_http:
        root_path = "../mysite/aitrader/myfolder/lstm/"

    def LSTMtest(data):
        tf.reset_default_graph()  # clear the computation graph
        n1 = data.shape[1] - 1  # because the last column is label
        n2 = len(data)
        print(n1, n2)

        # Set constant
        input_size = n1  # number of input neurons
        rnn_unit = 7  # number of neurons in the LSTM unit (a layer of neural network)
        lstm_layers = 2  # number of LSTM units
        output_size = 1  # number of output neurons（prediction）
        lr = 0.0006  # learning rate

        train_end_index = math.floor(n2 * 0.9)  # Round down
        print('train_end_index', train_end_index)

        # The first 90% of the data is used as the training set, and the last 10% is used as the test set

        # Training Set
        # time_step: time step，batch_size: how many examples are trained in each batch
        def get_train_data(batch_size=60, time_step=20, train_begin=0,
                           train_end=train_end_index):
            batch_index = []
            data_train = data[train_begin:train_end]
            normalized_train_data = (data_train - np.mean(data_train,
                                                          axis=0)) / np.std(
                data_train, axis=0)

            normalized_train_data = normalized_train_data.values

            train_x, train_y = [], []  # training set
            for i in range(len(normalized_train_data) - time_step):
                if i % batch_size == 0:
                    # start
                    batch_index.append(i)
                    # Get time_step rows data at one time
                # x stores the input dimension (not including label, the last one is not taken)
                # Standardization (normalization)
                x = normalized_train_data[i:i + time_step, :n1]

                # y store label
                y = normalized_train_data[i:i + time_step, n1, np.newaxis]
                # np.newaxis is to increase the dimension in the row or column respectively
                train_x.append(x.tolist())
                train_y.append(y.tolist())
            # end
            batch_index.append((len(normalized_train_data) - time_step))
            print('batch_index', batch_index)
            # print('train_x', train_x)
            # print('train_y', train_y)
            return batch_index, train_x, train_y

        # Test set
        def get_test_data(time_step=20, test_begin=train_end_index + 1):
            data_test = original[test_begin:]
            mean = np.mean(data_test, axis=0)
            std = np.std(data_test, axis=0)  # Matrix standard deviation
            # Standardization (normalization)
            normalized_test_data = (data_test - np.mean(data_test,
                                                        axis=0)) / np.std(
                data_test, axis=0)

            normalized_test_data = normalized_test_data.values
            # There are size samples
            test_size = (len(normalized_test_data) + time_step - 1) // time_step
            print('test_size', test_size)
            test_x, test_y = [], []

            j = test_size - 2
            for i in range(test_size - 1):
                x = normalized_test_data[i * time_step:(i + 1) * time_step, :n1]
                y = normalized_test_data[i * time_step:(i + 1) * time_step, n1]
                test_x.append(x.tolist())
                test_y.extend(y)
            test_x.append(
                (normalized_test_data[(j + 1) * time_step:, :n1]).tolist())
            test_y.extend(
                (normalized_test_data[(j + 1) * time_step:, n1]).tolist())
            return mean, std, test_x, test_y

        # ——————————————————Define neural network variables——————————————————
        # Input layer, output layer weights, bias, dropout parameters
        # Randomly generate w,b
        weights = {
            'in': tf.Variable(tf.random.normal([input_size, rnn_unit])),
            'out': tf.Variable(tf.random.normal([rnn_unit, 1]))
        }
        biases = {
            'in': tf.Variable(tf.constant(0.1, shape=[rnn_unit, ])),
            'out': tf.Variable(tf.constant(0.1, shape=[1, ]))
        }
        keep_prob = tf.placeholder(tf.float32,
                                   name='keep_prob')  # dropout prevents overfitting

        # ——————————————————Define the neural network——————————————————
        def lstmCell():
            basicLstm = tf.nn.rnn_cell.BasicLSTMCell(rnn_unit, forget_bias=1.0,
                                                     state_is_tuple=True)
            drop = tf.nn.rnn_cell.DropoutWrapper(basicLstm,
                                                 output_keep_prob=keep_prob)
            return basicLstm

        def lstm(X):  # Parameters: Enter the number of network batches
            batch_size = tf.shape(X)[0]
            time_step = tf.shape(X)[1]
            w_in = weights['in']
            b_in = biases['in']

            # Forgetting gate (input gate)
            input = tf.reshape(X, [-1, input_size])
            input_rnn = tf.matmul(input, w_in) + b_in
            input_rnn = tf.reshape(input_rnn, [-1, time_step, rnn_unit])
            print('input_rnn', input_rnn)

            # Update gate
            # Build multi-layer lstm
            cell = tf.nn.rnn_cell.MultiRNNCell(
                [lstmCell() for i in range(lstm_layers)])
            init_state = cell.zero_state(batch_size, dtype=tf.float32)

            # output gate
            w_out = weights['out']
            b_out = biases['out']
            # output_rnn is the output of each step of the last layer, and final_states is the output of the last step of each layer
            output_rnn, final_states = tf.nn.dynamic_rnn(cell, input_rnn,
                                                         initial_state=init_state,
                                                         dtype=tf.float32)
            output = tf.reshape(output_rnn, [-1, rnn_unit])
            # The output value is also used as the input of the input gate of the next layer
            pred = tf.matmul(output, w_out) + b_out
            return pred, final_states

        # ————————————————training model————————————————————
        def train_lstm(batch_size=60, time_step=20, train_begin=0,
                       train_end=train_end_index):
            X = tf.placeholder(tf.float32, shape=[None, time_step, input_size])
            Y = tf.placeholder(tf.float32, shape=[None, time_step, output_size])
            batch_index, train_x, train_y = get_train_data(batch_size,
                                                           time_step,
                                                           train_begin,
                                                           train_end)
            with tf.variable_scope("sec_lstm"):
                pred, state_ = lstm(X)
            print('pred,state_', pred, state_)

            # loss function
            loss = tf.reduce_mean(
                tf.square(tf.reshape(pred, [-1]) - tf.reshape(Y, [-1])))
            train_op = tf.train.AdamOptimizer(lr).minimize(loss)
            saver = tf.train.Saver(tf.global_variables(), max_to_keep=15)

            with tf.Session() as sess:
                # initialization
                sess.run(tf.global_variables_initializer())
                theloss = []
                # Number of iterations
                for i in range(number_of_iterations):
                    loss_ = 0
                    for step in range(len(batch_index) - 1):
                        # sess.run(b, feed_dict = replace_dict)
                        state_, loss_ = sess.run([train_op, loss], feed_dict={
                            X: train_x[batch_index[step]:batch_index[step + 1]],
                            Y: train_y[batch_index[step]:batch_index[step + 1]],
                            keep_prob: 0.5})
                    print("Number of iterations:", i, " loss:", loss_)
                    theloss.append(loss_)

                isExists = os.path.exists(
                    root_path + str(stockcode) + "/model/" + time)
                if not isExists:
                    os.makedirs(root_path + str(stockcode) + "/model/" + time)

                modelpath = root_path + str(
                    stockcode) + "/model/" + time + "/model.ckpt"
                print("model_save: ", saver.save(sess, modelpath))
                print("The train has finished")
            return theloss

        theloss = train_lstm()

        # ————————————————prediction————————————————————
        def prediction(time_step=20):

            X = tf.placeholder(tf.float32, shape=[None, time_step, input_size])
            mean, std, test_x, test_y = get_test_data(time_step)

            with tf.variable_scope("sec_lstm", reuse=tf.AUTO_REUSE):
                pred, state_ = lstm(X)
            saver = tf.train.Saver(tf.global_variables())
            modelpath = root_path + str(
                stockcode) + "/model/" + time + "/model.ckpt"
            with tf.Session() as sess:
                saver = tf.train.import_meta_graph(modelpath + '.meta')
                saver.restore(sess, modelpath)
                # module_file = tf.train.latest_checkpoint('model_save2//model.ckpt')
                # saver.restore(sess, module_file)
                test_predict = []
                for step in range(len(test_x) - 1):
                    predict = sess.run(pred, feed_dict={X: [test_x[step]],
                                                        keep_prob: 1})
                    predict = predict.reshape((-1))
                    test_predict.extend(predict)

                # Relative error=(measured value-calculated value)/calculated value×100%
                test_y = np.array(test_y) * std[n1] + mean[n1]
                test_predict = np.array(test_predict) * std[n1] + mean[n1]
                acc = np.average(
                    np.abs(test_predict - test_y[:len(test_predict)]) / test_y[
                                                                        :len(
                                                                            test_predict)])
                print("Relative error:", acc)

                print(theloss)
                plt.figure()
                plt.plot(list(range(len(theloss))), theloss, color='b', )
                plt.xlabel('times', fontsize=14)
                plt.ylabel('loss value', fontsize=14)
                plt.title('loss-----blue', fontsize=10)
                plt.show()
                # Show forecast results as a line graph
                prediction_result.append(test_predict[-1])
                print(prediction_result)
                plt.figure()
                plt.plot(list(range(len(test_predict))), test_predict,
                         color='b', )
                plt.plot(list(range(len(test_y) - day)), test_y[:-day],
                         color='r')
                plt.xlabel('time value/day', fontsize=14)
                plt.ylabel('close value/point', fontsize=14)
                plt.title(time + ': ' + 'predict-----blue,real-----red',
                          fontsize=10)

                isExists = os.path.exists(
                    root_path + str(stockcode) + "/figure")
                if not isExists:
                    os.makedirs(root_path + str(stockcode) + "/figure")
                figurepath = root_path + str(
                    stockcode) + "/figure/" + time + ".jpg"

                plt.savefig(figurepath)
                plt.show()

                # Save datapoint
                isExists = os.path.exists(
                    root_path + str(stockcode) + "/datapoint")
                if not isExists:
                    os.makedirs(root_path + str(stockcode) + "/datapoint")
                time_path = root_path + str(
                    stockcode) + "/datapoint/" + time + ".json"
                loss_path = root_path + str(
                    stockcode) + "/datapoint/" + 'loss' + ".json"

                jsObj = json.dumps({'test_predict': test_predict.tolist(),
                                    'test_y': test_y[:-day].tolist()})
                fileObject = open(time_path, 'w')
                fileObject.write(jsObj)
                fileObject.close()

                jsObj = json.dumps([float(x) for x in theloss])
                fileObject = open(loss_path, 'w')
                fileObject.write(jsObj)
                fileObject.close()

        prediction()

    day = 1
    # stockcode=600036
    data_path = root_path + str(stockcode) + ".SS.csv"
    prediction_result = []

    while day <= 5:
        dataframe = pd.read_csv(data_path)
        original = dataframe
        print("=====================predicting day", day,
              "=========================")
        time = "day" + str(day)
        dataframe[time] = dataframe['close']
        num_list = list(dataframe[time])
        i = 0
        while i < day:
            num_list.pop(0)
            num_list.append(0)
            i = i + 1
        dataframe[time] = num_list
        dataframe = dataframe[:-day]

        LSTMtest(dataframe)
        day = day + 1

    plt.figure()
    plt.plot(list(range(len(prediction_result))), prediction_result,
             color='b', )
    plt.xlabel('days', fontsize=14)
    plt.ylabel('close value', fontsize=14)
    plt.title('future 5 days', fontsize=16)
    figurepath_5days = root_path + str(stockcode) + "/figure/future5days.jpg"
    plt.savefig(figurepath_5days)
    plt.show()

    # Save datapoint
    isExists = os.path.exists(
        root_path + str(stockcode) + "/datapoint")
    if not isExists:
        os.makedirs(root_path + str(stockcode) + "/datapoint")
    future5days_path = root_path + str(
        stockcode) + "/datapoint/" + 'future5days' + ".json"

    jsObj = json.dumps([float(x) for x in prediction_result])
    fileObject = open(future5days_path, 'w')
    fileObject.write(jsObj)
    fileObject.close()

    isExists = os.path.exists(root_path + str(stockcode) + '/solution')
    if not isExists:
        os.makedirs(root_path + str(stockcode) + '/solution')
    with open(root_path + str(stockcode) + '/solution/prediction_result.txt',
              'w') as f:
        for item in prediction_result:
            f.write(str(item) + "\t")

        if prediction_result[0] > original['close'][len(original) - 1]:
            f.write("\n" + "1")
        elif prediction_result[0] == original['close'][len(original) - 1]:
            f.write("\n" + "0")
        elif prediction_result[0] < original['close'][len(original) - 1]:
            f.write("\n" + "-1")
