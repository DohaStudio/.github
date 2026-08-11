# FeatureRecord Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`FeatureRecord`는 음악·오디오·보컬 분석 결과를 versioned feature로 표현합니다. 분석기와 단위가 다른 값을 같은 feature로 비교하지 않습니다.

## 2. 공통 필드

| 필드 | 의미 |
|---|---|
| `feature_record_id` | immutable ID |
| `source_fingerprint` | 원본을 노출하지 않는 source identity |
| `feature_schema_version` | feature bundle version |
| `extractor_manifest_ids` | 분석기·model·config identity |
| `time_base` | seconds/beats/frames와 resolution |
| `features` | typed feature map |
| `section_metadata` | section ID·label·time range·confidence |
| `confidence` | 전체 및 feature별 신뢰도 |
| `rights_metadata_id` | feature 사용·보관 범위 |
| `content_fingerprint` | canonical feature payload checksum |

`schema_name`은 `feature_record`입니다.

## 3. Feature 종류

| Key | 값의 최소 의미 |
|---|---|
| `bpm` | tempo 값·변화·confidence |
| `key` | tonic·mode·tuning·confidence |
| `meter` | numerator·denominator·change positions |
| `structure` | section label과 구간 |
| `chord` | time-aligned chord symbols와 vocabulary version |
| `arrangement` | layer/role timeline |
| `instrument` | instrument taxonomy와 구간별 confidence |
| `energy` | 정규화된 curve와 window |
| `rhythm` | onset/duration/density representation |
| `groove` | swing·syncopation 등 descriptor |
| `melody_feature` | contour·range·interval statistics |
| `vocal_melody_feature` | vocal contour·range·phrase statistics |
| `embedding` | model ID·dimension·normalization·vector reference |
| `mix_feature` | loudness·spectral·stereo width·dynamics와 단위 |

## 4. 불변 조건

- 모든 수치는 단위, time base와 extractor version을 가져야 합니다.
- embedding은 model/revision/dimension이 같을 때만 직접 비교합니다.
- vocal/melody feature는 원본 음성을 복원하는 payload를 포함하지 않습니다.
- feature payload 변경은 새 FeatureRecord를 발급합니다.
- 원본 Reference Audio의 training 금지는 FeatureRecord의 training 허용과 별도 판정합니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 음악 공통 feature taxonomy와 version·unit·confidence 계약 정의 |
