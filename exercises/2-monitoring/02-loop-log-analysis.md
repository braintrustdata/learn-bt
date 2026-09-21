# 2.2 Analyze logs with Loop [UI]

Loop is Braintrust's AI assistant for the data you are viewing. Use it to turn a collection of traces into an investigation you can verify.

## Step 1: Ask Loop to surface traces

Open **learn-bt**, then **Logs**. Keep a useful filter or search active if you want Loop to analyze a specific slice of traffic.

Open Loop and enter:

~~~text
Surface interesting logs for me to inspect.
~~~

Read the suggested traces. A suggestion is a starting point, not evidence by itself.

## Step 2: Ask for possible failure modes

In the same conversation, enter:

~~~text
Identify themes in the potential failure modes of the agent.
~~~

Loop should cite traces for each theme. Open at least one cited trace for every pattern you plan to use. Inspect the root request, tool calls, and final response yourself.

## Step 3: State one testable hypothesis

Turn one supported pattern into a statement an eval could test. For example:

~~~text
When a request asks for an email and a CRM update, the agent sometimes drafts
the email without making the requested update.
~~~

The next section turns supported production examples into a dataset. Loop narrows the search. Trace evidence tells you whether the pattern is real.

## Optional: Compare a CLI investigation

Give a coding agent the same question and ask it to inspect **learn-bt** with the CLI. Compare the cited evidence, not only the prose summary. Repeated investigations that reliably surface useful evidence can become reusable team skills.
