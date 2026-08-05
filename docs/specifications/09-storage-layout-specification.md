# 09. Storage Layout 공통 명세

> 상태: [제안]
> 공식 문서 언어: 한국어

## 1. 목적

코드, Dataset, 보존 Artifact와 재생성 가능한 임시 파일의 lifecycle을 분리합니다. 아래 이름은 논리 Root이며 실제 drive와 mount 위치는 환경별 설정으로 주입합니다.

## 2. 공식 루트

```text
DohaProjects/
├── DohaMusic/
├── DohaLM/
├── DohaAudio/
├── DohaVocal/
└── .github/

DohaData/
├── lm/
├── audio/
└── vocal/

DohaArtifacts/
├── lm/
├── audio/
├── vocal/
└── music/

DohaTemp/
├── lm/
├── audio/
├── vocal/
└── music/
```

## 3. 루트 책임

| Root | 책임 | Git 포함 |
|---|---|---|
| `DohaProjects` | Repository 코드, 문서, Schema, 설정 예제와 test | 허용 |
| `DohaData` | 원본·전처리 Dataset, Manifest record, split와 private Metadata | 금지 |
| `DohaArtifacts` | Model, Checkpoint, 생성 결과, 평가, Mix와 Export | 금지 |
| `DohaTemp` | Cache, 임시 출력, chunk, test output와 venv | 금지 |

## 4. Dataset 구조

도메인별 `DohaData/{domain}`은 필요에 따라 다음 lifecycle을 사용합니다.

```text
raw/
interim/
processed/
rejected/
manifests/
splits/
registry/
reviews/
licenses/
consent/
private/
```

도메인에 필요하지 않은 폴더를 억지로 생성하지 않습니다. 실제 구조는 Dataset Manifest와 Repository Data 정책을 따릅니다.

## 5. Artifact 구조

| 경로 | 역할 |
|---|---|
| `DohaArtifacts/lm` | LLM model, adapter, evaluation, run과 Runtime 결과 |
| `DohaArtifacts/audio` | Music generation, stem, audio model, evaluation과 run |
| `DohaArtifacts/vocal` | Vocal generation·conversion·correction, adapter, evaluation과 run |
| `DohaArtifacts/music` | Workspace Mix, Export, Preview, Snapshot과 Job run |

`DohaArtifacts/music` 권장 구조는 다음과 같습니다.

```text
music/
├── mixes/
├── exports/
├── previews/
├── snapshots/
└── runs/
```

Provider Runtime 결과를 `music`에 저장하지 않고 각 Provider domain에 저장합니다. Mix·Export·Preview·Composition Snapshot은 DohaMusic 책임입니다.

## 6. 임시 파일 원칙

- 유일한 원본과 최종 Artifact를 Temp에 저장하지 않습니다.
- Temp 파일은 Job·Run ID로 격리하고 재생성 가능해야 합니다.
- 실패·취소·만료 후 정리 정책을 둡니다.
- Cache 삭제가 Dataset, Model Registry 또는 Artifact lineage를 깨뜨리지 않아야 합니다.

## 7. 경로 주입

코드, DB, 공개 Manifest와 API 응답에 `D:/...` 같은 절대 경로를 하드코딩하지 않습니다. `DOHA_DATA_ROOT`, `DOHA_ARTIFACT_ROOT`, `DOHA_TEMP_ROOT` 및 domain별 환경 설정으로 주입하고 외부 계약은 Artifact ID·URI를 사용합니다.

## 8. 보안

Dataset, AIHub package, 개인 음성, Checkpoint, 생성 미디어, Consent 증적과 Private Metadata를 Public Git에 포함하지 않습니다. 접근 권한과 삭제 정책은 domain과 Owner 요구에 따라 별도로 적용합니다.

## 관련 명세

- [Artifact 명세](03-artifact-specification.md)
- [Dataset Manifest 명세](07-dataset-manifest-specification.md)
- [공통 용어](10-common-terms.md)
