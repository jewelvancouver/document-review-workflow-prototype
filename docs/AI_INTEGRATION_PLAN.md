# Next step: connect an approved AI provider

The current demo deliberately uses explicit labelled-field rules so it runs offline, costs nothing, and has predictable tests. It is not an LLM integration and must not be described as one.

When the internship supervisor or an authorised adult provides an approved AI provider and credentials:

1. Keep the current `extract_fields` contract: it returns `dict[str, FieldValue]`.
2. Add an AI-backed extractor in a separate module. Do not remove the offline extractor.
3. Send only permitted fictional or approved test text to the provider.
4. Use the JSON schema in `schemas/extraction.schema.json` where the provider supports constrained structured output.
5. Validate every model response locally. A schema-valid answer may still be factually wrong.
6. Keep document contents out of logs. Keep API credentials outside source control.
7. Add tests for timeout, refusal, malformed response, missing fields and prompt-injection-like text.
8. Compare the AI mode with the offline demo using the same test documents.

Do not create a paid API account, bypass age restrictions, or upload private/company documents without explicit authorisation. For this application deadline, demonstrate the offline workflow honestly and describe AI API integration as a next step, not completed work.
