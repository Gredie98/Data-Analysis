import pandas as pd
import numpy as np
import json

np.random.seed(42)

# 유저 수 및 단계
n_users = 900_000
stage = '6-20'

# churning_data.py에서 저장한 이탈/통과 유저 수 불러오기
with open('churn_user_counts.json', 'r', encoding='utf-8') as f:
    churn_info = json.load(f)

n_churn = churn_info[stage]['churned']
n_pass = churn_info[stage]['passed']

# 유저 아이디 생성
user_ids = np.arange(1, n_users + 1)
np.random.shuffle(user_ids)

# 이탈/통과 구분
pass_fail = np.array([0]*n_churn + [1]*n_pass)
np.random.shuffle(pass_fail)

# 이탈 그룹 비율 (이탈자 기준)
churn_optimal = int(n_churn * np.random.uniform(0.05, 0.15))
churn_suboptimal = int(n_churn * np.random.uniform(0.23, 0.37))
churn_inefficient = n_churn - churn_optimal - churn_suboptimal
churn_group = (['최적의 조합']*churn_optimal +
               ['준최적 조합']*churn_suboptimal +
               ['비효율적 조합']*churn_inefficient)
np.random.shuffle(churn_group)

# 통과 그룹 비율 (통과자 기준)
pass_optimal = int(n_pass * np.random.uniform(0.60, 0.80))
pass_suboptimal = int(n_pass * np.random.uniform(0.18, 0.32))
pass_inefficient = n_pass - pass_optimal - pass_suboptimal
pass_group = (['최적의 조합']*pass_optimal +
              ['준최적 조합']*pass_suboptimal +
              ['비효율적 조합']*pass_inefficient)
np.random.shuffle(pass_group)

# 그룹 통합
group = np.empty(n_users, dtype=object)
group[pass_fail == 0] = churn_group
group[pass_fail == 1] = pass_group

# 데이터프레임 생성
df = pd.DataFrame({
    'stage': [stage]*n_users,
    'passed': pass_fail,
    'user_id': user_ids,
    'group_type': group
})

print(df.head())
print(df['passed'].value_counts(), '\n', df['group_type'].value_counts())

df.to_csv('chi_square_data_6-20.csv', index=False, encoding='utf-8-sig') 