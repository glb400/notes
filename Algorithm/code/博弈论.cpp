SG函数和SG定理【详解】
在介绍SG函数和SG定理之前我们先介绍介绍必胜点与必败点吧.

必胜点和必败点的概念：
       P点：必败点，换而言之，就是谁处于此位置，则在双方操作正确的情况下必败。
       N点：必胜点，处于此情况下，双方操作均正确的情况下必胜。
必胜点和必败点的性质：
        1、所有终结点是 必败点 P 。（我们以此为基本前提进行推理，换句话说，我们以此为假设）
        2、从任何必胜点N 操作，至少有一种方式可以进入必败点 P。
        3、无论如何操作，必败点P 都只能进入 必胜点 N。
我们研究必胜点和必败点的目的时间为题进行简化，有助于我们的分析。通常我们分析必胜点和必败点都是以终结点进行逆序分析。我们以hdu 1847 Good Luck in CET-4 Everybody!为例：
当 n = 0 时，显然为必败点，因为此时你已经无法进行操作了
当 n = 1 时，因为你一次就可以拿完所有牌，故此时为必胜点
当 n = 2 时，也是一次就可以拿完，故此时为必胜点
当 n = 3 时，要么就是剩一张要么剩两张，无论怎么取对方都将面对必胜点，故这一点为必败点。
以此类推，最后你就可以得到；
      n    ：   0    1    2    3    4   5    6 ...
position：  P    N   N    P   N   N   P ...
你发现了什么没有，对，他们就是成有规律，使用了 P/N来分析，有没有觉得问题变简单了。
现在给你一个稍微复杂一点点的： hdu 2147 kiki's game
        现在我们就来介绍今天的主角吧。组合游戏的和通常是很复杂的，但是有一种新工具，可以使组合问题变得简单————SG函数和SG定理。

Sprague-Grundy定理（SG定理）：

        游戏和的SG函数等于各个游戏SG函数的Nim和。这样就可以将每一个子游戏分而治之，从而简化了问题。而Bouton定理就是Sprague-Grundy定理在Nim游戏中的直接应用，因为单堆的Nim游戏 SG函数满足 SG(x) = x。对博弈不是很清楚的请参照http://www.cnblogs.com/ECJTUACM-873284962/p/6398385.html进行进一步理解。

SG函数：

        首先定义mex(minimal excludant)运算，这是施加于一个集合的运算，表示最小的不属于这个集合的非负整数。例如mex{0,1,2,4}=3、mex{2,3,5}=0、mex{}=0。

        对于任意状态 x ， 定义 SG(x) = mex(S),其中 S 是 x 后继状态的SG函数值的集合。如 x 有三个后继状态分别为 SG(a),SG(b),SG(c)，那么SG(x) = mex{SG(a),SG(b),SG(c)}。 这样 集合S 的终态必然是空集，所以SG函数的终态为 SG(x) = 0,当且仅当 x 为必败点P时。

【实例】取石子问题

有1堆n个的石子，每次只能取{ 1, 3, 4 }个石子，先取完石子者胜利，那么各个数的SG值为多少？

SG[0]=0，f[]={1,3,4},

x=1 时，可以取走1 - f{1}个石子，剩余{0}个，所以 SG[1] = mex{ SG[0] }= mex{0} = 1;

x=2 时，可以取走2 - f{1}个石子，剩余{1}个，所以 SG[2] = mex{ SG[1] }= mex{1} = 0;

x=3 时，可以取走3 - f{1,3}个石子，剩余{2,0}个，所以 SG[3] = mex{SG[2],SG[0]} = mex{0,0} =1;

x=4 时，可以取走4-  f{1,3,4}个石子，剩余{3,1,0}个，所以 SG[4] = mex{SG[3],SG[1],SG[0]} = mex{1,1,0} = 2;

x=5 时，可以取走5 - f{1,3,4}个石子，剩余{4,2,1}个，所以SG[5] = mex{SG[4],SG[2],SG[1]} =mex{2,0,1} = 3;

以此类推.....

   x        0  1  2  3  4  5  6  7  8....

SG[x]    0  1  0  1  2  3  2  0  1....

由上述实例我们就可以得到SG函数值求解步骤，那么计算1~n的SG函数值步骤如下：

1、使用 数组f 将 可改变当前状态 的方式记录下来。

2、然后我们使用 另一个数组 将当前状态x 的后继状态标记。

3、最后模拟mex运算，也就是我们在标记值中 搜索 未被标记值 的最小值，将其赋值给SG(x)。

4、我们不断的重复 2 - 3 的步骤，就完成了 计算1~n 的函数值。

代码实现如下：
 1 //f[N]:可改变当前状态的方式，N为方式的种类，f[N]要在getSG之前先预处理
 2 //SG[]:0~n的SG函数值
 3 //S[]:为x后继状态的集合
 4 int f[N],SG[MAXN],S[MAXN];
 5 void  getSG(int n){
 6     int i,j;
 7     memset(SG,0,sizeof(SG));
 8     //因为SG[0]始终等于0，所以i从1开始
 9     for(i = 1; i <= n; i++){
10         //每一次都要将上一状态 的 后继集合 重置
11         memset(S,0,sizeof(S));
12         for(j = 0; f[j] <= i && j <= N; j++)
13             S[SG[i-f[j]]] = 1;  //将后继状态的SG函数值进行标记
14         for(j = 0;; j++) if(!S[j]){   //查询当前后继状态SG值中最小的非零值
15             SG[i] = j;
16             break;
17         }
18     }
19 }
hdu 1848
 1 #include <stdio.h>
 2 #include <string.h>
 3 #define MAXN 1000 + 10
 4 #define N 20
 5 int f[N],SG[MAXN],S[MAXN];
 6 void getSG(int n){
 7     int i,j;
 8     memset(SG,0,sizeof(SG));
 9     for(i = 1; i <= n; i++){
10         memset(S,0,sizeof(S));
11         for(j = 0; f[j] <= i && j <= N; j++)
12             S[SG[i-f[j]]] = 1;
13         for(j = 0;;j++) if(!S[j]){
14             SG[i] = j;
15             break;
16         }
17     }
18 }
19 int main(){
20     int n,m,k;
21     f[0] = f[1] = 1;
22     for(int i = 2; i <= 16; i++)
23         f[i] = f[i-1] + f[i-2];
24     getSG(1000);
25     while(scanf("%d%d%d",&m,&n,&k),m||n||k){
26         if(SG[n]^SG[m]^SG[k]) printf("Fibo\n");
27         else printf("Nacci\n");
28     }
29     return 0;
30 } 
大家是不是还没有过瘾，那我就在给大家附上一些组合博弈的题目：

POJ 2234 Matches Game
HOJ 4388 Stone Game II
POJ 2975 Nim
HOJ 1367 A Stone Game
POJ 2505 A multiplication game
ZJU 3057 beans game
POJ 1067 取石子游戏
POJ 2484 A Funny Game
POJ 2425 A Chess Game
POJ 2960 S-Nim
POJ 1704 Georgia and Bob
POJ 1740 A New Stone Game
POJ 2068 Nim
POJ 3480 John
POJ 2348 Euclid's Game
HOJ 2645 WNim
POJ 3710 Christmas Game 
POJ 3533 Light Switching Game
