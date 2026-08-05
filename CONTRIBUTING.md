# DohaStudio 기여 안내

## 저장소 선택

- Workspace·Project·Asset·Mix·Export: DohaMusic
- Lyrics Generation·Analysis·Revision: DohaLM
- Music Generation·Stem·Audio Analysis: DohaAudio
- Singing Voice·Voice Conversion·Vocal Processing: DohaVocal
- Organization 공통 문서·Template: 이 `.github` 저장소

## 공통 작업 흐름

1. Repository의 `AGENTS.md`, README, Roadmap, ADR을 확인합니다.
2. 최신 `develop`에서 `feature/*`, `docs/*`, `fix/*` 작업 브랜치를 생성합니다.
3. 요청 범위만 변경하고 관련 검증을 실행합니다.
4. 문서와 CHANGELOG 영향을 반영합니다.
5. 명확한 Commit Convention으로 커밋하고 원격에 Push합니다.
6. `develop` 대상 Draft PR을 생성합니다.
7. Review와 필수 검증 후 Repository 정책에 따라 병합합니다.

`main`은 안정화·릴리스용이며 일반 작업에서 직접 변경하지 않습니다.

## 커밋 규칙

- `docs:` 문서
- `feat:` 기능
- `fix:` 오류 수정
- `refactor:` 동작 보존 구조 개선
- `test:` 테스트
- `chore:` 유지보수

Commit과 PR 제목은 변경 내용을 구체적으로 설명해야 합니다.

## 공통 안전 원칙

Dataset, 모델 weight, Checkpoint, 개인 음성, AIHub package, Private Metadata, 비밀정보와 생성 미디어를 Public Git에 포함하지 않습니다. 구현·검증되지 않은 기능은 `[계획]`, `[검증 필요]`, `[미구현]`, `[Legacy]`, `[제안]`으로 표현합니다.
