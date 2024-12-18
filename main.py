import scprep
import main_menu
import filtering
import gene_filtering
import pca_input
import phenograph
import pca_plotting
import cluster_number
import clustering_selection
import dbscan_inputs
import differential_analysis
import jitter_plot
import agglomerative_ui
import graphtools as gt
import sklearn
import search_ui
import numpy as np
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from scipy.spatial.distance import pdist, squareform
from sklearn.model_selection import train_test_split
from itertools import combinations
from scipy import sparse
import seaborn as sns
import sys
import pandas as pd
import os
import matplotlib.pyplot as plt

CLUSTERING_ALGO = ["KMeans", 
        "Phenograph", 
        "Spectral", 
        "DBSCAN",
        "Agglomerative Clustering",
        "ALL - Comparison"]

class Tissue():
    def __init__(self, tissue_dataframe):
        self.df = tissue_dataframe
    
    def get_DF(self):
        return self.df


class Tissues():
    def __init__(self, selected_list, new_experiment_path):
        self.selected_tissues = selected_list
        self.new_experiment_path = new_experiment_path
        self.tissue_list = []
        self.data = []
        self.initialize_tissues()
        self.annotation = pd.read_csv("database/annotations_facs.csv")
        

    def initialize_tissues(self):
        for tissue_name in self.selected_tissues:
            file_path = PATH_TO_FACS + tissue_name + "-counts.csv"
            new_tissue = scprep.io.load_csv(filename=file_path, 
                                            cell_axis='row',sparse=True).transpose()
            self.data.append(new_tissue)
            self.tissue_list.append(Tissue(new_tissue))
        self.data, self.sample_labels = scprep.utils.combine_batches(self.data, self.selected_tissues)
        lookup = pd.Series(self.data.index).apply(lambda x: x.split('.')[1])
        
        self.metadata = pd.read_csv("database/metadata_FACS.csv", 
                                    index_col=0).loc[lookup.values].reset_index()
        self.metadata.index = self.data.index

        fig, ax = plt.subplots()
        scprep.plot.plot_library_size(self.data, log=False, title='Library size before filtering',
                                      filename=f"{self.new_experiment_path}/lib_before_filtering.png",
                                      ax=ax) 
        plt.close(fig)
        
    
    def get_tissues(self):
        return self.tissue_list
    
    def get_data(self):
        return self.data
    
    def get_metadata(self):
        return self.metadata

            

