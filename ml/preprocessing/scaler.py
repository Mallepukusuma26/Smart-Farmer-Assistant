import joblib
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class FeatureScaler:
    """Wrapper for feature scaling with persistence."""
    def __init__(self, method='standard'):
        self.method = method
        self.scaler = StandardScaler() if method == 'standard' else MinMaxScaler()

    def fit_transform(self, X):
        return self.scaler.fit_transform(X)

    def transform(self, X):
        return self.scaler.transform(X)

    def save(self, filepath):
        joblib.dump(self.scaler, filepath)

    def load(self, filepath):
        self.scaler = joblib.load(filepath)
        return self
