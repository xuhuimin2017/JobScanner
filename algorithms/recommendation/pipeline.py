import re
import json
import time
from pprint import pprint

import numpy as np
import pandas as pd
import gensim
import pdfminer.high_level
from gensim.models.doc2vec import Doc2Vec, LabeledSentence

print('Data preparing...')
time_start = time.time()
# Load Google's pre-trained Word2Vec model.
model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)


def skill(x):
    a = ' '.join(x)
    a = a.split(' ')
    b = []
    for i in a:
        if i in model.wv.vocab:
            b.append(model[i])
    if not b:
        return [0] * 300
    else:
        return list(np.mean(b, axis=0))


with open("./hubstaff_profiles.json") as fp:  # speciality,skills,pay_rate
    profile = json.load(fp)

skill_dict = [j.lower() for i in profile for j in i['skills']]

with open("./hubstaff_job_descriptions.json") as fp:  # complete
    job_des = json.load(fp)

skill_dict1 = [j.lower() for i in job_des for j in i['skills']]

diction_all = list(set(skill_dict + skill_dict1))  # 得到一个技能字典

skill_emb = dict(zip([i for i in diction_all], [skill(i) for i in diction_all]))

# Job

skills = [i['skills'] for i in job_des]
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


def get_job_recommendations(cv_text: str, top=5):
    if not cv_text:
        raise ValueError('cv text not valid')

    text = cv_text.lower().split()
    print('text len =', len(text))
    my_skill = skill(list(set([i for i in text if i in skill_emb.keys()])))
    extract_skills = set([i for i in text if i in skill_emb.keys()])  # 从简历里面提取出在技能字典的词
    print('extract skills:', extract_skills)

    a = np.array(norm_skill_dimen).dot(np.array(normalize(my_skill)))  # 计算简历和所有技能的相似性

    jobs = [job_des[i] for i, j in sorted(enumerate(a), key=lambda x: x[1], reverse=True)[:top]]
    return jobs


if __name__ == '__main__':
    # Some quick and dirty texts
    cv = cv_from_text('./CV1.txt')
    job_recommendations = get_job_recommendations(cv)
    with open('Recom.json', 'w') as f:
        json.dump(job_recommendations, f)
    pprint(job_recommendations)

    cv = cv_from_pdf('./CV.pdf')
    job_recommendations = get_job_recommendations(cv)
    with open('Recom_pdf.json', 'w') as f:
        json.dump(job_recommendations, f)
    pprint(job_recommendations)
