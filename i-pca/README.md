# Interactive Contrastive Principal Component Analysis

Link to visualization code : https://observablehq.com/d/63cb8c1b032f35b1

In this visualization, I am visualizing results of **applying dimensionality reduction and clustering** on the dataset of [Bob Ross painting descriptions](https://github.com/fivethirtyeight/data/tree/master/bob-ross). Each item in the data corresponds to an individual painting, and its attributes are binary (0 or 1), indicating the presence of a particular landform feature - some natural, others person-made.

Specifically, I am visualizing two sets of data. 

The first, ```pca_data```, contains the results of applying principal component analysis (PCA) to this dataset. Associated with the results is an Array of 2D coordinates (```projection```) formed by projecting the data onto the top 2 principal components, and two Arrays that contain the loadings from PCA (```x_loading```, ```y_loading```), a quantitative value (property name ```loading```) per attribute (property name ```attribute```).

The second, ```kmeans_data```, contains the results of applying k-means to this dataset. This is an Array where each item corresponds to a specific painting's attribute, with the following properties:

* ```id```: unique identifier for the painting
* ```attribute```: the name of the attribute
* ```value```: 0 or 1, indicating presence of attribute
* ```label```: the cluster label for this painting

This design includes three primary visualizations from the above data: **a scatterplot for PCA projects, a diverging bar plot for PCA loadings, and heatmap for clustering**. Moreover, it supports the following **interactions**. 

1. **Hovering over a circle in the scatterplot** should show the title and image of the episode corresponding to the episode that painting was drawn. Hovering off of the circle should remove the display of the title and the image.
2. **Selecting a cluster, via clicking**, should highlight the corresponding set of circles that belong to the cluster. Clicking off of a cluster should reset all circles' appearance to their default. Further, multiple clusters can be selected.

3. **Allow users to steer dimension reduction using ccPCA**. Upon clicking the ```run ccPCA``` button, the method of [contrasting clusters in PCA](https://github.com/takanori-fujiwara/ccpca) should be run, using the set of circles that have been highlighted via cluster selection as the target set. The visualization would update accordingly with the results - a new 2D projection, and new loadings. The new projection will show how the highlighted data items _contrast_ from the remainder of the dataset, via their positions in the 2D projection, and the loadings. To this end, I will provide a python server backend to accomplish the computation.
