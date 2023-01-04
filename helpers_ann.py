#---------------------------------------------------------------------------------------------------#
# File name: helpers_ann.py                                                                         #
# Autor: Chrissi2802                                                                                #
# Created on: 19.12.2022                                                                            #
#---------------------------------------------------------------------------------------------------#
# This file provides auxiliary classes and functions for neural networks.
# Exact description in the functions.


import tensorflow as tf
import matplotlib.pyplot as plt


def count_parameters_of_pytorch_model(model):
    """This function counts all parameters of a passed PyTorch model.
    
    Args:
        model (pytorch model): Model from which the parameters are to be counted

    Returns:
        params (integer): Number of parameters
    """

    params = sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)

    return params


def hardware_config(device = "GPU"):
    """This function configures the hardware.
    
    Args:
        device (string, default "GPU"): Which device to use, TPU or GPU
        
    Returns:
        strategy (tensorflow MirroredStrategy): Strategy for the hardware
    """

    if (device == "TPU"):
        # TPU, use only if TPU is available
        tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
        tf.config.experimental_connect_to_cluster(tpu)
        tf.tpu.experimental.initialize_tpu_system(tpu)
        strategy = tf.distribute.TPUStrategy(tpu)
    else:
        # GPU, if not available, CPU is automatically selected
        gpus = tf.config.list_logical_devices("GPU")
        strategy = tf.distribute.MirroredStrategy(gpus)

    return strategy


def plot_loss_and_acc(history, fold = -1):
    """This function plots the loss and accuracy for training and testing.
    
    Args:
        history (tensorflow history): History of the training and testing
        fold (integer, default -1): Cross-validation run
    """

    # Extract data
    epochs = len(history.history["loss"])
    train_loss = history.history["loss"]
    train_acc = [acc * 100.0 for acc in history.history["accuracy"]]
    test_loss = history.history["val_loss"]
    test_acc = [acc * 100.0 for acc in history.history["val_accuracy"]]

    # Plot loss and accuracy, presettings
    fig, ax1 = plt.subplots()
    xaxis = list(range(1, epochs + 1))
    ax1.set_xlabel("Epochs")
    ax1.set_ylabel("Loss")
    ax2 = ax1.twinx()
    ax2.set_ylabel("Accuracy in %")
    ax2.set_ylim(0.0, 100.0)

    train_loss_plot = ax1.plot(xaxis, train_loss, label = "Training Loss", color = "red")       # Training loss
    train_acc_plot = ax2.plot(xaxis, train_acc, label = "Training Accuracy", color = "fuchsia") # Training accuracy
    test_loss_plot = ax1.plot(xaxis, test_loss, label = "Validation Loss", color = "lime")      # Test loss
    test_acc_plot = ax2.plot(xaxis, test_acc, label = "Validation Accuracy", color = "blue")    # Test accuracy

    plots = train_loss_plot + train_acc_plot + test_loss_plot + test_acc_plot 
    labels = [l.get_label() for l in plots]   # Labels for the legend
    ax1.legend(plots, labels)

    if (fold == -1):    # no cross-validation
        fold1 = ""
        fold2 = ""
    else:   # cross-validation
        fold1 = " Fold " + str(fold)
        fold2 = "_Fold_" + str(fold)
        
    plt.title("Loss and Accuracy" + fold1)
    fig.savefig("Loss_and_Accuracy" + fold2 + ".png")
    plt.show()


if (__name__ == "__main__"):

    # configures the hardware
    strategy = hardware_config("GPU")

    with strategy.scope():
        pass
        # Code here

