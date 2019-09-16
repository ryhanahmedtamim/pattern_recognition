import sys
from scipy.io import arff
from operator import itemgetter
import math

print()

f = open("wine_3.txt","w+")
train_file_name = sys.argv[1]
test_file_name = sys.argv[2]
k = int(sys.argv[3])

data = arff.loadarff(train_file_name +'.arff')
train_data_frame = data[0]

data = arff.loadarff(test_file_name + '.arff')
test_data_frame = data[0]

instances = 0
error = 0
for test_data_row in test_data_frame:
	instances += 1
	test_attributes = []
	original_response = test_data_row[-1]
	distances = []
	for train_data_row in train_data_frame:

		distance = 0
		for i in range(len(train_data_row)-1):
			distance += ((test_data_row[i]-train_data_row[i])**2)

		train_data_response = train_data_row[-1]
		distance = math.sqrt(distance)
		distances.append({'response': train_data_response, 'distance' : distance})

	response = 0
	for i in range(k):
		obj = min(distances, key=itemgetter('distance'))
		response += obj['response']
		distances.remove(obj)

	result = response/k
	error += abs(original_response-result)

	print('Predicted value : '+ str(round(result,6)) +'      Actual value : ' +str(round(original_response,6))+'\n')

print('Mean absolute error : '+ str(error/instances)+'\n')
print('Total number of instances : '+str(instances)+'\n')
f.close()