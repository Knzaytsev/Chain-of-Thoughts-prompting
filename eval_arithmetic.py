import json
import utils
from constants import EXPERIMENT_PATH, OFFSET, TARGET, SELF_CONSISTENCY, GREEDY
from texttable import Texttable

def answers_stats(answers):
  correct = 0
  for question, answers_info in answers.items():
    pred_list = []
    for pred in answers_info['model_answer']:
      pred = pred[OFFSET + len(question):]
      ans = utils.get_ans(pred)
      if ans:
        pred_list.append(ans)
    if not pred_list:
      continue
    maj_ans = utils.get_maj(pred_list)
    target = answers_info['correct_answer']
    target = target[target.rfind(TARGET)+len(TARGET):]
    if utils._is_float(target) and utils._is_float(maj_ans):
      if abs(float(target) - float(maj_ans)) <= 1e-5:
        correct += 1
    elif str(target) == str(maj_ans):
      correct += 1

  total = len(answers)
  return correct, total, round(correct/total, 2)

def run_eval(methods):
  method_answers = []
  for method in methods:
    experiment_path = EXPERIMENT_PATH(method)

    with open(experiment_path, 'r') as f:
      answers = json.loads(f.read())
    
    method_answers.append(answers)

  min_size = min([len(answers) for answers in method_answers])

  table = Texttable()
  rows = [['', 'correct', 'total', 'accuracy']]
  for j, answers in enumerate(method_answers):
    answers = dict(list(answers.items())[:min_size])
    correct, total, acc = answers_stats(answers)
    rows.append([methods[j], correct, total, acc])
  table.add_rows(rows)
  print(table.draw())
