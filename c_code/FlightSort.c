//航班排序
#include<stdio.h>
#include<stdlib.h>
#include<string.h>


char a[10][20]={"1","3","5","8","7","4","6","2","0","9"};


struct flight{
    char flight_id[20],departure_time[20],arrival_time[20],start[20],destination[20],company[20];
    int price,total_seats,seat_number;
    struct flight* next;
};
struct flight* head=NULL;
void insert(int i){
    struct flight* temp=(struct flight*)malloc(sizeof(struct flight));
    strcpy(temp->flight_id,a[i]);
    strcpy(temp->start,a[i]);
    strcpy(temp->destination,a[i+1]);
    strcpy(temp->departure_time,a[i]);
    strcpy(temp->arrival_time,a[i]);
    strcpy(temp->company,a[i]);
    temp->price=i;
    temp->seat_number=i;
    temp->next=head;
    head=temp;
}

/*该函数用于对一个链表中的航班数据进行排序。链表中的每个节点代表一个航班，节点中包含了航班的各种信息，如航班号、出发时间、到达时间、出发地、目的地、航空公司、价格、总座位数和座位号等。*/
void price(){
    int n=0;
    struct flight* temp=head;
    struct flight* temp1=head;
    while(temp!=NULL){
        temp=temp->next;
        n++;
    }
    for(int i=1;i<=n-1;i++){
        struct flight* temp1=head;
        for(int j=1;j<=n-1;j++){
            if(temp1->price>temp1->next->price){
                struct flight* temp2=temp1->next;
                struct flight* temp3=temp1->next->next;
                if(temp1==head){
                    head=temp2;
                    temp2->next=temp1;
                    temp1->next=temp3;
                }else{
                    struct flight* temp0=head;
                    while(temp0->next!=temp1){
                        temp0=temp0->next;
                    }
                    temp0->next=temp2;
                    temp2->next=temp1;
                    temp1->next=temp3;
                }
                continue;
            }
            temp1=temp1->next;
        }
    }
}

/*time 函数用于对航班列表按照出发时间进行排序，print 函数用于打印排序后的航班列表*/
void time(){
    int n=0;
    struct flight* temp=head;
    struct flight* temp1=head;
    while(temp!=NULL){
        temp=temp->next;
        n++;
    }
    for(int i=1;i<=n-1;i++){
        struct flight* temp1=head;
        for(int j=1;j<=n-1;j++){
            if(strcmp(temp1->departure_time,temp1->next->departure_time)>0){
                struct flight* temp2=temp1->next;
                struct flight* temp3=temp1->next->next;
                if(temp1==head){
                    head=temp2;
                    temp2->next=temp1;
                    temp1->next=temp3;
                }else{
                    struct flight* temp0=head;
                    while(temp0->next!=temp1){
                        temp0=temp0->next;
                    }
                    temp0->next=temp2;
                    temp2->next=temp1;
                    temp1->next=temp3;
                }
                continue;
            }
            temp1=temp1->next;
        }
    }
}
void print(){
    struct flight* temp=head;
    while(temp!=NULL){
        printf("%s %d\n",temp->departure_time,temp->price);
        temp=temp->next;
    }
}

int main(){
    for(int i=1;i<=8;i++){
        insert(i);
    }
    int n;
    scanf("%d",&n);
    if(n==1){
        price();
        print();
    }else if(n==2){
        time();
        print();
    }
    return 0;
}