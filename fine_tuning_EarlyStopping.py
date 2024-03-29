"""Untitled1.ipynb

Automatically generated by Colaboratory

Original file is located at
    https://colab.research.google.com/drive/1Ixjavahrp7BGt_sBdQKDBqcKNwEDTdbG

##Importing Necessary Libraries
"""
#%%
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import datetime

# import tensorflow_addons as tfa

import numpy as np
import matplotlib.pyplot as plt

import cv2
from glob import glob


print("loaded")
#%%
"""## Loading Dataset (TF tut)"""

# base_dir = '/Users/zoetzikra/Documents/2022-2023/BSc_Project/Van Gogh dataset/VincentVanGogh'
# base_dir = "VincentVanGogh"
base_dir = "50_small"
# base_dir = "50_large"


# path_to_zip = tf.keras.utils.get_file('VanGogh.zip', origin=_URL, extract=True)
# PATH = os.path.join(os.path.dirname("/Users/zoetzikra/Documents/Year_4 2021:22/BSc Project/Van Gogh dataset"), "VincentVanGogh")

train_dir = os.path.join(base_dir, 'train(sampled)')
data_dir = os.path.join(base_dir, 'source')
validation_dir = os.path.join(base_dir, 'val(sampled)')
print(train_dir)
print(validation_dir)

# what's the matter if this is 1?
BATCH_SIZE = 32
IMG_SIZE = (224, 224) # TODO This has to change, 224 x 224


print("ok until here")

# train_dataset = tf.keras.utils.image_dataset_from_directory(train_dir,
#                                                             shuffle=True,
#                                                             batch_size=BATCH_SIZE,
#                                                             image_size=IMG_SIZE)

train_dataset, validation_dataset = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    shuffle=True,
    validation_split=0.4,
    # subset="training",
    subset="both",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
)

# validation_dataset = tf.keras.utils.image_dataset_from_directory(validation_dir,
#                                                                  shuffle=True,
#                                                                  batch_size=BATCH_SIZE,
#                                                                  image_size=IMG_SIZE)
# validation_dataset = tf.keras.utils.image_dataset_from_directory(
#     data_dir,
#     shuffle=True,
#     validation_split=0.2,
#     subset="validation",
#     seed=123,
#     image_size=IMG_SIZE,
#     batch_size=BATCH_SIZE,
# )

print("train_dataset technically ok")
print("validation_dataset technically ok")


"""## Alternative way to load Dataset (Kaggle tut)"""

# main_path = "/Users/zoetzikra/Documents/2022:23/BSc Project/Van Gogh dataset/VincentVanGogh"

# style_img_paths = []

# for class_path in [os.path.join(main_path,class_name) for class_name in os.listdir(main_path)]:

#    class_img_paths = glob(class_path+"/*")
#    for class_img_path in class_img_paths:
#        style_img_paths.append(class_img_path)

# print("There are {} style images in Van Gogh Paintings Dataset".format(len(style_img_paths)))

# """## Read and plot the images """

# style_images = []

# for style_path in style_img_paths:
#     img = cv2.imread(style_path)
#     img = cv2.resize(img,(128,128))
#     img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#     style_images.append(img)

# print(len(style_images))

# # converting to float32
# style_images = np.array(style_images,dtype=np.float32)
# # scaling between -1 and 1
# style_images = style_images / 127.5 - 1
# # batching
# style_images = tf.data.Dataset.from_tensor_slices(style_images).batch(32)


# plt.figure(figsize=(7,7))
# plt.title("Style Images")
# for i,image in enumerate(style_images.shuffle(10000).take(16)):
#     plt.subplot(4,4,i+1)
#     plt.imshow(image[0])
#     plt.axis("off")
# plt.show()

"""## Alternative way to plot images (TF tut) """

for image_batch, labels_batch in train_dataset:
    print(image_batch.shape)  # it's (32, 224, 224, 3)
    print(labels_batch.shape)  # it's (32,)
    break

class_names = train_dataset.class_names

v_label = np.concatenate([y for _, y in validation_dataset], axis=0)
v_label_list = list(v_label)
t_label = np.concatenate([y for _, y in train_dataset], axis=0)
t_label_list = list(t_label)
print("Label Name\tTraining Sample\tValidation Samples")
for idx, _ in enumerate(class_names):
    print(f"{class_names[idx]}\t{t_label_list.count(idx)}\t{v_label_list.count(idx)}")


# plt.figure(figsize=(7, 7))
# plt.title("Style Images")
# for images, labels in train_dataset.take(1):          # what does the take(1) do here
#   for i in range(9):
#     plt.subplot(3, 3, i + 1)
#     plt.imshow(images[i].numpy().astype("uint8"))
#     plt.title(class_names[labels[i]])                 # --> why does it give seg fault if labels is removed from here
#     plt.axis("off")                                   # and if it's removed from the loop completely it gives
# plt.show()                                            # Invalid shape (32, 180, 180, 3) for image data


