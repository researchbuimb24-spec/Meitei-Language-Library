# Data Licensing and Provenance Statement

**Project:** Meitei Language Library (`meitei`)  
**Scope:** Lexical datasets, bibliographic citations, historical manuscript excerpts, and linguistic fieldwork records.

---

## 1. Separation of Software and Data Licenses

The Meitei Language Library explicitly distinguishes between software source code and linguistic data:

- **Software Code:** All Python scripts, modules, command-line interfaces, database schemas, and unit tests are licensed under the **MIT License** (see [`LICENSE`](LICENSE)).
- **Linguistic and Cultural Data:** Lexical databases, definitions, morphological analyses, example sentences, and bibliographic compilations are licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**, except where underlying historical texts reside in the Public Domain.

---

## 2. Core Methodological Principles: Attestation vs. Verification

To ensure academic rigor, linguistic integrity, and cultural respect for the Meitei language (*Meiteilon* / Manipuri), every lexical and textual item in this project is cataloged under a strict provenance model distinguishing **historical source attestation** from **contemporary native-speaker verification**.

```
                           +---------------------------------------+
                           |          Lexical Record / Entry       |
                           +---------------------------------------+
                                              |
                   +--------------------------+--------------------------+
                   |                                                     |
                   v                                                     v
   +-------------------------------+                     +-------------------------------+
   | Historical Source Attestation |                     | Contemporary Native-Speaker   |
   |                               |                     | Verification                  |
   | - Archaic Puyas (e.g. Numit   |                     | - Modern spoken Meiteilon     |
   |   Kappa, Poireiton Khunthok)  |                     |   (Imphal Valley standard)    |
   | - Royal Chronicles (Cheitharol|                     | - Current school/university   |
   |   Kumbaba)                    |                     |   curricula & official bodies |
   | - Classical manuscripts       |                     | - Living native speaker       |
   | - Historical dictionaries     |                     |   consultants                 |
   +-------------------------------+                     +-------------------------------+
```

### A. Historical Source Attestation (`HISTORICAL_ATTESTED`)
- **Definition:** Words, senses, or syntactic structures attested in written historical records, including traditional scrolls (*Puyas*), royal chronicles (*Cheitharol Kumbaba*), folk ballads (*Moirang Sai*, *Khamba Thoibi*), or early colonial linguistic surveys (e.g., G.A. Grierson's *Linguistic Survey of India*).
- **Linguistic Character:** These records often reflect archaic Meitei morphology, classical phonological features, obsolete honorific or courtly registers, and spellings predating modern orthographic standardization.
- **Ethics & Rights:** Ancient manuscripts and traditional Puyas are part of the cultural heritage of the Meitei people. Public domain historical texts are represented with citations to the physical manuscript, archival repository, or scholarly critical edition.

### B. Contemporary Native-Speaker Verification (`CONTEMPORARY_VERIFIED`)
- **Definition:** Words, senses, and expressions actively used, recognized, and confirmed by living native speakers of Meiteilon in Manipur, adhering to modern orthography recognized by the Directorate of Language Planning and Implementation (Government of Manipur) and the Council of Higher Secondary Education Manipur (COHSEM).
- **Linguistic Character:** Represents modern colloquial and formal Manipuri as spoken in everyday family life, market transactions, education, media, and state administration.
- **Review Requirement:** Contemporary entries must record the date of verification and validator identifiers, ensuring accountability without publishing private personal data of informants.

### C. Joint Classification (`BOTH`)
- Entries that are attested in classical historical literature and continue to exist with consistent or evolved semantic vitality in the contemporary language.

### D. Disputed Status (`DISPUTED`)
- Entries where historical puya orthography diverges from contemporary phonetic spelling, or where dialectal variations (e.g., Sekmai, Andro, Kakching, Phayeng dialects vs. standard Imphal valley) present alternative lexical realizations.

---

## 3. Strict No-Fabrication Guarantee

In adherence to scientific ethics:
1. **No Synthetic Words:** The project shall never invent, hallucinate, or algorithmically fabricate Meitei lexical items, definitions, or etymological roots.
2. **No Fabricated Citations:** Every bibliographic citation and puya folio reference must correspond to an authentic documented source or critical edition.
3. **No Fabricated Statistics:** Dataset statistics, headword counts, and frequency metrics must reflect actual verified records in the repository.

---

## 4. Attribution and Contributions

When citing or redistributing linguistic data from this project:
- Provide attribution to the **Meitei Language Project Contributors** and reference the specific `source_id` and bibliographic citations recorded in the provenance metadata.
- If you contribute new entries, you agree to license them under CC BY-SA 4.0 and provide verifiable source citations or native-speaker verification metadata.

