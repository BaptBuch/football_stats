
import joblib
import pandas as pd


PATH_TO_LOCAL_MODEL = 'model.joblib'

def get_model(path_to_joblib):
    pipeline = joblib.load(path_to_joblib)
    return pipeline

def get_real_pred(dict):
    model = get_model(PATH_TO_LOCAL_MODEL)
    df = pd.DataFrame(dict)
    result = model.predict(df)
    return result
