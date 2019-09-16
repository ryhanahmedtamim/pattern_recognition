import sys
from scipy.io import arff
from operator import itemgetter
import math
import statistics

train_file_name = sys.argv[1]
test_file_name = sys.argv[2]
k = int(sys.argv[3])

data = arff.loadarff(train_file_name +'.arff')
train_data_frame = data[0]

data = arff.loadarff(test_file_name +'.arff')
test_data_frame = data[0]

instances = 0
correct = 0
for test_data_row in test_data_frame:
	instances += 1
	test_attributes = []

	original_class = test_data_row[-1].decode("utf-8")
	
	distances = []
	for train_data_row in train_data_frame:

		distance = 0
		for i in range(len(test_data_row)-1):
			distance += ((test_data_row[i]-train_data_row[i])**2)

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
		correct+=1

	print('Predicted class : ', predicted_class,'      Actual class : ', original_class)
print('Number of correctly classified instances : ',correct)
print('Total number of instances : ', instances)
print('Accuracy : ', (correct / instances))
