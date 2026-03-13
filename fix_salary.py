import pandas as pd, re

df = pd.read_csv('data/job_skills.csv')
print('Before:', df['salary'].unique()[:3])

def convert(s):
    s = str(s).strip()
    nums = re.findall(r'\d+', s)
    if len(nums) == 2:
        lo = round(int(nums[0]) * 1000 * 84 / 100000)
        hi = round(int(nums[1]) * 1000 * 84 / 100000)
        return f'Rs.{lo}L-Rs.{hi}L'
    return s

df['salary'] = df['salary'].apply(convert)
print('After:', df['salary'].unique()[:3])
df.to_csv('data/job_skills.csv', index=False)
print('Done!')
