from scipy.io import arff
from operator import itemgetter
import math
import statistics
import matplotlib.pyplot as plt


allK = [1, 5, 10, 20, 30]
data = arff.loadarff("yeast_train" + '.arff')
global data_frame

data_frame = data[0]

global instances

def knn(k):

    instances = 0
    correct = 0
    train_data_frame = data_frame.copy()

    for test_data_row in data_frame:

        instances += 1
        original_class = test_data_row[-1].decode("utf-8")
        distances = []
        for train_data_row in train_data_frame:

            flag = False
            for i in range(len(train_data_row)):
                if test_data_row[i] != train_data_row[i]:
                    flag = True
                    break

            if flag:
                distance = 0
                for i in range(len(train_data_row)-1):
                    distance += ((test_data_row[i] - train_data_row[i]) ** 2)

                distance = math.sqrt(distance)
                train_data_class = train_data_row[-1].decode("utf-8")
                distances.append({'class': train_data_class, 'distance': distance})
        classes = []
        for i in range(k):
            obj = min(distances, key=itemgetter('distance'))
            classes.append(obj['class'])
            distances.remove(obj)

        try:
            predicted_class = statistics.mode(classes)
        except statistics.StatisticsError as e:
            predicted_class = classes[0]

        if predicted_class == original_class:
            correct += 1
    return correct


result = []

item = 0
for v_K in allK:
    result.append(knn(v_K))
    print("Correctly classified for k = " + str(v_K) + " : " + str(result[item]))
    item += 1

plt.plot(allK, result)
plt.xlabel('K')
plt.ylabel('Error')
plt.show()