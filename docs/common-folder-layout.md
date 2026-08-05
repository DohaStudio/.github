# 공통 폴더 구조

> 문서 상태: [제안]

```text
DohaProjects/
├── DohaMusic/
├── DohaLM/
├── DohaAudio/
└── DohaVocal/

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

`DohaProjects`는 Git 코드·문서, `DohaData`는 Dataset, `DohaArtifacts`는 보존 대상 결과, `DohaTemp`는 재생성 가능한 cache와 temporary output입니다. 실제 절대 경로는 코드·Manifest·공개 log에 하드코딩하지 않습니다.
