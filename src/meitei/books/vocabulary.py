# -*- coding: utf-8 -*-
"""
Vocabulary Candidate Extraction and Quarantine Engine for Book Texts.

Extracts potential lexical candidates linked to exact passages while strictly
quarantining unreviewed vocabulary from the authoritative core dictionary.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from meitei.books.models import Passage, VocabularyCandidate
from meitei.books.reader import BookReader
from meitei.unicode_utils import is_meitei_mayek_char, normalize_text


def tokenize_meitei_words(text: str) -> List[str]:
    """
    Tokenize Meitei Mayek text into individual word tokens, stripping punctuation.
    """
    # Remove punctuation: Cheikhei (꯫), Apun Iyek (꯭), commas, periods, quotes
    cleaned = re.sub(r"[꯫,\.?!\"';:()\[\]{}—\-]+", " ", text)
    tokens = [t.strip() for t in cleaned.split() if t.strip()]
    # Filter tokens that contain Meitei Mayek characters
    meitei_tokens = [
        t for t in tokens
        if any(is_meitei_mayek_char(c) for c in t) and len(t) >= 2
    ]
    return meitei_tokens


class VocabularyExtractor:
    """
    Extracts vocabulary candidates and ensures strict isolation from the core lexicon.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = Path(data_dir)
        self.candidates_dir = self.data_dir / "books" / "candidates"
        self.candidates_dir.mkdir(parents=True, exist_ok=True)
        self.reader = BookReader(data_dir=self.data_dir)

    def extract_passage_candidates(self, passage: Passage) -> List[VocabularyCandidate]:
        """
        Extract vocabulary candidate tokens from a single passage.
        """
        tokens = tokenize_meitei_words(passage.text)
        now_iso = datetime.now(timezone.utc).isoformat()
        candidates: List[VocabularyCandidate] = []

        seen: Set[str] = set()
        for idx, token in enumerate(tokens, start=1):
            if token in seen:
                continue
            seen.add(token)

            cand_id = f"MEI-CAN-{passage.book_id[:3].upper()}-{passage.chapter_number:02d}-{idx:04d}"
            candidates.append(
                VocabularyCandidate(
                    candidate_id=cand_id,
                    lemma=token,
                    lemma_roman="",
                    book_id=passage.book_id,
                    chapter_number=passage.chapter_number,
                    passage_id=passage.passage_id,
                    context_passage=passage.text,
                    frequency=tokens.count(token),
                    status="UNVERIFIED",
                    extracted_at=now_iso,
                )
            )

        return candidates

    def extract_book_candidates(self, book_id: str) -> List[VocabularyCandidate]:
        """
        Extract all vocabulary candidates from an imported book and save to quarantine ledger.
        """
        chapters = self.reader.get_chapters(book_id)
        token_occurrences: Dict[str, List[Tuple[int, str, str]]] = {}

        for ch in chapters:
            for p in ch.passages:
                tokens = tokenize_meitei_words(p.text)
                for t in tokens:
                    token_occurrences.setdefault(t, []).append(
                        (ch.chapter_number, p.passage_id, p.text)
                    )

        now_iso = datetime.now(timezone.utc).isoformat()
        candidates: List[VocabularyCandidate] = []

        for idx, (lemma, occurrences) in enumerate(sorted(token_occurrences.items()), start=1):
            first_ch, first_psg, context = occurrences[0]
            cand_id = f"MEI-CAN-{book_id[:3].upper()}-{idx:05d}"
            candidates.append(
                VocabularyCandidate(
                    candidate_id=cand_id,
                    lemma=lemma,
                    lemma_roman="",
                    book_id=book_id,
                    chapter_number=first_ch,
                    passage_id=first_psg,
                    context_passage=context,
                    frequency=len(occurrences),
                    status="UNVERIFIED",
                    extracted_at=now_iso,
                )
            )

        # Save to candidate quarantine storage (strictly isolated from core_lexicon.jsonl)
        dest = self.candidates_dir / f"{book_id}_candidates.jsonl"
        with open(dest, "w", encoding="utf-8") as f:
            for c in candidates:
                f.write(json.dumps(c.to_dict(), ensure_ascii=False) + "\n")

        return candidates

    def get_candidates(self, book_id: Optional[str] = None) -> List[VocabularyCandidate]:
        """
        Retrieve extracted candidate vocabulary from the quarantine ledger.
        """
        candidates: List[VocabularyCandidate] = []
        files = [self.candidates_dir / f"{book_id}_candidates.jsonl"] if book_id else self.candidates_dir.glob("*_candidates.jsonl")

        for f_path in files:
            if not f_path.exists():
                continue
            with open(f_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        candidates.append(VocabularyCandidate.from_dict(data))
                    except Exception:
                        continue

        return candidates

