# -*- coding: utf-8 -*-
"""
Meitei Language Library (meitei)
================================

A lightweight, offline-first Python library for the Meitei (Manipuri / Meiteilon)
language of Manipur, India.

Core Design Principles:
- Zero runtime external dependencies: Built strictly with the Python standard library.
- Offline-first architecture: Streaming JSONL source files and fast SQLite indexing.
- Rigorous linguistic provenance: Explicit separation between historical source
  attestation (Puyas, royal chronicles) and contemporary native-speaker verification.
- Structured Data Layer: Strict JSON Schemas, stable IDs (MEI-LEX-xxxxxxx, MEI-SRC-xxxxxx),
  cross-referential integrity validation, and separate candidate quarantine.
- Unicode & Orthographic support: NFC normalization, script detection, rule-governed
  conversion, unambiguous error reporting, and registered spelling variants.
- Unified Dictionary Search: Full-text search across headwords, scripts, variants,
  multilingual glosses (English, Hindi, Assamese, Bengali), and FTS5 acceleration.
- Strict scientific integrity: No invented or fabricated words, citations, or statistics.
"""

from meitei.audit import (
    AuditReport,
    ProvenanceAuditor,
    audit_repository,
)
from meitei.books import (
    BookAuditResult,
    BookCatalog,
    BookCatalogRecord,
    BookImporter,
    BookNotFoundError,
    BookNotImportedError,
    BookReader,
    BookSearchEngine,
    BookSearchResult,
    BookValidator,
    Chapter,
    ChapterNotFoundError,
    ImportManifest,
    ImportStatus,
    Passage,
    RightsStatus,
    VocabularyCandidate,
    audit_books,
    get_book_info,
    get_book_stats,
    list_books,
    read_passages,
    search_passages,
)
from meitei.database import MeiteiDatabase
from meitei.grammar import (
    GrammarExample,
    GrammarRecord,
    GrammarTopic,
    GrammarValidationError,
    get_grammar_record_by_id,
    get_grammar_records,
    get_populated_topics,
    get_topic_sources,
    get_unpopulated_topics,
    list_grammar_sources,
    list_grammar_topics,
    load_grammar_records,
    validate_grammar_record,
)
from meitei.languages import (
    canonicalize_language_code,
    get_supported_codes_summary,
    get_supported_languages,
    is_supported_language,
)
from meitei.loader import (
    CitationLocatorMissingError,
    DataLoader,
    DatasetPartitionError,
    DuplicateIDError,
    InvalidStatusError,
    MalformedJSONLError,
    MissingSourceError,
    ValidationError,
)
from meitei.models import (
    BibliographicSource,
    Entry,
    ExampleSentence,
    PartOfSpeech,
    ProvenanceRecord,
    ScriptType,
    Sense,
    VerificationStatus,
)
from meitei.orthography import (
    AmbiguousConversionError,
    ConversionStatus,
    ScriptConversionResult,
    UnsupportedConversionError,
    convert_bengali_to_mayek,
    convert_mayek_to_bengali,
    convert_mayek_to_roman,
    convert_script,
    get_script_variants,
)
from meitei.review import (
    ReviewDecision,
    ReviewLedger,
    ReviewRecord,
    ReviewValidationError,
    ReviewerRole,
    get_review_statistics,
    get_reviews_for_target,
    load_reviews,
    validate_review_record,
)
from meitei.schema import (
    ALL_ALLOWED_STATUSES,
    CANDIDATE_ALLOWED_STATUSES,
    CORE_ALLOWED_STATUSES,
    GLOSS_SCHEMA,
    LEXICAL_ENTRY_SCHEMA,
    REVIEWER_ATTRIBUTION_SCHEMA,
    REVIEW_RECORD_SCHEMA,
    SENSE_SCHEMA,
    SOURCE_SCHEMA,
    VARIANT_SCHEMA,
    RecordStatus,
    is_valid_gls_id,
    is_valid_lex_id,
    is_valid_rev_id,
    is_valid_sns_id,
    is_valid_src_id,
    is_valid_var_id,
)
from meitei.search import (
    SearchEngine,
    SearchResult,
    batch_search,
    check_fts5_available,
    search,
)
from meitei.translate import (
    TranslationResult,
    translate,
)
from meitei.unicode_utils import (
    decompose_to_codepoints,
    detect_script,
    has_combining_marks,
    is_bengali_char,
    is_combining_mark,
    is_latin_char,
    is_meitei_mayek_char,
    normalize_text,
)

