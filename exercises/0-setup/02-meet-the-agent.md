# 0.2 Meet the agent and your assignment

You are the developer responsible for a Sales Assistant being piloted by account
executives (AEs). It looks up accounts and opportunities, searches a knowledge
base, drafts customer emails, and updates CRM records. AEs sometimes forward a
customer message as a PDF or screenshot.

The team can read the assistant's replies, but cannot see how it reached them.
Did it retrieve the right account? Did it use the customer attachment? Does the
actual email draft match what the assistant says it produced? You need visibility before you can identify recurring problems or measure improvements.

## Step 1: Try the assistant

With dependencies and credentials configured, start the app:

```bash
uv run python main.py
```

Enter these requests in the same conversation:

```text
Look up ACC-1001 and summarize what I should know before my next customer call.
Please draft a concise follow-up email to their CRM primary contact.
```

Read the responses, then enter `/exit`.

Don't worry, the email drafts and CRM writes are mocked, so this course does not send real emails or change real records.

## Your assignment

In this workshop, you're going to learn 3 main things:

1. **Instrument:** capture model calls, tools, conversation context, and
   attachments into your traces.
2. **Observe:** understand how to investigate
   recurring failures and patterns in production logs. We'll then focus the investigation on a specific issue: mismatched customer email drafting.
3. **Evaluate:** pull failure traces into a regression dataset, define good
   behavior, measure a baseline, and compare improvements.
