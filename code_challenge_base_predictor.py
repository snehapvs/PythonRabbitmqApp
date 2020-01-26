import numpy as np
import sklearn
import pickle
from sklearn.linear_model import LogisticRegression

class Predictor():
    modelfile ='code_challenge_model.p'
    def __init__(self,datafile):
        # something here
        print("hii")
       
        c=self.predict(datafile)
        print(c)
    
    def create_data(self,datafile):
        # this is not the most straightforward way to feed the data
		# to the model, please adjust as you see fit
        
        data1 = np.loadtxt(datafile, delimiter=',', skiprows=1)
        data1.reshape(-1,1)
        data1=data1[:,1:4]
        return data1
    
    def predict(self,datafile):
        # this is just a suggestion, feel free to change
        infile = open(self.modelfile,'rb')
        model = pickle.load(infile, encoding='bytes')
        print(model)

        #print(data1)
        return model.predict_proba(self.create_data(datafile))[0,1]
    #[0,1]

    
if __name__ == "__main__": 
    p=Predictor('code_challenge_data2.csv')


