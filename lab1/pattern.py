import math
training_data_list = []
number_of_training_data = int(input("Number of training data :"))

print()
print("Input the training data:")
print("Height(inc) - Weight(kg) - Class")
for i in range(number_of_training_data):

    data = input()
    height, weight ,class_name = data.split(' ')
    data_dictionary = {'height' : height,
                       'weight' : weight,
                       'class' : class_name}
    training_data_list.append(data_dictionary)

print()
print("Enter the query")
print("Height - Weight")
query_data = input()

query_data2 = query_data.split(" ")
test_height = int(query_data2[0])
test_weight = int(query_data2[1])

training_item = training_data_list[0]
training_item_height = int(training_item['height'])
training_item_weight = int(training_item['weight'])
training_item_class = training_item['class']

e_distance = math.sqrt((test_height-training_item_height)**2+
                       (test_weight-training_item_weight)**2)
output_class_name = training_item_class

for item in training_data_list:
    training_item_height = int(item['height'])
    training_item_weight = int(item['weight'])
    training_item_class = item['class']

    temp_e_distance = math.sqrt((test_height-training_item_height)**2+
                       (test_weight-training_item_weight)**2)
    if temp_e_distance < e_distance:
        e_distance = temp_e_distance
        output_class_name = training_item_class


print("test data class is : ",output_class_name)