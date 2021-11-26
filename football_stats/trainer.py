import joblib
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.compose import ColumnTransformer

def get_x_y():
    df_prechange_clean = pd.read_csv("raw_data/df_all_clean.csv")

    X = df_prechange_clean[[
       'result_ht','Home_D_start',
       'Home_M_start', 'Home_A_start', 'Away_D_start', 'Away_M_start',
       'Away_A_start', 'Home_D_ht', 'Home_M_ht', 'Home_A_ht', 'Away_D_ht',
       'Away_M_ht', 'Away_A_ht', 'Home_D_60', 'Home_M_60', 'Home_A_60',
       'Away_D_60', 'Away_M_60', 'Away_A_60', 'Home_D_75', 'Home_M_75',
       'Home_A_75', 'Away_D_75', 'Away_M_75', 'Away_A_75', 'Home_D_final',
       'Home_M_final', 'Home_A_final', 'Away_D_final', 'Away_M_final',
       'Away_A_final']]
    y=df_prechange_clean['result_ft']
    return X, y




def set_pipeline():
    # scale qll num values
    num_transformer = Pipeline([('scaler', MinMaxScaler())])

    # Encode categorical variables
    #model = LogisticRegression(max_iter=1000)

    cat_transformer = OneHotEncoder(sparse=False)

    # Paralellize "num_transformer" and "One hot encoder"
    preprocessor = ColumnTransformer([
        ('num_tr', num_transformer, ['Home_D_start',
        'Home_M_start', 'Home_A_start', 'Away_D_start', 'Away_M_start',
        'Away_A_start', 'Home_D_ht', 'Home_M_ht', 'Home_A_ht', 'Away_D_ht',
        'Away_M_ht', 'Away_A_ht', 'Home_D_60', 'Home_M_60', 'Home_A_60',
        'Away_D_60', 'Away_M_60', 'Away_A_60', 'Home_D_75', 'Home_M_75',
        'Home_A_75', 'Away_D_75', 'Away_M_75', 'Away_A_75', 'Home_D_final',
        'Home_M_final', 'Home_A_final', 'Away_D_final', 'Away_M_final',
        'Away_A_final']),
        ('cat_tr', cat_transformer, ['result_ht'])])
        #, "Result_ht_D", "Result_ht_H", "Result_ht_A"
    pipeline = Pipeline([
                ('preproc', preprocessor),
                ('svc_model', SVC(kernel='rbf', C=10))
            ])
    return pipeline

def run(X_train, y_train):
    pipeline = set_pipeline()
    #mlflow_log_param("model", "Linear")
    return pipeline.fit(X_train, y_train)

#def evaluate(fit_pipe, X_test, y_test):
#    """evaluates the pipeline on df_test and return the RMSE"""
#    y_pred = fit_pipe.predict(X_test)
#    rmse = mean_squared_error(y_pred, y_test)**0.5
#    return round(rmse, 2)


def save_model_locally(fit_pipe):
    """Save the model into a .joblib format"""
    joblib.dump(fit_pipe, 'model.joblib')
    print("model.joblib saved locally", "green")


if __name__ == "__main__":
    X, y = get_x_y()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)
    fitted_pipe = run(X_train, y_train)
    #print(evaluate(fitted_pipe, X_test, y_test))
    save_model_locally(fitted_pipe)
