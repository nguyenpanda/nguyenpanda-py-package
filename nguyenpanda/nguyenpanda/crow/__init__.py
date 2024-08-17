"""
`crow` is a utility package designed to streamline the process of working
on Machine Learning (ML) and Deep Learning (DL) projects within Jupyter notebooks.
It provides a set of convenient functions to help manage datasets, directories,
and other common tasks that are essential in a typical ML/DL workflow.
"""

from .jupyter_notebook import NoteBookUtils
from .plotting import plot_train_test_loss_accuracy

nb_utils: NoteBookUtils = NoteBookUtils()

__all__ = [
    'NoteBookUtils',
    'nb_utils',
    'plot_train_test_loss_accuracy',
]
