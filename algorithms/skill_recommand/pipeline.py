from pathlib import Path
from pprint import pprint
from typing import List

import numpy as np

from algorithms.skill_recommand import find_skill_numpy as alg

_path_cur = Path(__file__).absolute().resolve().parent
_path_embedding = _path_cur / 'glove' / 'glove.hub_skill.txt'
_path_skill_chosen = _path_cur / 'Hub_skill.txt'


def find_skills(current_skill: List[str], top_n: int):
    vecs = alg.load_embeding(fpath=str(_path_embedding))

    current_shape = alg.skill_portrait_mix(current_skill, vecs)

    old_wage = alg.NN(np.array(current_shape), alg.SD)

    skill_chosen = alg.load_word_list(str(_path_skill_chosen))
    skill_chosen = [s for s in skill_chosen if s not in current_skill]
    skills = [current_skill + [s] for s in skill_chosen]
    skill_shapes = [alg.skill_portrait_mix(sk, vecs) for sk in skills]
    skill_shapes = np.array(skill_shapes)

    predict = alg.NN(skill_shapes, alg.SD)
    predict = np.array(predict).reshape(-1)

    d = dict(zip(skill_chosen, predict))

    res = sorted(d.items(), key=lambda x: x[1], reverse=True)
    wage_contrib = alg.skill_contributes(current_skill, vecs)
    print('Current Skills (Contribution Weight): ', wage_contrib)
    old_wage = np.exp(float(old_wage)) * 40 * 50
    print('Current Predicted Wage: ', old_wage)
    print('Top n skill', res[:top_n])
    print('=' * 10)
    # for i in range(top_n):
    #     new_skill_name = res[i][0]
    #     new_wage = res[i][1]
    #     print('Add ', new_skill_name)
    #     tmpi = alg.skill_contributes(current_skill + [new_skill_name], vecs)
    #     print('Contribution Weight', tmpi)
    #     print('New wage: ', new_wage)
    #     print('=' * 10)
    return old_wage, wage_contrib, res[:top_n]


if __name__ == '__main__':
    ret = find_skills(['adobe-photoshop', 'adobe-dreamweaver', 'log-design', 'css3', 'html5'], 5)
    pprint(ret, indent=2, width=80, compact=False)
