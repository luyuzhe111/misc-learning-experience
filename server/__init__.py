import flask
import numpy as np
import json

from flask import Flask
from flask_cors import CORS
from sklearn.cluster import KMeans

# create Flask app
app = Flask(__name__)
CORS(app)

# list of attribute names of size m
attribute_names=json.load(open('server/attribute_names.json','r'))

# a 2D numpy array containing binary attributes - it is of size n x m, for n paintings and m attributes
painting_attributes=np.load('server/painting_attributes.npy')

# a list of epsiode names of size n
episode_names=json.load(open('server/episode_names.json','r'))

# a list of painting image URLs of size n
painting_image_urls=json.load(open('server/painting_image_urls.json','r'))

'''
This will return an array of strings containing the episode names -> these should be displayed upon hovering over circles.
'''
@app.route('/get_episode_names', methods=['GET'])
def get_episode_names():
    return flask.jsonify(episode_names)
#

'''
This will return an array of URLs containing the paths of static for the paintings
'''
@app.route('/get_painting_urls', methods=['GET'])
def get_painting_urls():
    return flask.jsonify(painting_image_urls)
#

'''
TODO: implement PCA, this should return data in the same format as you saw in the first part of the assignment:
    * the 2D projection
    * x loadings, consisting of pairs of attribute name and value
    * y loadings, consisting of pairs of attribute name and value
'''
@app.route('/initial_pca', methods=['GET'])
def initial_pca():
    x = painting_attributes - np.mean(painting_attributes, axis=0)

    cov_mat = np.cov(x.T)
    eig_val, eig_vec = np.linalg.eig(cov_mat)
    comp_one = x.dot(eig_vec.T[0])
    comp_two = x.dot(eig_vec.T[1])
    arr = []
    for i in range(comp_one.shape[0]):
        arr.append([comp_one[i], comp_two[i]])

    loading_x = [{'attribute': i, 'loading': j} for i, j in zip(attribute_names, eig_vec.T[0])]
    loading_y = [{'attribute': i, 'loading': j} for i, j in zip(attribute_names, eig_vec.T[1])]

    pca_results = {'loading_x': loading_x, 'loading_y': loading_y, 'projection': arr}

    return flask.jsonify(pca_results)
#

'''
TODO: implement ccPCA here. This should return data in _the same format_ as initial_pca above.
It will take in a list of data items, corresponding to the set of items selected in the visualization. This can be acquired from `flask.request.json`. This should be a list of data item indices - the **target set**.
The alpha value, from the paper, should be set to 1.1 to start, though you are free to adjust this parameter.
'''
@app.route('/ccpca', methods=['GET','POST'])
def ccpca():
    alpha = 1.1
    ids = flask.request.json
    background = list(set([i for i in range(painting_attributes.shape[0])]) - set(ids))
    print('target?',ids,'background?',background)
    back = painting_attributes[background]
    y = back - np.mean(back, axis=0)
    cov_mat_y = np.cov(y.T)

    x = painting_attributes - np.mean(painting_attributes, axis=0)
    cov_mat_x = np.cov(x.T)

    cov_diff = cov_mat_x - alpha * cov_mat_y

    eig_val, eig_vec = np.linalg.eigh(cov_diff)
    comp_one = x.dot(eig_vec[:,-1])
    comp_two = x.dot(eig_vec[:,-2])
    print('eig vals?',eig_val)
    arr = []
    for i in range(comp_one.shape[0]):
        arr.append([comp_one[i], comp_two[i]])

    loading_x = [{'attribute': i, 'loading':float(np.sqrt(eig_val[-1])*j)} for i, j in zip(attribute_names, eig_vec[:,-1])]
    loading_y = [{'attribute': i, 'loading': float(np.sqrt(eig_val[-2])*j)} for i, j in zip(attribute_names, eig_vec[:,-2])]

    cpca_results = {'loading_x': loading_x, 'loading_y': loading_y, 'projection': arr}

    return flask.jsonify(cpca_results)
#

'''
TODO: run kmeans on painting_attributes, returning data in the same format as in the first part of the assignment. Namely, an array of objects containing the following properties:
    * label - the cluster label
    * id: the data item's id, simply its index
    * attribute: the attribute name
    * value: the binary attribute's value
'''
@app.route('/kmeans', methods=['GET'])
def kmeans():
    num_labels = 6
    kmeans = KMeans(n_clusters=num_labels, random_state=0).fit(painting_attributes)
    labels = kmeans.labels_
    kmeans_results = []
    for i, label in enumerate(labels):
        for j, attr in enumerate(attribute_names):
            kmeans_results.append({'attribute': attr,
                                   'id': str(i),
                                   'label': str(label),
                                   'value': str(painting_attributes[i][j])})

    return flask.jsonify(kmeans_results)


# if __name__=='__main__':
#     painting_image_urls = json.load(open('server/painting_image_urls.json','r'))
#     attribute_names = json.load(open('server/attribute_names.json','r'))
#     episode_names = json.load(open('server/episode_names.json','r'))
#     painting_attributes = np.load('server/painting_attributes.npy')