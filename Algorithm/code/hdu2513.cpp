#include <cstdio>
#include <cmath>
#include <queue>
#include <cstring>
#include <algorithm>
using namespace std;
#define mst(a,b) memset((a),(b),sizeof(a))
#define rush() int T;scanf("%d",&T);while(T--)
 
typedef long long ll;
const int maxn = 25;
const ll mod = 1e9+7;
const int INF = 0x3f3f3f3f;
const double eps = 1e-9;
 
int n,m,k;
int dp[maxn][maxn][maxn][maxn];
bool flag[maxn][maxn];     //记录某个点是否有樱桃
 
int fun(int a,int b,int c,int d)
{
    if(dp[a][b][c][d]!=-1)  //已经计算过
    {
        return dp[a][b][c][d];
    }
    int cnt=0;
    for(int i=a;i<=c;i++)
    for(int j=b;j<=d;j++)
    {
        if(flag[i][j])
            cnt++;
    }
    if(cnt<=1)            //区域内樱桃个数小于2，那么不用切割
    {
        return dp[a][b][c][d]=0;
    }
    int Min=INF;
    for(int i=a;i<c;i++)  //横着切
    {
        Min=min(Min,fun(a,b,i,d)+fun(i+1,b,c,d)+(d-b+1));
    }
    for(int i=b;i<d;i++)  //竖着切
    {
        Min=min(Min,fun(a,b,c,i)+fun(a,i+1,c,d)+(c-a+1));
    }
    return dp[a][b][c][d]=Min;
}
 
int main()
{
    int cas=1;
    int x,y;
    while(~scanf("%d%d%d",&n,&m,&k))
    {
        mst(dp,-1);
        mst(flag,0);
        for(int i=0;i<k;i++)
        {
            scanf("%d%d",&x,&y);
            flag[x][y]=1;
        }
        int ans=fun(1,1,n,m);
        printf("Case %d: %d\n",cas++,ans);
    }
    return 0;
}

