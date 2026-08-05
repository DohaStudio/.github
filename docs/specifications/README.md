# DohaStudio 공통 명세 기준선

> `specification_version`: `0.1.0`
> 상태: `draft-baseline`
> 적용일: 2026-08-06
> 구현 상태: 문서 기준선이며 Runtime·API·DB 구현 완료를 의미하지 않음

## 목적

이 문서는 DohaStudio 생태계가 공통으로 참조하는 Asset, Artifact, Job, Provider와 Manifest 계약의 기준 버전을 정의합니다. `0.1.0`은 구현 전 상호 검토를 위한 초안 기준선이며 안정 API를 뜻하는 `1.0.0`이 아닙니다.

## 명세 목록

1. [Asset 명세](01-asset-specification.md)
2. [AssetVersion 명세](02-asset-version-specification.md)
3. [Artifact 명세](03-artifact-specification.md)
4. [Provider 계약](04-provider-contract.md)
5. [Job 계약](05-job-contract.md)
6. [Model Manifest 명세](06-model-manifest-specification.md)
7. [Dataset Manifest 명세](07-dataset-manifest-specification.md)
8. [Composition Snapshot 명세](08-composition-snapshot-specification.md)
9. [Storage Layout 명세](09-storage-layout-specification.md)
10. [공통 용어](10-common-terms.md)

## 호환성과 버전 변경

- 문구 명확화나 오탈자 수정처럼 계약 의미를 바꾸지 않는 변경은 patch version 후보입니다.
- 선택 필드·capability처럼 기존 소비자를 깨뜨리지 않는 추가는 minor version 후보입니다.
- 필수 필드 제거·의미 변경, 식별자·상태·불변성 규칙 변경처럼 기존 소비자를 깨뜨리는 변경은 breaking change입니다.
- `0.x` 기간에도 breaking change는 새 version, 영향받는 저장소, 전환 순서와 호환 기간을 PR과 ADR에 명시합니다.
- `1.0.0` 전환은 구현·상호 운용·Migration·권리 검토 근거가 확보된 뒤 별도 결정합니다.

각 저장소는 문서 또는 Manifest에 지원하는 `specification_version`을 기록하고, 지원 범위를 넘는 계약을 구현 완료로 표현하지 않습니다.

## 변경 절차

1. `.github`의 `develop`에서 명세 변경과 영향도를 문서화합니다.
2. breaking 여부와 Provider·Workspace·Artifact·DB·API 영향을 검토합니다.
3. 영향받는 DohaMusic·DohaLM·DohaAudio·DohaVocal 문서와 전환 계획을 확인합니다.
4. 한국어 설명, 링크, 예제, ADR와 version 변경을 검증합니다.
5. `develop → main` PR 검토 후 수동으로 안정 기준선에 반영합니다.

## 링크 정책

| 목적 | 기준 링크 |
|---|---|
| 안정 문서와 일반 교차 저장소 참조 | `main` |
| 개발 중 명세와 통합 검토 | `develop` |
| 감사·재현·검증 근거 | 전체 commit SHA |
| PR 본문의 특정 검증 결과 | 필요 시 전체 commit SHA |

외부 저장소의 일반 문서는 [공통 명세 `main`](https://github.com/DohaStudio/.github/tree/main/docs/specifications)을 참조합니다. 아직 `main`에 반영되지 않은 변경을 시험할 때만 `develop` 링크를 사용하고 상태를 명시합니다.

## 라이선스와 권리

이 명세의 저장소 라이선스는 현재 [검토 필요](../../LICENSE) 상태입니다. Dataset, 외부 모델 코드, 모델 가중치, Adapter, Checkpoint, 생성 결과, 개인 음성과 Consent 증적은 이 저장소의 코드·문서 라이선스 적용 대상으로 간주하지 않으며 각각 별도로 검토합니다.
