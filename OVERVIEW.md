## write_seqs - Repository Overview

### Purpose

**write_seqs** is a data processing pipeline that converts symbolic music datasets into sequence-based training data for machine learning models. It takes structured music representations (notes, chords, timing) in "music_df" format and outputs tokenized sequences suitable for training models like transformers, specifically designed for the fairseq framework.

### Pipeline Flow

```
Music Corpora (CSV/JSON) → Segmentation → Encoding → Augmentation → Train/Valid/Test Splits
```

1. **Input**: Parent directory containing corpus subdirectories, each with:
   - `attrs.json` - corpus metadata
   - Score files: `name.csv` (events with onset, release, type, pitch) + optional `name.json`

2. **Processing**: Scores are segmented into windows, encoded into token representations, and optionally augmented

3. **Output**: Chunked CSV files with sequences, plus vocabulary files for ML training

### Key Components

| Module | Role |
|--------|------|
| `write_seqs.py` | Core pipeline orchestration |
| `settings.py` | `SequenceDataSettings` dataclass with 20+ configurable parameters |
| `__main__.py` | CLI entry point with YAML + argument parsing |
| `augmentations.py` | Key transposition, rhythmic variation, range-based augmentation |
| `splits_utils.py` | Weighted file-size-based train/valid/test partitioning |

### Configuration System

Settings are loaded via OmegaConf from YAML files (40+ configs in `/configs/`) and can be overridden by CLI args. Key parameter groups:

- **Features**: which musical features to extract
- **Segmentation**: `window_len`, `hop` stride, `min_window_len`
- **Augmentation**: `aug_by_key` (12-key transposition), `aug_within_range`, `aug_rhythms`
- **Corpus filtering**: include/exclude lists, synthetic corpus handling
- **Representation**: `repr_type` ("oct" for Octuple encoding, "midilike" fallback)

### Processing Details

**CorpusItem**: Wraps individual scores, caches file size, and provides a deterministic hash (MD5 of path) for reproducible windowing offsets.

**Segmentation**: Window-based chunking of encoded sequences. Each segment records its source score, transposition, scaling, and original dataframe indices.

**Augmentation** (training split only):
- Transpose to all 12 keys
- Transpose within playable pitch range (MIDI 21-108)
- Rhythmic variation

**Output format**: Chunked CSVs (default 50k lines each) with columns for `score_id`, `events` (token sequence), features, and provenance metadata. Vocabularies saved as JSON + pickle.

### Multiprocessing Architecture

The pipeline uses a multiprocessing pool with:
- Shared file counter for chunk naming
- Locks for thread-safe CSV writing
- Scales to CPU count automatically

### External Dependencies

- `reprs` - Music representation encoding library (git dependency)
- `music_df` - Music dataframe utilities (git dependency)
- `pandas`, `omegaconf`, `dacite` for data handling and config

### Utility Scripts

- `to_fair_seq.py` - Convert output to fairseq format
- `save_splits.py` - Persist split information
- `output_census.py` - Analyze output statistics

### Design Principles

1. **Reproducibility**: Deterministic hashing ensures consistent results across runs
2. **Weighted partitioning**: Splits by cumulative file size, not item count
3. **Error resilience**: Logs encoding failures without stopping the pipeline
4. **Streaming**: Large datasets written in manageable chunks
