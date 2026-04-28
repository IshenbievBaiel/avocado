from fastapi import FastAPI
import uvicorn
import joblib
from pydantic import BaseModel

model = joblib.load("model-2.pkl")
scaler = joblib.load("scaler-3.pkl")

avacado_app = FastAPI()


class AvocadoSchema(BaseModel):
    firmness: float
    hue: int
    saturation: int
    brightness: int
    color_category: str
    sound_db: int
    weight_g: int
    size_cm3: int


@avacado_app.post("/predict")
async def avacado_predict(avacado: AvocadoSchema):
    data = avacado.dict()
    color = data.pop("color_category")

    color_features = [
        1 if color == 'dark green' else 0,
        1 if color == 'green' else 0,
        1 if color == 'purple' else 0
    ]

    final_features = [
                        data["firmness"],
                        data["hue"],
                        data["saturation"],
                        data["brightness"],
                        data["color_category"],
                        data["sound_db"],
                        data["weight_g"],
                        data["size_cm3"]

                     ] + color_features
    scaled_data = scaler.transform([final_features])
    pred = model.predict(scaled_data)[0]

    pred_labels = {
        1: 'Hard',
        2: 'Pre-conditioned',
        3: 'Breaking',
        4: 'Firm-ripe',
        5: 'Ripe',
    }

    label = pred_labels.get(int(pred), 'Unknown')
    return{'Ansver': label}



if __name__ == "__main__":
    uvicorn.run(avacado_app, host="127.0.0.1", port=8000)


