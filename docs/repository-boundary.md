# 저장소 책임 경계

> 문서 상태: [제안]

| 저장소 | 책임 |
|---|---|
| [DohaMusic](https://github.com/DohaStudio/DohaMusic) | Frontend·Backend, Workspace, Project, Asset·AssetVersion, Recording, Snapshot, Mix, Export, Provider Client |
| [DohaLM](https://github.com/DohaStudio/DohaLM) | 가사 생성·분석·수정, Dataset, 학습, 평가, Runtime |
| [DohaAudio](https://github.com/DohaStudio/DohaAudio) | 음악 생성, Stem 분리, 오디오 분석, Dataset, 학습, 평가, Runtime |
| [DohaVocal](https://github.com/DohaStudio/DohaVocal) | 가창 음성, 음색 변환, Pitch·Timing·Noise 처리, Dataset, 학습, 평가, Runtime |

Repository간 직접 호출은 없습니다. Provider orchestration, 사용자 권한과 최종 AssetVersion 선택은 DohaMusic이 담당합니다. 구체적인 하위 책임은 각 Repository의 ADR과 README가 우선합니다.
