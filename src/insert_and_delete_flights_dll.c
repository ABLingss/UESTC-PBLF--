// 添加删除航班
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
__declspec(dllexport) struct flight
{
    char flight_id[100], departure_time[100], arrival_time[100], start[100], destination[100], company[100];
    int price, total_seats, seat_number;
    struct flight *next;
};
__declspec(dllexport) struct flight *head = NULL;
// void print(){
//     struct flight* temp=head;
//     while(temp!=NULL){
//         printf("%s\n%s\n%s\n%d\n%d\n%s\n%s\n",temp->flight_id,temp->start,temp->destination,temp->price,temp->total_seats,temp->departure_time,temp->arrival_time);
//         temp=temp->next;
//     }
// }
// 我在insert中加入了形参
__declspec(dllexport) int insert(char *flight_id, char *departure_time, char *arrival_time,
                                 char *start, char *destination, char *company, int price, int total_seats)
{
    // char flight_id[100],departure_time[100],arrival_time[100],start[100],destination[100],airline[100],company[100];
    int seat_number;
    // // printf("flight_id");
    // scanf("%s",flight_id);
    // // printf("start");
    // scanf("%s",start);
    // // printf("destination");
    // scanf("%s",destination);
    // // printf("price");
    // scanf("%d",&price);
    // printf("total_seats");
    // scanf("%d",&total_seats);
    // seat_number=total_seats;
    // printf("departure_time");
    // scanf("%s",departure_time);
    // printf("company");
    // scanf("%s",company);
    // 检查输入的数据是否完整
    if (flight_id == NULL || strlen(flight_id) == 0 ||
        departure_time == NULL || strlen(departure_time) == 0 ||
        arrival_time == NULL || strlen(arrival_time) == 0 ||
        start == NULL || strlen(start) == 0 ||
        destination == NULL || strlen(destination) == 0 ||
        company == NULL || strlen(company) == 0 ||
        price <= 0 || total_seats <= 0)
    {
        printf("Missing or invalid data for flight insertion.\n");
        return 0; // 数据不完整或无效，插入失败
    }
    struct flight *temp1 = head;
    while (temp1 != NULL)
    {
        if (strcmp(temp1->flight_id, flight_id) == 0 && strcmp(temp1->start, start) == 0 && strcmp(temp1->destination, destination) == 0 && strcmp(temp1->departure_time, departure_time) == 0 && strcmp(temp1->arrival_time, arrival_time) == 0)
        {
            return 0; // 重复就插入失败
        }
        temp1 = temp1->next; // 不重复就继续遍历
    }
    struct flight *temp = (struct flight *)malloc(sizeof(struct flight));
    strcpy(temp->flight_id, flight_id);
    strcpy(temp->start, start);
    strcpy(temp->destination, destination);
    strcpy(temp->departure_time, departure_time);
    strcpy(temp->arrival_time, arrival_time);
    strcpy(temp->company, company);
    temp->price = price;
    temp->total_seats = total_seats;
    temp->seat_number = seat_number; // 座位数初始化为总座位数
    temp->next = head;
    head = temp; // 将用户输入的航班信息复制到新结构体中。然后将新结构体插入到链表的头部。
    // print();
    return 1; // 插入成功
}
__declspec(dllexport) int update_seat_number(char *flight_id, char *departure_time, int seats_to_update)
{
    // 查找对应的航班
    struct flight *temp = head;
    while (temp != NULL)
    {
        // 找到匹配的航班
        if (strcmp(temp->flight_id, flight_id) == 0 && strcmp(temp->departure_time, departure_time) == 0)
        {
            // 更新剩余座位数
            if (seats_to_update > 0 && temp->seat_number + seats_to_update <= temp->total_seats)
            {
                temp->seat_number += seats_to_update; // 增加剩余座位
                return 1;
            }
            else if (seats_to_update < 0 && temp->seat_number + seats_to_update >= 0)
            {
                temp->seat_number += seats_to_update; // 减少剩余座位
                return 1;
            }
            else
            {
                printf("Invalid seat number update.\n");
                return 0;
            }
        }
        temp = temp->next;
    }
    printf("Flight not found.\n");
    return 0;
}

__declspec(dllexport) int delete(char departure_time[], char flight_id[])
{
    if (flight_id == NULL || strlen(flight_id) == 0 ||
        departure_time == NULL || strlen(departure_time) == 0)
    {
        printf("Missing or invalid flight ID or departure time.\n");
        return 0; // 数据无效
    }
    struct flight *temp1 = head;
    int n = 0;
    while (strcmp(temp1->flight_id, flight_id) != 0 || strcmp(temp1->departure_time, departure_time) != 0)
    {
        temp1 = temp1->next;
        n++; // 找到要删除的航班的位置
    }
    if (temp1 == NULL)
    {
        return 0;
    }
    if (temp1 == head)
    {
        head = temp1->next;
        free(temp1);
        return 1;
    }
    temp1 = head;
    for (int i = 1; i <= n - 1; i++)
    {
        temp1 = temp1->next;
    }
    struct flight *temp2 = temp1->next;
    temp1->next = temp2->next;
    free(temp2);
    return 1; // 成功删除
}
__declspec(dllexport) int main()
{
    int order_number;
    char departure_time[100], flight_id[100];
    char flight_id_input[100],  arrival_time_input[100],departure_time_input[100], start[100], destination[100], company[100];
    int price, total_seats;
    printf("Enter 1 to add flight, 2 to delete flight, 3 to exit: ");
    scanf("%d", &order_number);

    while (order_number == 1 || order_number == 2)
    {
        if (order_number == 1)
        {
            // 获取用户输入的航班信息
            printf("Enter flight_id: ");
            scanf("%s", flight_id_input);
            printf("Enter departure_time: ");
            scanf("%s", departure_time_input);
            printf("Enter arrival_time: ");
            scanf("%s", arrival_time_input);
            printf("Enter start: ");
            scanf("%s", start);
            printf("Enter destination: ");
            scanf("%s", destination);
            printf("Enter company: ");
            scanf("%s", company);
            printf("Enter price: ");
            scanf("%d", &price);
            printf("Enter total_seats: ");
            scanf("%d", &total_seats);

            // 调用 insert 函数来添加航班
            int result = insert(flight_id_input, departure_time_input, arrival_time_input,start, destination, company, price, total_seats);
            if (result == 0)
            {
                printf("Failed to insert the flight. Please check the input data.\n");
            }
            else
            {
                printf("Flight inserted successfully.\n");
            }
        }
        else if (order_number == 2)
        {
            // 获取用户输入的要删除的航班信息
            printf("Enter departure_time: ");
            scanf("%s", departure_time);
            printf("Enter flight_id: ");
            scanf("%s", flight_id);

            // 调用 delete 函数来删除航班
            int result = delete (departure_time, flight_id);
            if (result == 0)
            {
                printf("Failed to delete the flight. Please check the input data.\n");
            }
            else
            {
                printf("Flight deleted successfully.\n");
            }
        }

        // 继续询问用户操作
        printf("Enter 1 to add flight, 2 to delete flight, 3 to exit: ");
        scanf("%d", &order_number);
    }

    return 0;
}