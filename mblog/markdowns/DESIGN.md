# 异地快照系统设计文档

## 版本变更

| 版本号        | 变更时间       | 描述          | 变更人    |
| ------------ | ------------- | ------------ |----------|
| V0.1         | 2017.9.25     | V0.1        | 刘庆      |

----------

## 概述

容灾是指为计算机信息系统提供的一个能应付各种灾难的环境。当计算机系统在遭受如火灾、水灾、地震、战争等不可抗拒的自然灾难以及计算机犯罪、计算机病毒、掉电、网络/通信失败、硬件/软件错误和人为操作错误等人为灾难时，容灾系统将保证用户数据的安全性（数据容灾）。
磁盘快照(Snapshot)是针对整个磁盘卷册进行快速的档案系统备份，与其它备份方式最主要的不同点在于**速度**。进行磁盘快照时，并不牵涉到任何档案复制动作。就算数据量再大，一般来说，通常可以在数秒之内完成备份动作。磁盘快照一般都在一个同一个数据中心，对于单个数据中心不能工作的情况无能为力。


## 设计目标

Openstack cinder的快照无法在不同数据中心中可见，本系统的目的是根据用户的选择将公有云快照复制到私有云Openstack环境中去，使得用户的数据在块级别上具有容灾的功能。

## 整体构架
![](/statics/arch.png)

### 对Cinder的修改
需要在原有Openstack Cinder组件中添加新的API，用于快照复制。快照拷贝的执行过程中需要调用对端Openstack数据中心的Cinder API，所以还需要添加一个数据中心名字到对端Keystone endpoint的映射。这样用户选择了需要复制的快照和目标数据中心后，cinder就可以通过映射表获得keystone的信息，继而获得对端cinder的endpoint。

#### 在目标端快照建立过程
* TODO: 两边快照信息比对
* TODO: 对以下情况的调研：

  source 快照链：volume1 snap1 snap2 snap3 snap4

  用户复制：snap1，snap4

  复制完后看对端会不会有snap2/snap3，**对快照删除会不会有影响**。

* 第一次快照复制：
     * Cinder创建一个同样大小的Volume，Volume信息需要保持一致（TODO: Volume ID是mapping还是不变需要再考虑），source volume id/snapshot id等信息可以去掉。这个可以参考volume migration中的信息。Volume创建完成后，ceph pool中就会有一块空盘。
     * 接着在数据库中创建一个需要复制的snapshot的信息（TODO:哪些字段保留哪些字段去除需要考虑），此过程不对ceph做操作。
     * Cinder 调用rsnap服务的`/server`接口，cinder保持返回信息。
     * Cinder 将volume id，snapshot id，server信息返回给源端cinder

* 第二次及之后的快照复制：

  * 不需要创建Volume这个过程，其他和上一步类似。

#### 目标site信息如何存储,配置文件or数据库（TODO: guozhong考虑下）

### 异地快照系统
本系统是一个无状态HTTPS服务器，提供如下功能：
1. 获取服务器信息。
  * 在没有配置etcd的情况下。 对于目标端的Cinder只需要知道Keystone中本服务的VIP和对应的port即可。但是对于源端的Cinder来说，他需要将快照传递到本服务。由于快照传递数据量大，时间长，如果借助HAPPROXY的话，很可能引起HAPPROXY不稳定。HAPPROXY还需要为其他Openstack服务提供服务，所以其稳定性相当重要。为此对端Cinder可以通过本API获得实际的服务器IP和port，再将这些信息返回给源端Cinder。快照传输就可以绕过HAPPROXY。
  * 在使用etcd的情况下。所有服务使用单独线程往/rsnap/servers目录下写入自己的当前连接数，比如key: "ip:port" value: 2. TTL: 60。当获取服务器信息请求达到时，服务获取/rsnap/servers下的所有条目，并选择一条连接数最小的记录返回。在etcd连接失败的情况下直接返回本机信息。
    *增加连接数:* 一旦Snapshot资源的on_put方法被调用时就通过read-compare-modify增加连接计数。
    *减少连接数:* on_put在返回给客户端时通过read-compare-modify减少连接计数。
    *连接计数更新:* 可能存在多个worker更新同一个数据的情况，只需要将计数读出然后回写，如果回写失败直接忽略，因为其他worker已经更新过这个计数。

2. 快照传输。通过HTTP PUT方法将快照传送给本服务。接收到的快照会放入对应的存储后端。

### HAPPROXY和Keystone配置的修改
异地快照系统会将自己的服务地址注册到Keystone，而服务地址是通过HAPPROXY配置的。
