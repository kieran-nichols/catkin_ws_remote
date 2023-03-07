import subprocess
import os
import pandas as pd

# Execute the command and retrieve the output
subprocess.run('rostopic echo -b test_neutral_fast0.bag -p /europa_topic > europa_topic.csv', capture_output=True, text=True, shell=True)
subprocess.run('rostopic echo -b test_neutral_fast0.bag -p /sensing_topic > sensing_topic.csv', capture_output=True, text=True, shell=True)


df5 = pd.read_csv('europa_topic.csv')
df6 = pd.read_csv('sensing_topic.csv')

merged_df = pd.concat([df5, df6], axis=1)
merged_df.to_csv('result.csv', index=False)
#os.remove('test2.csv')
