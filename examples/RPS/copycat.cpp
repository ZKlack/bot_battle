#include<iostream>
#include<time.h>
#include<random>

using namespace std;

int main() {
	unsigned long long roundcount,move;
	cin>>roundcount;
	char moves[3]={'R','P','S'},other;
	srand(time(nullptr));
	move=rand()%3;
	while(roundcount--) {
		cout<<moves[move]<<'\n';
		cin>>other;
		for(int i=0;i<4;i++)
			if(i==3)
				return -1;
			else if(moves[i]==other) {
				move = i;
				break;
			}
	}
}
