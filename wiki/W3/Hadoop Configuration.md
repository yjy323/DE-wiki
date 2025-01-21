The objective of this homework project is to demonstrate your understanding of setting up and configuring an Apache Hadoop multi-node cluster using Docker.

You will use at least two Docker containers and configure core-site.xml, hdfs-site.xml, mapred-site.xml, and yarn-site.xml with important parameters.

# 사전지식

### Configuration Files:
##### hadoop-env.sh
Hadoop 데몬이 사용하는 JDK를 설정하는 환경 변수 파일
##### core-site.xml
Hadoop 코어의 설정을 포함하며, HDFS의 NameNode 위치를 지정한다.
- **fs.defaultFS**: Specifies the default file system URI.
- **hadoop.tmp.dir**: Specifies the temporary directory.
- **io.file.buffer.size**: Specifies the buffer size for reading/writing files.
##### hdfs-site.xml
HDFS 데몬(NameNode, DataNode 등)의 설정
- **dfs.replication**: Defines the default replication factor for HDFS.
- **dfs.blocksize**: Specifies the default block size.
- **dfs.namenode.name.dir**: Specifies the path on the local filesystem where the NameNode stores the namespace and transaction logs.
##### mapred-site.xml
MapReduce 프레임워크의 설정
- **mapreduce.framework.name:** Specifies the framework name for MapReduce.
- **mapreduce.job.tracker**: Specifies the JobTracker host and port.
- **mapreduce.task.io.sort.mb**: Specifies the amount of memory to use while sorting map output.
##### yarn-site.xml
YARN(ResourceManager와 NodeManager)의 설정
- **yarn.resourcemanager.address**: The address of the ResourceManager IPC.
- **yarn.nodemanager.resource.memory-mb**: Determines the amount of memory available to YARN.
- **yarn.scheduler.minimum-allocation-mb**: Specifies the minimum allocation for every container request at the ResourceManager.

# 기능요구사항

## Modifying Configuration Settings

For each configuration file, change the identified settings to the specified values. Ensure that you follow the correct XML structure and syntax.

##### core-site.xml
- Change fs.defaultFS to hdfs://namenode:9000.
- Change hadoop.tmp.dir to /hadoop/tmp.
- Change io.file.buffer.size to 131072.
##### hdfs-site.xml
- Change dfs.replication to 2.
- Change dfs.blocksize to 134217728 (128 MB).
- Change dfs.namenode.name.dir to /hadoop/dfs/name.
##### mapred-site.xml
- Change mapreduce.framework.name to yarn.
- Change mapreduce.jobhistory.address to namenode:10020.
- Change mapreduce.task.io.sort.mb to 256.

##### yarn-site.xml
- Change yarn.resourcemanager.address to namenode:8032.
- Change yarn.nodemanager.resource.memory-mb to 8192.
- Change yarn.scheduler.minimum-allocation-mb to 1024.
## Configuration Modification Script:

- The script should accept the path to the Hadoop configuration directory as an argument.
- It should back up the original configuration files before making any changes.
- The script should modify the specified settings in the XML files to the given values.
- It should handle any errors gracefully and report the status of each change.
- Backup the original configuration files.
- Modify the specified settings in the configuration files.
- Restart the Hadoop services.

## Verification Script:

- The script should confirm the default file system name is set correctly by running a relevant Hadoop command and parsing the output.
- **It should create a test file in HDFS and check its replication factor to verify the change.**
- **The script should run a simple MapReduce job and ensure it uses the YARN framework.**
- It should query YARN ResourceManager to verify the total available memory for YARN.
- The script should verify the temporary directory, buffer size, block size, NameNode directory, JobTracker, sort memory buffer size, ResourceManager hostname, NodeManager memory allocation, and container minimum allocation.
- Query the Hadoop configuration to check the modified settings.
- Print the results, indicating whether each setting matches the expected value.
- **Create a test file in HDFS and verify the replication factor.**

# 프로그래밍 요구사항

- Write a shell script or a Python program to modify the specified settings in the configuration files.
- Develop another script or program to verify the configuration changes.
- Use appropriate commands and APIs to interact with the Hadoop cluster.