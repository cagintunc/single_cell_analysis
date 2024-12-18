# Single Cell Analysis with GUI

## Table of Contents

1. [Abstract](#abstract) 
2. [Methods](#methods) <br> 
   1. [Dataset Selection](#dataset-selection) <br>
   2. [Interactive Filtering with GUI & Data Preprocessing](#interactive-filtering-and-preprocessing) <br>
        1. [Data Loading](#data-loading) <br>
        2. [Cell Filtering (Percentile-Based)](#cell-filtering) <br>
               1. [Gene Filtering (Cutoff-Based)](#gene-filtering) <br>
               2. [Normalization](#normalization) <br>
               3. [Saving the Filtered Data](#saving-filtered-data) <br>
  3. [Dimensionality Reduction](#dimensionality-reduction) <br>
      1. [PCA](#pca) <br>
  4. [Clustering Analysis](#clustering-analysis) <br>
      1. [ARS](#ars) <br>
  5. [Expression of Interesting Genes](#expression-of-genes) <br>
      1. [Discussion](#discussion) <br>
  6. [Software and Tools](#software-and-tools) <br>
      1.  [Programming](#programming) <br>
      2.  [Hardware Specifications](#hardware-specifications) <br>
  7. [Limitations and Feature Directions](#limitations) <br>
3. [Usage in Bioengineering (Experiment and Results)](#usage-in-bioengineering) <br>
  1. [Introduction](#introduction) <br>
  2. [Results](#results) <br>
4. [References](#references) <br>
5. [Appendix](#appendix) <br>


---

## <a name="program-related-part"></a>Program Related Part (Computer Science Related)

### <a name="abstract"></a>Abstract

Patterns of gene expression differences can be identified by detecting variations in the levels of gene expression across different cell types, tissues, or conditions. These patterns provide insights into the unique molecular functions and identities of cells. For the convenience of researchers, it would be simpler to use a desktop application with a user-friendly interface to do their analysis with just a few clicks instead of spending time on coding and finding the APIs to retrieve the data. In this project, Tabula Muris Single-cell RNA-seq data is used as a transcriptomic resource. By using this data, the aim of this project is to understand the gene expression differentiation process and, ultimately, to automate the analysis.

### <a name="methods"></a>Methods

#### <a name="dataset-selection"></a>Dataset Selection

The dataset used in this analysis was obtained from the Tabula Muris project, a collaborative effort to create a comprehensive single-cell transcriptomic atlas of mouse tissues. Specifically, we utilized the Single-cell RNA-seq data from Smart-seq2 sequencing of FACS sorted cells (v2), which includes high-quality count matrices for individual cells, along with corresponding annotations and metadata.

The project is structured into distinct directories to streamline data management and analysis. The root directory contains three main components:
- **Database folder**: Includes essential reference files like `annotations_facs.csv` and `metadata_FACS.csv`, and the `FACS` subfolder, which stores tissue-specific count matrices.
- **Main script (`main.py`)**: Orchestrates the preprocessing, analysis, and visualization of the scRNA-seq data.
- **Results directory**: Dynamically created during analysis to store output files, graphs, and processed data.

#### <a name="interactive-filtering-and-preprocessing"></a>Interactive Filtering with GUI & Data Preprocessing

##### <a name="data-loading"></a>Data Loading

Data loading is handled using the `scprep` library. Count matrices are loaded from CSV files located in the database folder and organized by tissue type.

##### <a name="cell-filtering"></a>Cell Filtering (Percentile-Based)

Percentile-based cell filtering is implemented using GUI controls that allow users to interactively set minimum and maximum percentiles. This ensures that cells with library sizes within a biologically meaningful range are retained.

##### <a name="gene-filtering"></a>Gene Filtering (Cutoff-Based)

Lowly expressed genes are filtered out using a cutoff-based approach. The cutoff value is set interactively by the user, ensuring that the dataset retains genes with sufficient data for meaningful analysis.

##### <a name="normalization"></a>Normalization

Library size normalization scales RNA counts in each cell to a uniform size, reducing technical biases and ensuring reliable comparisons across cells.

##### <a name="saving-filtered-data"></a>Saving the Filtered Data

Processed data frames are saved in compressed pickle format (`pickle.gz`) in the results directory, ensuring reproducibility and ease of access for downstream analyses.

#### <a name="dimensionality-reduction"></a>Dimensionality Reduction

##### <a name="pca"></a>Principal Component Analysis (PCA)

PCA is used to reduce the dimensionality of the data while retaining the most significant patterns. Users input the number of principal components, and the results are visualized and saved for further analysis.

#### <a name="clustering-analysis"></a>Clustering Analysis

##### <a name="ars"></a>Adjusted Rand Score (ARS)

The ARS metric evaluates the similarity between clustering results, providing insights into the performance of different clustering algorithms.

#### <a name="expression-of-genes"></a>Expression of Interesting Genes

##### <a name="discussion"></a>Discussion

Gene expression patterns are visualized on PCA plots, allowing researchers to identify distinct subpopulations and tissue-specific genes.

#### <a name="software-and-tools"></a>Software and Tools

##### <a name="programming"></a>Programming

Python version 3.9.6 is used for development. Key libraries include `scprep`, `PyQt5`, and `matplotlib`.

##### <a name="hardware-specifications"></a>Hardware Specifications

The program runs on standard desktop hardware with Windows OS.

### <a name="limitations"></a>Limitations and Feature Directions

- **Connection to Online Databases**: Future iterations could integrate online databases like NCBI for automatic data retrieval and updates.
- **Feature Correlation Panel**: Adding a feature correlation panel with explanatory details for genes would enhance usability for non-specialist users.

---

## <a name="usage-in-bioengineering"></a>Usage in Bioengineering (Experiment and Results)

### <a name="introduction"></a>Introduction

This tool supports bioengineering research by simplifying scRNA-seq data analysis, allowing for efficient identification of cell types and gene expression patterns.

### <a name="results"></a>Results

Results include:
- Cluster visualizations and ARS comparisons.
- Differential expression analyses.
- PCA plots highlighting tissue-specific gene expression.

---

## <a name="references"></a>References

- Consortium, Tabula Muris; Webber, James; Batson, Joshua; Pisco, Angela (2018). Single-cell RNA-seq data from Smart-seq2 sequencing of FACS sorted cells (v2). Figshare. Dataset. https://doi.org/10.6084/m9.figshare.5829687.v8
- The Tabula Muris Consortium et al. (2018). Single-cell transcriptomics of 20 mouse organs creates a Tabula Muris. *Nature*, 562, 367–372. https://doi.org/10.1038/s41586-018-0590-4
- Gupta, G., & Yerpude, V. (2018). K – Means Algorithm. *International Journal of Research*, 5, 354-360.
- Levine, J.H., et al. (2015). Data-Driven Phenotypic Dissection of AML Reveals Progenitor-like Cells that Correlate with Prognosis. *Cell*, 162, 184-197.

---

## <a name="appendix"></a>Appendix

- **Figure 1**: Directory structure of the project.
- **Figure 2**: List of tissue types in the dataset.
- **Figures 3-23**: Screenshots and plots demonstrating various steps of the analysis workflow.


---

## Thank you!
