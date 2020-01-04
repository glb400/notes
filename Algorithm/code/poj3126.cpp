#include<iostream>
#include<queue>
#include<cstring>
using namespace std;
#define Max 10000+5
bool vis[Max], is_prime[Max];
int d[Max];
int T, a, b;
void get_prime()    //打素数表
{
	memset(is_prime, true, sizeof is_prime);
	for (int i = 2; i*i < Max; i++)
		if (is_prime[i])
			for (int j = 2 * i; j < Max; j += i)
				is_prime[j] = false;
	return;
}
int judge(int v,int i,int j)
{
	if (!is_prime[v]) return 0;   //不是素数返回0
	if (i == 1 && j == 0) return 0;  //首位为0返回0
	char s[6] = "\0";
	sprintf(s, "%d", v);
	s[i - 1] = j + '0';   //将第i位改成j
	sscanf(s, "%d", &v);
	if (!vis[v]) return v;   //返回改变后的值
	return 0;
}
int bfs()
{
	queue<int> q; 
	q.push(a);
	vis[a] = 1;
	while (!q.empty())
	{
		int v = q.front();
		q.pop();
		for (int i = 1; i <= 4; i++)   //枚举40个入口,分别为第i位改成j
			for (int j = 0; j <= 9; j++)
			{
				int t = judge(v, i, j);
				if (t)
				{
					vis[t] = 1;
					d[t] = d[v] + 1;
					q.push(t);
					if (t == b) return d[t];
				}
			}
	}
	return -1;
}
int main()
{
	scanf("%d", &T);
	get_prime();
	while (T--)
	{
		memset(vis, false, sizeof vis);
		memset(d, false, sizeof d);
		scanf("%d%d", &a, &b);
		if (a == b) printf("0\n");
		else
		{
			int ans = bfs();
			if (ans == -1) printf("Impossible\n");
			else printf("%d\n", ans);
		}
	}
	return 0;
}

