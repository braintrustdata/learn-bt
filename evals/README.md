# Evals

Templates you complete during the evaluation exercises (sections 4 and 5). Each
file has a docstring and a `TODO`. The full reference implementation for each is
in the corresponding exercise's `.solution.md`.

| File | Exercise | What you build |
| --- | --- | --- |
| `dataset_pipeline.py` | 3-evals/01 | A dataset pipeline (source, transform, target). Run with `bt datasets pipeline run`. |
| `scorers.py` | 3-evals/02 | A code scorer and an LLM-judge scorer. Push with `bt functions push scorers.py`. |
| `eval_agent.py` | 3-evals/03 | An eval that runs the agent over a dataset and scores it: `bt eval evals/eval_agent.py`. |
| `parameters.py` | 4-human-review/03 | A saved parameters object built from the agent config. Push with `bt functions push parameters.py`. |
| `eval_remote_agent.py` | 4-human-review/03 | The remote eval server that loads the parameters and runs the agent: `bt eval evals/eval_remote_agent.py --dev`. |

All model calls route through the Braintrust gateway, so only `BRAINTRUST_API_KEY`
is required. The project name (`sales-assistant`) and dataset name
(`sales-assistant-eval`) are placeholders; change them to match what you create.

Push Python functions from inside this directory (`cd evals` first). Pushing with
a relative path is not supported for Python.
