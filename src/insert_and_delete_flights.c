//添加删除航班
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
struct flight{
    char flight_id[100],departure_time[100],arrival_time[100],start[100],destination[100],company[100];
    int price,total_seats,seat_number;
    struct flight* next;
};
struct flight* head=NULL;
// void print(){
//     struct flight* temp=head;
//     while(temp!=NULL){
//         printf("%s\n%s\n%s\n%d\n%d\n%s\n%s\n",temp->flight_id,temp->start,temp->destination,temp->price,temp->total_seats,temp->departure_time,temp->arrival_time);
//         temp=temp->next;
//     }
// }
int insert(){
    char flight_id[100],departure_time[100],arrival_time[100],start[100],destination[100],airline[100],company[100];
    int price,total_seats,seat_number;
    printf("flight_id");
    scanf("%s",flight_id);
    printf("start");
    scanf("%s",start);
    printf("destination");
    scanf("%s",destination);
    printf("price");
    scanf("%d",&price);
    printf("total_seats");
    scanf("%d",&total_seats);
    seat_number=total_seats;
    printf("departure_time");
    scanf("%s",departure_time);
    printf("company");
    scanf("%s",company);
    struct flight* temp1=head;
    while(temp1!=NULL){
        if(strcmp(temp1->flight_id,flight_id)==0&&strcmp(temp1->start,start)==0&&strcmp(temp1->destination,destination)==0&&strcmp(temp1->departure_time,departure_time)==0&&strcmp(temp1->arrival_time,arrival_time)==0){
        return 0; // 重复就插入失败
        }
        temp1=temp1->next; // 不重复就继续遍历
    }
    struct flight* temp=(struct flight*)malloc(sizeof(struct flight));
    strcpy(temp->flight_id,flight_id);
    strcpy(temp->start,start);
    strcpy(temp->destination,destination);
    strcpy(temp->departure_time,departure_time);
    strcpy(temp->arrival_time,arrival_time);
    strcpy(temp->company,company);
    temp->price=price;
    temp->total_seats=total_seats;
    temp->seat_number=seat_number;
    temp->next=head;
    head=temp; // 将用户输入的航班信息复制到新结构体中。然后将新结构体插入到链表的头部。
    // print();
    return 1;
}
int delete(char departure_time[],char flight_id[]){
    struct flight* temp1=head;
    int n=0;
    while(strcmp(temp1->flight_id,flight_id)!=0||strcmp(temp1->departure_time,departure_time)!=0){
        temp1=temp1->next;
        n++; // 找到要删除的航班的位置 没找到就返回0
    }
    if(temp1==NULL){
        return 0;
    }
    if(temp1==head){
        head=temp1->next;
        free(temp1);
        return 1;
    }
    temp1=head;
    for(int i=1;i<=n-1;i++){
        temp1=temp1->next;
    }
    struct flight* temp2=temp1->next;
    temp1->next=temp2->next;
    free(temp2);
    return 1;
}

int main(){
    int order_number;
    char departure_time[100],flight_id[100];
    printf("1or2"); // 1为添加 2为删除 
    scanf("%d",&order_number);
    while(order_number==1||order_number==2){
        if(order_number==1){
            printf("%d",insert());
        }else{
            printf("departure_time");
            scanf("%s",departure_time);
            printf("flight_id");
            scanf("%s",flight_id);
            printf("%d",delete(departure_time,flight_id));
        }
        printf("1or2or3");// 1为添加 2为删除 3为退出
        scanf("%d",&order_number);
    }
    return 0;
}