#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

struct flight {
    char flight_id[20], departure_time[20], arrival_time[20], start[20], destination[20], company[20];
    int price, total_seats, seat_number;
    struct flight* next;
};

struct flight* header[50] = {NULL};
struct flight* head = NULL;
struct flight* head1 = NULL;

int n = 0;

DLL_EXPORT void insert1(struct flight* temp) {
    struct flight* temp1 = (struct flight*)malloc(sizeof(struct flight));
    strcpy(temp1->flight_id, temp->flight_id);
    strcpy(temp1->departure_time, temp->departure_time);
    strcpy(temp1->arrival_time, temp->arrival_time);
    strcpy(temp1->start, temp->start);
    strcpy(temp1->destination, temp->destination);
    strcpy(temp1->company, temp->company);
    temp1->price = temp->price;
    temp1->seat_number = temp->seat_number;
    temp1->next = head1;
    head1 = temp1;
}

DLL_EXPORT void insert2(struct flight* first, struct flight* last) {
    n++;
    struct flight* temp1 = (struct flight*)malloc(sizeof(struct flight));
    struct flight* temp2 = (struct flight*)malloc(sizeof(struct flight));

    strcpy(temp1->flight_id, first->flight_id);
    strcpy(temp1->departure_time, first->departure_time);
    strcpy(temp1->arrival_time, first->arrival_time);
    strcpy(temp1->start, first->start);
    strcpy(temp1->destination, first->destination);
    strcpy(temp1->company, first->company);

    strcpy(temp2->flight_id, last->flight_id);
    strcpy(temp2->departure_time, last->departure_time);
    strcpy(temp2->arrival_time, last->arrival_time);
    strcpy(temp2->start, last->start);
    strcpy(temp2->destination, last->destination);
    strcpy(temp2->company, last->company);

    temp1->price = first->price;
    temp2->price = last->price;
    temp1->seat_number = first->seat_number;
    temp2->seat_number = last->seat_number;
    temp2->next = NULL;
    temp1->next = temp2;
    header[n] = temp1;
}

DLL_EXPORT void print1() {
    struct flight* temp = head1;
    if (temp == NULL) {
        printf("no flight");
        return;
    }
    while (temp != NULL) {
        printf("%s\n%s\n%s\n%d\n%d\n%s\n%s\n%s\n", temp->flight_id, temp->start, temp->destination, temp->seat_number, temp->price, temp->departure_time, temp->arrival_time, temp->company);
        temp = temp->next;
    }
}

DLL_EXPORT void print2() {
    for (int i = 1; i <= n; i++) {
        struct flight* temp = header[i];
        while (temp != NULL) {
            printf("%s\n%s\n%s\n%d\n%d\n%s\n%s\n%s\n", temp->flight_id, temp->start, temp->destination, temp->seat_number, temp->price, temp->departure_time, temp->arrival_time, temp->company);
            temp = temp->next;
        }
    }
}

DLL_EXPORT void search_direct(const char* start, const char* destination) {
    struct flight* temp = head;
    while (temp != NULL) {
        if (strcmp(temp->destination, destination) == 0 && strcmp(temp->start, start) == 0) {
            insert1(temp);
        }
        temp = temp->next;
    }
}

DLL_EXPORT void search_transfer(const char* start, const char* destination) {
    struct flight* temp = head;
    struct flight* temp1 = head;
    while (temp != NULL) {
        if (strcmp(temp->destination, destination) == 0 && strcmp(temp->start, start) != 0) {
            while (temp1 != NULL) {
                if (strcmp(temp1->destination, temp->start) == 0 && strcmp(temp1->start, start) == 0) {
                    insert2(temp1, temp);
                }
                temp1 = temp1->next;
            }
        }
        temp = temp->next;
    }
}
