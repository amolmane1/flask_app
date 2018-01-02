from sklearn.pipeline import Pipeline
import logging

logger = logging.getLogger(__name__)


def predict(x, model):
    prediction_dict = {}
    try:
        prediction = model.predict(x)
        prediction_dict['value'] = '{:f}'.format(prediction[0])
        if isinstance(model, Pipeline):
            if "predict_proba" in dir(model.steps[-1][-1]):
                prediction_dict['probability'] = dict(zip(model.classes_, model.predict_proba(x)))
    except:
        logging.error("Couldn't predict using model")
        return None
    return prediction_dict
