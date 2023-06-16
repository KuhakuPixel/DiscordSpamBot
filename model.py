"""
    code for loading the model 

"""
from enum import Enum
from joblib import dump, load
import pandas as pd

class ClassifierModelType(Enum):
    naiveBayes = "naiveBayes"
    randomForest = "randomForest"
    def __str__(self):
        return self.value

MODEL_PATH_DICT = {
    ClassifierModelType.naiveBayes: "nb_model.joblib",
    ClassifierModelType.randomForest: "random_forest_model.joblib",
}

# ==================== load model ===========
def get_model(modelType: ClassifierModelType):
    model_file_path = MODEL_PATH_DICT[modelType]
    return load(model_file_path)


def model_predict_is_spam(model, vect , msg: str)-> bool:
    # 
    x_to_predict = pd.Series(data=[msg])
    x_to_predict_dtm = vect.transform(x_to_predict)
    predicted = model.predict(x_to_predict_dtm)
    # predicted has to 1
    assert len(predicted) == 1

    # if ham = 0, spam = 1 
    is_spam = predicted[0] == 1
    return is_spam
