# 4.1 Curate datasets

Build a dataset of test cases from real logs, three ways.

## Task

1. On the **Logs** page, open specific logs and use **Add to dataset** to add them
   to a dataset named `sales-assistant-eval`.
2. Ask Loop to find logs that match a criterion (for example, runs where the agent
   was asked to draft an email), then add those to the dataset.
3. Create a **dataset pipeline**. A pipeline has a source (which logs to read), a
   transform function (how to turn each into a dataset row), and a target (which
   dataset to write to). Write the pipeline in the top-level `evals/` directory.
   Find the logs that match your criterion, transform them so the production
   answer becomes the `expected` value, and write them to `sales-assistant-eval`.
   You can do this by hand or with a coding agent. See the
   [dataset pipelines docs](https://www.braintrust.dev/docs/annotate/datasets/pipelines).

Write the pipeline in [`evals/dataset_pipeline.py`](../../evals/dataset_pipeline.py).

## Solution

See [01-curating-datasets.solution.md](01-curating-datasets.solution.md).
