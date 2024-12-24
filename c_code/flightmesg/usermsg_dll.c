#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>


struct passenger {
    char name[20];
    char code[31];
    char phone[23];
    char id_card[37];
    char mail[321];
}user;



__declspec(dllexport) int Creat_DB(sqlite3* db) {
    char* err_msg = 0;
    const char* sql = "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT UNIQUE, "
        "code TEXT , "
        "phone TEXT , "
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
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
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

    printf("Enter name: ");
    if (scanf("%19s", user.name) != 1) {
        fprintf(stderr, "name������Ҫ��\n");
        sqlite3_close(db);
        return 1;
    }
    printf("Enter code: ");
    if (scanf("%30s", user.code) != 1) {
        fprintf(stderr, "code������Ҫ��\n");
        sqlite3_close(db);
        return 1;
    }
    printf("Enter phone: ");
    if (scanf("%22s", user.phone) != 1) {
        fprintf(stderr, "phone������Ҫ��\n");
        sqlite3_close(db);
        return 1;
    }
    printf("Enter id_card: ");
    if (scanf("%36s", user.id_card) != 1) {
        fprintf(stderr, "id_card������Ҫ��\n");
        sqlite3_close(db);
        return 1;
    }
    printf("Enter mail: ");
    if (scanf("%320s", user.mail) != 1) {
        fprintf(stderr, "Invalid input for mail\n");
        sqlite3_close(db);
        return 1;
    }

    if (insert_user(db, &user)) {
        sqlite3_close(db);
        return 1;
    }

    sqlite3_close(db);
    return 0;
}