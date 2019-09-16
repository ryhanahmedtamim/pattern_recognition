def open_file(file):
    train_file = open(file, "r")
    data = ""
    if train_file.mode == 'r':
        data = train_file.read()
    return data


stopwords = open_file('stopwords.txt').split()
#print(stopwords)

def clean_data(stopwords, data):
    data = data.replace(',', '')
    data = ' '.join(i for i in data.split() if i not in stopwords)
    return data


def data_formation(data):
    sentence_list = []

    for sentence in data:

        #try:
        global stopwords
        splited_data = sentence.split('\n')
        comments = clean_data(stopwords,splited_data[2].lower())
        data_and_class ={'data' : comments.strip(),
         'class' : splited_data[1].strip()}
        sentence_list.append(data_and_class)
        #except:

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
          number_of_class+=1
          all_class.append(cls)
          all_class_comment.append({"class": cls, 'data': cmt, 'freq' : 1})

      else:
          for i in range(len(all_class_comment)):
              if all_class_comment[i]['class'] == cls:
                  all_class_comment[i]['data'] += ' '+cmt
                  all_class_comment[i]['freq'] += 1
                  #print(all_class_comment[i]['freq'])

  word_frequency_by_class = []
  number_of_words = 0

  for c in all_class_comment:
      cls = c['class']
      cmnt = c['data'].split()
      word = []
      word_frequency = []
      cnt = 0
      word_count = 0
      for w in cmnt:
          cnt+=1
          if w not in word:
              w = w.replace('.', '')
              word.append(w)
              word_frequency.append({'word' : w, 'freq' : 1})
              word_count+=1
          else:
              for i in range(len(word_frequency)):
                  if word_frequency[i]['word'] == w:
                      word_frequency[i]['freq'] += 1

      number_of_words += cnt
      p_cls = c['freq']/len(data)


      word_frequency_by_class.append({'class' : cls,'probability': p_cls, 'total_words' : cnt,'word_freq' : word_frequency})
  #print(word_frequency_by_class)
  return word_frequency_by_class, number_of_class, number_of_words, word_count


def word_freq(data,word):
    cnt = 0
    for datum in data:
        for w in datum['data'].split():
            w = w.replace('.','')
            if w == word:
                cnt+=1
    return cnt


def word_freq_class(data, word):
    cnt = 0
    for datum in data:
        if datum['word'] == word:
            return datum['freq']
    return cnt


train_data = open_file('train3.txt').split("\n\n")

train_data = data_formation(train_data)

word_frequency_by_class, number_of_class, number_of_words, word_count = count(train_data)

test_data1 = open_file('test3.txt').split("\n\n")

names = []
for d in test_data1:
    d_list = d.split('\n')
    names.append(d_list[0])
#print(names)
print()
test_data = data_formation(test_data1)
total_test_data = 0
test_corrected = 0
names_index = 0
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
        p_of_s_c = 1
        t_d = len(test_sentence.split())
        for w in test_sentence.split():
            w = w.replace('.','')
            w_freq = word_freq(train_data,w)
            if w_freq != 0:
                p_of_w = (w_freq)/(number_of_words)
                p_of_s *= p_of_w
                w_freq_by_c = word_freq_class(word_freq_by_c,w)
                #print(total_word+number_of_words)
                p_of_w_c = (w_freq_by_c+1)/(total_word+word_count)
                p_of_s_c *= p_of_w_c

        e_probability = (p_of_s_c*p_of_class)/p_of_s
        t_p+=e_probability

        print('class :', temp_class," p",e_probability)
        #print('original :', original_cls)
        if e_probability > p:
            _class = temp_class
            p = e_probability

    print(names[names_index]," : " ,_class)
    names_index+=1

    if original_cls ==_class:
        print("Right")
        test_corrected += 1
    else:
        print("Wrong")
    print('\n')
print("accuracy" , test_corrected*100/total_test_data,"%")