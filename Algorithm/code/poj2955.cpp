#include <cstdio>
#include <queue>
#include <cstring>
#include <algorithm>
using namespace std;
#define mst(a,b) memset((a),(b),sizeof(a))
#define rush() int T;scanf("%d",&T);while(T--)
 
typedef long long ll;
const int maxn = 105;
const ll mod = 1e9+7;
const ll INF = 1e18;
const double eps = 1e-9;
 
char s[maxn];
int dp[maxn][maxn];
 
int main()
{
    while(~scanf("%s",s+1)&&s[1]!='e')
    {
        int n=strlen(s+1);
        mst(dp,0);
        for(int len=2;len<=n;len++)
        for(int i=1;i<=n;i++)
        {
            int j=i+len-1;
            if(j>n) break;
            if(s[i]=='('&&s[j]==')'||s[i]=='['&&s[j]==']')
            {
                dp[i][j]=dp[i+1][j-1]+2;
            }
            for(int k=i;k<j;k++)
            {
                dp[i][j]=max(dp[i][j],dp[i][k]+dp[k][j]);
            }
        }
        printf("%d\n",dp[1][n]);
    }
    return 0;
}

