//管理员删除用户->删除用户订单
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
__declspec(dllexport)  struct passenger{
    char name[20],code[1000],phone[20],id[20],mail[20];
    struct passenger* next;
};
__declspec(dllexport) struct passenger* head=NULL;
__declspec(dllexport)  struct flight{
    char flight_id[20],departure_time[20],arrival_time[20],start[20],destination[20],company[20];
    int price,total_seats,seat_number;
    struct flight* next;
};
__declspec(dllexport)  struct flight* now=NULL;
__declspec(dllexport)  struct order{
    char name[20];
    struct flight* flight;
};
__declspec(dllexport)  struct order head1[50];
__declspec(dllexport)  void delete2(char name[]){//传入04.c的name、03.c的订单和n
    int n=5;//改为03.c的n
    struct passenger* temp=head;
    while(temp!=NULL){
        if(strcmp(temp->name,name)==0){
            struct passenger* temp1=head;
            while(temp1->next!=temp){
                temp1=temp1->next;
            }
            temp1->next=temp->next;
            free(temp);
            break;
        }    
    }
    for(int i=1;i<=n;i++){
        if(strcmp(head1[i].name,name)==0){
            head1[i].flight=NULL;
        }
    }    
}
int main(){
    char name[20];
    delete2(name);
    return 0;
}