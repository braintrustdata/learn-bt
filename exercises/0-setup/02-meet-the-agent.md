# 0.2 Meet the agent and your assignment

You are the developer responsible for a Sales Assistant being piloted by account
executives (AEs). It looks up accounts and opportunities, searches a knowledge
base, drafts customer emails, and updates CRM records. AEs sometimes forward a
customer message as a PDF or screenshot.

The team can read the assistant's replies, but cannot see how it reached them.
Did it retrieve the right account? Did it use the customer attachment? Does the
actual email draft match what the assistant says it produced? You need visibility
before you can identify recurring problems or measure improvements.

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

Read the responses, then enter `/exit`. Write down one question about the
assistant's behavior that the final reply alone cannot answer. Keep these
requests to try again after instrumentation.

The fixtures stand in for a CRM and internal documents. Email drafts and CRM
writes are mocked, so this course does not send email or change real records.

## Your assignment

1. **Instrument:** capture model calls, tools, conversation context, and
   attachments. Build a view an account-team reviewer can use to inspect drafts.
2. **Observe:** simulate production traffic, understand usage, and investigate
   recurring failures. Focus the investigation on customer email drafting.
3. **Evaluate:** preserve proven failures in one regression dataset, define good
   behavior, measure a baseline, and compare improvements. Expose configuration
   so domain experts can participate in the same process.

You begin as the developer. During human review and playground iteration, you
also take the role of an account-team expert who knows whether a draft is usable.
Tracing provides the execution evidence needed to answer those questions.
