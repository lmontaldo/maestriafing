import pandas as pd

class Standardization:
    def __init__(self, dataframe):
        # Convert the 'ymd' column to datetime format and normalize, then set as index
        dataframe['ymd'] = pd.to_datetime(dataframe['ymd']).dt.normalize()
        self.dataframe = dataframe.set_index('ymd')
        self.original_dataframe = self.dataframe.copy()
        self.mean = None
        self.std = None
        
    def log1_transform(self):
        """Applies a log1p transformation to every column in the dataframe."""
        self.dataframe = self.dataframe.applymap(lambda x: pd.np.log1p(x))
        
    def z_score_standardization(self):
        """Performs Z-score standardization over each column."""
        self.mean = self.dataframe.mean()
        self.std = self.dataframe.std()
        self.dataframe = (self.dataframe - self.mean) / self.std
        
    def standardize(self):
        """Applies log1p transformation followed by Z-score standardization."""
        self.log1_transform()
        self.z_score_standardization()
        
    def inverse_transform(self):
        """Inverse the Z-score standardization and log1p transformation to return to the original scale."""
        # Inverse of Z-score standardization
        self.dataframe = (self.dataframe * self.std) + self.mean
        
        # Inverse of log1p transformation
        self.dataframe = self.dataframe.applymap(lambda x: pd.np.expm1(x))
        
    def get_dataframe(self):
        """Returns the standardized dataframe."""
        return self.dataframe
