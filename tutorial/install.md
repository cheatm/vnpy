# 安装

本教程基于Win10环境

安装方案：

* VeighNa Studio: 整合环境，包括python环境，vnpy本体，扩展模组和依赖库，相当于一个量化开发平台，适用于学习，测试等。
* 手动安装: 基于本机python环境安装，只包含vnpy本体，扩展模块需要自行下载安装，适用于不需要GUI的实盘环境。

## VeighNa Studio方案

从官网下载直接安装即可: https://www.vnpy.com/


## 手动安装

首先安装python环境,推荐使用3.7以上版本的anaconda。

单独下载并安装ta-lib，ta-lib是用与指标计算的工具包，因为有c++依赖所以直接使用pip安装会失败，
这里推荐使用直接下载第三方编译的.whl文件安装：https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib。
下载对应版本的.whl文件后，在CMD用下面给命令更新, `FILENAME`为.whl文件的绝对路径。

需要手动编译可以参考 https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/

```
pip install FILENAME
```


下载vnpy源码，本教程基于`3.4.0`版本。

* github: https://github.com/vnpy
* gitee(国内加速): https://gitee.com/mirrors/vn-py

源码下载后在CMD进入项目根目录，运行`install.bat`将vnpy安装到本地python环境。
此方法安装的vnpy框架，实际运行还需要安装其他组件，
相关代码可以在https://github.com/vnpy的仓库下找到，也可以根据命名从pip仓库直接下载，
下面是主要使用的模块。

```txt
vnpy_ctastrategy
vnpy_ctabacktester
vnpy_spreadtrading
vnpy_algotrading
vnpy_optionmaster
vnpy_portfoliostrategy
vnpy_scripttrader
vnpy_chartwizard
vnpy_rpcservice
vnpy_excelrtd
vnpy_datamanager
vnpy_datarecorder
vnpy_riskmanager
vnpy_webtrader
vnpy_portfoliomanager
vnpy_paperaccount
```





