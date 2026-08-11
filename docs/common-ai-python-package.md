# Common AI Contract Python package

`dohastudio-common-ai-contracts`는 Python 소비자가 Common AI Contract Schema
v1과 validator를 offline으로 사용하는 배포 패키지입니다. Python import
namespace는 `dohastudio_common_ai`입니다.

## 권위와 버전

Git의 권위 resource는 `schemas/common-ai/v1`에 한 번만 존재합니다. Build는 이
디렉터리를 wheel의 package resource로 포함하며 별도의 관리 사본을 만들지
않습니다. 현재 package distribution version은 `0.1.0`, executable contract
policy version은 `1.0.0`, 직렬화 객체 version은 `schema_version: 1.x.y`입니다.
문서의 `0.2.0-draft`는 또 다른 specification version 축입니다.

이 패키지는 아직 PyPI, GitHub Release 또는 다른 registry에 publish되지
않았습니다. Release 이후 소비자는 immutable artifact version과 SHA256을 함께
pin해야 하며 rollback은 직전 검증 artifact pin으로 되돌리는 방식으로 합니다.

## Build와 설치

```text
python -m build
python -m pip install dist/dohastudio_common_ai_contracts-0.1.0-py3-none-any.whl
```

## Offline resource와 validation

```python
from dohastudio_common_ai import (
    build_registry,
    contract_policy_version,
    get_schema,
    schema_names,
    validate_contract,
)

assert contract_policy_version() == "1.0.0"
assert len(schema_names()) == 12
schema = get_schema("music_intent")
registry = build_registry()
issues = validate_contract(contract_object, "music_intent")
```

모든 `$ref`는 package resource로 만든 local registry에서 해결합니다. Schema
`$id`는 identifier일 뿐 network endpoint가 아닙니다. Unknown schema/resource는
fallback하지 않고 `ContractResourceError`를 발생시킵니다. API는 package 내부
filesystem path를 반환하지 않습니다.

## 범위

이 패키지는 Contract Schema·Registry·version policy·validator를 배포합니다.
이번 단계는 DohaMusic·DohaLM 등 consumer dependency pin, DTO mapping, DB/API,
Provider/Runtime, Dataset/Model 또는 Training/Evaluation을 연결하지 않습니다.
