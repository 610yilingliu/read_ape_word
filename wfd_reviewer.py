import os
import string
import pandas as pd
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

#查看函数被调用多少次的，比较方便的计数器
def count_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        result = func(*args, **kwargs)
        return result, wrapper.calls  # 返回结果和调用次数
    wrapper.calls = 0
    return wrapper

class wfd_reviewer:
    def __init__(self, input_folder = './wfd/input', output_folder = './wfd/output'):
        self.wfd_table = None
        self.input_folder = input_folder
        self.output_folder = output_folder


    def first_time_init(self, path):
        data = pd.read_csv(os.path.join(self.input_folder, path))
        data['wrong'] = 0
        data['reviewed'] = 0
        data['wrong_date'] = pd.Series([[] for _ in range(len(data))])
        data['wrong_record'] = pd.Series([[] for _ in range(len(data))])

        self.wfd_table = data

    def load_existed_data(self, input_path):
        self.wfd_table = pd.read_csv(os.path.join(self.input_folder, input_path))
        self.wfd_table['wrong_date'] = self.wfd_table['wrong_date'].apply(eval)
        self.wfd_table['wrong_record'] = self.wfd_table['wrong_record'].apply(eval)

    def review(self, output_path, prob_range = 'all'):
        if prob_range == 'all':
            for i in range(len(self.wfd_table)):
                print(f'WFD Question Number {i + 1}')
                check_res, call_cnt = self.checker(self.wfd_table['English Content'][i])
                res, stud_input = check_res
                if res == 'exit':
                    self.save_result(output_path)
                    print(f'Reviewed {call_cnt} Questions')
                    return
                if res == True:
                    self.wfd_table['reviewed'][i] = 1
                else:
                    self.wfd_table['wrong_date'][i].append(datetime.now().strftime("%Y-%m-%d"))
                    self.wfd_table['wrong'][i] += 1
                    self.wfd_table['wrong_record'][i].append(stud_input)
        else:
            prob_range_start = prob_range[0] - 1
            prob_range_end = prob_range[1]
            for i in range(prob_range_start, prob_range_end):
                print(f'WFD Question Number {i + 1}')
                check_res, call_cnt = self.checker(self.wfd_table['English Content'][i])
                res, stud_input = check_res
                if res == 'exit':
                    self.save_result(output_path)
                    print(f'Reviewed {call_cnt} Questions')
                    return
                if res == True:
                    self.wfd_table['reviewed'][i] = 1
                else:
                    self.wfd_table['wrong_date'][i].append(datetime.now().strftime("%Y-%m-%d"))
                    self.wfd_table['wrong'][i] += 1
                    self.wfd_table['wrong_record'][i].append(stud_input)
        self.save_result(output_path)
        print(f'Reviewed {call_cnt} Questions')
        
    @count_calls
    def checker(self, target):
        stud_input = input('Enter Sentence You heard: ')
        if stud_input == 'exit':
            return 'exit', stud_input
        stud_input_dict = self.sentence_to_dict(stud_input)
        target_dict = self.sentence_to_dict(target)
        res = all(k in stud_input_dict and stud_input_dict[k] >= v for k, v in target_dict.items())
        if res == False:
            print('Wrong Answer, answer is: ', target)
        return res, stud_input
                

    def remove_punctuations(self, text):
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text
    
    def sentence_to_dict(self, text):
        text = self.remove_punctuations(text)
        text = text.lower()
        word_counts = {}
        for word in text.split():
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
        return word_counts
    
    def save_result(self, output_path):
        self.wfd_table.to_csv(os.path.join(self.output_folder, output_path), index = False, encoding = 'gbk')
        print('Result Saved to ', os.path.join(self.output_folder, output_path))


if __name__ == '__main__':
    reviewer = wfd_reviewer()
    reviewer.first_time_init('wfd_table.csv')
    reviewer.review('wfd_table_20240810.csv', prob_range = [1, 5])