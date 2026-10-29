# Meitei Language Library - Community Review Record Template

Use this template to propose an editorial decision (acceptance, correction, rejection, or update) on any lexical entry, candidate, spelling variant, translation gloss, grammar record, or literary book passage.

---

```json
{
  "id": "MEI-REV-0000000",
  "target_id": "MEI-LEX-0000001",
  "target_type": "lexical_entry",
  "decision": "ACCEPTED",
  "reviewer_role": "NATIVE_SPEAKER",
  "reviewer_id": "REV-CONTRIBUTOR-01",
  "review_date": "2026-10-29",
  "source_id": "MEI-SRC-000004",
  "source_locator": "Page 253, Entry 12",
  "previous_value": null,
  "corrected_value": null,
  "revision_history": [
    {
      "date": "2026-10-29",
      "reviewer_id": "REV-CONTRIBUTOR-01",
      "comment": "Initial review and physical verification against primary text."
    }
  ],
  "rationale": "Verified headword orthography and semantic definition against primary source and native speaker usage.",
  "cultural_sensitivity_checked": true,
  "consent_confirmed": true,
  "license": "CC BY-SA 4.0"
}
```

---

## Instructions for Reviewers:

1. **Target ID**: Must reference a valid repository ID (`MEI-LEX-...`, `MEI-VAR-...`, `MEI-GLS-...`, `MEI-GRM-...`, or book passage ID `{book_id}-c{ch}-p{psg}`).
2. **Decision**:
   - `ACCEPTED`: Promotes or affirms the record based on primary evidence.
   - `CORRECTED`: Fixes errors in orthography, meaning, or citations (supply `corrected_value` and `previous_value`).
   - `REJECTED`: Formally discards ungrounded, spurious, or AI-hallucinated submissions.
   - `AWAITING_REVIEW`: Marks item as needing further field inspection or archival research.
3. **Reviewer Role**: State role accurately (`NATIVE_SPEAKER`, `LINGUIST`, `CULTURAL_AUTHORITY`, `COMMUNITY_ELDER`, `ACADEMIC_EDITOR`, `CONTRIBUTOR`).
4. **Citations**: Never invent page numbers or folio references. If you did not physically inspect the page, leave `source_locator` as `null` and status as unverified.
5. **Cultural Sensitivity & Consent**: Confirm that no sacred traditions are violated and that community informant consent was obtained.