"""## Split validation dataset batches in val and test batches"""

# val_batches = tf.data.experimental.cardinality(validation_dataset)
# test_dataset = validation_dataset.take(val_batches // 5)
# validation_dataset = validation_dataset.skip(val_batches // 5)

# print(
#     "Number of validation batches: %d"
#     % tf.data.experimental.cardinality(validation_dataset)
# )
# print("Number of test batches: %d" % tf.data.experimental.cardinality(test_dataset))

"""## Configure the dataset for performance"""

# AUTOTUNE = tf.data.AUTOTUNE #TODO check wrt size #TODO check

# train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
# validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
# test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

"""## Use data augmentation"""

data_augmentation = tf.keras.Sequential(
    [
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.2),
    ]
)

# for image, _ in train_dataset.take(1):
#   plt.figure(figsize=(10, 10))
#   first_image = image[0]
#   for i in range(9):
#     ax = plt.subplot(3, 3, i + 1)
#     augmented_image = data_augmentation(tf.expand_dims(first_image, 0))
#     plt.imshow(augmented_image[0] / 255)
#     plt.axis('off')
# plt.show()


"""## Preprocessing: re-scale pixel values"""
## TF tut KEEP THIS!

preprocess_input = tf.keras.applications.vgg19.preprocess_input
rescale = tf.keras.layers.Rescaling(1.0 / 127.5, offset=-1)

# ## Style Transfer colab file
# x = tf.keras.applications.vgg19.preprocess_input(content_image*255)
# x = tf.image.resize(x, (224, 224))

# ## Kaggle thing
# # converting to float32
# train_dataset = np.array(train_dataset,dtype=np.float32)
# validation_dataset = np.array(validation_dataset,dtype=np.float32)
# # scaling between -1 and 1
# train_dataset = train_dataset / 127.5 - 1
# validation_dataset = validation_dataset / 127.5 - 1
# # batching
# # style_images = tf.data.Dataset.from_tensor_slices(style_images).batch(32)

"""##Create the base model from the pre-trained convnets"""
IMG_SHAPE = IMG_SIZE + (3,)
base_model = tf.keras.applications.VGG19(
    input_shape=IMG_SHAPE, include_top=False, weights="imagenet"
)

for layer in base_model.layers:
    print(layer.name)

    # This feature extractor converts each 180x180x3 image into a 512 block of features.
    # Let's see what it does to an example batch of images:

image_batch, label_batch = next(iter(train_dataset))
feature_batch = base_model(image_batch)
print(feature_batch.shape)
#%%

"""## Feature extraction"""

"""### Freeze the convolutional base"""

# base_model.trainable = False
base_model.trainable = True
# THIS DOESN'T WORK BUT THE ABOVE LINE DOES
# for layer in base_model.layers:
#     layer.trainable = True

base_model.summary()

#%%
"""### Add a classification head"""
# convert the features to a single 512-element vector per image
global_average_layer = (tf.keras.layers.GlobalAveragePooling2D())
# average over the spatial 5x5 spatial locations To generate predictions from the block of features
feature_batch_average = global_average_layer(feature_batch)
print("feature batch average shape:", feature_batch_average.shape)
# use Dense layer to convert these features into a single prediction per image
prediction_layer = tf.keras.layers.Dense(len(class_names), activation="softmax")

prediction_batch = prediction_layer(feature_batch_average)
print("prediction batch shape:", prediction_batch.shape)
#%%

## Build a model by chaining together the data augmentation, rescaling,
# base_model and feature extractor layers using the Keras Functional API.
# As previously mentioned, use training=False as our model contains a BatchNormalization layer.
inputs = tf.keras.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)
x = preprocess_input(x)
x = base_model(x, training=True)
x = global_average_layer(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)
model = tf.keras.Model(inputs, outputs)

model.summary()
#%%
"""### Compile the model"""

# base_learning_rate = 0.0001
# model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
#     loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
#     metrics=["accuracy"],
# )

# model.summary()
# print("Num of trainable variables:", len(model.trainable_variables))
#%%
"""### Train the model"""

# initial_epochs = 10

# loss0, accuracy0 = model.evaluate(validation_dataset)

# print("initial loss: {:.2f}".format(loss0))
# print("initial accuracy: {:.2f}".format(accuracy0))

# history = model.fit(
#     train_dataset,
#     epochs=initial_epochs,
#     validation_data=validation_dataset
# )



# model.save(
#     base_dir
#     + "/saved_model/feature_extracted"
#     + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# )
# #%%
# """### Learning curves"""

# acc = history.history["accuracy"]
# val_acc = history.history["val_accuracy"]

