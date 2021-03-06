from simplecv import dp_train as train
import torch
from simplecv.util.logger import eval_progress, speed
import time
from module import CLSJE
from simplecv.util import metric
from simplecv.util import registry
from torch.utils.data.dataloader import DataLoader
from simplecv import registry
from simplecv.core.config import AttrDict
from scipy.io import loadmat
import data.dataloader
import time 
import matplotlib.pyplot as plt
import os
from sklearn.metrics import confusion_matrix 



confusion_matrix =[[0.9718, 0.0266, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0016,
         0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],
        [0.0161, 0.9622, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0217, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],
        [0.0000e+00, 0.0000e+00, 0.9971, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0029],

        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.9854, 0.0000e+00, 0.0000e+00,
         0.0008, 0.0089, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0049, 0.0000e+00, 0.0000e+00],

        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],
        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],

        [0.0000e+00,0.0016, 0.0000e+00, 0.0079, 0.0000e+00, 0.0000e+00,
         0.9746, 0.0000e+00, 0.0079, 0.0000e+00, 0.008, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],

        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0032, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.9968, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],

        [0.0000e+00, 0.0024, 0.0000e+00, 0.0032, 0.0024, 0.0000e+00,
        0.0073, 0.0000e+00, 0.9847, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],

        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],

        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0033, 0.0000e+00, 0.0000e+00,0.9967, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],

        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00],

        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         1.0000e+00, 0.0000e+00, 0.0000e+00],

        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 1.0000e+00, 0.0000e+00],
         
        [0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
         0.0000e+00, 0.0000e+00, 1.0000e+00]]
# Healthy Grass
# Stressed Grass
# Synthetic Grass
# Tree
# Soil
# Water
# Residential
# Commercial
# Road
# Highway
# Railway
# Parking Lot 1
# Parking Lot 2
# Tennis Court
# Running Track

# C1 = confusion_matrix(mask.view(-1), y_pred.view(-1), self._model.module.config.num_classes)
import seaborn as sns #?????????
# xtick=['water','Hippo grass ','Floodplain grasses1','Floodplain grasses2','Reeds1','Riparian','Fierscar2','Island interior','Acacia woodlands','Acacia shrublands','Acacia grasslands','Short mopane','Mixed mopane','Exposed soils' ]
# ytick=['water','Hippo grass ','Floodplain grasses1','Floodplain grasses2','Reeds1','Riparian','Fierscar2','Island interior','Acacia woodlands','Acacia shrublands','Acacia grasslands','Short mopane','Mixed mopane','Exposed soils' ]
xtick=["Healthy Grass", "Stressed Grass","Synthetic Grass","Tree","Soil","Water","Residential","Commercial","Road","Highway","Railway","Parking Lot 1","Parking Lot 2","Tennis Court","Running Track" ]
ytick=["Healthy Grass", "Stressed Grass","Synthetic Grass","Tree","Soil","Water","Residential","Commercial","Road","Highway","Railway","Parking Lot 1","Parking Lot 2","Tennis Court","Running Track" ]
sns.heatmap(confusion_matrix,fmt='g',cmap='Blues', annot=True,cbar=True,xticklabels=xtick, yticklabels=ytick) #????????????,annot=True ?????? ??????????????? ??????????????? fmt ?????? ???????????????????????????cbar=False, ????????? ?????????
# plt.xlabel('x_label',fontsize=7, color='k') #x???label????????????????????????
# plt.ylabel('y_label',fontsize=7, color='k') #y???label????????????????????????
plt.xticks(fontsize=10,rotation=45) #x??????????????????????????????????????????pd_data?????????
plt.yticks(fontsize=10) #y??????????????????????????????????????????pd_data??????
plt.show()
# plt.matshow(confusion_matrix, cmap=plt.cm.Blues) # ????????????????????????????????????????????????
# for i in range(len(confusion_matrix)):
#     for j in range(len(confusion_matrix)):
#         plt.annotate(confusion_matrix[j, i], xy=(i, j), horizontalalignment='center', verticalalignment='center')
# plt.ylabel('True label')
# plt.xlabel('Predicted label')
# path=r"./001.jpg"
dst1 = os.path.join("confusion_matrix",str(1)+ '.png')
plt.savefig(dst1)
# t=t+1
