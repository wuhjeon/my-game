# vendor

외부 CDN 없이 사이트를 돌리기 위해 저장소에 그대로 넣어 둔 라이브러리.

## three.min.js

- Three.js **r128** (npm `three@0.128.0`의 `build/three.min.js`, 수정 없음)
- 출처: https://registry.npmjs.org/three/-/three-0.128.0.tgz
- sha512 (base64): `dLxUelApnYxpLt6K2iomGngnHO83iUvZytA3YjDUCjT0HDOHKXnVYdf3hU4JjM8uEhxf9nD1/ey98U3t2vZ0qQ==`
  - 확인: `openssl dgst -sha512 -binary vendor/three.min.js | base64`
- 라이선스: MIT (Copyright 2010-2021 Three.js Authors, 파일 맨 위 주석에 표기)
- 게임 코드가 r128 API에 맞춰져 있으므로 버전을 올리지 말 것.
- 각 게임 페이지에서 `<script src="../vendor/three.min.js"></script>`로 불러온다.
