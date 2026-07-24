# Solution: Curate datasets

The reference for the pipeline (part 3) is
[`evals/dataset_pipeline.py`](../../evals/dataset_pipeline.py).

```python
from braintrust import DatasetPipeline

PROJECT = "sales-assistant"


def to_row(id=None, input=None, output=None, metadata=None, expected=None, trace=None):
    return {
        "input": input,
        "expected": output,
        "metadata": metadata,
    }


DatasetPipeline(
    source={
        "project_name": PROJECT,
        "filter": "metadata.num_writes > 0",
        "scope": "trace",
    },
    transform=to_row,
    target={
        "project_name": PROJECT,
        "dataset_name": "sales-assistant-eval",
    },
)
```

Run it:

```bash
bt datasets pipeline run evals/dataset_pipeline.py --limit 100 --window 30d
```

## Notes

- The `source` filter is a SQL expression over your logs. Here it selects runs
  where the agent took an action (`metadata.num_writes > 0`), which are the
  interesting cases to evaluate.
- The `transform` maps the production output to `expected`. That gives you a
  starting point for each row; review and correct the expected values afterward.
- `scope: "trace"` gives the transform the whole trace. Use `"span"` to operate on
  individual spans instead.
- The pipeline is version-controlled code, so unlike clicking **Add to dataset**
  it is repeatable and reviewable.