if __name__ == "__main__":
    PATH_TO_FACS = "database/FACS/"

    list_dir = os.listdir("results")
    new_experiment_name = None

    if len(list_dir) > 0:
        new_experiment_name = f"Experiment_{len(list_dir)+1}"
        os.mkdir(f"results/{new_experiment_name}")
    else:
        new_experiment_name = "Experiment_1"
        os.mkdir(f"results/{new_experiment_name}")

    new_experiment_path = f"results/{new_experiment_name}"

    app = QtWidgets.QApplication(sys.argv)
    selected_tissues = main_menu.set_up(app)
    tissues = Tissues(selected_tissues, new_experiment_path)
    # filtering

    data = tissues.get_data()

    #for i in data.columns:
        #if "ag" == i[0:2].lower() or "nk" == i[0:2].lower() or "sf" == i[0:2].lower():
            #print(i)

    percentiles = filtering.main(app, data, new_experiment_path)

    # cutoff
    data, metadata = scprep.filter.filter_library_size(data, tissues.get_metadata(),percentile=percentiles)

    fig, ax = plt.subplots()
    scprep.plot.histogram(scprep.measure.gene_capture_count(data), log=True,
                            title="Gene Captured",
                            xlabel='# of cells with nonzero expression',
                            ylabel='# of genes',
                            ax=ax,
                            filename=new_experiment_path+"/before_cutoff.png")
    plt.close(fig)

    cut_off = gene_filtering.main(app, data, new_experiment_path)

    data = scprep.filter.filter_rare_genes(data, min_cells=cut_off)

    fig, ax = plt.subplots()
    scprep.plot.histogram(scprep.measure.gene_capture_count(data),
                            cutoff =10,
                            log=True,
                            title="Gene capture after filtering",
                            xlabel='# of cells with nonzero expression',
                            ylabel='# of genes',
                            ax=ax,
                            filename=new_experiment_path+"/after_gene_filtering.png")
    plt.close(fig)

    # normalization step
    fig, ax = plt.subplots()
    scprep.plot.plot_library_size(data, title='Library size before normalization',
                                ax=ax,
                                filename=new_experiment_path+"/lib_size_Before_Normalization.png")
    plt.close(fig)

    data, metadata['library_size'] = scprep.normalize.library_size_normalize(data,
                                                                            return_library_size=True)
    fig, ax = plt.subplots()
    scprep.plot.plot_library_size(data, title='Library size after normalization', 
                                ax=ax, filename=new_experiment_path+"/lib_size_After_Normalization.png")
    plt.close(fig)

    data = scprep.transform.sqrt(data)

    fig, ax = plt.subplots()
    scprep.plot.histogram(data.mean(axis=0), log='y',
        title= "Mean Expression of Each Gene",
        xlabel= "Genes",
        ylabel= "Mean Expression Level", ax=ax, filename=new_experiment_path+"/mean_expressionOf_genes.png")
    plt.close(fig)

    if not os.path.exists(new_experiment_path+"/filtered_data"):
        os.mkdir(new_experiment_path+"/filtered_data")

    data.to_pickle(new_experiment_path+"/filtered_data/data.pickle.gz") 
    metadata.to_pickle(new_experiment_path+"/filtered_data/meta.pickle.gz") 

    if not os.path.exists(new_experiment_path+"/scatter_PCA"):
        os.mkdir(new_experiment_path+"/scatter_PCA")

    pca_number = pca_input.main(app)
    data_pca = scprep.reduce.pca(data, n_components=pca_number, method='dense')

    # Fill missing subtissue values with tissue values
    metadata['subtissue'].fillna(metadata["tissue"], inplace=True)

    pca_plotting.main(app, data_pca, metadata, 
                new_experiment_path)


    # for clustering.
    clustering_algorithm_polymorphic = None
    n_cluster = None
    selected_algo = clustering_selection.main(app, CLUSTERING_ALGO)
    os.mkdir(new_experiment_path+"/clusters")

    if selected_algo == "ALL - Comparison":
        n_cluster = cluster_number.main(app)

        phenograph_clusters, x, y = phenograph.cluster(data_pca)
        kmeans_clusters = sklearn.cluster.KMeans(n_clusters = n_cluster, n_init='auto').fit_predict(data_pca)
        G = gt.Graph(data_pca)
        G_igraph = G.to_igraph()
        spec_op = sklearn.cluster.SpectralClustering(n_clusters = n_cluster,affinity='precomputed')
        spectral_clusters = spec_op.fit_predict(G.K)

        eps, min_samples = dbscan_inputs.main(app)
        dbscan_op = sklearn.cluster.DBSCAN(eps=eps, min_samples=min_samples)
        dbscan_clusters = dbscan_op.fit_predict(data_pca)

        n_cluster, linkage = agglomerative_ui.main(app)
        agg_op = sklearn.cluster.AgglomerativeClustering(n_clusters=n_cluster, linkage=linkage)
        agglo_clusters = agg_op.fit_predict(data_pca)

        clusterings = {
            'Phenograph':phenograph_clusters,
            'KMeans':kmeans_clusters,
            'Spectral':spectral_clusters,
            'DBSCAN': dbscan_clusters,
            'Agglomerative': agglo_clusters
        }

        for alg in clusterings:
            cl_nu = scprep.utils.sort_clusters_by_values(clusterings[alg], -data_pca.iloc[:,0])
            clusterings[alg] = cl_nu

        fig, axes = plt.subplots(2, 3, figsize=(16, 16), subplot_kw={'aspect': 'equal'})

        for ax, algorithm in zip(axes.flatten(), clusterings):
            scprep.plot.scatter2d(
                data_pca, 
                c=clusterings[algorithm], 
                cmap=plt.cm.rainbow,
                title='{} - ({})'.format(algorithm, len(np.unique(clusterings[algorithm]))),
                ticks=False, 
                label_prefix="PCA", 
                legend=False,
                discrete=True,
                ax=ax,
                filename=new_experiment_path + f"/clusters/{algorithm}.png"
            )

        for ax in axes.flatten()[len(clusterings):]:
            ax.axis('off')  
        plt.show()

        all_clusterings = []
        all_algorithms = list(clusterings.keys())
        for algo in all_algorithms:
            all_clusterings.append(clusterings[algo])

        all_clusterings = np.vstack(all_clusterings)
    
        cluster_similarities = squareform(pdist(all_clusterings, metric=sklearn.metrics.adjusted_rand_score))
        cluster_similarities = cluster_similarities + np.eye(5)

        clustermap = sns.clustermap(cluster_similarities, 
                                    xticklabels=all_algorithms, 
                                    yticklabels=all_algorithms)
        clustermap.savefig(new_experiment_path+f"/clusters/clustermap.png") 

        plt.show()
        clustering_algorithm_polymorphic, x, y = phenograph.cluster(data_pca) #DEFAULT


    else:

        if selected_algo == "Phenograph":
            clustering_algorithm_polymorphic, x, y = phenograph.cluster(data_pca)
            
        elif selected_algo == "KMeans":
            n_cluster = cluster_number.main(app)
            clustering_algorithm_polymorphic = sklearn.cluster.KMeans(n_clusters = n_cluster, n_init='auto').fit_predict(data_pca)

        elif selected_algo == "Spectral":
            G = gt.Graph(data_pca)
            G_igraph = G.to_igraph()
            n_cluster = cluster_number.main(app)
            spec_op = sklearn.cluster.SpectralClustering(n_clusters = n_cluster,affinity='precomputed')
            clustering_algorithm_polymorphic = spec_op.fit_predict(G.K)
        
        elif selected_algo == "DBSCAN":
            eps, min_samples = dbscan_inputs.main(app)
            dbscan_op = sklearn.cluster.DBSCAN(eps=eps, min_samples=min_samples)
            clustering_algorithm_polymorphic = dbscan_op.fit_predict(data_pca)

        elif selected_algo == "Agglomerative Clustering":
            n_cluster, linkage = agglomerative_ui.main(app)
            agg_op = sklearn.cluster.AgglomerativeClustering(n_clusters=n_cluster, linkage=linkage)
            clustering_algorithm_polymorphic = agg_op.fit_predict(data_pca)

        cl_nu = scprep.utils.sort_clusters_by_values(clustering_algorithm_polymorphic, -data_pca.iloc[:,0])
        clustering_algorithm_polymorphic = cl_nu
        fig, ax = plt.subplots(figsize=(10, 10))  # Use plt.subplots for a Figure and Axes
        scprep.plot.scatter2d(data_pca,c=clustering_algorithm_polymorphic, title=selected_algo,
                            cmap=plt.cm.rainbow,ticks=False, label_prefix="PCA", 
                            legend=False,discrete=True,ax=ax,
                            filename=new_experiment_path+f"/clusters/{selected_algo}.png")
        plt.show()

    os.mkdir(new_experiment_path + "/gene_search")
    os.mkdir(new_experiment_path + "/gene_search/jitter_plots")

    genes = None
    gene = search_ui.main(app)

    if "," in gene:
        genes = [g.strip().rstrip() for g in gene.split(",")]
        valid_genes = [g for g in genes if g in data.columns]
        genes = valid_genes

        if not valid_genes:
            print("No valid genes found in the dataset.")
            raise ValueError("No genes to plot.")

        n_genes = len(valid_genes)
        cols = min(3, n_genes)  
        rows = math.ceil(n_genes / cols)

        fig_width = 5 * cols  
        fig_height = 5 * rows  
        fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))

        if n_genes == 1:
            axes = [axes]  
        else:
            axes = axes.flatten()

        # Plot only for valid genes
        for g, ax in zip(valid_genes, axes):
            expression = scprep.select.select_cols(data, exact_word=g)
            sort_index = expression.sort_values().index
            
            scprep.plot.scatter2d(data_pca.loc[sort_index], 
                                c=expression.loc[sort_index], 
                                shuffle=False, 
                                title=g, 
                                ticks=None, 
                                label_prefix='PC', 
                                ax=ax)

        for ax in axes[n_genes:]:
            ax.axis('off')
        
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        plt.tight_layout() 
        plt.savefig(new_experiment_path + "/gene_search/multi_gene_plot.png")  
        plt.show()


    else:
        while gene not in data.columns:
            gene = search_ui.main(app)
        expression = scprep.select.select_cols(data, exact_word=gene)
        sort_index = expression.sort_values().index
        scprep.plot.scatter2d(data_pca.loc[sort_index], 
                            c=expression.loc[sort_index], 
                            shuffle=False, 
                            title=gene, 
                            ticks=None, 
                            label_prefix='PC', 
                            ax= ax,
                            filename=new_experiment_path + f"/gene_search/{gene}.png")
        genes = gene
        plt.plot()

    
    jitter_plot.main(app, genes, 
                    data, 
                    clustering_algorithm_polymorphic, 
                    new_experiment_path + "/gene_search/jitter_plots")
    
    data_sparse = scprep.utils.SparseDataFrame(data)
    differential_analysis.main(app, 
                               list([str(i) for i in range(1, n_cluster+1)]), 
                               data_sparse, 
                               new_experiment_path,
                               clustering_algorithm_polymorphic)

        
    










