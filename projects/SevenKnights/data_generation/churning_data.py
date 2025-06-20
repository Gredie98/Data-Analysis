import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json

np.random.seed(42)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 단계별 유저 수 생성 (6-10부터 9-30까지)
stages = ['6-10', '6-20', '6-30', '7-10', '7-20', '7-30', '8-10', '8-20', '8-30', '9-10', '9-20', '9-30']
initial_users = 900000

# 각 단계별 유저 수 계산
users = [initial_users]
for i in range(1, len(stages)):
    # 특정 단계에서 높은 이탈률 적용
    if stages[i] == '6-20':  # 6-10에서 6-20으로 넘어갈 때
        churn_rate = np.random.uniform(0.25, 0.30)
    elif stages[i] == '7-20':  # 7-10에서 7-20으로 넘어갈 때
        churn_rate = np.random.uniform(0.25, 0.30)
    elif stages[i] == '8-20':  # 8-10에서 8-20으로 넘어갈 때
        churn_rate = 0.07  # 7% 고정
    elif stages[i] == '8-30':  # 8-20에서 8-30으로 넘어갈 때
        churn_rate = 0.18  # 18% 고정
    else:  # 일반적인 이탈률 적용
        churn_rate = np.random.uniform(0.03, 0.07)
    
    remaining_users = int(users[-1] * (1 - churn_rate))
    users.append(remaining_users)

# 데이터프레임 생성
df = pd.DataFrame({
    'stage': stages,
    'users': users,
    'churn_rate': [0] + [(users[i-1] - users[i])/users[i-1] for i in range(1, len(users))]
})

print("데이터프레임:")
print(df)

# 퍼널 시각화
plt.figure(figsize=(12, 6))
plt.bar(df['stage'], df['users'], color='skyblue')
plt.title('게임 단계별 유저 수 퍼널')
plt.xlabel('게임 단계')
plt.ylabel('유저 수')
plt.xticks(rotation=45)

# 유저 수 표시
for i, v in enumerate(df['users']):
    plt.text(i, v, f'{v:,}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('funnel_visualization.png')
plt.close()

# 이탈률 시각화
plt.figure(figsize=(12, 6))
plt.plot(df['stage'][1:], df['churn_rate'][1:], marker='o', color='red')
plt.title('게임 단계별 이탈률')
plt.xlabel('게임 단계')
plt.ylabel('이탈률')
plt.xticks(rotation=45)

# 이탈률 표시
for i, v in enumerate(df['churn_rate'][1:]):
    plt.text(i+1, v, f'{v:.1%}', ha='center', va='bottom')

plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('churn_rate_visualization.png')
plt.close()

# 단계별 이탈/통과 유저 수 저장
churn_info = {}
for i in range(1, len(stages)):
    churned = users[i-1] - users[i]
    passed = users[i]
    churn_info[stages[i]] = {'churned': int(churned), 'passed': int(passed)}

with open('churn_user_counts.json', 'w', encoding='utf-8') as f:
    json.dump(churn_info, f, ensure_ascii=False, indent=2) 