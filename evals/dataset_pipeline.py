"""Dataset pipeline for the Sales Assistant (exercise 4.1, part 3).

Transform production traces into rows of the `sales-assistant-eval` dataset. A
pipeline has three parts: a source (which logs to read), a transform (how to turn
each into a dataset row), and a target (which dataset to write to). Run with:

    bt datasets pipeline run evals/dataset_pipeline.py --limit 100 --window 30d

The reference implementation is in
exercises/3-evals/01-curating-datasets.solution.md.
"""

from braintrust import DatasetPipeline  # noqa: F401

# TODO: define the source (filter), the transform function, and the target
# dataset, then wrap them in DatasetPipeline(...).
