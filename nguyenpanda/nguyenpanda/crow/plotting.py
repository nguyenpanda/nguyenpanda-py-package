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
                        - 'eval_loss': List of evaluating loss values.
                        - 'train_acc': List of training accuracy values.
                        - 'test_acc': List of testing accuracy values.
                        - 'eval_acc': List of evaluating accuracy values.
        **kwargs: Optional keyword arguments for customizing the plot appearance:
                  - 'figsize' (tuple): Size of the figure.
                  - 'titlesize' (int): Font size of the plot titles.
                  - 'labelsize' (int): Font size of the axis labels.
                  - 'facecolor' (str): Background color of the plot area.
                  - 'figpath' (PathLike): Image saving path (default None)

    Returns:
        None: Displays the plot of loss and accuracy curves.
    """

    plt.figure(figsize=kwargs.get('figsize', (14, 5)))
    plot_config = [
        # (suffix, title, keys)
        ('loss', 'Loss', ['train_loss', 'test_loss', 'eval_loss']),
        ('acc', 'Accuracy', ['train_acc', 'test_acc', 'eval_acc']),
    ]

    for i, (suffix, title, keys) in enumerate(plot_config, 1):
        colors = ['blue', 'red', 'green']
        markers = ['o', 'x', 'o']

        for key, color, marker in zip(keys, colors, markers):
            if key in history:
                plt.subplot(1, len(plot_config), i)
                epochs = len(history[key])
                epoch_range = range(1, epochs + 1)
                plt.plot(epoch_range, history[key], label=key.replace('_', ' ').title(), color=color, linestyle='--',
                         marker=marker)

                plt.title(title, fontsize=kwargs.get('titlesize', 16))
                plt.xlabel('Epoch', fontsize=kwargs.get('labelsize', 14))
                plt.ylabel(title, fontsize=kwargs.get('labelsize', 14))
                plt.legend()
                plt.xlim(0.9, epochs + 0.1)
                plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
                plt.gca().set_facecolor(kwargs.get('facecolor', '#f0f0ff'))

    plt.tight_layout()
    figpath = kwargs.get('figpath', None)
    if figpath:
        plt.savefig(figpath)
    plt.show()


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

    figpath = kwargs.get('figpath', None)
    if figpath:
        plt.savefig(figpath)
    plt.show()
