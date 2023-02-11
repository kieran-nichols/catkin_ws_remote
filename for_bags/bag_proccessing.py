import subprocess
import os
import pandas as pd

# Execute the command and retrieve the output
subprocess.run('rostopic echo -b test_hang.bag -p /xsens_com > xsens_com.csv', capture_output=True, text=True, shell=True)
subprocess.run('rostopic echo -b test_hang.bag -p /xsens_joint_angle > xsens_joint_angle.csv', capture_output=True, text=True, shell=True)
subprocess.run('rostopic echo -b test_hang.bag -p /angular_moments > angular_moments.csv', capture_output=True, text=True, shell=True)
subprocess.run('rostopic echo -b test_hang.bag -p /linear_moments > linear_moments.csv', capture_output=True, text=True, shell=True)
subprocess.run('rostopic echo -b test_hang.bag -p /europa_topic > europa_topic.csv', capture_output=True, text=True, shell=True)
subprocess.run('rostopic echo -b test_hang.bag -p /sensing_topic > sensing_topic.csv', capture_output=True, text=True, shell=True)

df1 = pd.read_csv('xsens_com.csv')
df2 = pd.read_csv('xsens_joint_angle.csv')
df3 = pd.read_csv('angular_moments.csv')
df4 = pd.read_csv('linear_moments.csv')
df5 = pd.read_csv('europa_topic.csv')
df6 = pd.read_csv('sensing_topic.csv')

merged_df = pd.concat([df1, df2,df3, df4, df5, df6], axis=1)
#merged_df.to_csv('result.csv', index=False)
#os.remove('test2.csv')
