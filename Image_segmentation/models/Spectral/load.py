from tensorflow.keras import layers
from tensorflow import keras
from keras.models import load_model
import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import load_img
def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def loadeig(myself,imagepath):
    
    sp = imagepath.split('/'); name=sp[-1].replace('.jpg','.pth.npy');eigpath = sp[-2]+'_'+name;
    eig = np.load(myself.baseinput+'data/VOC2012/eigs/laplacian/'+eigpath)
    if myself.config==0:
        dim = (myself.img_size[1],myself.img_size[0])
        e1 = eig[:,:,1];
        eig = cv2.resize(e1, dim, interpolation = cv2.INTER_NEAREST)
        eig = NormalizeData(eig)
        eig = np.expand_dims(eig,2);
        return eig
    elif myself.config==1:
        img = load_img(myself.basepath+'train/'+imagepath, target_size=myself.img_size,grayscale=True)
        #img = NormalizeData(np.asarray(img));
        img = np.expand_dims(img,2);
        dim = (myself.img_size[1],myself.img_size[0])
        e1 = eig[:,:,1];
        eig = cv2.resize(e1, dim, interpolation = cv2.INTER_NEAREST)
        eig = NormalizeData(eig)
        eig = np.expand_dims(eig,2);
        return np.concatenate((img,eig),axis=-1)
    elif myself.config==2:
        img = np.asarray(load_img(myself.basepath+'train/'+imagepath, target_size=myself.img_size,grayscale=False))
        #img = NormalizeData(np.asarray(img));
        #img = np.expand_dims(img,2);
        dim = (myself.img_size[1],myself.img_size[0])
        e1 = eig[:,:,1];
        eig = cv2.resize(e1, dim, interpolation = cv2.INTER_NEAREST)
        eig = NormalizeData(eig)
        eig = np.expand_dims(eig,2);
        return np.concatenate((img,eig),axis=-1)   


