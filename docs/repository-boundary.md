# Repository Boundary

> 문서 상태: [제안]

| Repository | 책임 |
|---|---|
| [DohaMusic](https://github.com/DohaStudio/DohaMusic) | Frontend, Backend, Workspace, Project, Asset/AssetVersion, Recording, Snapshot, Mix, Export, Provider Client |
| [DohaLM](https://github.com/DohaStudio/DohaLM) | Lyrics Generation, Analysis, Revision, Dataset, Training, Evaluation, Runtime |
| [DohaAudio](https://github.com/DohaStudio/DohaAudio) | Music Generation, Stem Separation, Audio Analysis, Dataset, Training, Evaluation, Runtime |
| [DohaVocal](https://github.com/DohaStudio/DohaVocal) | Singing Voice, Voice Conversion, Pitch/Timing/Noise, Dataset, Training, Evaluation, Runtime |

Repository간 직접 호출은 없습니다. Provider orchestration, 사용자 권한과 최종 AssetVersion 선택은 DohaMusic이 담당합니다. 구체적인 하위 책임은 각 Repository의 ADR과 README가 우선합니다.
