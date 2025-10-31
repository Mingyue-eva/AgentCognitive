### Actual Results

When using `transform_output="pandas"`, a ValueError is raised because the transformer output has only 4 rows (one per day) but scikit-learn’s pandas output wrapper tries to assign the original 96-row index to it, causing a length mismatch between the existing axis (4 elements) and the new labels (96 elements).