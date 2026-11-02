# fonts

Google Fonts 대신 저장소에서 직접 내려주는 웹 폰트. 외부 요청 없이 `fonts.css` 하나만 불러오면 된다.

- 루트 `index.html`: `<link rel="stylesheet" href="fonts/fonts.css">`
- 게임 폴더의 `index.html`: `<link rel="stylesheet" href="../fonts/fonts.css">`

| 파일 | font-family | weight | 종류 |
| --- | --- | --- | --- |
| `BlackHanSans-400.woff2` | Black Han Sans | 400 | 서브셋 (`make-subset.py`로 만듦) |
| `IBMPlexSansKR-Regular.woff2` | IBM Plex Sans KR | 400 | IBM 공식 파일, 수정 없음 |
| `IBMPlexSansKR-SemiBold.woff2` | IBM Plex Sans KR | 600 | IBM 공식 파일, 수정 없음 |
| `IBMPlexSansKR-Bold.woff2` | IBM Plex Sans KR | 700 | IBM 공식 파일, 수정 없음 |

라이선스는 모두 SIL Open Font License 1.1.

## IBM Plex Sans KR (공식 WOFF2, 수정 없음)

- 출처: IBM이 배포하는 npm 패키지 `@ibm/plex-sans-kr` 1.1.0
  - https://registry.npmjs.org/@ibm/plex-sans-kr/-/plex-sans-kr-1.1.0.tgz
  - 패키지 안의 `fonts/complete/woff2/hinted/` 파일을 바이트 그대로 복사 (재인코딩·서브셋·이름 변경 없음)
- sha256:
  - `IBMPlexSansKR-Regular.woff2` (438,540 B): `055a35664c3c3965161c92292504c5633ba9604ec904edc1ed799bf2a436276d`
  - `IBMPlexSansKR-SemiBold.woff2` (434,484 B): `5ad7db28ba74d59fe14c260205c62ddb701320f4f098d8a45ef2757bebc29666`
  - `IBMPlexSansKR-Bold.woff2` (370,492 B): `cf874a368dc2c2c0e4d1933c35611b849e48942023bfdd1fa11128475dbc4860`
  - 확인: `sha256sum fonts/IBMPlexSansKR-*.woff2`
- 라이선스: `OFL-IBMPlexSansKR.txt` (패키지의 `LICENSE.txt` 그대로, Copyright 2017 IBM Corp., Reserved Font Name "Plex")
- **일부러 서브셋을 만들지 않았다.** 이 폰트의 OFL에는 예약 글꼴 이름(Reserved Font Name) "Plex"가 있어서,
  수정한 버전(서브셋도 수정에 해당)은 그 이름을 쓸 수 없다. 그래서 IBM이 배포한 파일을 그대로 쓴다.
  한글 11,172자가 모두 들어 있어 글자를 새로 써도 다시 만들 필요가 없다.

## Black Han Sans (서브셋)

- 원본 TTF: https://github.com/google/fonts 의 `ofl/blackhansans/BlackHanSans-Regular.ttf` (`main` 브랜치)
- 라이선스: `OFL-BlackHanSans.txt` (Copyright 2015 The Black Han Sans Project Authors, 예약 글꼴 이름 없음)
- 용량을 줄이려고 필요한 글자만 남긴 WOFF2로 만들었다 (`make-subset.py`, fontTools 사용). 남기는 글자:
  1. 출력 가능한 ASCII (U+0020–U+007E)
  2. KS X 1001 한글 음절 2,350자
  3. 한글 호환 자모 (U+3131–U+318E)
  4. 저장소에서 git이 추적하는 모든 `.html` 파일에 들어 있는 글자
  5. 자주 쓰는 문장 부호 (· … – — ‘ ’ “ ” NBSP ×)
- 폰트에 없는 글자(예: 화살표, 이모지)는 빠지고, 브라우저가 예전처럼 다른 폰트로 대신 그린다.
  OpenType 레이아웃 기능은 모두 남기고 힌팅은 뺐다.

### 다시 만들기 (게임에 새 글자를 넣었을 때)

KS X 1001 밖의 글자(드문 한글 등)를 Black Han Sans로 새로 쓰면 서브셋을 다시 만든다.
HTML을 먼저 고치고 커밋(또는 `git add`)한 뒤 저장소 루트에서:

```sh
pip install fonttools brotli
mkdir -p /tmp/gf
curl -fL -o /tmp/gf/BlackHanSans-Regular.ttf \
  https://raw.githubusercontent.com/google/fonts/main/ofl/blackhansans/BlackHanSans-Regular.ttf
python3 fonts/make-subset.py /tmp/gf
```

`make-subset.py`는 원본 TTF 폴더를 인자로 받고, 결과 `BlackHanSans-400.woff2`를 `fonts/`에 덮어쓴다
(`--out`, `--repo`로 바꿀 수 있음). IBM Plex Sans KR은 건드리지 않는다.
