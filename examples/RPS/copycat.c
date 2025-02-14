#include<stdio.h>
#include<time.h>
#include<stdlib.h>

int main() {
	unsigned long long roundcount,move;
	char moves[3]={'R','P','S'},other;
	scanf("%llu",&roundcount);
	srand(time(NULL));
	move=rand()%3;
	while(roundcount--) {
		printf("%c\n",moves[move]);
		fflush(stdout);
		scanf("\n%c",&other);
		for(int i=0;i<3;i++)
			if(moves[i]==other) {
				move=i;
				break;
			}
	}
}