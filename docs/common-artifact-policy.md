# 공통 Artifact 정책

> 문서 상태: [제안]

```text
DohaArtifacts/
├── lm/       # LLM model, adapter, evaluation과 run
├── audio/    # Music generation, stem, audio model/evaluation과 run
├── vocal/    # Vocal generation/conversion/correction, adapter/evaluation과 run
└── music/    # Workspace mix, export, preview, snapshot과 run
```

Provider 결과와 DohaMusic Workspace 결과를 구분합니다. Artifact는 ID, version, kind, checksum, producer, Model Manifest, source/parent와 생성 시각을 기록하고 로컬 절대 경로를 외부 계약에 노출하지 않습니다.

유일한 원본이나 최종 결과를 `DohaTemp`에 보관하지 않으며 Dataset과 Artifact를 Git에 포함하지 않습니다.
