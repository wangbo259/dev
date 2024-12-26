
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

![alt text](image-34.png)

![alt text](image-35.png)

![alt text](image-36.png)

# 参数设置
1. 有多少服务器exector就设计最少多少个
2. spark.sql.shuffle.partitions，该参数指的是在sql计算中，shuffle算子阶段默认的分区数，根据集群中可用cpu核数设置，在实际项目中需要合理设置，和并行度的参数相互独立。
3. 自适应查询参数
```
set spark.sql.adaptive.enabled = true
```
![alt text](image-37.png)
![alt text](image-38.png)
![alt text](image-39.png)
> 触发动态优化倾斜join需要满足两个条件，即图中所示，需要该分区的大小大于中位数的10倍（可调参数）以及该分区大小大于某个值（可调参数）

4. Sort Merge Join最适合用于以下情况：

- 已经排序的数据：如果数据集已经按照连接键排序，或者可以很容易地被排序，那么Sort Merge Join是一个非常好的选择。
- 大数据量：对于大数据量，Sort Merge Join可以减少数据的shuffle，从而减少网络传输和磁盘I/O，提高性能。
>配置: 在Spark中，你可以通过设置spark.sql.join.preferSortMergeJoin配置项来控制是否优先使用Sort Merge Join。如果设置为true，Spark会尽可能使用Sort Merge Join，如果设置为false，则会使用Shuffle Hash Join作为默认的连接方式。
```
spark.conf.set("spark.sql.join.preferSortMergeJoin", "true")
```


# 参数调优
【sparksql默认并行度为200，即task数量】
## 物理执行计划解读
![alt text](image-40.png)

## 资源估算
1. 给出每个exector分配的线程数，这样就可以估算出exector的个数
2. 需要知道yarn的容器的内存上下限，之后可以根据内存大小和exector的个数来估计每个exector的内存的最大值
![alt text](image-41.png)

## exector内存估计
- 其中Executor的内存为最核心的部分，首先知道每个exector设定了几个线程（核心），通过数据大小和并行度可以估算每个线程需要的内存大小，相乘即可得到每个exector的Executor部分需要的内存，再估算得到每个exector需要的内存。
![alt text](image-42.png)

## 充分利用cpu，设置合适并发度
- 先确定exector的数量和每个exector的核数，相乘即为并行度，再由并行度确定并发度（2～3倍）
![alt text](image-44.png)
![alt text](image-43.png)


# sparksql优化
## 基于RBO的优化
### 谓词下推【着重注意，避免这种问题】
> 左连接（或右连接）后如果要筛选结果，如果连接字段存在null，放在on和where的筛选条件会产生不同的谓词下推结果，防止意外出现统一操作（大部分适用）：
1. 连接字段的筛选条件尽量放在on部分
2. 筛选条件尽量基于主表字段
![alt text](image-45.png)

### 列裁剪
> 只保留有用字段

## 基于CBO的优化（代价最小优化）
### 