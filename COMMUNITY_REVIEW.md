# Community Review, Provenance Audit & Verification Guidelines

**Meitei Language Library (`meitei`)**  
*Rigorous, evidence-backed linguistic and cultural data curation.*

---

## 1. Principles of Verification & Review Pedigree

The Meitei Language Library strictly adheres to an **offline-first, evidence-backed methodology**. No synthetic, hallucinated, or ungrounded Meitei words, translations, grammatical rules, or literary passages may ever enter the authoritative dataset.

A foundational principle is the **absolute separation** between:
1. **Historical Source Attestation (`SOURCE_ATTESTED`):**
   Textual evidence documented in primary historical literature, ancient *Puyas* (e.g. *Numit Kappa*, *Poireiton Khunthok*), royal chronicles (*Cheitharol Kumbaba*), or peer-reviewed historical grammars and dictionaries. These must cite an exact source ID (`MEI-SRC-xxxxxx`) and precise citation locator (e.g., page, folio, line).
2. **Contemporary Community Verification (`VERIFIED`):**
   Direct verification by living native speakers and cultural elders of Manipur, reflecting contemporary standardized orthography (State Board of Secondary Education Manipur / Directorate of Language Planning).

```
+-------------------------------------------------------------------------+
|                         LEXICAL PROVENANCE LEDGER                       |
+-------------------------------------------------------------------------+
                  |                                     |
                  v                                     v
   +------------------------------+     +-------------------------------+
   | Historical Source Attestation|     | Contemporary Living Speaker   |
   | (Puyas, Chronicles, Grammars)|     | Verification (Native Speakers)|
   | - Exact folio / page locator |     | - Modern Imphal standard /    |
   | - Preserves archaic forms    |     |   dialectal attestation       |
   | - Source ID mandatory        |     | - Ethical consent recorded    |
   +------------------------------+     +-------------------------------+
                  \                                     /
                   \                                   /
                    v                                 v
   +---------------------------------------------------------------------+
   |                      Editorial Review Ledger                        |
   |                   (data/reviews/reviews.jsonl)                      |
   |  - Review decisions: ACCEPTED | CORRECTED | REJECTED | AWAITING     |
   |  - Roles: NATIVE_SPEAKER | LINGUIST | CULTURAL_AUTHORITY | ELDER    |
   |  - Diff tracking: previous_value vs. corrected_value                |
   |  - Full revision history and citation verification                  |
   +---------------------------------------------------------------------+
```

---

## 2. Review Decisions & Lifecycle

Every review record is registered with a stable identifier (`MEI-REV-xxxxxxx`) in `data/reviews/reviews.jsonl`.

| Decision | State Code | Definition and Criteria |
| :--- | :--- | :--- |
| **Accepted** | `ACCEPTED` | The entry or reading is corroborated by verified primary source citation or by native speaker consensus. Eligible for promotion to `core_lexicon.jsonl`. |
| **Corrected** | `CORRECTED` | Errors in orthography (e.g. Mayek Lonsum Iyek vs. Onset, vowel mark placement), translation gloss, or citation metadata have been corrected. Requires documented `previous_value`, `corrected_value`, and revision diff. |
| **Rejected** | `REJECTED` | Proposed entry is spurious, ungrounded, an AI hallucination, or lacks linguistic corroboration. Kept recorded in the audit trail to prevent re-ingestion. |
| **Awaiting Review** | `AWAITING_REVIEW` | Provisional candidate ingested from fieldwork or textual scan. **Strictly quarantined** in `candidate_lexicon.jsonl`. |

---

## 3. Reviewer Roles & Attribution

Reviewers must state their perspective and qualification role:

- `NATIVE_SPEAKER`: First-language speaker of Meiteilon (Manipuri), verifying vernacular usage and living phonology.
- `LINGUIST`: Professional or academic linguist verifying phonology, morphology, syntax, glossing (Leipzig Glossing Rules), or IPA.
- `CULTURAL_AUTHORITY`: Recognized custodian of Meitei traditional heritage, Puyas, or Sanamahi theological literature.
- `COMMUNITY_ELDER`: Elder informant sharing traditional oral heritage, dialectal variants, or historical idioms.
- `ACADEMIC_EDITOR`: Editorial member maintaining corpus integrity, archival citations, and schema compliance.
- `CONTRIBUTOR`: General community contributor submitting field observations or bug reports for editorial review.

