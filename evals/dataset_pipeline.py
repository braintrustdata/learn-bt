"""Dataset pipeline for the Sales Assistant.

A pipeline has three parts: a source (which logs to read), a transform (how to
turn each into a dataset row), and a target (which dataset to write to). Run it
with:

    bt datasets pipeline run evals/dataset_pipeline.py --limit 10 --window 30d

The reference implementation is in exercises/3-evals/01-curating-datasets.solution.md.
"""

from braintrust import DatasetPipeline


# def transform(id=None, input=None, output=None, metadata=None, expected=None, trace=None):
#     """Turn one source span into a dataset row."""
#     pass
#
# DatasetPipeline(
#     name="my-pipeline",
#     source={},
#     transform=transform,
#     target={},
# )
