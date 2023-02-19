import json
from constants import EXPERIMENT_PATH, OFFSET

def print_answers(experiment: str):
    experiment_path = EXPERIMENT_PATH(experiment)

    with open(experiment_path, 'r') as f:
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
            print(sample[OFFSET + len(question):])
        print('-'*10)
        print('-'*10)