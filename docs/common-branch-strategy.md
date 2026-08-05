# 공통 브랜치 전략

> 문서 상태: [제안]

```text
main
└── develop
    ├── feature/*
    ├── docs/*
    └── fix/*
```

- `main`: 안정화·릴리스
- `develop`: 일반 작업 통합 대상
- 작업 브랜치: 최신 `develop`에서 요청 한 건 수행
- 기본 흐름: 검증 → Commit → Push → `develop` 대상 Draft PR → Review → Merge

Commit type은 `docs:`, `feat:`, `fix:`, `refactor:`, `test:`, `chore:`를 사용합니다. Repository별 더 구체적인 `AGENTS.md`와 보호 규칙이 우선합니다.
