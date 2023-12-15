import pickle
import pandas as pd


class UserBasedCF:
    # declare file path for saved model
    file_path='final_model_svd.pkl'
    # function to execute user-based Collaborative Filtering
    def load_model(self):
        loaded_model=pickle.load(open(self.file_path, 'rb'))

        return loaded_model
    