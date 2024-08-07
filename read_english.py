import pyttsx3
import json
import os
from collections import defaultdict
from datetime import datetime
from translate import Translator

class LearnEnglish:
    def __init__(self, input_folder = './ape_json/', output_folder = './wrong_list/'):
        self.folder = input_folder
        self.output_folder = output_folder

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        self.word_dicts = defaultdict(set)
        self.wrong_dict = defaultdict(set)
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'en')

    def see_available_voice(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print('ID:', voice.id)
            print('Name:', voice.name)
            print('Lang:', voice.languages)

    def set_voices(self, voice_id):
        self.engine.setProperty('voice', voice_id)

    def import_words(self):
        cnt = 0
        for filename in os.listdir(self.folder):
            with open(self.folder + filename, 'r') as f:
                date = filename.split('.')[0]
                data = json.load(f)
                words = data['data']['nwords']
                for item in words:
                    self.word_dicts[date].add(item['word'])
                    cnt += 1

        print('Total words Loaded:', cnt)

    def review_words(self, review_key = 'all'):
        cnt = 0
        if review_key == 'all':
            for k in self.word_dicts:
                for word in self.word_dicts[k]:
                    word_zhcn = Translator(to_lang='zh-cn').translate(word)
                    self.engine.say(word)
                    self.engine.runAndWait()
                    input_word = input('Input word you heard:')
                    if input_word == 'exit':
                        return
                    if input_word == 'end':
                        self.save_wrong_words()
                        return
                    while input_word == 'repeat':
                        self.engine.say(word)
                        self.engine.runAndWait()
                        input_word = input('Input word you heard:')
                    if input_word == word:
                        print('Correct, word means:', word_zhcn)
                    else:
                        print('Wrong, answer is:', word, 'means', word_zhcn)
                        self.wrong_dict[k].add((word, word_zhcn))
                    cnt += 1
                    print('Reviewed:', cnt)
                    
        else:
            print('Word in current dict', len(self.word_dicts[review_key]))
            for word in self.word_dicts[review_key]:    
                word_zhcn = Translator(to_lang='zh-cn').translate(word)
                self.engine.say(word)
                self.engine.runAndWait()
                input_word = input('Input word you heard:')
                if input_word == 'exit':
                    return
                if input_word == 'end':
                    self.save_wrong_words()
                    return
                while input_word == 'repeat':
                    self.engine.say(word)
                    self.engine.runAndWait()
                    input_word = input('Input word you heard:')
                if input_word == word:
                    print('Correct, word means:', word_zhcn)
                else:
                    print('Wrong, answer is:', word, 'means', word_zhcn)
                    self.wrong_dict[review_key].add((word,word_zhcn))
                cnt += 1
                print('Reviewed:', cnt)
        is_save = input('Save wrong words? (y/n):')
        if is_save == 'y':
            self.save_wrong_words()
        return

    def save_wrong_words(self):
        current_time = datetime.now()
        formatted_date = current_time.strftime("%Y%m%d")
        hours_minutes = current_time.strftime("%H%M%S")
        filename = hours_minutes + '_wrong.json'
        save_dict = {k:list(list(pair) for pair in v) for k, v in self.wrong_dict.items()}
        suffix = 0
        filename = hours_minutes + '_wrong.json'
        if not os.path.exists(os.path.join(self.output_folder, formatted_date)):
            os.makedirs(os.path.join(self.output_folder, formatted_date))

        with open(os.path.join(self.output_folder, formatted_date, filename), 'w', encoding = 'utf8') as f:
            json.dump(save_dict, f, ensure_ascii= False)
        
    def load_wrong_words(self, foldername = None):
        if not filename:
            filename = input('Input the foldername:')
        for filename in os.listdir(os.path.join(self.output_folder, foldername)):
            with open(os.path.join(self.output_folder, filename), 'r', encoding = 'utf8') as f:
                loaded = json.load(f)
                cnt = 0
                for k, words in loaded.items():
                    for word in words:
                        prev = self.word_dicts[k].copy()
                        self.word_dicts[k].add(word[0])
                        if prev != self.word_dicts[k]:
                            cnt += 1
        print('Loaded words:', cnt)
    
    def check_wrong_words_dup(self, filename):
        with open(os.path.join(self.output_folder, filename), 'r', encoding = 'utf8') as f:
            return json.load(f)

if __name__ == '__main__':
    learn = LearnEnglish('./ape_json/', './wrong_record/')
    # learn.see_available_voice()
    learn.set_voices('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    learn.import_words()
    learn.review_words('20240807')
    # learn.load_wrong_words('20240808')
    learn.review_words()