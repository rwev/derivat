
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

def buildGraphsViewWidget():

    graphs_view_widget = gl.GLViewWidget()
    return graphs_view_widget

    # graphs_view_widget.addItem(buildGridItem())
    # graphs_view_widget.addItem(buildScatterPlotItem())
    # return graphs_view_widget

def buildGridItem():
    grid_item = gl.GLGridItem()

    grid_item.setSize(100,100)
    grid_item.setSpacing(5, 5)

    return grid_item

def buildScatterPlotItem():
    xx = np.array([0, 10])
    yy = np.array([0, 10]) 
    zz = np.array([0, 10]) 

    means = [xx.mean(), yy.mean(), zz.mean()]  
    stds = [xx.std() / 3, yy.std() / 3, yy.std() / 3]

    xy_corr = 0.6         
    yz_corr = -0.8
    xz_corr = -0.6

    covs = [
            [stds[0]**2,                stds[0]*stds[1]*xy_corr,    stds[0]*stds[2]*xz_corr], 
            [stds[1]*stds[0]*xy_corr,   stds[1]**2,                 stds[1]*stds[2]*yz_corr],
            [stds[2]*stds[0]*xz_corr,   stds[2]*stds[1]*yz_corr,    stds[2]**2] 
            ]

    m = np.random.multivariate_normal(means, covs, 1000).T # (3 x 1000)
    pos = np.array([(c[0], c[1], c[2]) for c in m.T])

    scatter = gl.GLScatterPlotItem(pos=pos, size=0.1, pxMode=False)
    return scatter