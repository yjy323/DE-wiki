# RDD
---
### Apache Spark의 데이터 단위
- 분산/병렬 환경에서의 처리를 기본 전제로 한다.
	- 불변성(Immutable)
		- Fault Tolerance
			- Task가 실패하더라도 쉽고 빠르게 재실행할 수 있다.
		- 병렬 처리
			- 동기화와 Lock 문제에서 자유롭다.
1. [Parallelized Collections](https://spark.apache.org/docs/latest/rdd-programming-guide.html#parallelized-collections)
2. [External Datasets](https://spark.apache.org/docs/latest/rdd-programming-guide.html#external-datasets)
3. Existing RDDs
## RDD Operations
### Transformation
- which create a new dataset from an existing one.
- Transformation은 매번 RDD를 재생성하지만 메모리를 이용해 최적화할 수 있다
	- _persist_ an RDD in memory using the `persist` (or `cache`) method.
	- in which case Spark will keep the elements around on the cluster for much faster access the next time you query it.
- **Narrow**
	- computed in parallel *without shuffling data* across partitions.
- **Wide**
	- *shuffling data* across partitions and may involve *data movement* between nodes.
		- Node 간 Netword I/O가 발생한다.
- [**Shuffle operations**](https://spark.apache.org/docs/latest/rdd-programming-guide.html#shuffle-operations)
	- 클러스터 워커에 데이터를 재분배(re-distributing)하는 작업
	- [Performance Impact](https://spark.apache.org/docs/latest/rdd-programming-guide.html#performance-impact)
### Action
- which return a value to the driver program after running a computation on the dataset.
### Lazy Evaluation
- Spark는 operations를 lineage하게 추적 관리하다가, action이 호출되었을 때 transformation을 실행한다.
- 지연 평가를 통해 불필요한 연산을 최소화하도록 실행 계획을 최적화할 수 있다.
### Partition
- 병렬 연산하기 위한 작은 논리적 단위의 데이터
- 단일 executor의 **단일 task가 처리**하는 데이터 단위이다.
	- Task가 실행되는 *노드*에 위치하는 데이터
	- 독립적인 실행 단위
		- task 실행 중 에러가 발생해도 코드와 데이터가 같은 노드에 저장되어 있으므로 빠르게 재실행 할 수 있다.
### Q. Python 변수와 RDD 사이의 관계는?
## Executing Spark Jobs
1. Driver 프로그램 시작
	1. SparkContext 생성
	2. RDD Lineage Graph 생성, Transformation의 실행 계획이 메모리에 저장
2. Job 제출(Action)
3. SparkContext의 DAG Scheduler가 Job을 여러 Stage로 나눈다.
	1. Stage는 narrow/wide 기준으로 구분된다.
	2. Stage는 내부에서 다시 병렬로 처리 단위의 Task로 쪼개진다.
4. Task Scheduler
	1. Task를 Executor에 분배한다.
	2. Executor를 실행하기 위한 리소스를 Cluster Manager에 요청한다.
	3. Spark driver는 task 실행에 필요한 프로그램과 의존성을 모두 worker node에 전송한다.
### Job
- Action이 호출될 때 생성되는 처리 작업 단위
- Transformations는 DAG가 되고, Job은 Stages of tasks로 구성된다.
### Stage and Task
- Stage는 Job의 구성 단위이며 tasks의 집합이다. 
	- Boundary는 **shuffle이 발생하는 지점**으로 Job의 Stage를 구분하는 기준이다.
	- Spark는 shuffle이 발생하면 stage를 재구성하고, executor 간 데이터 교환이 발생한다.
- Task는 **독립적인 병렬 작업의 실행 단위**로, partition of data와 일대일로 매핑된다.
	- task가 실행될 때 이미 partition된 데이터가 노드에 위치한다.
---
### Summary
- Spark의 RDD & DAG는 분산/병렬 환경을 전제로, 그 최적화를 목적으로 한다.
- Task와 Partition 컨셉은 Fault Tolerance와 Parallel process를 쉽게 한다.
	- Partition이 크면 Task가 커지고 분산 처리의 이점이 사라지고, 재실행이 오래 걸린다.
	- Partition이 너무 작으면 Task가 너무 많이 생성돼 스케줄링/리소스 관리 비용, I/O 비용이 커진다.
- RDD는 WORM 컨셉처럼 데이터의 일관성을 신경쓰지 않고 작업을 효율적으로 처리하는데만 집중할 수 있게 한다.
- Lazy Evaluation은 최적화된 DAG를 만들어 Spark가 효율적으로 Job을 실행할 수 있게 한다.
- Spark의 컨셉과 동작을 잘 이해해 최적화된 코드를 작성할 수 있어야 한다.
	- DAG의 Stage가 적을 수록 좋다.
		- Stage의 Boundary가 적다 = Wide Transformation이 적다.
	- Stage의 Task가 적을 수록 좋다.
	- 같은 기능을 처리할 때 RDD를 적게 생성할수록 좋다.
	- Partition 수, 메모리 크기 단위까지 최적화할 수도 있다.