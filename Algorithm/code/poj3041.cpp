#include<iostream>
#include<stdio.h>
#include<string.h>
#define Max 505
using namespace std;
int a[Max][Max];
int visit[Max];
int match[Max];
int N,K;
int path(int u)
{
    int v;
    for(v=1;v<=N;v++)
    {
          if(a[u][v] && !visit[v])
          {
                visit[v] = 1;
                if(match[v] == -1 || path(match[v]))
                {
                            match[v] = u;
                            return 1;
                }  
          }
    }
    return 0;
}
int main()
{
                                                                                                          
      int i,j,k,count;
      scanf("%d %d",&N,&K);
                                                                                                          
      memset(a,0,sizeof(a));
      memset(match,-1,sizeof(match));
      count = 0;
      for(i=1;i<=K;i++)
      {
           scanf("%d %d",&j,&k);
           a[j][k] = 1;
      }
                                                                                                            
      for(i=1;i<=N;i++)
      {
             memset(visit,0,sizeof(visit));
             if(path(i))
               count++;
      }
      printf("%d\n",count);
                                                                                                          
      return 0;
}
