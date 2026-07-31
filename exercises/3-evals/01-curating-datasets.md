# 4.1 Curate a dataset

Before you can evaluate the agent, you need a set of test cases to run it
against. In practice the best test cases are the requests real users already sent. So you curate them from production logs.

Datasets are commonly built for specific scenarios. Here, we're going to build a dataset using 3 common patterns for scenarios where our agent needs to draft emails. 

Create a dataset `email-drafting`.

## Task

1. **Curate by hand from the UI.** On the **Logs** page, filter to the runs where the agent drafted an email (the `draft_email` tool was called). Open a few good ones, look at the request that came in, and use **Add to dataset** to add them to `email-drafting`.

2. **Curate with Loop.** Manually adding spans to a dataset from the UI is quick and easy, but limited. For example, it's hard to do in bulk, and we cannot transform the span before we add it. Next we'll look at how Loop can assist with this task. Ask **Loop** to find more email-drafting runs and add them to `email-drafting` for you. A coding agent driving the `bt` CLI can do the same job.

3. **Curate with a dataset pipeline.** The previous methods don't offer much flexibility in doing this in bulk in a granular way. Often, we need to transform/preprocess the span or trace before adding it to a dataset. A dataset pipeline bridges that gap. A dataset pipeline has a source (which logs to read), a transform (how to turn each into a dataset row), and a target (which dataset, and optionally project, to write to). Fill in [`evals/dataset_pipeline.py`](../../evals/dataset_pipeline.py) so it filters for the same email-drafting traces and writes them to `email-drafting`. Here, however, we want to transform the span before adding it to our dataset. In our input we just want to preserve the user prompt. In the metadata, save the drafted email in the log to `metadata.original_reference`.  

   See the
   [dataset pipelines docs](https://www.braintrust.dev/docs/annotate/datasets/pipelines).

## Solution

See [01-curating-datasets.solution.md](01-curating-datasets.solution.md).
