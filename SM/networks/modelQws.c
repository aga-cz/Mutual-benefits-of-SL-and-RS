#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <string.h>


#define frand() ((double) rand()/(RAND_MAX+1.0))


double ran_expo(double lambda){
    double u;

    u = rand() / (RAND_MAX + 1.0);

    return -log(1.- u) / lambda;
}


int gen_pay(double lambda){
    double x;
    x = ran_expo(lambda);
    return round(2.0*x*x);
}



int main(int argc, char *argv[]){
srand(time(0));

int N, X, L, Cs, Ci, Cr, Q, k;
double pWS, r;

N = atoi(argv[1]); // number of agents
int T; // number of time steps
T=20*N;
pWS = atof(argv[2]); // p in WS net
X = atoi(argv[3]); // number of items
L = atoi(argv[4]); // budget of an agent
Cs = atoi(argv[5]); // cost of social learning
Ci = atoi(argv[6]); // cost of innovation
Cr = atoi(argv[7]); // cost of recommendation 
r = atof(argv[8]); // prob of recommendation
Q = atoi(argv[9]); // number of system's realizations 
k = atoi(argv[10]); // number of neighbors

char *out_dir_t;
out_dir_t = argv[11];

//char *out_dir_d;
//out_dir_d = argv[11];



int iter;
int **AA; //adjacency matrix
AA = (int**) malloc(N * sizeof(int*));
memset(AA,0,N*sizeof(int*));


for(iter=0;iter<N;iter++){
AA[iter] = (int*) malloc(N * sizeof(int));
memset(AA[iter],0,N * sizeof(int));
}


int *IP; //items' payoffs
IP = (int*) malloc(T * sizeof(int*));
memset(IP,0,T*sizeof(int));


int **UI; //users' items
UI = (int**) malloc(N * sizeof(int*));
memset(UI,0,N*sizeof(int*));

for(iter=0;iter<N;iter++){
UI[iter] = (int*) malloc(T * sizeof(int));
memset(UI[iter],0,T * sizeof(int));
}

int *UB; //users' budget
UB = (int*) malloc(N * sizeof(int));
memset(UB,L,N*sizeof(int));

int *UL; //users' level
UL = (int*) malloc(N * sizeof(int));
memset(UL,0,N*sizeof(int));

int *UP; //users' payoff
UP = (int*) malloc(N * sizeof(int));
memset(UP,0,N*sizeof(int));


int *Xa; //users' level
Xa = (int*) malloc(X * sizeof(int));
memset(Xa,0,X*sizeof(int));

double los;
int los_pay;

int lvl, item, user, i, j, step, maxP, maxL, maxU;




//// initialize tables
int *tot_pay; 
tot_pay = (int*) malloc(T * sizeof(int));
memset(tot_pay,0,T*sizeof(int));

int *tot_lvl; 
tot_lvl = (int*) malloc(T * sizeof(int));
memset(tot_lvl,0,T*sizeof(int));

int *tot_bud; 
tot_bud = (int*) malloc(T * sizeof(int));
memset(tot_bud,0,T*sizeof(int));

int *max_pay; 
max_pay = (int*) malloc(T * sizeof(int));
memset(max_pay,0,T*sizeof(int));

int *max_lvl; 
max_lvl = (int*) malloc(T * sizeof(int));
memset(max_lvl,0,T*sizeof(int));

int *max_pos_pay; 
max_pos_pay = (int*) malloc(T * sizeof(int));
memset(max_pos_pay,0,T*sizeof(int));

int *n_items; 
n_items = (int*) malloc(T * sizeof(int));
memset(n_items,0,T*sizeof(int));

int *n_inn; 
n_inn = (int*) malloc(T * sizeof(int));
memset(n_inn,0,T*sizeof(int));

int *n_sl; 
n_sl = (int*) malloc(T * sizeof(int));
memset(n_sl,0,T*sizeof(int));

int *n_rs; 
n_rs = (int*) malloc(T * sizeof(int));
memset(n_rs,0,T*sizeof(int));


int max_pay_t, max_lvl_t, n_items_t;
int n_inn_t, n_sl_t, n_rs_t;
int if_sl_or_rs;

int iq;



for(iq=0;iq<Q;iq++){
max_pay_t=0;
max_lvl_t=0;
n_items_t=0;
n_inn_t=0;
n_sl_t=0;
n_rs_t=0;

//initialization of budget&level
//initialization of social network
for(i=0;i<N;i++){
UB[i]=L;
UL[i]=0;
UP[i]=0;
for(j=0;j<i;j++){
		AA[i][j]=0; AA[j][i]=0;
	}
}


//initialization of items' payoffs (-1 if item was not discovered yet)
for(item=0;item<X;item++){
Xa[item]=0;
}

for(lvl=0;lvl<T;lvl++){
	IP[lvl]=-1;
}

//initialization of users' items (-1 if no item on this level)
for(i=0;i<N;i++){
for(item=0;item<T;item++){
	UI[i][item]=-1;
}}

//initialization of budget&level
//initialization of social network

//// build WS network
 // Create ring lattice: each node connects to k/2 nearest neighbors
    for (i = 0; i < N; i++){
        for(j = 1; j <= k / 2; j++){
            int neighbor = (i + j) % N;  // Wrap around for ring topology
            AA[i][neighbor] = 1;
            AA[neighbor][i] = 1;
        }
    }

    // Rewire edges with probability pWS
    for(i = 0; i < N; i++){
        for (j = 1; j <= k / 2; j++){
            int neighbor = (i + j) % N;  // Original neighbor
            los = frand();
            if(los < pWS){  // Rewire with probability pWS
                int new_neighbor;
                do {
                    new_neighbor = rand() % N;  // Random new neighbor
                } while (new_neighbor == i || AA[i][new_neighbor] == 1);  // Avoid self-loops and duplicate edges
                AA[i][neighbor] = 0;  // Remove original edge
                AA[neighbor][i] = 0;
                AA[i][new_neighbor] = 1;  // Add new edge
                AA[new_neighbor][i] = 1;
            }
        }
    }
/////////////////////end of building network


for(user=0;user<N;user++){

	//innovation step
	lvl = UL[user]+1;
	UB[user]-=Ci;
		
		
		
	los_pay = gen_pay(1.0);
	if(los_pay>0){
		if(los_pay>IP[lvl]){ IP[lvl] = los_pay;}
		n_items_t++;
		n_inn_t++;
		UI[user][lvl]=los_pay;
		UL[user]+=1;
		UP[user]+=los_pay;
		
		}
	
	//end of innovation	
	
	tot_pay[0]+=UP[user];
	tot_lvl[0]+=UL[user];
	tot_bud[0]+=UB[user];
	if(UP[user]>max_pay_t){ max_pay_t=UP[user];}
	max_pay[0]+=max_pay_t;
	max_lvl[0] += 1;
	
	for(lvl=1;lvl<UL[user]+1;lvl++){
		max_pos_pay[0] += IP[lvl];
	}
	
	
	
}

n_items[0]+=n_items_t;
n_inn[0]+=n_inn_t;
n_sl[0]+=n_sl_t;
n_rs[0]+=n_rs_t;

////////////////////////time dynamics
for(step=1;step<T;step++){

	max_pay_t=0;
	max_lvl_t=0;
	
	for(user=0;user<N;user++){
	
		los = frand();
		if(los<= (double) 1.0/(double)N){ 
			UB[user]=L;
			UL[user]=0;
			UP[user]=0;
			for(i=0;i<T;i++){
				UI[user][i] = -1;
			}
		}
		
		los = frand();
		if(los<r || r==1.0){//RS
			if_sl_or_rs=0;
			if(UB[user]>=Cr){
				
				lvl=UL[user]+1;
				maxP=IP[lvl];
				
				if(maxP>0){
					UB[user]-=Cr;
					UI[user][lvl]=maxP;
					
					UL[user]+=1;
					UP[user]+=maxP;
					if_sl_or_rs=1;
					n_rs_t++;
				}
				}
				
			
		}//end RS 

		else if(los>r || r==0.0){//SL
			if_sl_or_rs=0;
			if(UB[user]>=Cs){
				
				lvl=UL[user]+1;
				maxP=-1;
				maxU=-1;
				maxL=-1;
				for(i=0;i<N;i++){
					if(i!=user){
					if(AA[user][i]==1){ 
						if(UP[i]>=maxP){
							maxP=UP[i];
							maxU=i;
							maxL=UL[i];
							}
					
					}
					}
				}

				if(maxL>=lvl){
					UB[user]-=Cs;
					item = UI[maxU][lvl]; //note that item here actually means payoff
					UI[user][lvl] = item;
					UL[user]+=1;
					
					UP[user]+=item;
					if_sl_or_rs=1;
					n_sl_t++;
				}
				}
			
			
					
		}//end SL
		
		if((if_sl_or_rs==0) && (UB[user]>=Ci)){
					//innovation step
					lvl = UL[user]+1;
					UB[user]-=Ci;
						
						
					los_pay = gen_pay(1.0);
					if(los_pay>0){
						if(los_pay>IP[lvl]){ IP[lvl] = los_pay;}
						n_items_t++;
						n_inn_t++;
						UI[user][lvl]=los_pay;
						UL[user]+=1;
						UP[user]+=los_pay;
						
						}
					//end of innovation

				}	
		

	tot_pay[step]+=UP[user];
	tot_lvl[step]+=UL[user];
	tot_bud[step]+=UB[user];
	if(UP[user]>max_pay_t){ max_pay_t=UP[user];}
	if(UL[user]>max_lvl_t){ max_lvl_t=UL[user];}
	
	
	max_pay[step]+=max_pay_t;
	max_lvl[step]+=max_lvl_t;
	

	
	}//end user loop

	
	
	for(user=0;user<N;user++){
	for(lvl=1;lvl<UL[user]+1;lvl++){
		max_pos_pay[step] += IP[lvl];
	}}

	n_items[step] += n_items_t;
	n_inn[step] += n_inn_t;
	n_sl[step] += n_sl_t;
	n_rs[step] += n_rs_t;
	

}//end time dynamics

}//end Q realizations


//fclose(plik_ft);
//free(ft);

char *rs;
rs = (char*) malloc(250 * sizeof(char));

FILE *plik_rs;

sprintf(rs, "%savg_N_%d_pWS_%.3lf_k_%d_X_%d_L_%d_Cs_%d_Ci_%d_Cr_%d_r_%.1lf__%d.csv",out_dir_t,N,pWS,k,X,L,Cs,Ci,Cr,r,Q);

plik_rs = fopen(rs,"wt");

fprintf(plik_rs, "time\tavg_payoff\tavg_level\tavg_budget\tmax_payoff\tmax_level\tmax_ach_payoff\tn_items\tinnovations\tsocial_learning\trecommendations\n");

for(step=0;step<T;step++){
fprintf(plik_rs, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n", step, (double) tot_pay[step]/N/Q, (double) tot_lvl[step]/N/Q, (double) tot_bud[step]/N/Q, (double) max_pay[step]/N/Q, (double) max_lvl[step]/N/Q, (double) max_pos_pay[step]/N/Q, (double) n_items[step]/Q, (double) n_inn[step]/Q, (double) n_sl[step]/Q, (double) n_rs[step]/Q);
}	


fclose(plik_rs);
free(rs);


/////////////////free

free(IP);

for(iter=0;iter<N;iter++){
free(UI[iter]);
free(AA[iter]);
}

free(UI);
free(AA);

free(UB);
free(UL);
free(UP);

free(Xa);

free(tot_pay);
free(tot_lvl);
free(tot_bud);
free(max_pay);
free(max_lvl); 
free(max_pos_pay);
free(n_items);

free(n_inn);
free(n_sl);
free(n_rs);


return 0;
}//end main
