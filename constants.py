from os.path import join

PATH = 'grade-school-math/grade_school_math/data/test.jsonl'
EXPERIMENT_RESULTS_FOLDER = 'data'
SELF_CONSISTENCY = 'self_consistency'
GREEDY = 'greedy'
TASK_PREFIX = '_math.json'
EXPERIMENT = SELF_CONSISTENCY
EXPERIMENT_PATH = join(EXPERIMENT_RESULTS_FOLDER, EXPERIMENT + TASK_PREFIX)
OFFSET = 2458
TARGET = '#### '