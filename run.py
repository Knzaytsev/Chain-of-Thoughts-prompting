import argparse
from experiment import run_experiment
from eval_arithmetic import run_eval
from answers_reader import print_answers
from constants import SELF_CONSISTENCY, GREEDY

parser = argparse.ArgumentParser(description='Метод запускает скрипт с проведением эксперимента или оценкой результатов в зависиомсти от переданных аргументов.')
parser.add_argument('-t','--task', help='Название задачи.', required=True)
parser.add_argument('-m','--methods', help='Метод получения ответа.', nargs='+', required=True)

if __name__ == '__main__':
    args = vars(parser.parse_args())

    methods = args['methods']
    if all(method in [SELF_CONSISTENCY, GREEDY] for method in methods):
        task = args['task']
        if task == 'experiment':
            run_experiment(methods[0])
        elif task == 'evaluation':
            run_eval(methods)
        elif task == 'answers':
            print_answers(methods[0])
        else:
            print('[-t, --task] Введено некорректное значение аргумента. Значение должно быть experiment, evaluation, answers.')
    else:
        print(f'[-m, --method] Введено некорректное значение аргумента. Значение должно быть {[SELF_CONSISTENCY, GREEDY]}')