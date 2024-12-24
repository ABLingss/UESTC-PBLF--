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

__declspec(dllexport) void initDB() {
    int rc = sqlite3_open(DB_FILENAME, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "�޷������ݿ�%s\n", sqlite3_errmsg(db));
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
        fprintf(stderr, "SQL����%s\n", sqlite3_errmsg(db));
    }
}

__declspec(dllexport) void loadFlights() {
    const char* sql = "SELECT DISTINCT company FROM comments ORDER BY company";
    sqlite3_exec(db, sql, loadFlightsCallback, 0, 0);
}

__declspec(dllexport) int loadFlightsCallback(void* NotUsed, int argc, char** argv, char** azColName) {
    CompanyNode* newNode = (CompanyNode*)malloc(sizeof(CompanyNode));
    if (newNode == NULL) {
        fprintf(stderr, "�ڴ����ʧ��\n");
        return SQLITE_ERROR;
    }
    strncpy(newNode->company_number, argv[0], MAX_FLIGHT_LENGTH - 1);
    newNode->company_number[MAX_FLIGHT_LENGTH - 1] = '\0';
    newNode->next = head;
    head = newNode;
    return SQLITE_OK;
}

__declspec(dllexport) void ShowCompanies() {
    int i = 0;
    CompanyNode* current = head;
    printf("��ѡ�񺽿չ�˾:\n");
    while (current != NULL) {
        printf("%d.%s", i++, current->flight_number);
        current = current->next;
    }
}

__declspec(dllexport) void addCommentForFlight(const char* company) {
    printf("�������������ۣ����255�����֣�: ");
    char content[MAX_COMMENT_LENGTH];
    fgets(content, MAX_COMMENT_LENGTH, stdin);
    content[strcspn(content, "\n")] = 0;

    char sql[512];
    sprintf(sql, "INSERT INTO comments (content, company) VALUES ('%s', '%s')", content, company);
    char* errMsg = 0;
    int rc = sqlite3_exec(db, sql, 0, 0, &errMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL ����: %s\n", errMsg);
        sqlite3_free(errMsg);
    }
    else {
        printf("�������ӳɹ���\n");
    }
}

__declspec(dllexport) void showCommentsForFlight(const char* company) {
    char sql[1024];
    sprintf(sql, "SELECT * FROM comments WHERE company = '%s'", company);
    sqlite3_exec(db, sql, callback, 0, 0);
}

__declspec(dllexport) void callback(void* NotUsed, int argc, char** argv, char** azColName) {
    if (argc > 1) {
        printf("%s: %s\n", argv[0] ? argv[0] : "NULL", argv[1] ? argv[1] : "NULL");
    }
}

__declspec(dllexport) void freeCompanies() {
    while (head != NULL) {
        CompanyNode* temp = head;
        head = head->next;
        free(temp);
    }
}

__declspec(dllexport) void closeDB() {
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
        printf("\n�̼�����ϵͳ\n");
        printf("1. ��������\n");
        printf("2. ��ʾ�Ըú��չ�˾����\n");
        printf("3. �˳�\n");
        printf("��ѡ��һ��ѡ��: ");
        if (scanf("%d", &userChoice) != 1) {
            fprintf(stderr, "�������\n");
            continue;
        }
        getchar(); 

        switch (userChoice) {
        case 1:
            ShowCompanies();
            printf("�����뺽�չ�˾�����������: ");
            if (scanf("%d", &flightChoice) != 1) {
                fprintf(stderr, "�������\n");
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
                printf("��Ч�ĺ��չ�˾��š�\n");
            }
            break;
        case 2:
            ShowCompanies();
            printf("�����뺽�չ�˾��Ų鿴����: ");
            if (scanf("%d", &flightChoice) != 1) {
                fprintf(stderr, "�������\n");
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
                printf("��Ч�ĺ��չ�˾��š�\n");
            }
            break;
        case 3:
            printf("��л�������ۡ�\n");
            break;
        default:
            printf("��Чѡ�������ѡ��\n");
        }
    } while (userChoice != 3);

    closeDB();
    return 0;
}

