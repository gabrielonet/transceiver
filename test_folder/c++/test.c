#include <pthread.h>
#include <stdio.h>
#include <unistd.h>



int a=120;
pthread_mutex_t lock;

void *run(void *p){

        while(1){
                pthread_mutex_lock(&lock);
                a++;
                pthread_mutex_unlock(&lock);
        }

}


void start(){

        pthread_t th;

        /* create a second thread which executes inc_x(&x) */
        if(pthread_create(&th, NULL, run, NULL)) {
                fprintf(stderr, "Error creating thread\n");
                return ;
        }
}


int get_value(){
        int r;
        pthread_mutex_lock(&lock);
        r=a;
        pthread_mutex_unlock(&lock);    
        return r;
}

