#include <iostream>
#include <cstdlib>
#include <memory>
#include <string>
#include <cstring>
using namespace std;

char orilights[5];
char lights[5];
char result[5];

int GetBit(char c,int i){
	return (c >> i) & 1;// get the ith light's condition.
}

void SetBit(char & c,int i, int v){
	if (v){
		c |= (1 << i); 
	}
	else
		c &= ~(1 << i); 
}

void FlipBit(char & c,int i){
	c ^= (1 << i);
}

void OutputResult(int t,char result[]){
	cout << "PUZZLE #" << t << endl;
	for(int i = 0;i < 5; ++i){
		for(int j = 0; j < 6;  ++j){
			cout << GetBit(result[i],j);
			if(j < 5)
			cout << " ";
		}
		cout << endl;
	}
}

int main(){
	int T;
	cin >> T;
	for(int t = 1; t <= T; ++t){
		for(int i = 0;i < 5; ++i)
			for(int j = 0;j < 6; ++j){
				int s;
				cin >> s;
				SetBit(orilights[i],j,s);
			}
		for(int n = 0;n < 64; ++n){
			int switchs = n;
			memcpy(lights,orilights,sizeof(orilights));
			for(int i = 0;i < 5; ++i){
				result[i] = switchs;
				for(int j = 0;j < 6; j++){
					if(GetBit(switchs,j)){
						if(j > 0)
							FlipBit(lights[i],j-1);
						FlipBit(lights[i],j);
						if(j < 5)
							FlipBit(lights[i],j+1);
					}
				}
				//if(i < 5)
					lights[i+1] ^= switchs;
				switchs = lights[i];
			}
			if(lights[4] == 0){
				OutputResult(t,result);
				break;
			}
		}
	}
	return 0;
}
