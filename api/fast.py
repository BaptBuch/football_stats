from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from predict import get_real_pred

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# define a root `/` endpoint
@app.get("/")
def index():
    return {"ok": True}

@app.get("/predict")
def predict(result_ht='D',Home_D_start=4,
        Home_M_start=3, Home_A_start=3, Away_D_start=4, Away_M_start=3,
        Away_A_start=3, Home_D_ht=4, Home_M_ht=3, Home_A_ht=3, Away_D_ht=4,
        Away_M_ht=3, Away_A_ht=3, Home_D_60=4, Home_M_60=3, Home_A_60=3,
        Away_D_60=4, Away_M_60=3, Away_A_60=3, Home_D_75=4, Home_M_75=3,
        Home_A_75=3, Away_D_75=3, Away_M_75=3, Away_A_75=3, Home_D_final=4,
        Home_M_final=3, Home_A_final=3, Away_D_final=4, Away_M_final=3,
        Away_A_final=3):
    '''
    Call the params "input" with the value you want
    ex: http://localhost:8000/predict?input=2
    '''
    columns = ['result_ht','Home_D_start',
       'Home_M_start', 'Home_A_start', 'Away_D_start', 'Away_M_start',
       'Away_A_start', 'Home_D_ht', 'Home_M_ht', 'Home_A_ht', 'Away_D_ht',
       'Away_M_ht', 'Away_A_ht', 'Home_D_60', 'Home_M_60', 'Home_A_60',
       'Away_D_60', 'Away_M_60', 'Away_A_60', 'Home_D_75', 'Home_M_75',
       'Home_A_75', 'Away_D_75', 'Away_M_75', 'Away_A_75', 'Home_D_final',
       'Home_M_final', 'Home_A_final', 'Away_D_final', 'Away_M_final',
       'Away_A_final']
    y = [result_ht,Home_D_start,
        Home_M_start, Home_A_start, Away_D_start, Away_M_start,
        Away_A_start, Home_D_ht, Home_M_ht, Home_A_ht, Away_D_ht,
        Away_M_ht, Away_A_ht, Home_D_60, Home_M_60, Home_A_60,
        Away_D_60, Away_M_60, Away_A_60, Home_D_75, Home_M_75,
        Home_A_75, Away_D_75, Away_M_75, Away_A_75, Home_D_final,
        Home_M_final, Home_A_final, Away_D_final, Away_M_final,
        Away_A_final]
    result_dictionary = dict(zip(columns, y))
    result = get_real_pred(result_dictionary)
    if input=='no':
        return {'Prediction': 'N/A',
                'Status': 'Incorrect input, please try again or refer to /docs for details on how to use it.'}
    return {'Prediction':
            {'Probability the winner is the home team': round((result[0][2]*100),2),
             'Probability the winner is the away team': round((result[0][0]*100),2),
             'Probability the game ends up in a draw': round((result[0][1]*100),2)},
            'Status': 'OK'}
