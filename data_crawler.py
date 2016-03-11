''' Load data autocamtical an save into a CSV file, which
is compatible with gobnilp Bayes network solver
'''

from data import Data

data_object = Data()
data = []
m = len(data_object.cluster_objects_vectors)
n = len(data_object.cluster_objects_vectors[0].data)


for cluster in data_object.cluster_objects_vectors:
    data.append(cluster.data)

