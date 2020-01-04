#include <iostream>
#include <cstdio>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <cstring>

using namespace std;

int dp[10][10];

void init()
{
    for(int i=0; i<10; i++)
        dp[1][i]=1;
    dp[1][4]=0;

    for(int i=2; i<=7; i++)
    {
        for(int j=0; j<10; j++)
        {
            for(int k=0; k<10; k++)
            {
                if(j!=4&&!(j==6&&k==2))
                    dp[i][j]  += dp[i-1][k];
            }
        }
    }
}

int solve(int n)
{
    int digit[10];
    int len=0;
    int ans=0;
    while(n>0)
    {
        digit[++len]=n%10;
        n/=10;
    }
    digit[len+1]=0;
    for(int i=len; i>0; i--)
    {
        for(int j=0; j<digit[i]; j++)
        {
            if(j!=4&&!(digit[i+1]==6&&j==2))
                ans+=dp[i][j];
        }
        if(digit[i]==4||(digit[i]==2&&digit[i+1]==6))
            break;
    }
    return ans;
}

int main()
{
    init();
    int l,r;
    while(cin>>l>>r)
    {
        if(l+r==0)
            break;
        else
            cout<<solve(r+1)-solve(l)<<endl;
    }
    return 0;
}

