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

    if I.ndim > 2:
        # apparently RGB, let's take G 
        I = I[:,:,1].squeeze()
        J = J[:,:,1].squeeze()
    

    x,y,u,v,s2n = simple_piv(I, J, plot=False)
    # sample vector image-like data
    n = np.prod(x.shape)
    # n x m grid of slanted lines
    # random data on the open interval (-1, 1)
    pos = np.zeros(shape=(n, 2, 2), dtype=np.float32)

    u = np.nan_to_num(u)
    v = np.nan_to_num(v)

    # assign projections for each vector
    # note the coordinate definitions:
    # x = columns, y = rows
    pos[:, 0, 1] = x.flatten()
    pos[:, 0, 0] = np.max(y.flatten()) - y.flatten()  # napari shows in image coordinates
    pos[:, 1, 1] = u.flatten()
    pos[:, 1, 0] = -1*v.flatten() # napari shows in image coordinates

    
    # make the angle feature, range 0-2pi
    velocity = np.sqrt(u.flatten()**2 + v.flatten()**2)

    # create a feature that is true for all angles  > pi
    angle = np.arctan2(v.flatten(),u.flatten())

    # create the features dictionary.
    features = {
        'velocity': velocity,
        'angle': angle,
    }

    # add the vectors
    vectors = viewer.add_vectors(
        pos,
        edge_width=1.5,
        features=features,
        edge_color=velocity,
        edge_colormap='husl',
        vector_style = 'arrow',
        name='vectors',
        blending='additive',
        length = 2
    )

    # set the edge color mode to colormap
    vectors.edge_color_mode = 'colormap'
    # vectors.edge_property = 'velocity'

    # # add the vectors a bit longer to show the direction
    # vect = viewer.add_vectors(pos, edge_width=0.8, length=1.1, name = 'direction')



# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
def example_function_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")
