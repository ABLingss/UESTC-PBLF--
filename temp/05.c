//用户查询订单
#include<stdio.h>
#include<stdlib.h>
#include<string.h>



struct flight{
    char flight_id[20],departure_time[20],arrival_time[20],start[20],destination[20],company[20];
    int price,total_seats,seat_number;
    struct flight* next;
};
struct flight* now=NULL;
struct order{
    char name[20];
    struct flight* flight;
};
struct order head;
struct order head1[50];


void search(char name[]){//把03.c的n和head1[1~n](n条链表，即所有用户的订单信息）全部传入
    int n=5;//改为03.c的n
    for(int i=1;i<=n;i++){
        if(strcmp(head1[i].name,name)==0){
            struct flight* temp=head1[i].flight;
            while(temp!=NULL){
                printf("%s %s %s %s %s %s %d\n",temp->flight_id,temp->departure_time,temp->arrival_time,temp->start,temp->destination,temp->company,temp->price);
                temp=temp->next;
            }
        }
    }
}

int main(){
    char name[20];
    printf("name");
    scanf("%s",name);
    search(name);
    return 0;
}