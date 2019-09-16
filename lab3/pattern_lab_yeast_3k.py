from scipy.io import arff
from operator import itemgetter
import math
import statistics
import matplotlib.pyplot as plt


allK = [3, 5, 7]
data = arff.loadarff("yeast_train" + '.arff')
global data_frame

data_frame = data[0]


def knn(k):
    instances = 0
    result = []
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

        result.append('Predicted class : '+ predicted_class+ '      Actual class : '+ original_class+'\n')
    result.append('Number of correctly classified instances : '+ str(correct)+'\n')
    print(correct, instances)
    return [result, correct, instances]


result1 = knn(allK[0])
final_result = result1.copy()
best = allK[0]
result2 = knn(allK[1])
result3 = knn(allK[2])

if result2[1] > final_result[1]:
    final_result = result2.copy()
    best = allK[1]
if result3[1] > final_result[1]:
    final_result = result3.copy()
    best = allK[2]

f = open("output/yeast_3_5_7.txt","w+")
print("Number of incorrectly classified instances for k ="+str(allK[0])+ " :"+str(result1[2]-result1[1]))
print("Number of incorrectly classified instances for k ="+str(allK[1])+ " :"+str(result2[2]-result2[1]))
print("Number of incorrectly classified instances for k ="+str(allK[2])+ " :"+str(result3[2]-result3[1]))
print("Best k value : "+str(best))

errors = [result1[2]-result1[1], result2[2]-result2[1],result3[2]-result3[1]]

f.write("Number of incorrectly classified instances for k ="+str(allK[0])+ " :"+str(result1[2]-result1[1])+"\n")
f.write("Number of incorrectly classified instances for k ="+str(allK[1])+ " :"+str(result2[2]-result2[1])+'\n')
f.write("Number of incorrectly classified instances for k ="+str(allK[2])+ " :"+str(result3[2]-result3[1])+"\n")
f.write("Best k value : "+str(best)+"\n")

for item in final_result[0]:
    f.write(item)

# plt.plot(allK, errors)
# plt.xlabel('K')
# plt.ylabel('Error')
