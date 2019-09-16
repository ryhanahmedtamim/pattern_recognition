from scipy.io import arff
from operator import itemgetter
import math
import matplotlib.pyplot as plt


allK = [3, 5, 7]

data = arff.loadarff("wine_train" + '.arff')
global data_frame
data_frame = data[0]


def knn(k):
    instances = 0
    result_string = []
    error = 0

    train_data_frame = data_frame.copy()
    for test_data_row in data_frame:

        instances += 1
        original_response = test_data_row[-1]
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
                train_data_response = train_data_row[-1]
                distances.append({'response': train_data_response, 'distance': distance})

        response = 0
        for i in range(k):
            obj = min(distances, key=itemgetter('distance'))
            response += obj['response']
            distances.remove(obj)

        result = response / k
        error += abs(original_response - result)

        result_string.append('Predicted value : ' + str(round(result, 6)) + '      Actual value : ' + str(round(original_response, 6)) + '\n')

    return [result_string, (error / instances)]


result1 = knn(allK[0])

final_result = result1.copy()
best = allK[0]
result2 = knn(allK[1])
result3 = knn(allK[2])

if result2[1] < final_result[1]:
    final_result = result2.copy()
    best = allK[1]
if result3[1] < final_result[1]:
    final_result = result3.copy()
    best = allK[2]


print("Mean absolute error for k ="+str(allK[0])+ " :"+str(result1[1]))
print("Mean absolute error for k ="+str(allK[1])+ " :"+str(result2[1]))
print("Mean absolute error for k ="+str(allK[2])+ " :"+str(result3[1]))
print("Best k value : "+str(best))
f = open("output/wine_3_5_7.txt","w+")
f.write("Mean absolute error for k ="+str(allK[0])+ " :"+str(result1[1]))
f.write("Mean absolute error for k ="+str(allK[1])+ " :"+str(result2[1]))
f.write("Mean absolute error for k ="+str(allK[2])+ " :"+str(result3[1]))
f.write("Best k value : "+str(best))

for item in final_result[0]:
    f.write(item)
f.close()
# errors = [result1[1], result2[1], result3[1]]
# plt.plot(allK, errors)
# plt.xlabel('K')
# plt.ylabel('Error')