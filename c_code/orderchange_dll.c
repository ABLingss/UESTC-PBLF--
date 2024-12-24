#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__declspec(dllexport) struct flight {
    char flight_id[20], departure_time[20], arrival_time[20], start[20], destination[20], company[20];
    int price, total_seats, seat_number;
    struct flight* next;
};

__declspec(dllexport) struct order {
    char name[20];
    struct flight* flight;
};

__declspec(dllexport) struct order head1[50];

// 创建订单函数
__declspec(dllexport) int order_change(char departure_time[], char flight_id[], int n, int action) {
    struct flight* temp1 = head1[n].flight;

    while (temp1 != NULL) {
        if (strcmp(temp1->departure_time, departure_time) == 0 && strcmp(temp1->flight_id, flight_id) == 0) {
            if (action == 1) {
                // 创建订单
                struct flight* temp = (struct flight*)malloc(sizeof(struct flight));
                strcpy(temp->flight_id, temp1->flight_id);
                strcpy(temp->departure_time, temp1->departure_time);
                strcpy(temp->arrival_time, temp1->arrival_time);
                strcpy(temp->start, temp1->start);
                strcpy(temp->destination, temp1->destination);
                strcpy(temp->company, temp1->company);
                temp->price = temp1->price;
                temp->total_seats = temp1->total_seats;
                temp1->seat_number--;
                temp->seat_number = temp1->seat_number;
                temp->next = head1[n].flight;
                head1[n].flight = temp;
                return 1;
            } else if (action == 2) {
                // 取消订单
                struct flight* temp3 = head1[n].flight;
                while (temp3 != NULL) {
                    if (strcmp(temp3->departure_time, departure_time) == 0 && strcmp(temp3->flight_id, flight_id) == 0) {
                        temp3->seat_number++;
                    }
                    temp3 = temp3->next;
                }
                if (temp1 == head1[n].flight) {
                    head1[n].flight = temp1->next;
                    free(temp1);
                    return 1;
                }
                struct flight* temp2 = head1[n].flight;
                while (temp2 != NULL && temp2->next != temp1) {
                    temp2 = temp2->next;
                }
                if (temp2 != NULL) {
                    temp2->next = temp1->next;
                }
                free(temp1);
                return 1;
            }
        }
        temp1 = temp1->next;
    }
    return 0;
}

// 打印航班信息函数
__declspec(dllexport) void print(int n) {
    struct flight* temp = head1[n].flight;
    while (temp != NULL) {
        printf("%s %s %s %s %s %s %d\n", temp->flight_id, temp->departure_time, temp->arrival_time, temp->start, temp->destination, temp->company, temp->price);
        temp = temp->next;
    }
}
