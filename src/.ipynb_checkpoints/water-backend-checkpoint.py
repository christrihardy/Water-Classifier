# import library
from fastapi import FastAPI
from fastapi import Request
import pickle
import uvicorn
import src.util as utils

config = utils.load_config()

# init app
app = FastAPI()

# check status [GET]
@app.get("/")
def hello():
    return "Hi there, Your API is UP!"


# load model function 
def load_model():
    # load model
    # with open('models/production_model.pkl', 'rb') as file:
    #     model = pickle.load(file)
    model = utils.pickle_load(config["production_model_path"])
    return model


# check model with api [GET]
@app.get("/check-model")
def check_model():
    # load model
    try:
        model = load_model()
        response = {
            "code": 200,
            "messages": "Model is ready!"
        }
    except Exception as e:
        response = {
            "code": 404,
            "messages": "Model is not ready! please check your path or model",
            "error": str(e)
        }
    return response


# predict with api [POST]
@app.post("/predict")
async def predict(request: Request):
    # get data from request
    # sepal_length, sepal_width, petal_length, petal_width
    data = await request.json()


    ph = data['ph']
    hardness = data['Hardness']
    solids = data['Solids']
    chloramines = data['Chloramines']
    sulfate = data['Sulfate']
    conductivity = data['Conductivity']
    organic_carbon = data['Organic_carbon']
    trihalomethanes = data['Trihalomethanes']
    turbidity = data['Turbidity']
    
    
    # load model & label
    model = load_model()
    label = ['0', '1']


    # validation
#    """  if ph < 0 or hardness < 0 or solids < 0 or chloramines < 0 or sulfate < 0 or conductivity < 0 or organic_carbon < 0 or trihalomethanes < 0 or turbidity < 0:
#         response = {
#             "code": 404,
#             "messages": "Failed your input must greater than 0!"
#         }
#         return response """

    
    # predict
    

    try:
        prediction = model.predict([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])
        # print(prediction)
        response = {
            "code": 200,
            "messages": "Success",
            "prediction": label[prediction[0]]
        }
    except Exception as e:
        response = {
            "code": 404,
            "messages": "Failed",
            "error": str(e)
        }

    # return response
    return response

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)