/* Makefile */

1.makefile & make 命令一起使用
2.makefile主要的五个部分
	|-显示规则：说明如何生成一个或多个目标文件（包括生成的文件，文件的依赖文件，生成的命令）
	|-隐晦规则：make的自动推导功能所执行的规则
	|-变量定义：makefile中定义的变量
	|-文件指示：makefile中引用其他makefile,指定makefile中有效部分，定义一个多行命令
	|-注释：makefile只有行注释'#'

makefile基本格式：
target ... : prerequisites ...
	command
	...
	...

target - 目标文件，可以是object file,也可以是可执行文件
prerequisites - 生成target所需要的文件或目标
command - make需要执行的命令，makefile中命令必须以\tab开头


GNU make的工作方式
1.读入主makefile(主makefile中可以引用其他makefile)
2.读入被include的其他makefile
3.初始化文件中的变量
4.推导隐晦规则，并分析所有规则
5.为所有的目标文件创建依赖关系链
6.根据依赖关系，决定哪些目标要重新生成
7.执行生成命令

## makefile初级语法
makefile规则
|-依赖关系
|-生成目标的方法
语法有以下2种：
target ... : prerequisites ...
	command
	...
或者
target ... : prerequisites ; command
	command
	...


## 通配符
1.* : 表示任意一个或多个字符
2.? : 表示任意一个字符
3.[...] : [abcd]表示a,b,c,d种任意一个字符，[^abcd]表示除a,b,c,d以外的字符，[0-9]表示0-9中任意一个数字
4.~ ： 表示用户的home目录

## 路径搜索
当一个makefle中涉及到大量源文件时（这些源文件极有可能不在同一个目录中）
这时，最好将源文件的路径明确在makefile中，以便编译时查找
此时使用VPATH
指定VPATH后，如果当前目录中没有找到相应文件或依赖文件，再到VPATH指定的路径中查找
VPATH：
vpath <directories>            :: 当前目录中找不到文件时, 就从<directories>中搜索
vpath <pattern> <directories>  :: 符合<pattern>格式的文件, 就从<directories>中搜索
vpath <pattern>                :: 清除符合<pattern>格式的文件搜索路径
vpath                          :: 清除所有已经设置好的文件路径
I.E.
# 示例1 - 当前目录中找不到文件时, 按顺序从 src目录 ../parent-dir目录中查找文件
VPATH src:../parent-dir   
# 示例2 - .h结尾的文件都从 ./header 目录中查找
VPATH %.h ./header
# 示例3 - 清除示例2中设置的规则
VPATH %.h
# 示例4 - 清除所有VPATH的设置
VPATH

## 变量
1.变量定义（= or :=）
OBJS = programA.o programB.o
OBJS-ADD = $(OBJS) programC.o
# 或者
OBJS := programA.o programB.o
OBJS-ADD := $(OBJS) programC.o
其中 = 和 := 的区别在于, := 只能使用前面定义好的变量, = 可以使用后面定义的变量
I.E.
# makefile 
OBJS2 = $(OBJS1) programC.o
OBJS1 = programA.o programB.o

all:
	@echo $(OBJS2)a

$ make
2.变量替换$

linux shell命令
$0	当前脚本的文件名
$n	传递给脚本或函数的参数。n 是一个数字，表示第几个参数。例如，第一个参数是$1，第二个参数是$2。
$#	传递给脚本或函数的参数个数。
$*	传递给脚本或函数的所有参数。
$@	传递给脚本或函数的所有参数。被双引号(" ")包含时，与 $* 稍有不同，下面将会讲到。
$?	上个命令的退出状态，或函数的返回值。
$$	当前Shell进程ID。对于 Shell 脚本，就是这些脚本所在的进程ID。

$* 和 $@ 的区别
$* 和 $@ 都表示传递给函数或脚本的所有参数，不被双引号(" ")包含时，都以"$1" "$2" … "$n" 的形式输出所有参数。

但是当它们被双引号(" ")包含时，"$*" 会将所有的参数作为一个整体，以"$1 $2 … $n"的形式输出所有参数；"$@" 会将各个参数分开，以"$1" "$2" … "$n" 的形式输出所有参数。