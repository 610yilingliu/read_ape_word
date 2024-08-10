import string
import os

class check_essay:
    def __init__(self, essay_name, folder_path = './essay', ):
        self.essay_path = os.path.join(folder_path, essay_name)
        self.essay = open(self.essay_path, 'r').read()
        self.paragraphs = self.paragraph_processing(self.essay)
        
    def remove_punctuations(self, text):
        # Remove all punctuation marks from the text
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text
    
    def paragraph_processing(self, paragraph):
        paragraphs_raw = paragraph.split('\n')
        paragraphs = []
        for paragraph in paragraphs_raw:
            paragraph = self.remove_punctuations(paragraph)
            paragraph = ' '.join(paragraph.split())
            paragraph = paragraph.strip()
            if len(paragraph)  > 0:
                paragraphs.append(paragraph)
        return paragraphs
    
    def check_input(self, input_file_name, input_file_folder = './essay/record', paragraph_num = 'all'):
        input_file = open(os.path.join(input_file_folder, input_file_name), 'r').read()
        input_paragraphs = self.paragraph_processing(input_file)
        if paragraph_num == 'all':
            curp = 0
            for ip in input_paragraphs:
                if ip == self.paragraphs[curp]:
                    print(f'Paragraph {curp + 1} Correct')
                else:
                    print(f'Paragraph {curp + 1} Incorrect')
                    print('Input:\n ',ip)
                    print('Should be:\n ', self.paragraphs[curp])
                curp += 1
        else:
            for ip in input_paragraphs:
                curp = 0
                if ip in self.paragraphs:
                    print(f'Input Paragraph {curp + 1} Correct')
                else:
                    print(f'Input Paragraph {curp + 1} Cannot be found')
                    print('Input:\n ',ip)

if __name__ == '__main__':
    checker = check_essay('template.txt')
    checker.check_input('20240810.txt', paragraph_num= None)

