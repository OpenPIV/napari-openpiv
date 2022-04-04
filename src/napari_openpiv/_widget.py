"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from magicgui import magic_factory


class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Click me!")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")


@magic_factory
def example_magic_widget(img_layer: "napari.layers.Image", 
                         viewer: "napari.viewer.Viewer"):
    print(f"you have selected {img_layer}")
    from openpiv.piv import simple_piv
    import numpy as np
    # assuming the layer is a stack
    I = np.array(img_layer.data[0]).astype(np.int32)
    J = np.array(img_layer.data[1]).astype(np.int32)
    x,y,u,v = simple_piv(I,J, plot=False)
    # sample vector image-like data
    n = np.prod(x.shape)
    # n x m grid of slanted lines
    # random data on the open interval (-1, 1)
    pos = np.zeros(shape=(n, 2, 2), dtype=np.float32)

    # assign projections for each vector
    pos[:, 0, 0] = x.flatten()
    pos[:, 0, 1] = y.flatten()
    pos[:, 1, 0] = x.flatten() + u.flatten()
    pos[:, 1, 1] = y.flatten() + v.flatten()

    # add the vectors
    vect = viewer.add_vectors(pos, edge_width=0.2, length=2.5)



# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
def example_function_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")
