#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>

#define MAX_COMMENT_LENGTH 1001
#define MAX_FLIGHT_LENGTH 51
#define DB_FILENAME "flights_comments.db"

int loadCompaniesCallback(void* NotUsed, int argc, char** argv, char** azColName);

sqlite3* db;
CompanyNode* head = NULL;

typedef struct {
    char content[MAX_COMMENT_LENGTH];
    char name[20];
    char company[MAX_FLIGHT_LENGTH];
} Comment;

typedef struct {
    char company_number[MAX_FLIGHT_LENGTH];
    struct FlightNode* next;
} CompanyNode;

void initDB() {
    int rc = sqlite3_open(DB_FILENAME, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "无法打开数据库%s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return;
    }
    const char* sql = "CREATE TABLE IF NOT EXISTS comments ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "FOREIGN KEY(name) REFRENCES usermsg.db.users(name)"
        "company TEXT, "
        "content TEXT)";
    rc = sqlite3_exec(db, sql, 0, 0, 0);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL错误%s\n", sqlite3_errmsg(db));
    }
}

void loadFlights() {
    const char* sql = "SELECT DISTINCT company FROM comments ORDER BY company";
    sqlite3_exec(db, sql, loadFlightsCallback, 0, 0);
}

int loadFlightsCallback(void* NotUsed, int argc, char** argv, char** azColName) {
    CompanyNode* newNode = (CompanyNode*)malloc(sizeof(CompanyNode));
    if (newNode == NULL) {
        fprintf(stderr, "内存分配失败\n");
        return SQLITE_ERROR;
    }
    strncpy(newNode->company_number, argv[0], MAX_FLIGHT_LENGTH - 1);
    newNode->company_number[MAX_FLIGHT_LENGTH - 1] = '\0';
    newNode->next = head;
    head = newNode;
    return SQLITE_OK;
}

void ShowCompanies() {
    int i = 0;
    CompanyNode* current = head;
    printf("请选择航空公司:\n");
    while (current != NULL) {
        printf("%d.%s", i++, current->flight_number);
        current = current->next;
    }
}

void addCommentForFlight(const char* company) {
    printf("请输入您的评论（最多255个汉字）: ");
    char content[MAX_COMMENT_LENGTH];
    fgets(content, MAX_COMMENT_LENGTH, stdin);
    content[strcspn(content, "\n")] = 0;

    char sql[512];
    sprintf(sql, "INSERT INTO comments (content, company) VALUES ('%s', '%s')", content, company);
    char* errMsg = 0;
    int rc = sqlite3_exec(db, sql, 0, 0, &errMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL 错误: %s\n", errMsg);
        sqlite3_free(errMsg);
    }
    else {
        printf("评论添加成功。\n");
    }
}

void showCommentsForFlight(const char* company) {
    char sql[1024];
    sprintf(sql, "SELECT * FROM comments WHERE company = '%s'", company);
    sqlite3_exec(db, sql, callback, 0, 0);
}

void callback(void* NotUsed, int argc, char** argv, char** azColName) {
    if (argc > 1) {
        printf("%s: %s\n", argv[0] ? argv[0] : "NULL", argv[1] ? argv[1] : "NULL");
    }
}

void freeCompanies() {
    while (head != NULL) {
        CompanyNode* temp = head;
        head = head->next;
        free(temp);
    }
}

void closeDB() {
    sqlite3_close(db);
    freeCompanies();
}

int main() {
    initDB();
    loadFlights();

    int userChoice;
    int flightChoice;                  
    char flightNumber[MAX_FLIGHT_LENGTH];
    do {
        printf("\n商家评论系统\n");
        printf("1. 添加评论\n");
        printf("2. 显示对该航空公司评论\n");
        printf("3. 退出\n");
        printf("请选择一个选项: ");
        if (scanf("%d", &userChoice) != 1) {
            fprintf(stderr, "输入错误\n");
            continue;
        }
        getchar(); 

        switch (userChoice) {
        case 1:
            ShowCompanies();
            printf("请输入航空公司编号添加评论: ");
            if (scanf("%d", &flightChoice) != 1) {
                fprintf(stderr, "输入错误\n");
                continue;
            }
            getchar(); 
            CompanyNode* current = head;
            while (current != NULL) {
                if (--flightChoice == 0) {
                    strcpy(flightNumber, current->flight_number);
                    addCommentForFlight(flightNumber);
                    break;
                }
                current = current->next;
            }
            if (current == NULL) {
                printf("无效的航空公司编号。\n");
            }
            break;
        case 2:
            ShowCompanies();
            printf("请输入航空公司编号查看评论: ");
            if (scanf("%d", &flightChoice) != 1) {
                fprintf(stderr, "输入错误\n");
                continue;
            }
            getchar();  
            current = head;
            while (current != NULL) {
                if (--flightChoice == 0) {
                    strcpy(flightNumber, current->flight_number);
                    showCommentsForFlight(flightNumber);
                    break;
                }
                current = current->next;
            }
            if (current == NULL) {
                printf("无效的航空公司编号。\n");
            }
            break;
        case 3:
            printf("感谢您的评论。\n");
            break;
        default:
            printf("无效选项，请重新选择。\n");
        }
    } while (userChoice != 3);

    closeDB();
    return 0;
}

