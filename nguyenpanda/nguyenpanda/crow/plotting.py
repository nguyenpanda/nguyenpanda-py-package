import matplotlib.pyplot as plt

import random
from pathlib import Path

def plot_train_test_loss_accuracy(history: dict[str, list | tuple], **kwargs):
    """
    Plots training and testing loss and accuracy over epochs.

    Args:
        history (dict): A dictionary containing lists or tuples of loss and accuracy values
                        for both training and testing. The dictionary keys should be:
                        - 'train_loss': List of training loss values.
                        - 'test_loss': List of testing loss values.
                        - 'train_acc': List of training accuracy values.
                        - 'test_acc': List of testing accuracy values.
        **kwargs: Optional keyword arguments for customizing the plot appearance:
                  - 'figsize' (tuple): Size of the figure.
                  - 'titlesize' (int): Font size of the plot titles.
                  - 'labelsize' (int): Font size of the axis labels.
                  - 'figpath' (PathLike): Image saving path (default None)

    Returns:
        None: Displays the plot of loss and accuracy curves.
    """
    epochs = len(history['train_loss'])
    epoch_range = list(range(1, epochs + 1))

    plt.figure(figsize=kwargs.get('figsize', (14, 5)))

    plt.subplot(1, 2, 1)
    plt.plot(epoch_range, history['train_loss'], label='Train Loss', color='blue', linestyle='--', marker='o')
    plt.plot(epoch_range, history['test_loss'], label='Test Loss', color='red', linestyle='--', marker='x')
    plt.title('Loss', fontsize=kwargs.get('titlesize', 16))
    plt.xlabel('Epoch', fontsize=kwargs.get('lablesize', 14))
    plt.ylabel('Loss', fontsize=kwargs.get('lablesize', 14))
    plt.legend()
    plt.xlim(1 - 0.1, epochs + 0.1)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gca().set_facecolor(kwargs.get('facecolor', '#f0f0ff'))

    plt.subplot(1, 2, 2)
    plt.plot(epoch_range, history['train_acc'], label='Train Accuracy', color='blue', linestyle='--', marker='o')
    plt.plot(epoch_range, history['test_acc'], label='Test Accuracy', color='red', linestyle='--', marker='x')
    plt.title('Accuracy', fontsize=kwargs.get('titlesize', 16))
    plt.xlabel('Epoch', fontsize=kwargs.get('lablesize', 14))
    plt.ylabel('Accuracy', fontsize=kwargs.get('lablesize', 14))
    plt.legend()
    plt.xlim(1 - 0.1, epochs + 0.1)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gca().set_facecolor(kwargs.get('facecolor', '#f0f0ff'))

    plt.tight_layout()
    plt.show()
    plt.savefig(kwargs.get('figpath', None))


def plot_random_transformed_image(dataset, n_row: int = 6, n_col: int = 3, **kwargs):
    """
    Plots random original and transformed images from a dataset.

    Args:
        dataset (torch.Dataset): The dataset containing images and their corresponding labels.
        n_row (int): Number of rows in the subplot grid. Default is 6.
        n_col (int): Number of columns in the subplot grid. Each column will contain two images
                     (original and transformed). Default is 3.
        **kwargs: Optional keyword arguments for customizing the plot appearance:
                  - 'figsize' (tuple): Size of the figure.
                  - 'supsize' (int): Font size of the subplot title.
                  - 'y' (float): Vertical alignment of the subplot title.
                  - 'figpath' (PathLike): Image saving path (default None)

    Returns:
        None: Displays a plot of original and transformed images.
    """
    fig, axs = plt.subplots(nrows=n_row, ncols=n_col * 2, figsize=kwargs.get('figsize', (20, 25)))
    fig.suptitle(f'Random transformed image', size=kwargs.get('supsize', 25), y=kwargs.get('y', 0.92))

    for r in range(n_row):
        for c in range(0, n_col * 2, 2):
            idx = random.randint(0, len(dataset) - 1)

            img, label = dataset.dataset[idx]
            axs[r, c].set_title(f'Original {dataset.classes_dict[label]}')
            axs[r, c].imshow(img)

            img, label = dataset[idx]
            axs[r, c + 1].set_title(f'Transformed {dataset.classes_dict[label]}')
            axs[r, c + 1].imshow(img.permute([1, 2, 0]).numpy())

            axs[r, c].axis(False)
            axs[r, c].grid('off')
            axs[r, c + 1].axis(False)
            axs[r, c + 1].grid('off')

    plt.show()
    plt.savefig(kwargs.get('figpath', None))
