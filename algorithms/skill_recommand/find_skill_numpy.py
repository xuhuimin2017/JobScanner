from pathlib import Path

import numpy as np
import argparse
import json 
import re

_path_cur = Path(__file__).absolute().resolve().parent
_path_param_mix = _path_cur / 'Parameters_mix.json'
_path_weight = _path_cur / 'Weight.txt'


def get_skill_vec(skills,vecs):
    skill_vecs = []
    for skill in skills:
        for word in re.split('-|/', skill):
            if word in vecs:
                skill_vecs += [vecs[word]]
    return skill_vecs 
def load_word_list(fpath):
    word = []
    with open(fpath,'r')as f:
        for line in f:
            tmp = line.strip().split()
            if tmp:
                word.append(tmp[0].replace(' ','-').replace('(','-').replace(')','-'))
    return word
def load_embeding(fpath='./glove/glove.twitter.27B.25d.txt'):
    vecs = {}
    with open(fpath,'r')as f:
        for line in f:
            tmp =line.strip().split(' ')
            vecs[tmp[0]]=list(map(float,tmp[1:]))
    vecs['c#'] = vecs['c']
    vecs['html5'] = vecs['html']
    vecs['css3'] = vecs['css']
    vecs['win32'] = vecs['windows']
    
    return vecs
def skill_portrait_mix(skills,vecs):
    s_vecs = get_skill_vec(skills,vecs)
    
    if len(s_vecs) == 0:
        res = np.array([0.] * 75)
    else:
        res = list(np.min(s_vecs,0))+list(np.max(s_vecs,0))+list(np.mean(s_vecs,0))
    return res
    

def leakyrelu(x,slope=0.1):
  x = np.array(x)
  x[x<0]=x[x<0]*slope
  return np.matrix(x)

with open(_path_param_mix,'r')as f:
  SD = json.load(f)

def NN(x,SD):
  x = np.matrix(x).T
  fcn1 = np.matrix(SD['fcn1.weight'])
  fcn1_b = np.matrix(SD['fcn1.bias']).T
  fcn2 = np.matrix(SD['fcn2.weight'])
  fcn2_b = np.matrix(SD['fcn2.bias']).T
  fcn3 = np.matrix(SD['fcn3.weight'])
  fcn3_b = np.matrix(SD['fcn3.bias']).T
  x1 = leakyrelu(fcn1*x + fcn1_b)
  x2 = leakyrelu(fcn2*x1 + fcn2_b)
  x3 = leakyrelu(fcn3*x2 + fcn3_b)
  return x3

def skill_contributes(skills,vecs):
    
    if len(skills)==1:
        tmp={skills[0]:1}
    else:
        skill_vecs = []
        skill_vecs_d = {}
        n=0
        W = np.loadtxt(str(_path_weight))
        for skill in skills:
            for word in re.split('-|/', skill):
                if word in vecs:
                    skill_vecs += [vecs[word]]
                    skill_vecs_d[n] = skill
                    n+=1
        tmp = {}
        for d in skill_vecs_d:
            if skill_vecs_d[d] not in tmp:
                tmp[skill_vecs_d[d]]=[]
            tmp[skill_vecs_d[d]].append(d)
        if len(tmp)==1:
            tmp = {i:1. for i in tmp}
        else:
            s_vecs = get_skill_vec(skills,vecs)
            if len(s_vecs) == 0:
                res = np.array([0.] * 75)
            else:
                res = list(np.min(s_vecs,0))+list(np.max(s_vecs,0))+list(np.mean(s_vecs,0))
            m1 = np.argmin(s_vecs,0)
            m2 = np.argmax(s_vecs,0)
            A = np.zeros((75,len(skill_vecs_d)))
            for n,i in zip(range(25),m1):
                A[n,i]=1
            for n,i in zip(range(25,50),m2):
                A[n,i]=1
            s = 1./len(skill_vecs_d)
            for n in range(50,75):
                A[n,:]=s
            B = np.array(s_vecs)
            r = np.dot(W,np.multiply(A,np.hstack([B,B,B]).T))
    
            for t in tmp:
                tmp[t]=sum([r[i] for i in tmp[t]])
                if tmp[t]<0:
                    tmp[t]=0
            s = sum(tmp.values())
            tmp = {t:tmp[t]/s for t in tmp}
    return tmp
    

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='learn the high paid skill')
    parser.add_argument('--skill_choosen', type=str, default='./skill_choosen.txt',
                        help='a file that gives the all of the skill')
    parser.add_argument('--current_skill', nargs='+',
                        help=' current skill u own')

    parser.add_argument('--embedding_fpath', default='./glove/glove.twitter.27B.25d.txt')
    parser.add_argument('--topn', default=3, type=int)

    args = parser.parse_args()
    embedding_fpath = args.embedding_fpath
    topn = int(args.topn)
    current_skill = args.current_skill
    skill_choosen = args.skill_choosen
    
    #print(args.is_cuda)



    vecs = load_embeding(fpath=embedding_fpath)

    current_shape = skill_portrait_mix(current_skill,vecs)

    old_wage = NN(np.array(current_shape),SD)


    skill_choosen = load_word_list(skill_choosen)
    skill_choosen = [s for s in skill_choosen if s not in current_skill]
    skills= [current_skill+[s] for s in skill_choosen]
    skill_shapes = [skill_portrait_mix(sk,vecs) for sk in skills]
    skill_shapes = np.array(skill_shapes)

    predict = NN(skill_shapes,SD)
    predict = np.array(predict).reshape(-1)
        
    res = sorted([[i,j] for i,j in zip(skill_choosen,predict)],key = lambda x:x[1],reverse=True)
    tmp1 = skill_contributes(current_skill,vecs)
    print('Current Skills (Contribution Weight): ',tmp1)
    print('Current Predicted Wage: ',old_wage)
    print('='*10)
    for i in range(topn):
        print('Add ',res[i][0])
        tmpi = skill_contributes(current_skill+[res[i][0]],vecs)
        print('Contribution Weight',tmpi)
        print('New wage: ',res[i][1])
        print('='*10)