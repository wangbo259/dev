
# Yarn和Spark对比
![alt text](image-2.png)

# Standalone架构（并行环境下）
![alt text](image-3.png)

# spark的配置文件
![alt text](image-4.png)

# 一般默认的webui端口
- master的端口8080
- driver的端口4040
- history的端口18080
![alt text](image-6.png)

# 运行层级划分
![alt text](image-5.png)

![alt text](image-7.png)

# 避免master崩溃造成单点崩溃问题
![alt text](image-8.png)

# spark on yarn
## 本质
将spark程序提交到yarn中，yarn来充当master和worker角色来管理资源，在yarn容器内部创建driver来进行数据处理。
![alt text](image-9.png)
![alt text](image-10.png)

## 两种模式：Cluster和Client
- Cluster：集群模式，在yarn容器内部创建driver进程，所有的通讯都在容器内部完成，通讯成本低，但是需要去容器内部查看日志，不方便
- Client：客户端模式，在客户端内创建driver进程，通讯成本高，但是日志输出在客户端内，方便查看。

![alt text](image-11.png)

## yarn模式流程
![alt text](image-12.png)
![alt text](image-13.png)

# pyspark代码的原理（相对于java/scala）
![alt text](image-15.png)
![alt text](image-14.png)

# SparkCore知识点

## RDD
### RDD定义
![alt text](image-16.png)

### RDD特性
![alt text](image-17.png)

![alt text](image-18.png)

![alt text](image-19.png)

![alt text](image-20.png)

![alt text](image-21.png)

## DAG（有向无环图）
### job划分：
整个任务可能会有很多job，一个job对应一个DAG
### 宽窄依赖的划分
![alt text](image.png)
### stage的划分
![alt text](image-1.png)
### 内存迭代计算
![alt text](image-22.png)
![alt text](image-23.png)
![alt text](image-24.png)

## spark并行度的规划---先有并行度规划才确定有几个分区
![alt text](image-25.png)


## spark任务调度
![alt text](image-26.png)

# sparksql的dataframe
![alt text](image-27.png)
![alt text](image-28.png)

## 读取外部数据
![alt text](image-29.png)

# sparksql执行逻辑
sql经过Catalyst优化器解析并优化后经由rdd执行任务
![alt text](image-30.png)

两种优化方法：
![alt text](image-31.png)


# spark on hive的原理：借用了hive的MetaStore服务
![alt text](image-32.png)

# spark的shuffle过程
![alt text](image-33.png)


# 参数设置
1. 有多少服务器exector就设计最少多少个
2. spark.sql.shuffle.partitions，该参数指的是在sql计算中，shuffle算子阶段默认的分区数，根据集群中可用cpu核数设置，在实际项目中需要合理设置，和并行度的参数相互独立。