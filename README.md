# deepin release系统的使用说明（草稿）

## 系统简介

从deepin项目启动开始，伴随着越来越多的deepin子项目产生，不同开源/商业定制版本的分割加剧，项目间的版本依赖问题、上游项目的patch丢失问题和系统环境无法恢复问题越来越严重，我们迫切需要一个统一的系统来帮助我们记录不同版本的ISO/软件仓库的状态，做各个子项目版本的版本控制和patch的版本控制，以达到快速恢复开发/系统环境，进而使针对不同系统版本的开发更加高效。

deepin release系统就是这样一个辅助系统，它的目标在于将它的每一个状态都对应到我们所有发布的ISO/软件仓库状态、每一个针对ISO/软件仓库的改动都能反映到这个仓库的改动上。

## deepin-code-release 仓库

deepin-code-release仓库(git)作为整个release系统的核心，目前包含一下几个重要组件：

- projects

    deepin所有子项目都以submodule的形式包含在这个目录，主要用于子项目的添加/删除和版本管理，所有对外推送的deepin系列包都是通过修改这个目录下对应的子项目版本来控制；

- patches

    patches目录主要用于记录相应软件仓库上游软件被deepin打过的patch，防止patch丢失和混乱；所有相应软件仓库中被deepin打过patch的上游应用都应该能在此找到所有patch；

    patch规范 （待补充）

- 分支结构和tag

    分支命名规范 软件仓库[-PPA]/current

        没有指定PPA的分支，改动过后打的包进入内网仓库，指定了PPA的则进入相应的内网 unstable PPA；

    tag命名规范 软件仓库/[系统新版本号|更新日期]

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

## CI系统

目前实现为panda-dde/current分支提交CL后，将更新的项目打包，打包完成后 verified +1；CL合并后推送包更新至内网dde PPA的unstable仓库；

其他（待补充）

