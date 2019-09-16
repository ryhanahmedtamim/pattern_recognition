
def check(flags):

    for flag in flags:
        if flag == False:
            return False
    return True


number_of_data = int(input('number of training data : '))
number_of_feature = int(input('number of feature : '))
training_data = []
flags = []
print()
for i in range(number_of_data):
    flags.append(False)
    data = input('features (x1,x2,x3,x4,...), class : ').split()
    length_of_data = len(data)
    d = []
    for datum in data:
        d.append(int(datum))
    training_data.append(d)


weights = []

for i in range(number_of_feature+1):
    weights.append(0)


item = 0
c = 1
k = 1
while True:

    if check(flags):
        break

    d = weights[0]

    for i in range(1,number_of_feature+1):

        d += (training_data[item][i-1]*weights[i])

    dd = training_data[item][number_of_feature]

    if d>=0 and dd < 0:

        dd = training_data[item][number_of_feature]
        weights[0] = (weights[0] + c * dd * k)

        for kk in range(1,len(weights)):
            weights[kk] = (weights[kk] + c*dd*training_data[item][kk-1])

    elif d < 0 and dd > 0:


        weights[0] = (weights[0] + c * dd *k)

        for kk in range(1,len(weights)):
            weights[kk] = (weights[kk] + c * dd *training_data[item][kk-1] )
    else:

        flags[item] = True

    item += 1
    item %= number_of_data

print('d = ', end='')
print(weights[0], end='')
for i in range(1, len(weights)):
    print(' + ', end='')
    print(weights[i], end='')
    print('*X'+str(i)+" ", end='')
