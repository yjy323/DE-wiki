> **SQL** is a standard language for storing, manipulating and retrieving data in databases.

> SQLite는 별도의 서버 프로세스 없이 SQL을 사용하여 DB에 액세스할 수 있는 디스크 기반 경량 임베디드 DB이다.
<br> 파이썬은 내장된 SQLite 모듈을 통해 RDB를 관리할 수 있다.

SQLite3에는 다양한 기능이 있지만 SQL Tutorial의 DML을 처리하기 위한 최소한의 기능과 개념 위주로 학습한다.
1. Connection과 Cursor 객체
2. SQL 실행
3. 트랜잭션 관리
4. 테이블 생성과 초기화
5. 쿼리 파라미터
6. 쿼리 실행 결과 처리

### 실행 흐름
1. DB 연결 및 커서 객체 생성
2. SQL 실행
3. 트랜잭션 관리
4. 자원 해제

### Connection과 Cursor
SQLite DB와 상호작용하는 핵심 역할
- Connection
  - DB와 파이썬 프로그램 간 연결을 관리한다.
  - DB 파일을 열거나 In-memory DB를 생성한다.
  - 트랜잭션을 제어한다.
    - connection.commit()
    - connection.rollback()
    - connection.close()
- Cursor
  - SQL 구문을 실행하고 결과 처리를 담당한다.
  - DB와 상호작용한다.
    - SQL 실행: cursor.execute()
    - 결과 조회: cursor.fetchX()
