## word_cloud
A little word cloud generator in Python.
이 워드클라우드 생성 도구의 장점은 다음과 같이 소개된다.
1. 사용 가능한 모든 공간을 효율적으로 채운다.
2. 임의의 마스크(워드클라우드 모양)를 자유롭게 사용할 수 있다.
3. 쉽게 수정할 수 있는 간단한 stupid 알고리즘을 사용한다.
4. 파이썬 기반으로 작동한다.
### wordcloud.WordCloud
Word cloud object for generating and drawing.
**파라미터**
1. 워드클라우드 이미지 관련
2. 폰트 관련
3. 색상 관련
4. 배치 및 레이아웃 관련
5. 단어 처리
	1. stopwords
	2. collocation
	3. regexp
	4. ...
**메서드**
1. 텍스트 처리/이미지 생성
	1. generate()
	2. generate_from_frequencies()
	3. generate_from_file()
	4. generate_from_text()
2. 단어 빈도 처리
	1. process_text()
	2. fit_words()
3. 이미지 변환/파일 입출력
**wordcloud.WordCloud.generate(text: str)를 기준으로 한 작동 방법**
text는 하나의 문자열이다.
1. generate()는 내부적으로 generate_from_text()를 호출하는 alias이다.
2. generate_from_text()는 각각 다음 두 메서드를 호출한다.
	1. process_text(text)-> fregs: dict
	2. generate_from_frequencies(fregs: dict)
3. process_text(text)는 WordCloud 객체가 갖고 있는 정보를 이용해 전달받은 문자열을 처리해 {단어:빈도수} 형태의 딕셔너리를 반환한다.
4. generate_from_frequencies(fregs)는 계산된 {단어:빈도수} 딕셔너리를 이용해 실제로 워드 클라우드를 생성한다.
	1. 입력 빈도수를 정규화한다.
	2. 이미지를 그릴 캔버스를 준비한다.
	3. 글자 크기 등 폰트 정보를 결정한다.
	4. 모든 단어를 각각 Brute Force하게 배치한다.
		1. 단어 배치 방향 결정, 배치 시도
		2. 충돌 시 폰트 크기를 줄이거나 방향을 바꿔 다시 시도
		3. 최소 폰트 사이즈보다 작아지면 break
	5. 이미지 생성 처리
### 결론
워드클라우드는 문자열을 파라미터에 따라 전처리하고 단어-빈도 정보를 계산한 후, 내부 알고리즘에 따라 레이아웃에 단어를 배치하는 방식으로 생성된다.
## Reference
https://github.com/amueller/word_cloud
https://amueller.github.io/word_cloud/index.html