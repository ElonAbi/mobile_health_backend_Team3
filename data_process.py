import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.signal import medfilt

def preprocess(data):
    df = pd.read_csv(data, sep= ";")

    #--------------------------------------DATA SCALING ----------------------------------------
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df)

    # Replace original data with scaled values
    data_scaled = pd.DataFrame(scaled_features, columns=df.columns)
    data_scaled['label'] = 'drinking'  # Add labels back

    #--------------------------------------DATA SMOOTHENING------------------------

    values = ['ax','ay','az','gx','gy','gz']

    for value in values:
        data_scaled[value] = data_scaled[value].rolling(window=5).mean()
        print(data_scaled.head()) #find out why printing it does not show values but plotting gives no problems


    #--------------------add accel- and gyro- magnitude????-----------------


    # Save the preprocessed dataset
    data_scaled.to_csv("preprocessed_sensor_data.csv", index=False)