import json
import time
from pathlib import Path
from pprint import pprint
from typing import Dict, List

import numpy as np
import pdfminer.high_level

_path_cur = Path(__file__).absolute().resolve().parent
_path_data = _path_cur / 'data'
_path_embedded = _path_data / 'skill_emb.json'
_path_hoff_desc = _path_data / 'hubstaff_job_descriptions.json'


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


class PipelineBase:
    def cv_from_pdf(self, cv_path):
        raise NotImplementedError()

    def cv_from_text(self, cv_path):
        raise NotImplementedError()

    def get_job_recommendations(self, cv_text: str, top=5):
        raise NotImplementedError()


class Pipeline(PipelineBase):

    def __init__(self):
        self._skill_emb = None
        self._norm_skill_dimen = None
        self._job_des = None

    def load(self):
        print('Data preparing...')
        time_start = time.time()
        with open(_path_embedded) as json_file:
            self._skill_emb = json.load(json_file)

        with open(_path_hoff_desc) as fp:
            self._job_des = json.load(fp)

        _skills = [i['skills'] for i in self._job_des]
        # 计算所有工作的embedding
        skill_dimen = [self._skill([j.lower() for j in i]) for i in _skills]

        self._norm_skill_dimen = [normalize(i) for i in skill_dimen]
        print(f'... done in {time.time() - time_start:.3} seconds')
        return self

    def _skill(self, x):
        a = ' '.join(x)
        a = a.split(' ')
        b = []
        for i in a:
            if i in self._skill_emb:
                b.append(self._skill_emb[i])
        if b == []:
            return [0] * 300
        else:
            return list(np.mean(b, axis=0))

    def cv_from_pdf(self, pdf_file) -> str:
        return pdfminer.high_level.extract_text(pdf_file)

    def cv_from_text(self, txt_file) -> str:
        with open(txt_file) as f:
            text = f.read()
        return text

    def get_job_recommendations(self, cv_text: str, top=5) -> List[Dict]:
        """Return jobs from CV string"""
        if not cv_text:
            raise ValueError('CV text not valid')

        text = cv_text.lower().split()
        print('Text len =', len(text))
        my_skill = self._skill(list(set([i for i in text if i in self._skill_emb.keys()])))
        extract_skills = set([i for i in text if i in self._skill_emb.keys()])  # 从简历里面提取出在技能字典的词
        print('Extract skills:', extract_skills)

        a = np.array(self._norm_skill_dimen).dot(np.array(normalize(my_skill)))  # 计算简历和所有技能的相似性

        jobs = [self._job_des[i] for i, j in sorted(enumerate(a), key=lambda x: x[1], reverse=True)[:top]]
        return jobs
    
    def get_new_recommendations(self, skill_list, top=5) -> List[Dict]:

        text = skill_list
        print('Text len =', len(text))
        my_skill = self._skill(list(set([i for i in text if i in self._skill_emb.keys()])))
        extract_skills = set([i for i in text if i in self._skill_emb.keys()])  # 从简历里面提取出在技能字典的词
        print('Extract skills:', extract_skills)

        a = np.array(self._norm_skill_dimen).dot(np.array(normalize(my_skill)))  # 计算简历和所有技能的相似性

        jobs = [self._job_des[i] for i, j in sorted(enumerate(a), key=lambda x: x[1], reverse=True)[:top]]
        return jobs


if __name__ == '__main__':
    # Some quick and dirty tests
    pipe = Pipeline().load()

    cv = pipe.cv_from_text('research/CV1.txt')
    job_recommendations = pipe.get_job_recommendations(cv)
    with open('research/Recom.json', 'w') as f:
        json.dump(job_recommendations, f)
    pprint(job_recommendations)

    cv = pipe.cv_from_pdf('research/CV.pdf')
    job_recommendations = pipe.get_job_recommendations(cv)
    with open('research/Recom_pdf.json', 'w') as f:
        json.dump(job_recommendations, f)
    pprint(job_recommendations)
    
    #skill list is the new skill list which add or delete other skills, but i do not know where to read this file
    new_recommendations = pipe.get_new_recommendations(skill_list)
    with open('research/New_pdf.json', 'w') as f:
        json.dump(new_recommendations, f)
    pprint(new_recommendations)