__version__ = "0.1.0"
__author__ = "Meitei Language Project Contributors"
__license__ = "MIT (Code) / CC BY-SA 4.0 (Data)"

__all__ = [
    # Core Models & Database
    "BibliographicSource",
    "Entry",
    "ExampleSentence",
    "MeiteiDatabase",
    "PartOfSpeech",
    "ProvenanceRecord",
    "ScriptType",
    "Sense",
    "VerificationStatus",
    # Structured Data Layer & Schemas
    "RecordStatus",
    "CORE_ALLOWED_STATUSES",
    "CANDIDATE_ALLOWED_STATUSES",
    "ALL_ALLOWED_STATUSES",
    "SOURCE_SCHEMA",
    "SENSE_SCHEMA",
    "LEXICAL_ENTRY_SCHEMA",
    "VARIANT_SCHEMA",
    "GLOSS_SCHEMA",
    "REVIEWER_ATTRIBUTION_SCHEMA",
    "is_valid_lex_id",
    "is_valid_src_id",
    "is_valid_sns_id",
    "is_valid_var_id",
    "is_valid_gls_id",
    # Loader & Validation Exceptions
    "DataLoader",
    "ValidationError",
    "MalformedJSONLError",
    "DuplicateIDError",
    "MissingSourceError",
    "InvalidStatusError",
    "CitationLocatorMissingError",
    "DatasetPartitionError",
    # Unicode & Orthography
    "normalize_text",
    "detect_script",
    "is_meitei_mayek_char",
    "is_bengali_char",
    "is_latin_char",
    "is_combining_mark",
    "has_combining_marks",
    "decompose_to_codepoints",
    "convert_script",
    "convert_mayek_to_bengali",
    "convert_mayek_to_roman",
    "convert_bengali_to_mayek",
    "get_script_variants",
    "ConversionStatus",
    "ScriptConversionResult",
    "UnsupportedConversionError",
    "AmbiguousConversionError",
    # Search Engine & Queries
    "search",
    "batch_search",
    "SearchResult",
    "SearchEngine",
    "check_fts5_available",
    # Translation & Glossing
    "translate",
    "TranslationResult",
    # Languages
    "get_supported_languages",
    "canonicalize_language_code",
    "is_supported_language",
    "get_supported_codes_summary",
    # Grammar Subsystem
    "GrammarRecord",
    "GrammarExample",
    "GrammarTopic",
    "GrammarValidationError",
    "load_grammar_records",
    "list_grammar_topics",
    "get_grammar_records",
    "get_grammar_record_by_id",
    "get_topic_sources",
    "list_grammar_sources",
    "get_populated_topics",
    "get_unpopulated_topics",
    "validate_grammar_record",
    # Digital Book Library Subsystem
    "BookCatalogRecord",
    "Chapter",
    "Passage",
    "ImportManifest",
    "VocabularyCandidate",
    "ImportStatus",
    "RightsStatus",
    "BookCatalog",
    "BookImporter",
    "BookReader",
    "BookSearchEngine",
    "BookSearchResult",
    "BookValidator",
    "BookAuditResult",
    "BookNotFoundError",
    "BookNotImportedError",
    "ChapterNotFoundError",
    "list_books",
    "get_book_info",
    "read_passages",
    "search_passages",
    "get_book_stats",
    "audit_books",
    # Community Review & Provenance Audit Subsystem
    "ReviewRecord",
    "ReviewDecision",
    "ReviewerRole",
    "ReviewValidationError",
    "ReviewLedger",
    "REVIEW_RECORD_SCHEMA",
    "is_valid_rev_id",
    "load_reviews",
    "get_reviews_for_target",
    "get_review_statistics",
    "validate_review_record",
    "ProvenanceAuditor",
    "AuditReport",
    "audit_repository",
    # Version
    "__version__",
]
