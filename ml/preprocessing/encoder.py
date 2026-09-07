import joblib
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd

class CategoricalEncoder:
    """Categorical encoder wrapper for ML pipelines."""
    def __init__(self, method='label'):
        self.method = method
        self.encoder = LabelEncoder() if method == 'label' else OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    def fit_transform(self, y_or_df):
        return self.encoder.fit_transform(y_or_df)

    def transform(self, y_or_df):
        return self.encoder.transform(y_or_df)

    def inverse_transform(self, y):
        return self.encoder.inverse_transform(y)

    def save(self, filepath):
        joblib.dump(self.encoder, filepath)

    def load(self, filepath):
        self.encoder = joblib.load(filepath)
        return self
