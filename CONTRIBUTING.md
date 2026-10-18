# Contributing to `meitei-lang`

Thank you for your interest in contributing to the Meitei Language Python library! We welcome contributions from linguists, native speakers, NLP researchers, and software developers.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/meitei-lang.git
   cd meitei-lang
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install the package in editable mode with development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run the test suite:**
   ```bash
   pytest tests/
   ```

## Adding Vocabulary Entries

When proposing additions to `src/meitei_lang/data/vocabulary.json`:
- Words must be written in canonical **Meitei Mayek** (Unicode `U+ABC0`–`U+ABFF`).
- Provide an accurate Roman transliteration.
- Include a clear English definition (`meaning_en`).
- Categorize using one of the established thematic categories (`actions`, `animals`, `body`, `clothing`, `culture`, `family`, `food`, `nature`, `society`, etc.).
- Cite a verifiable linguistic source (e.g., Directorate of Language Planning, standard dictionaries).

## Rebuilding Datasets

If you modify base lexical lists or literary texts in `scripts/`:
```bash
python scripts/build_datasets.py
```
This will rebuild `vocabulary.json`, `books.json`, `songs.json`, and update `src/meitei_lang/data/README.md`.

## Submitting Pull Requests

1. Create a feature branch: `git checkout -b feature/your-feature-name`.
2. Ensure all tests pass: `pytest tests/`.
3. Ensure no lint/type errors exist.
4. Commit your changes with informative messages.
5. Open a Pull Request on GitHub.
