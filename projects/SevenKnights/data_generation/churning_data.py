import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 단계별 유저 수 생성
stages = ['7-10', '7-20', '7-30', '8-10', '8-20', '8-30', '9-10', '9-20', '9-30', '10-10', '10-20', '10-30']
initial_users = 900000

# 각 단계별 유저 수 계산
users = [initial_users]
for i in range(1, len(stages)):
    if stages[i] in ['7-30', '8-30']:  # 특정 단계에서 큰 이탈률 적용
        churn_rate = np.random.uniform(0.20, 0.30)
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