---

## 4. Prohibition on Automatic AI Promotion

> [!CAUTION]
> **Strict Prohibition Against Automatic AI Promotion:**
> Computational language models, machine translation outputs, and algorithmic extraction tools may **NEVER** automatically promote an entry from `candidate_lexicon.jsonl` into `core_lexicon.jsonl`.
> Any entry proposed by an AI model must be tagged with status `AI_CANDIDATE` and remain quarantined until an authenticated human reviewer performs a physical check against authoritative sources and native speaker intuition.

---

## 5. Cultural Sensitivity, Consent & Data Reuse

1. **Sacred and Ritual Texts (*Puyas*):**
   Ancient Meitei Puyas and Sanamahi cosmological texts carry deep religious, ritual, and cultural significance for the Meitei community. Reviewers must handle sacred terms with dignity, consulting cultural authorities where customary restrictions apply.
2. **Free, Prior, and Informed Consent (FPIC):**
   All contemporary fieldwork, elder recordings, and informant contributions must have documented, verifiable consent (`consent_confirmed: true`).
3. **Attribution and Open Knowledge:**
   Reviewers and contributors receive permanent attribution in the provenance ledger (`reviewer_attribution`).
4. **Data Reuse & Licensing:**
   All reviews, data records, and translations are released under the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](DATA-LICENSE.md) license. Software logic is licensed under the [MIT License](LICENSE).

---

## 6. Review Submission Workflow

1. **Locate Target Record:** Identify the target ID (e.g. `MEI-LEX-0000011`, `MEI-VAR-0000001`, `MEI-GLS-0000001`, or passage `khamba_thoibi-c01-p001`).
2. **Prepare Review Record:** Use the template in `templates/review_template.md`.
3. **Verify Evidence:** Inspect primary sources or record native speaker consultation notes.
4. **Submit via Pull Request or CLI:**
   ```bash
   # Validate review ledger
   meitei review audit
   
   # Run dataset validation
   meitei validate --strict
   ```

---

## 7. Review Record Template

Use this format when filing review issues or PR submissions:

```markdown
### Review Record Submission

- **Review ID:** `MEI-REV-000000X` (Assigned by editor)
- **Target ID:** `MEI-LEX-0000011`
- **Target Type:** `candidate_entry` (lexical_entry | candidate_entry | variant | gloss | grammar_record | book_passage)
- **Review Decision:** `ACCEPTED` (ACCEPTED | CORRECTED | REJECTED | AWAITING_REVIEW)
- **Reviewer Role:** `NATIVE_SPEAKER` (NATIVE_SPEAKER | LINGUIST | CULTURAL_AUTHORITY | COMMUNITY_ELDER | ACADEMIC_EDITOR)
- **Reviewer ID:** `REV-YOURNAME-01`
- **Review Date:** `2026-10-29`
- **Source ID:** `MEI-SRC-000004` (Optional if living vernacular verification)
- **Source Locator:** `Page 253, Entry 12` (Exact page, folio, or verse)

#### Previous Value (if applicable)
```json
{
  "status": "UNVERIFIED",
  "citation_locator": null
}
```

#### Corrected Value (if decision is CORRECTED)
```json
{
  "headword_meitei": "...",
  "citation_locator": "Page 253"
}
```

#### Revision History
- `2026-10-29` - `REV-YOURNAME-01`: Initial editorial review and source corroboration.

#### Linguistic & Cultural Rationale
[Provide detailed explanation of the word, its meaning, historical or contemporary context, and citations]

#### Ethical Compliance
- [x] Cultural sensitivity guidelines respected (`cultural_sensitivity_checked: true`)
- [x] Free, prior, and informed consent confirmed (`consent_confirmed: true`)
- [x] Contributed under CC BY-SA 4.0 license (`license: "CC BY-SA 4.0"`)
```

