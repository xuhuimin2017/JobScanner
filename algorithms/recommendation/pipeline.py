import json
import time
from pathlib import Path
from pprint import pprint
from typing import Dict

import numpy as np
import pdfminer.high_level

_path_cur = Path(__file__).absolute().resolve().parent
_path_data = _path_cur / 'data'
_path_embedded = _path_data / 'skill_emb.json'
_path_hoff_desc = _path_data / 'hubstaff_job_descriptions.json'

print('Data preparing...')
time_start = time.time()
with open(_path_embedded) as json_file:
    skill_emb = json.load(json_file)

with open(_path_hoff_desc) as fp:
    job_des = json.load(fp)

skills = [i['skills'] for i in job_des]


def skill(x):
    a = ' '.join(x)
    a = a.split(' ')
    b = []
    for i in a:
        if i in skill_emb:
            b.append(skill_emb[i])
    if b == []:
        return [0] * 300
    else:
        return list(np.mean(b, axis=0))


skill_dimen = [skill([j.lower() for j in i]) for i in skills]  # 计算所有工作的embedding


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


norm_skill_dimen = [normalize(i) for i in skill_dimen]
print(f'... done in {time.time() - time_start:.3} seconds')


def cv_from_pdf(pdf_file):
    return pdfminer.high_level.extract_text(pdf_file)


def cv_from_text(txt_file):
    with open(txt_file) as f:
        text = f.read()
    return text


def get_job_recommendations(cv_text: str, top=5) -> Dict:
    if not cv_text:
        raise ValueError('CV text not valid')

    text = cv_text.lower().split()
    print('Text len =', len(text))
    my_skill = skill(list(set([i for i in text if i in skill_emb.keys()])))
    extract_skills = set([i for i in text if i in skill_emb.keys()])  # 从简历里面提取出在技能字典的词
    print('Extract skills:', extract_skills)

    a = np.array(norm_skill_dimen).dot(np.array(normalize(my_skill)))  # 计算简历和所有技能的相似性

    jobs = [job_des[i] for i, j in sorted(enumerate(a), key=lambda x: x[1], reverse=True)[:top]]
    return jobs


if __name__ == '__main__':
    # Some quick and dirty tests
    cv = cv_from_text('research/CV1.txt')
    job_recommendations = get_job_recommendations(cv)
    with open('research/Recom.json', 'w') as f:
        json.dump(job_recommendations, f)
    pprint(job_recommendations)

    cv = cv_from_pdf('research/CV.pdf')
    job_recommendations = get_job_recommendations(cv)
    with open('research/Recom_pdf.json', 'w') as f:
        json.dump(job_recommendations, f)
    pprint(job_recommendations)
