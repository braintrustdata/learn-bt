# Solution: Create a custom view

Example prompt for creating a custom view:

```
Create a custom view that shows me the execution diagram of the agent with the input prompt, the steps followed / tools executed by the agent, and the final answer. I want to also be able to provide thumbs up/down feedback on the trace w/ my thoughts, and that should be written to the metadata field on the root span. This should be an array metdata.feedback, so that multiple people can provide feedback.
```

Loop will generate the view and ask you to confirm the changes.

Once confirmed, the view can be saved.

Test that the new view works by providing feedback on a trace, and verifying that it is written back to the root span metadata. Iterations on the view can be saved as new versions.