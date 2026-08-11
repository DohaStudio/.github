# Common AI Contract Schema v1

This package is the machine-checkable ORG-02 implementation of the Common AI
Contracts. It validates contract documents and synthetic cross-object lineage;
it does not implement a Runtime, API, database, Dataset pipeline, Provider, or
external resource lookup.

## Package contents

- `v1/common-envelope.schema.json`: shared identity, audit, producer, and
  namespaced extension fields.
- `v1/*.schema.json`: Draft 2020-12 schemas for MusicIntent,
  ProviderCapability, RightsMetadata, TrainingEligibility, LearningCandidate,
  DatasetVersion, DatasetManifest, TrainingRun, EvaluationRun, ModelVersion,
  and ModelManifest.
- `v1/version-policy.json`: supported major/minor/patch and unknown-field policy.
- `tools/validate_common_ai.py`: deterministic schema and cross-object validator.
- `tests/fixtures/common-ai/v1`: synthetic valid, invalid, promotion, and
  immutable replacement examples.

The schema `$id` values are stable identifiers. They do not authorize a network
fetch and are not production endpoints; the validator resolves every `$ref`
from the local registry.

## Version axes

`schema_version: 1.x.y` is the version of a serialized object. The current
organizational specification label (`0.2.0-draft`) describes the governing
documentation and is a separate version axis. A consumer must not substitute
one for the other.

Major version `1` is supported. Patch changes are compatible. A later `1.x`
minor object is accepted only when new data is carried in a namespaced
`extensions` member; unknown core fields and enum members fail validation.
Unknown majors fail closed. See `v1/version-policy.json` for the executable
policy.

## Validation

Install the isolated validation dependency, then run:

```text
python -m pip install -r requirements-validation.txt
python tools/validate_common_ai.py --check-registry
python tools/validate_common_ai.py --scenario tests/fixtures/common-ai/v1/scenarios/runtime-promotion.json
python -m unittest discover -s tests -p "test*.py" -v
```

`jsonschema` is the only added validation dependency. It is bounded to the
maintained `4.x` major line in `requirements-validation.txt`, is MIT-licensed,
and is not connected to application Runtime code. A future major upgrade needs
an explicit compatibility review; this repository does not currently maintain
a lockfile or an application dependency manifest.

Validation errors contain a stable code, object kind and opaque ID, JSON path,
rule, and sanitized message. They do not include local absolute paths, stack
traces, credentials, raw Provider responses, or artifact payloads.
Malformed JSON, invalid UTF-8, and unreadable input files use the same sanitized
JSON error envelope and return a non-zero exit code.

## Enforced invariants

- issued manifests cannot be edited in place; replacement uses a new identity
  and `supersedes` lineage;
- DatasetVersion eligibility is aggregated from each candidate's current,
  purpose-matched TrainingEligibility and RightsMetadata;
- train, validation, and test members and group keys cannot leak across splits;
- content fingerprints cannot cross splits, and every included candidate must
  declare a group key;
- ModelVersion runtime promotion requires successful training lineage, an
  eligible DatasetVersion, completed and approved evaluation, issued manifest
  evidence, current runtime rights, declared ProviderCapability compatibility,
  and a non-deprecated approved model;
- TrainingEligibility cannot grant runtime authority, and
  ProviderCapability cannot expose endpoint, credential, token, or path data.
- MusicIntent must reference one available ProviderCapability that declares the
  requested operation and a compatible input schema major.
- issued Manifest replacements form one complete linear `supersedes` chain,
  and duplicate candidate-purpose TrainingEligibility decisions fail closed.

Dataset and Runtime scenarios require an explicit timezone-aware `evaluated_at`.
Every TrainingEligibility used by a Dataset gate requires a timezone-aware
`expires_at` later than that instant; missing, malformed, naive, and expired
eligibility evidence fails the entire Dataset and its Runtime promotion lineage.
Gated Rights require structured `retention_allowed` evidence with
`allowed=true`, a purpose-matched `training` or `runtime` scope, and a
timezone-aware `expires_at`; the legacy Boolean form never grants Dataset or
Runtime authority. If the expiry is earlier than or equal to `evaluated_at`, the
Rights check fails closed; a later expiry remains subject to every other Rights
and purpose constraint.

Manifest checks validate declared identity and synthetic integrity evidence.
This package does not read artifact bytes, contact schema IDs, inspect a model
registry, or prove that an external checksum matches production storage.
