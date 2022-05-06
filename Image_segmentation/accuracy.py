from tensorflow.keras.preprocessing.image import load_img
import pandas as pd
import data
import cv2
import numpy as np
import os
from tensorflow import keras

def run2(test_preds,allpath,name,args):
  Taccuracy=0
  Tprecision=0
  Trecall=0
  TFS=0
  full_result=[]
  for ii in range(len(test_preds)):

    path = allpath[ii]
    frameindex= list(path.keys())[0]
    imagepath = path[frameindex][0]
    #tep.append(imagepath)
    seq = path[frameindex][1]
    mask = seq.load_one_masks([frameindex])
    # resize image
    dim = (args.imagesize[1],args.imagesize[0])
    gtn = cv2.resize(mask, dim, interpolation = cv2.INTER_NEAREST)
            

    frame=test_preds[ii]

    mask = np.argmax(frame, axis=-1)
    mask = np.expand_dims(mask, axis=-1)
    mask = mask[:,:,0];

    result = np.zeros((args.imagesize[0],args.imagesize[1],3),'uint8')
    TP=0;FP=0;FN=0;TN=0;
    
    fast_res=mask-gtn
    
    tp = np.where(fast_res==0) and np.where(mask==1)
    TP = TP + len(tp[0])
    result[tp]=(0,255,0)
    
    fp = np.where(fast_res!=0) and np.where(mask==1)
    FP = FP + len(fp[0])
    result[fp]=(255,0,0)
    
    fn = np.where(fast_res!=0) and np.where(mask==0)
    FN = FN + len(fn[0])
    result[fn]=(255,255,0)
   
    tn = np.where(fast_res==0) and np.where(mask==0)
    TN = TN + len(tn[0])
    
    """
    for i in range(mask.shape[0]):
      for j in range(mask.shape[1]):
        if mask[i][j] == gtn[i][j] and mask[i][j]==1:
          result[i][j][0]=0;result[i][j][1]=255;result[i][j][2]=0;
          TP+=1;
        elif mask[i][j] != gtn[i][j] and mask[i][j]==1:
          result[i][j][0]=255;result[i][j][1]=0;result[i][j][2]=0;
          FP+=1;
        elif mask[i][j] != gtn[i][j] and mask[i][j]==0:
          result[i][j][0]=255;result[i][j][1]=255;result[i][j][2]=0;
          FN+=1;
        else:
          TN+=1;
    """
    accuracy = (TP + TN) / (TP + TN + FN + FP)
    try:
      precision = TP / (TP + FP)
    except:
      precision = 0
    try:
      recall = TP / (TP + FN)
    except:
      recall = 0

    try:
      FS = (2*recall*precision)/(precision+recall)
    except:
      FS=0

    Taccuracy+=accuracy
    Tprecision+=precision
    Trecall+=recall
    TFS+=FS

    res = keras.preprocessing.image.array_to_img(result)
    filename = imagepath.split('/'); filename=filename[-2]+'_'+filename[-1]
    full_result.append((filename,accuracy,precision,recall,FS))
    try:
      os.mkdir('result')
    except:
      pass
    res.save('result/'+filename)
  lendata=len(test_preds)
  print("accuracy",Taccuracy/lendata)
  print("precision",Tprecision/lendata)
  print("recall",Trecall/lendata)
  print("FS",TFS/lendata)
  TT = [] ; TT.append(('Total',Taccuracy/lendata,Tprecision/lendata,Trecall/lendata,TFS/lendata))
  full_result = TT + full_result
  df = pd.DataFrame(full_result,columns =['Names','accuracy','precision','recall','FS'])
  df.to_csv('result_'+name+'.csv')

  
def run(test_preds,allpath,name,args):
  Taccuracy=0
  Tprecision=0
  Trecall=0
  TFS=0
  full_result=[]
  for ii in range(len(test_preds)):

    path = allpath[ii]
    frameindex= list(path.keys())[0]
    imagepath = path[frameindex][0]
    #tep.append(imagepath)
    seq = path[frameindex][1]
    mask = seq.load_one_masks([frameindex])
    # resize image
    dim = (args.imagesize[1],args.imagesize[0])
    gtn = cv2.resize(mask, dim, interpolation = cv2.INTER_NEAREST)
            
    """
    gtn = load_img(test_target_img_paths[ii],target_size=img_size, color_mode="grayscale")
    gtn = np.array(gt)
    ys = gtn.copy()
    ys[np.where(gtn==2)]=0
    ys[np.where(gtn!=2)]=1
    gtn = ys.copy()

    frame=test_preds[ii]
    bg = frame[:,:,0]
    fg = frame[:,:,1]
    fg[fg<0.6]=0;
    #new_frame=np.concatenate((bg.reshape(320,320,1),fg.reshape(320,320,1)),axis=2)
    """
    frame=test_preds[ii]

    mask = np.argmax(frame, axis=-1)
    mask = np.expand_dims(mask, axis=-1)
    mask = mask[:,:,0];

    result = np.zeros((args.imagesize[0],args.imagesize[1],3),'uint8')
    TP=0;FP=0;FN=0;TN=0;
    for i in range(mask.shape[0]):
      for j in range(mask.shape[1]):
        if mask[i][j] == gtn[i][j] and mask[i][j]==1:
          result[i][j][0]=0;result[i][j][1]=255;result[i][j][2]=0;
          TP+=1;
        elif mask[i][j] != gtn[i][j] and mask[i][j]==1:
          result[i][j][0]=255;result[i][j][1]=0;result[i][j][2]=0;
          FP+=1;
        elif mask[i][j] != gtn[i][j] and mask[i][j]==0:
          result[i][j][0]=255;result[i][j][1]=255;result[i][j][2]=0;
          FN+=1;
        else:
          TN+=1;

    accuracy = (TP + TN) / (TP + TN + FN + FP)
    try:
      precision = TP / (TP + FP)
    except:
      precision = 0
    try:
      recall = TP / (TP + FN)
    except:
      recall = 0

    try:
      FS = (2*recall*precision)/(precision+recall)
    except:
      FS=0

    Taccuracy+=accuracy
    Tprecision+=precision
    Trecall+=recall
    TFS+=FS

    res = keras.preprocessing.image.array_to_img(result)
    filename = imagepath.split('/'); filename=filename[-2]+'_'+filename[-1]
    full_result.append((filename,accuracy,precision,recall,FS))
    try:
      os.mkdir('result')
    except:
      pass
    res.save('result/'+filename)
  lendata=len(test_preds)
  print("accuracy",Taccuracy/lendata)
  print("precision",Tprecision/lendata)
  print("recall",Trecall/lendata)
  print("FS",TFS/lendata)
  TT = [] ; TT.append(('Total',Taccuracy/lendata,Tprecision/lendata,Trecall/lendata,TFS/lendata))
  full_result = TT + full_result
  df = pd.DataFrame(full_result,columns =['Names','accuracy','precision','recall','FS'])
  df.to_csv('result_'+name+'.csv')
