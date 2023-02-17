import json
import utils

with open('answers.json', 'r') as f:
  answers = json.loads(f.read())

correct = 0
for question, answers_info in answers.items():
  pred_list = []
  for pred in answers_info['model_answer']:
    pred = pred[2449 + 8 + len(question)+1:]
    ans = utils.get_ans(pred)
    if ans:
      pred_list.append(ans)
  if not pred_list:
    continue
  maj_ans = utils.get_maj(pred_list)
  target = answers_info['correct_answer']
  target = target[target.rfind('#### ')+5:]
  if utils._is_float(target) and utils._is_float(maj_ans):
    if abs(float(target) - float(maj_ans)) <= 1e-5:
      correct += 1
  elif str(target) == str(maj_ans):
    correct += 1

total = len(answers)
print(correct, total, correct/total)