import pyttsx3
import json
import os
from collections import defaultdict
from datetime import datetime

class LearnEnglish:
    def __init__(self, input_folder, output_folder):
        self.folder = './ape_json/'
        self.output_folder = './wrong_record/'
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

        print('Total words:', cnt)

    def review_words(self, review_key = 'all'):
        if review_key == 'all':
            for k in self.word_dicts:
                for word in self.word_dicts[k]:
                    self.engine.say(word)
                    self.engine.runAndWait()
                    input_word = input('Input word you heard:')
                    if input_word == 'exit':
                        break
                    if input_word == word:
                        print('Correct')
                    else:
                        print('Wrong')
                        self.wrong_dict[k].add(word)
                    
        else:
            for word in self.word_dicts[review_key]:
                engine = pyttsx3.init()
                engine.say(word)
                input_word = input('Input word you heard:')
                if input_word == 'exit':
                    break
                if input_word == word:
                    print('Correct')
                else:
                    print('Wrong')
                    self.wrong_dict[review_key].add(word)
                engine.runAndWait()

    def save_wrong_words(self):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d")
        filename = formatted_time + '_wrong.json'
        suffix = 0
        while os.path.exists(os.path.join(self.output_folder, filename)):
            suffix += 1
            filename = formatted_time + '_wrong' + str(suffix) + '.json'
        with open(os.path.join(self.output_folder, filename), 'w') as f:
            json.dump(self.wrong_dict, f)
        
    def load_wrong_words(self):
        filename = input('Input the filename:')
        with open(os.path.join(self.output_folder, filename), 'r') as f:
            self.wrong_dict = json.load(f)

if __name__ == '__main__':
    learn = LearnEnglish('./ape_json/', './wrong_record/')
    learn.import_words()
    learn.review_words()
    learn.save_wrong_words()
