from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
def predict(input='no'):
    '''
    Call the params "input" with the value you want
    ex: http://localhost:8000/predict?input=2
    '''
    if input=='no':
        return {'Prediction': 'N/A',
                'Status': 'Incorrect input, please try again or refer to /docs for details on how to use it.'}
    return {'Prediction': input*2,
                'Status': 'OK'}
