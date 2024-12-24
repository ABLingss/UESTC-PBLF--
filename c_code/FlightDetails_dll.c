//航班详情
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define EXPORT __declspec(dllexport)

// char a[10][20]={"0","1","2","3","4","5","6","7","8","9"};


EXPORT struct flight{
    char flight_id[20],departure_time[20],arrival_time[20],start[20],destination[20],company[20];
    int price,total_seats,seat_number;
    struct flight* next;
};
EXPORT struct flight* head=NULL;

// void insert(int i){
//     struct flight* temp=(struct flight*)malloc(sizeof(struct flight));
//     strcpy(temp->flight_id,a[i]);
//     strcpy(temp->start,a[i]);
//     strcpy(temp->destination,a[i+1]);
//     strcpy(temp->departure_time,a[i]);
//     strcpy(temp->arrival_time,a[i]);
//     strcpy(temp->company,a[i]);
//     temp->price=i;
//     temp->seat_number=i;
//     temp->next=head;
//     head=temp;
// }


EXPORT void detail(char departure_time[],char flight_id[]){
    struct flight* temp=head;
    while(temp!=NULL){
        if(strcmp(temp->departure_time,departure_time)==0&&strcmp(temp->flight_id,flight_id)==0){
            printf("%s\n%s\n%s\n%s\n%d\n%d\n",temp->flight_id,temp->company,temp->departure_time,temp->arrival_time,temp->seat_number,temp->price);
        }
        temp=temp->next;
    }
    int n;
    scanf("%d",&n);
    if(n==1){
        //对接03.c下订单
    }
}

EXPORT int main(){
    // for(int i=1;i<=8;i++){
    //     insert(i);
    // }
    char departure_time[20],flight_id[20];
    printf("departure_time");
    scanf("%s",departure_time);
    printf("flight_id");
    scanf("%s",flight_id);
    detail(departure_time,flight_id);
    return 0;
}