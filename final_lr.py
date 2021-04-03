# -*- coding: utf-8 -*-
"""final_LR

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16cW8KcVvY7S8TOPBYUkrkgPGpwuEdeiH
"""

import tensorflow as tf
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import cv2
import os
from PIL import Image
from sklearn.model_selection import train_test_split

! git clone "https://github.com/Mohamed-Salah62/UTFface.git"

#--------------------------------------**********--------------------------

os.chdir('UTFface/UTKFace')
all_data = os.listdir()

x_data =[]
Y_data=[]
for Img in all_data:
    img = cv2.imread(Img,0)            #take img gray scale
    img =cv2.resize(img, (35, 35) )    #resize_imgs to make size   
    x_data.append(img)                 #to_make_arr_contant_all_imgs(X_data)
    Y_data.append(int(Img.split('_')[0]))   #make_array_contant_age_all_photos(age_label)
X_data=np.array(x_data)  
X_data.shape,Y_data[:5]

X_data= X_data.reshape(23708, 35*35)/255
X_data.shape

Y_age = []
for i in Y_data:
    i = int(i)
    if i <= 14:
        Y_age.append(0)
    if (i>14) and (i<=25):
        Y_age.append(1)
    if (i>25) and (i<60):
        Y_age.append(2)
    if (i>=60) and (i<150):
        Y_age.append(3)
len(Y_age)

with tf.compat.v1.Session() as sess:
    y_age = sess.run(tf.one_hot(Y_age , 4))
y_age[:5]

x_train , x_test , y_train , y_test = train_test_split(X_data,y_age,test_size=0.2, random_state  =42)
len(x_test),len(x_train),len(X_data),len(y_test),len(y_train),len(y_age)

learning_rate = 0.01
epochs = 20
batch_size = 50
batches = int(x_train.shape[0] / batch_size)

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

X = tf.placeholder(tf.float32, [None, 1225])
Y = tf.placeholder(tf.float32, [None, 4])

W = tf.Variable(tf.zeros([1225, 4]))
B = tf.Variable(tf.zeros([4]))

pred = tf.nn.softmax(tf.add(tf.matmul(X,W),B))
entropy=-tf.reduce_sum(Y * tf.log(pred), axis=1)
loss = tf.reduce_mean(entropy)
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)
init = tf.global_variables_initializer()

y_pred=[]
accuracy_history=[]
val_accracy_history=[]
with tf.Session() as session:
    session.run(init)
    
    for epoch in range(epochs):
        for i in range(batches):
            offset = i * epoch
            x_imgs = x_train[offset: offset + batch_size]
            y_ages = y_train[offset: offset + batch_size]
            session.run(optimizer, feed_dict={X: x_imgs, Y:y_ages})
            

        cost_avg = session.run(loss, feed_dict={X:x_imgs, Y:y_ages})
        Actual_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
        Accuracy = tf.reduce_mean(tf.cast(Actual_pred, tf.float32))
        acc_train = Accuracy.eval({X:x_train, Y: y_train})* 100       
        accuracy_history.append(acc_train)  
        acc_test = Accuracy.eval({X: x_test, Y: y_test})*100  
        val_accracy_history.append(acc_test)   
        print(f'epoch:{epoch:2d} ==> cost_avg={cost_avg:.4f} ==> train_Accuracy: {acc_train:.3f}%')

    print(f'Test_Accuracy:==> {acc_test:.3f}%')

    for img in (x_test[:]):
      guess = np.argmax(session.run(pred, feed_dict={X: [img]}))
      y_pred.append(int(guess))

plt.plot(list(range(epochs)), accuracy_history) 
plt.plot(list(range(epochs)), val_accracy_history) 
plt.xlabel('Epochs') 
plt.ylabel('Accuracy') 
plt.title('Increase in Accuracy with Epochs')  
plt.legend(['train', 'test'], loc='upper left')
plt.show()

fig = plt.figure(figsize=(25, 10))
words =["tfl","4abab","2rb3enyy mo7trm","elmofrod ytkl",]
for i, j in enumerate(np.random.choice(x_test.shape[0], size=10, replace=False)):
    ax = fig.add_subplot(3, 5, i + 1, xticks=[], yticks=[])
    ax.imshow(x_test[j].reshape((35, 35)),cmap='gray')
    pred_j = y_pred[j]
    actual_j = np.argmax(y_test[j])
    ax.set_title("{} ({})".format(words[pred_j],words[actual_j]),color=("green" if pred_j == actual_j else "red"))
plt.show()

li =[]

for i in y_test:
   li.append(i.argmax())
li[:10]

from sklearn.metrics import confusion_matrix

c=confusion_matrix(li, y_pred)
c

CM = confusion_matrix(np.array(li),np.array( y_pred))
    plt.imshow(CM[:, :], interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('age_groub(confusion matrix)', fontsize=17)

    NUM_IMG = plt.colorbar(fraction=0.1, pad=0.05)
    NUM_IMG.set_label('COUNT_OF_IMAGES ', rotation=270, labelpad=30, fontsize=15)

    NUM_CLASS_X = np.arange(4)
    NUM_CLASS_Y = np.arange(4)

    plt.xticks(NUM_CLASS_X, rotation=90)
    plt.yticks(NUM_CLASS_Y )
    plt.tight_layout()
    plt.ylabel('Actual label')
    plt.xlabel('Predect label')
    plt.show()

from sklearn.metrics import classification_report
print(classification_report(np.array(li),np.array( y_pred)))

from sklearn.linear_model import LogisticRegression
from sklearn import  metrics
xtrain , xtest , ytrain , ytest = train_test_split(X_data,Y_age,test_size=0.2, random_state  =42)
MOD_LR=LogisticRegression(random_state=42)
MOD_LR.fit(xtrain,ytrain)
MOD_LR_TEST=MOD_LR.predict(xtest)
print(metrics.accuracy_score(ytest,MOD_LR_TEST))

from sklearn.metrics import confusion_matrix

c=confusion_matrix(ytest, MOD_LR_TEST)
c