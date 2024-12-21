#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct passenger {
    char name[20], code[1000], phone[20], id[20], mail[20];
    struct passenger* next;
};

struct passenger* head = NULL;
struct passenger* now = NULL;

// 注册新乘客
__declspec(dllexport) const char* regis(const char* name, const char* code, const char* phone, const char* id, const char* mail) {
    struct passenger* temp1 = head;
    
    // 检查是否有相同的乘客信息
    while (temp1 != NULL) {
        if (strcmp(temp1->name, name) == 0) {
            return "name used";
        }
        if (strcmp(temp1->phone, phone) == 0) {
            return "phone used";
        }
        if (strcmp(temp1->id, id) == 0) {
            return "id used";
        }
        if (strcmp(temp1->mail, mail) == 0) {
            return "mail used";
        }
        temp1 = temp1->next;
    }

    // 创建一个新的乘客记录
    struct passenger* temp = (struct passenger*)malloc(sizeof(struct passenger));
    strcpy(temp->name, name);
    strcpy(temp->code, code);
    strcpy(temp->phone, phone);
    strcpy(temp->id, id);
    strcpy(temp->mail, mail);
    temp->next = head;
    head = temp;
    
    return "yes";
}

// 登录检查乘客
__declspec(dllexport) const char* login(const char* name, const char* code) {
    struct passenger* temp1 = head;

    while (temp1 != NULL) {
        if (strcmp(temp1->name, name) == 0 && strcmp(temp1->code, code) == 0) {
            now = temp1;
            return "yes";
        } else if (strcmp(temp1->name, name) == 0 && strcmp(temp1->code, code) != 0) {
            return "wrong code";
        }
        temp1 = temp1->next;
    }
    return "no name";
}

// 修改乘客信息
__declspec(dllexport) int change(int order_number, const char* value) {
    if (now == NULL) {
        return 0; // 没有登录用户
    }

    if (order_number == 1) {
        strcpy(now->name, value);
    } else if (order_number == 2) {
        strcpy(now->code, value);
    } else if (order_number == 3) {
        strcpy(now->phone, value);
    } else if (order_number == 4) {
        strcpy(now->id, value);
    } else if (order_number == 5) {
        strcpy(now->mail, value);
    } else {
        return 0; // 无效的修改选项
    }

    return 1;
}
