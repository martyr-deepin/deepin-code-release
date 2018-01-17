# deepin release系统的使用说明（草稿）

## 系统简介

从deepin项目启动开始，伴随着越来越多的deepin子项目产生，不同开源/商业定制版本的分割加剧，项目间的版本依赖问题、上游项目的patch丢失问题和系统环境无法恢复问题越来越严重，我们迫切需要一个统一的系统来帮助我们记录不同版本的ISO/软件仓库的状态，做各个子项目版本的版本控制和patch的版本控制，以达到快速恢复开发/系统环境，进而使针对不同系统版本的开发更加高效。

deepin release系统就是这样一个辅助系统，它的目标在于将它的每一个状态都对应到我们所有发布的ISO/软件仓库状态、每一个针对ISO/软件仓库的改动都能反映到这个仓库的改动上。

## deepin-code-release 仓库

作为整个release系统的核心，deepin-code-release仓库目前包含一下几个重要组件：

- projects

    deepin所有子项目都以submodule的形式包含在这个目录，主要用于子项目的添加/删除和版本管理，所有仓库变动的dde系列包都是通过修改这个目录下对应的子项目版本来控制；


- patches (废弃)

    patches目录主要用于记录相应软件仓库上游软件被deepin打过的patch，防止patch丢失和混乱；所有相应软件仓库中被deepin打过patch的上游应用都应该能在此找到所有patch；

    patch规范 （待补充）

- 分支命名与仓库关系 (特指此项目自身的分支和tag)

    项目根目录的TARGET文件指定了对应的实际仓库地址。 TARGET格式为
       ```name repo\_url repo\_suite [可选的feature list. 以空格作为分隔符]```

    分支合并后一定对应到TARGET仓库的实际变动。(特殊情况下，反之不一定)

    分支命名规范 TARGET[0]/current

        目前只有current子分支，其他子分支预留给将来扩展使用。

    tag命名规范 TARGET[0]/[系统新版本号|更新日期]

        如果是发布新系统则写系统新版本号，如果只是例行更新，则写更新日期；


- 辅助工具

    project_list.json记录了所有包含子项目的版本号和tag，一方面方便开发更直观的查看自己的提交，另一方面也方便其他社区获取一次更新的内容及时跟进更新；pre-commit是git的一个hook脚本，它的作用是在每次提交的时候更新project_list.json文件；

    tools目录维护着方便操作这个仓库的一些工具，目前只有dcr:

    ```
    dcr submodule list 列举所有子项目

    dcr submodule status [--local] [--remote] [--diff] [submodules [submodules ...]]
    指定一个项目或者多个项目时只针对这些项目，不指定项目默认所有项目；

        --local  显示项目本地的版本
        --remote 显示项目上游的最新提交和最新版本
        --diff   列举本地版和上游最新版本的版本不同的项目

    dcr submodule sync [submodules [submodules ...]]
    指定一个项目或者多个项目时只针对这些项目，不指定项目默认所有项目；

        将项目同步至上游最新版本

    dcr patch （待补充）
    ```

说明：使用deepin-code-release仓库之前，需要

- 简单配置一下ssh，编辑~/.ssh/config，添加以下内容：

  ```
  HOST cr.deepin.io
    Port 29418
    User gerrit用户名
  ```

- 将 pre-commit 脚本拷贝到项目的.git/hooks目录

- git submodule update --init [SUBMODULE] 初始化以下相应的submodule项目

####使用举例说明
1.配置环境
  编辑~/.ssh/config,添加配置文件,目的是让每个submoudle引用我们都有权限提交代码。
  HOST cr.deepin.io
    Port 29418
    User gerrit用户名
2.拉取deepin-code-release 代码
git clone ssh://deepin@cr.deepin.io:29418/deepin-code-release && scp -p -P 29418 deepin@cr.deepin.io:hooks/commit-msg deepin-code-release/.git/hooks/

3.拷贝hook文件,目的是每次提交刷新project_list.json文件。
cd  deepin-code-release
cp pre-commit .git/hooks

4.切换到对应分之
例如：git checkout panda/current
git submodule init //初始化submodule引用
git submodule updae project/dde-daemon//拉取引用项目源码
cd project/dde-daemon
git checkout 3.1.6   //切换submodule引用commit,原则上commit必须在tag上面
cd ../../
git add project/dde-daemon    //添加新修改到本地
git commit -a -m "update 3.1.6"   //提交新修改到本地，此时会调用3步里面pre-commit hook文件刷新json文件并自动提交
git review panda/current   //提交新修改

至此一个正常提交流程完成，需要说明，切换引用commit，必须在tag上面。
5.添加新项目到对应project目录，操作如下
git submodule add ssh://cr.deepin.io:29418/deepin-calculator  project/deepin-calculator
git add project/deepin-calculator
git commit -a -m "***"
git review panda/current 
正常提交此次submodule 项目添加即可。



## 当前分支说明

### panda/current
TARGET内容
```panda http://packages.deepin.com/deepin panda [RR OnTag]```
1. panda/current对应官方仓库(packages.deepin.com/deepin panda)
2. 此分支出现CL后会自动触发rr.deepin.io (TARGET特性列表中含RR)
3. 且合并前需要保证所有的project落在具体的tag上 (TARGET特性列表中含OnTag)


### panda-dde/current
TARGET内容
```panda-dde http://pools.corp.deepin.com/ppa/dde unstable```
1. 对应内网ppa/dde仓库
