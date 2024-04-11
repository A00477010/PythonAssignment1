import tensorflow as tf
from tensorflow.keras import layers, models

def build_model():
    model = models.Sequential([
        # Convolutional layer with 32 filters, kernel size of 3x3, activation function 'relu'
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        # Max pooling layer with pool size 2x2
        layers.MaxPooling2D((2, 2)),
        # Convolutional layer with 64 filters
        layers.Conv2D(64, (3, 3), activation='relu'),
        # Another max pooling layer
        layers.MaxPooling2D((2, 2)),
        # Convolutional layer with 64 filters
        layers.Conv2D(64, (3, 3), activation='relu'),
        # Flatten the output to feed into a DNN
        layers.Flatten(),
        # Dense layer with 64 units
        layers.Dense(64, activation='relu'),
        # Output layer with 10 units (for 10 classes) with 'softmax' activation
        layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model
def load_data():
    mnist = tf.keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    # Normalize pixel values to be between 0 and 1
    train_images, test_images = train_images / 255.0, test_images / 255.0
    # Add a channel dimension
    train_images = train_images[..., tf.newaxis]
    test_images = test_images[..., tf.newaxis]
    return (train_images, train_labels), (test_images, test_labels)

model = build_model()
(train_images, train_labels), (test_images, test_labels) = load_data()

# Train the model for a specified number of epochs
model.fit(train_images, train_labels, epochs=5)

# Evaluate the model on the test dataset
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print('\nTest accuracy:', test_acc)

model.save('digit_classifier.h5')