# loss = history.history["loss"]
# val_loss = history.history["val_loss"]

# plt.figure(figsize=(8, 8))
# plt.subplot(2, 1, 1)
# plt.plot(acc, label="Training Accuracy")
# plt.plot(val_acc, label="Validation Accuracy")
# plt.legend(loc="lower right")
# plt.ylabel("Accuracy")
# plt.ylim([min(plt.ylim()), 1])
# plt.title("Training and Validation Accuracy")

# plt.subplot(2, 1, 2)
# plt.plot(loss, label="Training Loss")
# plt.plot(val_loss, label="Validation Loss")
# plt.legend(loc="upper right")
# plt.ylabel("Cross Entropy")
# plt.ylim([0, 10.0])
# plt.title("Training and Validation Loss")
# plt.xlabel("epoch")
# # plt.show()
# plt.savefig("feature_extraction.png")


"""## Fine tuning"""

"""### Un-freeze the top layers of the model"""

# base_model.trainable = True
#%%
#UNNECESSARY IF YOU'RE NOT RUNNING THE ABOVE
print("Number of layers in the base model: ", len(base_model.layers))

fine_tune_at = 0  # Fine-tune from this layer onwards

for layer in base_model.layers[
    :fine_tune_at
]:  # Freeze all the layers before the `fine_tune_at` layer
    layer.trainable = False

base_model.summary()
#%%
""""## Compile the model"""

# As you are training a much larger model and want to readapt the pretrained weights,
# it is important to use a lower learning rate at this stage.
# Otherwise, your model could overfit very quickly.
# IS THIS LEARNING RATE COMMENT RELEVANT IF THE FEATURE SELECTION SECTION IS NOT RUN AT ALL?
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer=tf.keras.optimizers.RMSprop(learning_rate = 0.0001 / 10),
    metrics=["accuracy"],
)

model.summary()

print("Num of trainable variables:", len(model.trainable_variables))

#%%
"""## Continue training the model"""

# fine_tune_epochs = 10
# total_epochs = initial_epochs + fine_tune_epochs

#callback = tf.keras.callbacks.EarlyStopping(monitor="val_loss", mode='min', patience=7, verbose=1)
callback = tf.keras.callbacks.EarlyStopping(monitor="val_loss", mode='min', min_delta=0, patience=20, verbose=1, restore_best_weights=True)

history_fine = model.fit(
    train_dataset,
    epochs=4000,
    callbacks=callback,
    validation_data=validation_dataset,
)
print(len(history_fine.history["val_loss"]))

model.save(
    base_dir
    + "/saved_model/fine_tuned"
    + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
)

acc = history_fine.history["accuracy"]
val_acc = history_fine.history["val_accuracy"]
print("acc, val_acc:", acc, val_acc)

loss = history_fine.history["loss"]
val_loss = history_fine.history["val_loss"]
print("loss, val_loss", loss, val_loss)

#%%


plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label="Training Accuracy")
plt.plot(val_acc, label="Validation Accuracy")
plt.ylim([0.2, 1])
plt.legend(loc="lower right")
plt.title("Training and Validation Accuracy")
plt.xticks(ticks=plt.xticks()[0], labels=plt.xticks()[0].astype(int))
plt.xlim(left=0)

plt.subplot(2, 1, 2)
plt.plot(loss, label="Training Loss")
plt.plot(val_loss, label="Validation Loss")
plt.ylim([0, 6.0])
plt.legend(loc="upper right")
plt.title("Training and Validation Loss")
plt.xlabel("epoch")
plt.xticks(ticks=plt.xticks()[0], labels=plt.xticks()[0].astype(int))
plt.xlim(left=0)
# plt.show()
plt.savefig(f"fine_tuning-{base_dir}-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.png")

#%% Testing

print(loss)
# print(history.history["accuracy"])

# %%

# v_data = np.concatenate([x for x, _ in validation_dataset], axis=0)
v_label = np.concatenate([y for _, y in validation_dataset], axis=0)

from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
# plot_confusion_matrix(model, v_data, v_label)

#Confusion Matrix and Classification Report
Y_pred = model.predict(validation_dataset)
y_pred = np.argmax(Y_pred, axis=1)
print('Confusion Matrix')
conf_matrix = confusion_matrix(v_label, y_pred)
print(conf_matrix)

# Print the confusion matrix using Matplotlib
import seaborn as sns

# Normalise
conf_matrix_norm = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
fig, ax = plt.subplots(figsize=(30,30))
sns.heatmap(conf_matrix_norm, annot=True, fmt='.2f', xticklabels=class_names, yticklabels=class_names)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.savefig(f"conf_matrix-{base_dir}-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.png")

print('Classification Report')
print(classification_report(v_label, y_pred, target_names=class_names))


