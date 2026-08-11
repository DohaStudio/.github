# AI Music Common Contracts Architecture

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. Ecosystem Architecture

```mermaid
flowchart TB
    U[User] --> DM[DohaMusic<br/>작업·Project·승인·Orchestration]
    DM --> LC[LearningCandidate]
    LC --> TE[TrainingEligibility]
    TE --> DV[Approved & Frozen DatasetVersion]
    DV --> LM[DohaLM Training/Evaluation Lineage]
    LM --> MI[MusicIntent]
    MI --> DM
    DM --> DA[DohaAudio Capability]
    DM --> VO[DohaVocal Capability]
    DA --> FR[FeatureRecord]
    VO --> FR
    FR --> SR[SimilarityReport]
    SR --> LM
    LM --> RP[RevisionPlan]
    RP --> DM
    DM -->|사용자 승인·수정 결과| LC
```

이 순환은 자동 학습 loop가 아닙니다. `LearningCandidate → TrainingEligibility → DatasetVersion`의 명시적 검토가 매 회전마다 필요합니다.

## 2. Intent 실행 흐름

```mermaid
sequenceDiagram
    participant U as User
    participant M as DohaMusic
    participant L as DohaLM
    participant P as DohaAudio/DohaVocal
    U->>M: 작업 요청
    M->>L: Project context + capability
    L-->>M: MusicIntent / RevisionPlan
    M->>U: 계획 확인·승인
    U-->>M: 승인
    M->>P: MusicIntent
    P-->>M: 새 Artifact/AssetVersion + FeatureRecord
    M->>L: 결과 context / SimilarityReport
    L-->>M: QA 또는 추가 RevisionPlan
```

## 3. Reference Analysis 흐름

```mermaid
flowchart LR
    R[Reference Audio] --> G[RightsMetadata<br/>analysis gate]
    G --> A[ReferenceAnalysis]
    A --> F[FeatureRecord]
    F --> C[DohaLM Context]
    C --> P[Planning]
    P --> X[Generation]
    X --> V[Revision]
```

원본은 접근 통제된 source 영역에 남으며 공통 객체에는 opaque reference와 fingerprint만 기록합니다.

## 4. Model Lineage

```mermaid
flowchart LR
    C[LearningCandidate] --> E[TrainingEligibility]
    E --> D[DatasetVersion]
    D --> T[TrainingRun]
    T --> V[EvaluationRun]
    V --> M[ModelVersion]
    M --> R[Provider Runtime]
```

`approved`, `training_allowed`, `evaluation approval`, `runtime_allowed`를 독립 Gate로 유지합니다.

## 5. Failure Boundary

- 권리·lineage·schema가 불완전하면 fail closed합니다.
- Provider 실패는 MusicIntent나 기존 AssetVersion을 성공 상태로 바꾸지 않습니다.
- Similarity metric version이 호환되지 않으면 score를 만들지 않습니다.
- 권리 철회는 후속 Dataset/Model 영향 분석을 시작하지만 evidence를 삭제해 계보를 끊지 않습니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 사용자 작업·학습·Intent·Similarity·Revision의 순환 architecture 정의 |
