from joblib import load
import pandas as pd
from sklearn.preprocessing import StandardScaler

def test_anomaly(time_diff, amount, amount_diff, zscore):
    data = pd.DataFrame([{
        'time_diff': time_diff,
        'amount': amount, 
        'amount_diff': amount_diff,
        'zscore': zscore
    }])
    
    scaler = StandardScaler()
    scaled = scaler.fit_transform(data)
    
    # Load model
    path = 'model/basic.joblib'
    model = load(path)
    
    res = model.predict(scaled)
    
    return res[0]