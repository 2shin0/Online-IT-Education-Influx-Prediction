# 데이터프레임을 다루기 위한 라이브러리를 불러옵니다.
import numpy as np
import pandas as pd
import re

# 시각화를 위한 라이브러리를 불러옵니다.
import seaborn as sns
import math
import matplotlib.pyplot as plt

# 정규성, 등분산성과 같은 데이터 분포를 살펴보기 위한 라이브러리를 불러옵니다.
from scipy import stats
from scipy.stats import shapiro
from scipy.stats import anderson
from scipy.stats import bartlett
from scipy.stats import levene
from scipy.stats import pearsonr
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 원하는 csv파일을 불러옵니다.
df = pd.read_csv('데이터 최종본(완).csv')
pd.set_option('display.max_rows', None)

# 새로운 열 이름을 생성하고 열 이름을 변경합니다.
new_columns = ['강좌명','수강생수','가격','평점','수강평수','난이도','강의시간','강의게시일']
df.columns = new_columns


# 각각의 속성을 원하는 시각화를 위해 형태를 바꿔줍니다. -> 시각화를 위한 데이터프레임을 생성합니다.
df['강좌명'] = df['강좌명'].str.replace('\n대시보드', '')
df['강의게시일'] = pd.to_datetime(df['강의게시일'].str.extract(r'(\d+)년 (\d+)월 (\d+)일').agg('-'.join, axis=1))
df['수강평수'] = df['수강평수'].str.extract(r'(\d+)개의').fillna(0).astype(int)
df['수강생수'] = df['수강생수'].str.replace('명', '')
df['수강생수'] = df['수강생수'].str.replace(',', '').astype(int)
df['가격'] = df['가격'].replace('무료', '₩0')
df['가격'] = df['가격'].str.extract(r'₩([^₩]+)$')
df['가격'] = df['가격'].str.replace(',', '').astype(int)
df['시간'] = df['강의시간'].str.extract(r'(\d+)시간', expand=False).fillna(0)
df['분'] = df['강의시간'].str.extract(r'(\d+)분', expand=False).fillna(0)
df['강의시간_분'] = df['시간'].astype(int)*60 + df['분'].astype(int)
df = df.drop(['시간', '분', '강의시간'], axis=1)
df['평점'] = df['평점'].str.extract(r'([\d.]+)').fillna(0).astype(float)
df['무료/유료'] = df['가격'].apply(lambda x: '무료' if x == 0 else '유료')
df['평가지수'] = df['수강평수'] * df['평점']
df = df[df['강의시간_분'] != 0]
df['강의시간당가격'] = df.apply(lambda row: int(row['가격'] / (row['강의시간_분'] / 60)), axis=1)
df = df[df['평가지수'] != 0]
# 중복되는 행을 제거해줍니다.
df = df.drop_duplicates('강좌명', keep='first')
#df.to_csv('데이터 시각화용.csv', index=False)


df_regression = df.copy()
df_regression = pd.concat([df_regression, pd.get_dummies(df_regression['난이도'], prefix='난이도')], axis=1)
df_regression['유무료'] = df['무료/유료'].apply(lambda x: 1 if x == '유료' else 0) #유료(1)/무료(0)
df_regression= df_regression.drop(['난이도', '무료/유료'], axis=1)

df_regression['로그_수강생수'] = np.log1p(df_regression['수강생수'])
df_regression['로그_가격'] = np.log1p(df_regression['가격'])
df_regression['로그_강의시간'] = np.log1p(df_regression['강의시간_분'])
df_regression


df1 = df_regression.copy()
# outliers remeove
def remove_outliers_iqr(df1, column):
    Q1 = df1[column].quantile(0.25)
    Q3 = df1[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df1[(df1[column] >= lower_bound) & (df1[column] <= upper_bound)].reset_index(drop=True)

columns_to_remove_outliers = ['수강생수', '가격', '강의시간_분']
for column in columns_to_remove_outliers:
    df1 = remove_outliers_iqr(df1, column)

df1['로그_수강생수'] = np.log1p(df1['수강생수'])
#plt.hist(df1['로그_수강생수'] , color ='lightgrey')
# plt.title('로그_수강생수 분포')
# plt.show()
df1['로그_가격'] = np.log1p(df1['가격'])
# 3. 로그 변환 조절
#df1['로그_변환2'] = np.log(df1['가격'] + 1)
#df1['로그_가격2'] = np.log1p(df1['로그_가격'])
#plt.hist(df1['로그_가격2'] , color ='lightgrey')
# plt.title('로그_가격 분포')
# plt.show()
df1['로그_강의시간'] = np.log1p(df1['강의시간_분'])
#plt.hist(df1['로그_강의시간'] , color ='lightgrey')
# plt.title('로그_강의시간 분포')
# plt.show()
df1
