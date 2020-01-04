#include <cstdio>
#include <iostream>
#include <cstring>
#include<vector>
#include <queue>
#include<algorithm>
using namespace std;
int N,M;
const int maxN=202;
const int maxM=202;
const int maxC=10000005;
const int INF =0x3f3f3f3f;
typedef long long ll;
int pre[maxN];
int vis[maxN];
int mp[maxN][maxN];
bool bfs(int start,int end){
	memset(vis,0,sizeof vis);
	memset(pre,0,sizeof pre);
	queue<int> que;
	que.push(start);
	pre[start]=start;
	while(!que.empty()){
		int front=que.front();
		que.pop();
		vis[front]=1;
		for(int i=1;i<=M;i++)
			if(!vis[i]&&mp[front][i]>0)
			{
				pre[i]=front;
				que.push(i);
			}
	}
	if(vis[end])
		return 1;
	else
		return 0;
}
int main()
{
	while(~scanf("%d%d",&N,&M)){
	memset(vis,0,sizeof vis);
	memset(pre,-1,sizeof pre);
	memset(mp,0,sizeof mp);
	
	for(int i=0;i<N;i++)
	{
		int u,v,c;
		scanf("%d%d%d",&u,&v,&c);
		if(!mp[u][v])
		mp[u][v]=c;
		else
		mp[u][v]+=c; 
	}
	int ans=0;
	while(bfs(1,M)){
		int Max=INF;
		for(int i=M;i!=1;i=pre[i])
		{
			Max=min(Max,mp[pre[i]][i]);
		}
		for(int i=M;i!=1;i=pre[i])
		{
			mp[pre[i]][i]-=Max;
			mp[i][pre[i]]+=Max;
		}
		ans+=Max;
	}
	cout<<ans<<endl;
	}
	return 0;
}
