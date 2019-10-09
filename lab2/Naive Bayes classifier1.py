def open_file(file):
    train_file = open(file, "r")
    data = ""
    if train_file.mode == 'r':
        data = train_file.read()
    return data


stopwords = open_file('stopwords.txt').split()


# print(stopwords)

def clean_data(stopwords, data):
    data = data.replace(',', '')

    data = ' '.join(i for i in data.split() if i not in stopwords)
    return data


def data_formation(data):
    sentence_list = []

    for sentence in data:
        # try:
        global stopwords
        splited_data = sentence.split('\n')
        comments = clean_data(stopwords, splited_data[2].lower())
        data_and_class = {'data': comments.strip(),
                          'class': splited_data[1].strip()}
        sentence_list.append(data_and_class)
        # except:

    return sentence_list


def count(data):
    frequency_list = []

    number_of_class = 0
    all_class = []
    all_class_comment = []
    for datum in data:
        cls = datum['class']
        cmt = datum['data']

        if cls not in all_class:
            number_of_class += 1
            all_class.append(cls)
            all_class_comment.append({"class": cls, 'data': cmt, 'freq': 1})

        else:
            for i in range(len(all_class_comment)):
                if all_class_comment[i]['class'] == cls:
                    all_class_comment[i]['data'] += ' ' + cmt
                    all_class_comment[i]['freq'] += 1
                    # print(all_class_comment[i]['freq'])

    word_frequency_by_class = []
    number_of_words = 0

    for c in all_class_comment:

        # print(c['freq'])

        cls = c['class']

        cmnt = c['data'].split()
        words = []
        word_frequency = []
        cnt = 0
        for w in cmnt:
            cnt += 1
            if w not in words:
                w = w.replace('.', '')
                words.append(w)
                word_frequency.append({'word': w, 'freq': 1})
            else:
                for i in range(len(word_frequency)):
                    if word_frequency[i]['word'] == w:
                        word_frequency[i]['freq'] += 1

        number_of_words += cnt
        p_cls = (c['freq'] / len(data) + .1) / (1 + number_of_class * .1)

        word_frequency_by_class.append(
            {'class': cls,'cls_freq':c['freq'] ,'probability': p_cls, 'total_words': cnt, 'word_freq': word_frequency})
    # print(word_frequency_by_class)
    return word_frequency_by_class, number_of_class, number_of_words


def word_freq(data, word):
    cnt = 0
    for datum in data:
        for w in datum['data'].split():
            w = w.replace('.', '')
            if w == word:
                cnt += 1
    return cnt


def word_freq_class(data, word):
    cnt = 0
    for datum in data:
        if datum['word'] == word:
            return datum['freq']
    return cnt


def training(data, word_frequency_by_class):
    trained_data = []
    cls = []
    for datum in data:
        s = datum['data']
        #print(s)
        for w in s.split():
            #print(w)
            #input()
            for all_class in word_frequency_by_class:
                temp_class = all_class['class']
                total_word = all_class['total_words']
                word_freq_by_c = all_class['word_freq']
                c = all_class['cls_freq']
                w_freq_by_c = word_freq_class(word_freq_by_c,w)

                p_of_w_c = (w_freq_by_c/c + .1) / (1 + 2 * .1)
                #print(w)
                ww = w + temp_class

                trained_data.append({'c':ww ,'f':p_of_w_c})
    return trained_data



train_data = open_file('train2.txt').split("\n\n")

train_data = data_formation(train_data)

word_frequency_by_class, number_of_class, number_of_words = count(train_data)

trained_data =training(train_data,word_frequency_by_class)
#input()
print(number_of_words)
print(number_of_class)

test_data1 = open_file('test2.txt').split("\n\n")

test_data = data_formation(test_data1)
total_test_data = 0
test_corrected = 0
for data in test_data:
    t_p = 0
    total_test_data += 1
    original_cls = data['class']
    test_sentence = data['data']
    _class = original_cls
    p = 0
    for all_class in word_frequency_by_class:
        temp_class = all_class['class']
        p_of_class = all_class['probability']
        total_word = all_class['total_words']
        word_freq_by_c = all_class['word_freq']
        p_of_s = 1
        p_of_s_c = p_of_class
        for w in test_sentence.split():
            w = w.replace('.', '')
            w_freq = word_freq(train_data, w)

            if w_freq != 0:
                w= w+temp_class
                for i in range(len(trained_data)):
                    if trained_data[i]['c'] == w:
                        p_of_s_c*=trained_data[i]['f']
                p_of_s = (w_freq/number_of_words + .1) / (1 + number_of_class * .1)


        # print(((p_of_s_c*p_of_class)),p_of_s)
        e_probability = (p_of_s_c * p_of_class) / p_of_s
        t_p += e_probability

        print('class :', temp_class, " p", e_probability)
        print()
        # print('original :', original_cls)
        if e_probability > p:
            _class = temp_class
            p = e_probability
    print(_class)
    print()
    print(t_p)
    print()

    if original_cls == _class:
        test_corrected += 1

print("accuracy", test_corrected / total_test_data)
