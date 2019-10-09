import math


def euclidean_distance(object1, object2):

    dis = 0
    for i in range(len(object1)):
        dis += ((object1[i]-object2[i])**2)
    dis = math.sqrt(dis)
    return dis


def class_distance(class1, class2, all_sample):
    distance = 0
    n = len(class1['class'])*len(class2['class'])

    for cls1 in class1['class']:
        for cls2 in class2['class']:
            d = euclidean_distance(all_sample[cls1-1], all_sample[cls2-1])

            distance += d
    distance /= n
    return round(distance, 1)


def initial_distance(all_samples):
    _distances = []
    for i in range(len(all_samples)):
        _distance = []
        for j in range(len(all_samples)):
            _distance.append(euclidean_distance(all_samples[i], all_samples[j]))
        _distances.append(_distance)
    return _distances


def join_classes(all_classes, class1, class2):
    for c in range(len(all_classes)):
        if all_classes[c] == class1:
            for cc in class2['class']:
                all_classes[c]['class'].append(cc)
            all_classes[c]['class'].sort()

    for c in range(len(all_classes)):
        if all_classes[c] == class2:
            all_classes.remove(all_classes[c])
            break
    return all_classes


def classify(_classes, _distances, all_sample):
    min_distance = 999999999
    index1 = 0
    index2 = 0
    for i in range(len(_classes)):
        for j in range(i):

            if i != j:
                if _distances[i][j] < min_distance:
                    min_distance = distances[i][j]
                    index1 = i
                    index2 = j

    updated_classes = join_classes(_classes, _classes[index1], _classes[index2])

    update_distance = []
    for i in range(len(updated_classes)):
        d = []
        for j in range(len(updated_classes)):

            if i == j:
                d.append(0)
                #print(0, " ", end="")
            else:
                cc1 = updated_classes[i]
                cc2 = updated_classes[j]

                d.append(class_distance(cc1, cc2, all_sample))
               # print(class_distance(cc1, cc2, all_sample), " ",  end="")
        update_distance.append(d)
        print()

    #print("\nupdated class\n", updated_classes)
    for cls in updated_classes:
        print(cls['class'], end="")
    return updated_classes, update_distance


input_file = open("input.txt", "r")

if input_file.mode == 'r':
    contents = input_file.read().split("\n")


number_of_sample = int(contents[0])
number_of_feature = int(contents[1])

samples = []
classes = []
for i in range(number_of_sample):
    data = contents[i+2].split()
    classes.append({"class": [i+1]})
    for j in range(len(data)):
        data[j] = int(data[j])
    samples.append(data)

distances = initial_distance(samples)

for i in range(len(classes)):
    for j in range(len(classes)):

        if i == j:
            print("0 ", end=" ")
        else:
            print(round(distances[i][j], 1), end="  ")
    print()

print()
samples2 = samples.copy()
for k in range(len(samples)-1):
    classes, distances = classify(classes, distances,samples)

