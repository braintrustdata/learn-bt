# Solution: Human review scorer

1. Navigate to Human review, either via Settings -> Human review, or Logs page -> Review -> Manage scores and create a new human review scorer.
2.  Enter a name and description (e.g. "email-quality")
3.  Score type: free-form text input
4.  Set the metadata path to `review`
5.  Expand the Score visibility section and add a span filter `span_attributes.name = "draft_email"`
6.  Save this scorer. Test it via Review in the Logs page by assigning a `draft_email` span to yourself, and navigating to the Review tab.