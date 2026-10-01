# 1.4 Create a custom view [UI]

Trace views contain the technical details developers need for debugging. Those
details can make it harder for PMs and subject matter experts (SMEs) to inspect
the part of a trace relevant to their review.

Custom views present trace data in a UI built for a specific workflow. In this
exercise, you will create a view that makes a drafted email easy to inspect.

## Step 1: Open a trace with a drafted email

Select a trace that contains a `draft_email` span, then open the **Views** tab.
Starting from a representative trace gives Loop the data it needs to build and
preview the view.

## Step 2: Ask Loop to create the view

Enter into the prompt window:

~~~text
Create a custom view for reviewing drafted customer emails. Show the original
request and the output of the draft_email span as an email, with the email body, subject, and recipient. Only show this when there is an actual draft_email span in the trace. Provide a thumbs up/down feedback option that will can be used to provide feedback, which writes back to the draft_email span metadata.
~~~

Loop uses the current trace to identify the relevant fields and generate the
view. Review the preview and refine the prompt if any email fields are missing.

## Step 3: Save and test the view

Save the view, then open another trace that contains a `draft_email` span and
select the new view.

You should see the original request and drafted email in a focused layout,
without navigating the raw span tree.

You can edit a saved view to create a new version. When the view is ready for
the broader review workflow, publish it so everyone with access to the project
can use it.
