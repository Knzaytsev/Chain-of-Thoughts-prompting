import json

with open('answers.json', 'r') as f:
    answers = json.loads(f.read())

for question, answers_info in answers.items():
    correct_answer = answers_info['correct_answer']
    answer_samples = answers_info['model_answer']
    print('QUESTION')
    print(question)
    print('ANSWER')
    print(correct_answer)
    for sample in answer_samples:
        print('SAMPLE')
        print(sample[2449 + 8 + len(question)+1:])
    print('-'*10)
    print('-'*10)