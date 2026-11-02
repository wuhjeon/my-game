# fonts

Google Fonts 대신 저장소에서 직접 내려주는 웹 폰트. 외부 요청 없이 `fonts.css` 하나만 불러오면 된다.

- 루트 `index.html`: `<link rel="stylesheet" href="fonts/fonts.css">`
- 게임 폴더의 `index.html`: `<link rel="stylesheet" href="../fonts/fonts.css">`

| 파일 | font-family | weight |
| --- | --- | --- |
| `BlackHanSans-400.woff2` | Black Han Sans | 400 |
| `IBMPlexSansKR-400.woff2` | IBM Plex Sans KR | 400 |
| `IBMPlexSansKR-600.woff2` | IBM Plex Sans KR | 600 |
| `IBMPlexSansKR-700.woff2` | IBM Plex Sans KR | 700 |

## 출처와 라이선스

- 원본 TTF: https://github.com/google/fonts (`main` 브랜치)
  - `ofl/blackhansans/BlackHanSans-Regular.ttf`
  - `ofl/ibmplexsanskr/IBMPlexSansKR-Regular.ttf`, `-SemiBold.ttf`, `-Bold.ttf`
- 라이선스: SIL Open Font License 1.1
  - Black Han Sans: `OFL-BlackHanSans.txt` (Copyright 2015 The Black Han Sans Project Authors)
  - IBM Plex Sans KR: `OFL-IBMPlexSansKR.txt` (Copyright 2017 IBM Corp.)

## 서브셋 만드는 방법

용량을 줄이려고 필요한 글자만 남긴 WOFF2로 만들었다 (`make-subset.py`, fontTools 사용).
남기는 글자:

1. 출력 가능한 ASCII (U+0020–U+007E)
2. KS X 1001 한글 음절 2,350자
3. 한글 호환 자모 (U+3131–U+318E)
4. 저장소에서 git이 추적하는 모든 `.html` 파일에 들어 있는 글자
5. 자주 쓰는 문장 부호 (· … – — ‘ ’ “ ” NBSP ×)

폰트에 없는 글자(예: 이모지)는 빠지고, 브라우저가 예전처럼 시스템 폰트로 대신 그린다.
OpenType 레이아웃 기능은 모두 남기고 힌팅은 뺐다.

## 다시 만들기 (게임에 새 글자를 넣었을 때)

KS X 1001 밖의 글자(드문 한글, 한자 등)를 새로 쓰면 서브셋을 다시 만든다.
HTML을 먼저 고치고 커밋(또는 `git add`)한 뒤 저장소 루트에서:

```sh
pip install fonttools brotli
mkdir -p /tmp/gf && cd /tmp/gf
B=https://raw.githubusercontent.com/google/fonts/main/ofl
curl -fLO $B/blackhansans/BlackHanSans-Regular.ttf
curl -fLO $B/ibmplexsanskr/IBMPlexSansKR-Regular.ttf
curl -fLO $B/ibmplexsanskr/IBMPlexSansKR-SemiBold.ttf
curl -fLO $B/ibmplexsanskr/IBMPlexSansKR-Bold.ttf
cd -
python3 fonts/make-subset.py /tmp/gf
```

`make-subset.py`는 원본 TTF 폴더를 인자로 받고, 결과 WOFF2를 `fonts/`에 덮어쓴다
(`--out`, `--repo`로 바꿀 수 있음).
