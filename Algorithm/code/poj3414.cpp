#pragma comment(linker, “/STACK:1024000000,1024000000”) 
#include <iostream>
#include <cstring>
#include <vector>
#include <set>
#include <map>
#include <queue>
#include <stack>
#include <string>
#include <cmath>
#include <cstdio>
#include <algorithm>
#include <stdlib.h>
#include <ctype.h>
#include <sstream>
#include <fstream>
using namespace std;
int A,B,C;
const int maxn=1010;
int vis[maxn*maxn];
struct point{
	int x,y,dep;
	point * pre;
	int mark;
};
string marks[10];
vector<point> rec;
int cnt=0;
int depth=0;
point final;
bool bfs(){
	if(C>max(A,B))
	return 0;
	queue<point> que;
	point start;
	start.x=0;
	start.y=0;
	start.dep=0;
	start.pre=NULL;
	que.push(start);
	while(!que.empty()){
	point node=que.front();
	que.pop();
	rec.push_back(node);
	
	int tmpx=node.x;
	int tmpy=node.y;
	int tmpd=node.dep;
	point * p=node.pre;
	int tmpmark = node.mark;
	if(tmpx==C||tmpy==C)
	{
		final.x=tmpx;
		final.y=tmpy;
		final.dep=tmpd;
		final.pre=p;
		final.mark=tmpmark;
		cout << tmpd << endl;
		return 1;
	}
	vis[tmpx*maxn+tmpy]=1;
	for(int i=0;i<6;i++)
	{
		if(i==0)
		{
			if(vis[A*maxn+tmpy])
				continue;
			point next;
			next.x=A;
			next.y=tmpy;
			next.dep=tmpd+1;
			next.pre=&rec[cnt];
			next.mark=0;
			que.push(next);
		}
		else if(i==1)
		{
			if(vis[tmpx*maxn+B])
				continue;
			point next;
			next.x=tmpx;
			next.y=B;
			next.dep=tmpd+1;
			next.pre=&rec[cnt];
			next.mark=1;
			que.push(next);
		}
		else if(i==2)
		{
			if(vis[0*maxn+tmpy])
				continue;
			point next;
			next.x=0;
			next.y=tmpy;
			next.dep=tmpd+1;
			next.pre=&rec[cnt];
			next.mark=2;
			que.push(next);
		}
		else if(i==3)
		{
			if(vis[tmpx*maxn+0])
				continue;
			point next;
			next.x=tmpx;
			next.y=0;
			next.dep=tmpd+1;
			next.pre=&rec[cnt];
			next.mark=3;
			que.push(next);
		}
		else if(i==4)
		{
			if(tmpx>(B-tmpy))
			{
				if(vis[(tmpx-(B-tmpy))*maxn+B])
					continue;
				point next;
				next.x=(tmpx-(B-tmpy));
				next.y=B;
				next.dep=tmpd+1;
				next.pre=&rec[cnt];
				next.mark=4;
				que.push(next);
			}
			else
			{
				if(vis[0*maxn+tmpx+tmpy])
					continue;
				point next;
				next.x=0;
				next.y=tmpx+tmpy;
				next.dep=tmpd+1;
				next.pre=&rec[cnt];
				next.mark=4;
				que.push(next);				
			}
		}
		else if(i==5)
		{
			if(tmpy>(A-tmpx))
			{
				if(vis[A*maxn+tmpy-(A-tmpx)])
					continue;
				point next;
				next.x=A;
				next.y=tmpy-(A-tmpx);
				next.dep=tmpd+1;
				next.pre=&rec[cnt];
				next.mark=5;
				que.push(next);
			}
			else
			{
				if(vis[(tmpx+tmpy)*maxn+0])
					continue;
				point next;
				next.x=tmpx+tmpy;
				next.y=0;
				next.dep=tmpd+1;
				next.pre=&rec[cnt];
				next.mark=5;
				que.push(next);
			}
		}
	}
	cnt++;
	}
	return 0;
}
void output(point * ptr){
	if(ptr==NULL)
		return;
	if(ptr!=NULL){
		output((*ptr).pre);
	if(ptr->pre!=NULL)
	cout <<marks[ptr->mark]<<endl;
	}
}
int main(){
	marks[0]="FILL(1)";
	marks[1]="FILL(2)";
	marks[2]="DROP(1)";
	marks[3]="DROP(2)";
	marks[4]="POUR(1,2)";
	marks[5]="POUR(2,1)";
	while(scanf("%d%d%d",&A,&B,&C)!=EOF){
	memset(vis,0,sizeof vis);
	rec.clear();
	final.x=0;
	final.y=0;
	final.dep=0;
	final.mark=0;
	final.pre=NULL;
	cnt=0;
	depth=0;
	if(A==C)
	{
		cout<<1<<endl<<"FILL(1)"<<endl; 
	}
	else if(B==C)
	{
		cout<<1<<endl<<"FILL(2)"<<endl;
	}
	else {
		if(bfs())
			output(&final);
		else
			cout << "impossible" << endl;
		}
	}
}

