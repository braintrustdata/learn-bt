# 4.1 Create a custom view [UI]

Raw traces are useful for debugging, but reviewers often need a focused view of the decision they are making. Create a view for one reviewer and write that review back to the trace.

## Step 1: Pick one reviewer and decision

Choose a specific persona. For example:

~~~text
An account executive deciding whether a drafted customer email is ready to send.
~~~

The view should help that person make one decision. It does not need to show every field in the trace.

## Step 2: Ask Loop to create the view

Open a representative trace and select the **Views** tab. Open Loop and enter:

~~~text
Create a custom view for an account executive reviewing a drafted customer
email. Show the original request, the relevant tool steps, and the final
outcome. Add a thumbs-up or thumbs-down control and a comment field. Save each
review to metadata.feedback on the root span so multiple reviewers can add
feedback.
~~~

Review the proposed view before you save it. It should show the request, drafted email, and outcome without requiring the reviewer to navigate the raw span tree.

## Step 3: Test the write action

Open a trace with the new view. Submit a thumbs-up or thumbs-down and a short comment. Then inspect the root span metadata.

You should find the review at:

~~~text
metadata.feedback
~~~

If the write did not land on the root span, revise the view in Loop and test again. A useful custom view improves the path to a decision and reliably stores review evidence.
