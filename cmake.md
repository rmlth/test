# Cmake实践指南
## 配置CMakeLists（内部构建）
```bash
# 设置 CMake 最低版本要求
cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(main)

# 设置C++标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 定义源文件列表
set(SRC_LIST
   main.cpp
    
)



# 添加可执行文件
# 包含 main.cpp 和 src/other_file.cpp
# 如果有更多的源文件，可以继续添加
add_executable(hello main.cpp src/other_file.cpp)
```
### projiect的作用
* 设置项目名称：
该名称用于在构建过程中标识项目，并且可以在后续的 CMake 脚本中引用。
* 定义项目使用的编程语言：
默认情况下，CMake 会根据后续命令（如 add_executable 或 add_library）中的源文件类型自动检测项目使用的编程语言。
* 初始化一些全局变量：
例如 PROJECT_NAME、PROJECT_SOURCE_DIR 和 PROJECT_BINARY_DIR，这些变量在构建过程中可以用来引用项目的名称、源目录和构建目录。
#### 示例 CMakeLists.txt
```bash
cmake_minimum_required(VERSION 3.10)

# 定义项目名称
project(hell0)

# 显示项目名称
message("Project name: ${PROJECT_NAME}")

# 添加可执行文件
add_executable(${PROJECT_NAME} main.c)


```
### 关于语法的疑惑
```bash cmake 的语法还是比较灵活而且考虑到各种情况，比如
* SET(SRC_LIST main.c)也可以写成 SET(SRC_LIST “main.c”)
是没有区别的，但是假设一个源文件的文件名是 fu nc.c(文件名中间包含了空格)。
这时候就必须使用双引号，如果写成了 SET(SRC_LIST fu nc.c)，就会出现错误，提示
你找不到 fu 文件和 nc.c 文件。这种情况，就必须写成:
SET(SRC_LIST “fu nc.c”)
* 此外，你可以可以忽略掉 source 列表中的源文件后缀，比如可以写成
ADD_EXECUTABLE(t1 main)，cmake 会自动的在本目录查找 main.c 或者 main.cpp
等，当然，最好不要偷这个懒，以免这个目录确实存在一个 main.c 一个 main.
* 同时参数也可以使用分号来进行分割。
下面的例子也是合法的：
ADD_EXECUTABLE(t1 main.c t1.c)可以写成 ADD_EXECUTABLE(t1
main.c;t1.c).
我们只需要在编写 CMakeLists.txt 时注意形成统一的风格即可。
```
### 清理工程
```bash 跟经典的 autotools 系列工具一样，运行:
make clean
即可对构建结果进行清理。
```
## 配置CMakeLists（外部构建）
```bash 1，首先，请清除 t1 目录中除 main.c CmakeLists.txt 之外的所有中间文件，最关键
的是 CMakeCache.txt。
2，在 t1 目录中建立 build 目录，当然你也可以在任何地方建立 build 目录，不一定必
须在工程目录中。
3，进入 build 目录，运行 cmake ..(注意,..代表父目录，因为父目录存在我们需要的
CMakeLists.txt，如果你在其他地方建立了 build 目录，需要运行 cmake <工程的全
路径>)，查看一下 build 目录，就会发现了生成了编译需要的 Makefile 以及其他的中间
文件.
4，运行 make 构建工程，就会在当前目录(build 目录)中获得目标文件 hello。
上述过程就是所谓的 out-of-source 外部编译，一个最大的好处是，对于原有的工程没
有任何影响，所有动作全部发生在编译目录。通过这一点，也足以说服我们全部采用外部编
译方式构建工程。
```
***这里需要特别注意的是：
通过外部编译进行工程构建，HELLO_SOURCE_DIR 仍然指代工程路径，即
/backup/cmake/t1
而 HELLO_BINARY_DIR 则指代编译路径，即/backup/cmake/t1/build***    


