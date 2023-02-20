import torch
from transformers import BloomTokenizerFast
from petals import DistributedBloomForCausalLM
from tqdm import tqdm
import json
from os.path import exists
from constants import PATH, EXPERIMENT_PATH, SELF_CONSISTENCY, PROMPT


def read_jsonl(path: str):
    with open(path) as fh:
        return [json.loads(line) for line in fh.readlines() if line]


def read_json(path: str):
    with open(path) as fh:
        return json.loads(fh.read())


def run_experiment(experiment: str):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(device)

    model = DistributedBloomForCausalLM.from_pretrained("bigscience/bloom-petals", tuning_mode="ptune",
                                                        pre_seq_len=16, request_timeout=1800).to(device)
    tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-petals")

    print('model is ready')

    data = read_jsonl(PATH)

    outputs = dict()

    experiment_path = EXPERIMENT_PATH(experiment)
    if exists(experiment_path):
        outputs = read_json(experiment_path)

    start_position = len(outputs)

    print('data is read')

    input_prompt = PROMPT

    for row in tqdm(data[start_position:]):
        question, answer = row['question'], row['answer']

        input_text = input_prompt + '\n\nQ: ' + question + '\nA:'
        inputs = tokenizer(input_text, return_tensors="pt", )["input_ids"].to(device)

        answers = []
        if experiment == SELF_CONSISTENCY:
            for _ in tqdm(range(5)):
                output = model.generate(inputs, max_new_tokens=128, temperature=0.9,
                                        top_k=32, do_sample=True)
                answers.append(tokenizer.decode(output[0]))
        else:
            output = model.generate(
                inputs, max_new_tokens=128, do_sample=False)
            answers.append(tokenizer.decode(output[0]))

        outputs[question] = {'correct_answer': answer, 'model_answer': answers}

        with open(experiment_path, 'w') as f:
            json.dump(outputs, f)
