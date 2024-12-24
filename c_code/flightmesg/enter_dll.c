#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>

struct passenger {
    char name[20];
    char code[31];
    char phone[23];
    char id[37];
    char mail[321];
} user;

__declspec(dllexport) int Creat_DB(sqlite3* db) {
    char* err_msg = 0;
    const char* sql = "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT UNIQUE, "
        "code TEXT, "
        "phone TEXT, "
        "id_card TEXT UNIQUE, "
        "mail TEXT UNIQUE);";

    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    return 0;
}

__declspec(dllexport) int insert_user(sqlite3* db, struct passenger* user) {
    char* err_msg = 0;
    const char* tail;
    sqlite3_stmt* stmt;

    const char* sql = "INSERT INTO users (name, code, phone, id_card, mail) VALUES (?,?,?,?,?);";
    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, &tail);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "�޷�ִ��: %s\n", sqlite3_errmsg(db));
        return 1;
    }

    sqlite3_bind_text(stmt, 1, user->name, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, user->code, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, user->phone, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 4, user->id_card, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 5, user->mail, -1, SQLITE_STATIC);

    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(stmt);
        return 1;
    }

    sqlite3_finalize(stmt);
    return 0;
}

__declspec(dllexport) int test_user(sqlite3* db, const char* username, const char* password) {
    char* err_msg = 0;
    const char* tail;
    sqlite3_stmt* stmt;
    const char* sql = "SELECT * FROM users WHERE name=? AND code=?;";

    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, &tail);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "���ִ���: %s\n", sqlite3_errmsg(db));
        return 1;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, password, -1, SQLITE_STATIC);

    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        sqlite3_finalize(stmt);
        return 0;
    }
    else if (rc == SQLITE_DONE) {
        sqlite3_finalize(stmt);
        return 2;
    }
    else {
        fprintf(stderr, "���ִ���: %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(stmt);
        return 1;
    }
}

__declspec(dllexport) int date_input(const char* input, int max_len) {
    if (input == NULL) {
        return 0;
    }
    size_t len = strlen(input);
    for (size_t i = 0; i < len; i++) {
        if (!((input[i] >= 'a' && input[i] <= 'z') || (input[i] >= 'A' && input[i] <= 'Z') || (input[i] >= '0' && input[i] <= '9') || input[i] == '_')) {
            return 0;
        }
    }
    return len <= max_len;
}

int main() {
    sqlite3* db;
    int rc;

    rc = sqlite3_open("usermsg.db", &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return 1;
    }

    if (Creat_DB(db)) {
        sqlite3_close(db);
        return 1;
    }

    printf("�����������û��� ");
    scanf("%19s", user.name);
    while (!date_input(user.name, 19)) {
        printf("�����ʽ��������������: ");
        scanf("%19s", user.name);
    }

    printf("��������������: ");
    scanf("%30s", user.code);
    while (!date_input(user.code, 30)) {
        printf("�����ʽ��������������: ");
        scanf("%30s", user.code);
    }

    int result = test_user(db, user.name, user.code);
    if (result == 0) {
        printf("��¼�ɹ�!\n");
    }
   
    else {
        printf("��½ʧ��.\n");
    }

    sqlite3_close(db);
    return 0;
}




