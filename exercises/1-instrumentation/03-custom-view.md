# 1.3 Create a custom view [UI]

Trace views contain the technical details developers need for debugging. Those
details can make it harder for PMs and subject matter experts (SMEs) to inspect
the part of a trace relevant to their review.

Custom views present trace data in a UI built for a specific workflow. In this
exercise, create a customer-email review view that an account-team expert can
use to confirm recipient failures and assess writing quality.

## Step 1: Open a trace with a drafted email

Select a trace that contains a `draft_email` span, then open the **Views** tab.
Starting from a representative trace gives Loop the data it needs to build and
preview the view.

## Step 2: Ask Loop to create the view

Enter into the prompt window:

~~~text
Create a custom view named Customer email review. Show it only when the trace
contains a draft_email tool span. Show the current request from the chat_turn
root, its conversation history, and previewable root input attachments when
present. Render each draft_email output as an email with recipient, subject,
and body. Show the CRM primary-contact name and email from lookup_customer next
to the draft so a reviewer can check the recipient. Clearly mark missing CRM
evidence. Use tool outputs for the draft, not the final assistant reply.
Include thumbs up/down feedback that writes to the draft_email span metadata.
Keep this quick feedback separate from the written human-review form used for written assessments.
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
