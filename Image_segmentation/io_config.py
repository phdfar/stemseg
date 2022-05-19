import data
from tensorflow.keras.preprocessing.image import load_img
import numpy as np
import cv2

def run(args,myself,path):
  frameindex= list(path.keys())[0]
  imagepath = path[frameindex][0]
  seq = path[frameindex][1]
  flagmulti = path[frameindex][2]  
  
  img = load_img(myself.basepath+'train/'+imagepath, target_size=myself.img_size)
  """
  if self.colorspace=='rgb':
    img = load_img(self.basepath+'train/'+imagepath, target_size=self.img_size)
  if self.colorspace=='lab':
    img = load_img(self.basepath+'train/'+imagepath, target_size=self.img_size)
    img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2LAB)
  if self.colorspace=='hsv':
    img = load_img(self.basepath+'train/'+imagepath, target_size=self.img_size)
    img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2HSV)
  """
  if myself.channel_input==3:
    x = np.asarray(img)

  elif myself.channel_input==4:
    opt = load_img(self.basepath+'train_rgo/train/'+imagepath, target_size=myself.img_size)
    opt = np.asarray(opt);opt = opt[:,:,2];opt = np.expand_dims(opt, 2)
    x = np.concatenate((np.asarray(img),opt),axis=-1)


  if flagmulti==0:
    if myself.task == 'semantic_seg':  
      mask = seq.load_one_masks_semantic([frameindex],myself.dicid)
    else:
      mask = seq.load_one_masks([frameindex],myself.dicid)
  else:
    if myself.task == 'semantic_seg':  
      mask = seq.load_multi_masks_semantic([frameindex],myself.dicid)
    else:
      mask = seq.load_multi_masks([frameindex]);
  # resize image
  dim = (myself.img_size[1],myself.img_size[0])
  temp = cv2.resize(mask, dim, interpolation = cv2.INTER_NEAREST)
  y= np.expand_dims(temp, 2)
  return x,y
