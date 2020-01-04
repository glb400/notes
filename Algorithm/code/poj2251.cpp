#include <cstdio>
#include <iostream>
#include <cstring>
#include <queue>
using namespace std;
const int maxn=33;
int L,R,C;
int map[maxn][maxn][maxn];
int vis[maxn][maxn][maxn];
struct direct{
	int x,y,z;
	// direct(){
	// }
	// direct(int _x,int _y,int _z):x(_x),y(_y),z(_z){
	// }
};
struct point{
	int x,y,z;
	int l;
	// point(){
	// }
	// point(int _x,int _y,int _z,int _l):x(_x),y(_y),z(_z),l(_l){
	// }
};
int depth;
int sx,sy,sz;
int ex,ey,ez;
direct dir[6];
bool bfs(){
	queue<point> que;
	point start;
	start.x=sx;
	start.y=sy;
	start.z=sz;
	start.l=0;
	que.push(start);
	while(!que.empty()){
		point temp=que.front();
		que.pop();
		int tmpx=temp.x;
		int tmpy=temp.y;
		int tmpz=temp.z;
		if(tmpx==ex&&tmpy==ey&&tmpz==ez)
			{
				depth=temp.l;
				return 1;
			}
		int level=temp.l;
//		vis[tmpx][tmpy][tmpz]=1;
		for(int i=0;i<6;i++){
			if(tmpx+dir[i].x>=0&&tmpx+dir[i].x<L&&tmpy+dir[i].y>=0
			&&tmpy+dir[i].y<R&&tmpz+dir[i].z>=0&&tmpz+dir[i].z<C&&
			!vis[tmpx+dir[i].x][tmpy+dir[i].y][tmpz+dir[i].z]&&
			map[tmpx+dir[i].x][tmpy+dir[i].y][tmpz+dir[i].z])
			{
			point node;
			node.x=tmpx+dir[i].x;
			node.y=tmpy+dir[i].y;
			node.z=tmpz+dir[i].z;
			node.l=level+1;
			que.push(node);
			vis[node.x][node.y][node.z]=1;
			}
		}
	}
	return 0;
}
int main(){
	dir[0].x=0;
	dir[0].y=0;
	dir[0].z=1;
	
	dir[1].x=0;
	dir[1].y=0;
	dir[1].z=-1;
	
	dir[2].x=0;
	dir[2].y=1;
	dir[2].z=0;
	
	dir[3].x=0;
	dir[3].y=-1;
	dir[3].z=0;
	
	dir[4].x=1;
	dir[4].y=0;
	dir[4].z=0;
	
	dir[5].x=-1;
	dir[5].y=0;
	dir[5].z=0;
	
	
	while(~scanf("%d%d%d",&L,&R,&C)&&L&&R&&C){
		memset(vis,0,sizeof vis);
		depth=0;
		for(int i=0;i<L;i++){
			for(int j=0;j<R;j++)
			{
				for(int k=0;k<C;k++)
				{
					
					char s;
					cin>>s;
					if(s=='#')
					{
						map[i][j][k]=0;
					}
					else if(s=='.')
						map[i][j][k]=1;
					else if(s=='S')
					{
						map[i][j][k]=1;
						sx=i;
						sy=j;
						sz=k;
					}
					else if(s=='E')
					{
						map[i][j][k]=1;
						ex=i;
						ey=j;
						ez=k;
					}
				}
			}
		}
		if(bfs())
			cout << "Escaped in "<< depth << " minute(s)." << endl;
		else
			cout << "Trapped!"<<endl;

	}
	return 0;
}
