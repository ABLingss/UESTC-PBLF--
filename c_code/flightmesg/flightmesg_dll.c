#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>


// ��ȡCSV�ļ����������ݵ����ݿ�ĺ���
__declspec(dllexport) void import_csv_to_db(sqlite3* db, const char* csv_file) {
    FILE* file = fopen(csv_file, "r");
    if (!file) {
        fprintf(stderr, "�޷���CSV�ļ�\n");
        return;
    }

    char line[1024];//��֤�������㹻��
    sqlite3_stmt* stmt;
    //const char* sql_insert = "INSERT INTO Flights (flight_id,  departure_time, arrival_time,start, destination,company, price,  total_seats) VALUES (?, ?, ?, ?, ?, ?, ?, ?);";

    if (sqlite3_prepare_v2(db, sql_insert, -1, &stmt, 0) != SQLITE_OK) {
        fprintf(stderr, "׼���������ʧ��: %s\n", sqlite3_errmsg(db));
        fclose(file);
        return;
    }

    fgets(line, sizeof(line), file);//����������

    while (fgets(line, sizeof(line), file)) {
        char* flight_id, * start, * destination, * departure_time, * arrival_time;
        double price;
        char* company, * total_seats, * tmp;

        tmp = strtok(line, ",");
        flight_id = tmp; 
        tmp = strtok(NULL, ",");
        start = tmp;
        tmp = strtok(NULL, ",");
        destination = tmp;
        tmp = strtok(NULL, ",");
        departure_time = tmp;
        tmp = strtok(NULL, ",");
        arrival_time = tmp;
        tmp = strtok(NULL, ",");
        price = atof(tmp); 
        tmp = strtok(NULL, ",");
        company = tmp;
        tmp = strtok(NULL, ",");
        total_seats = tmp;

        sqlite3_bind_text(stmt, 1, flight_id, -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, start, -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 3, destination, -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 4, departure_time, -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 5, arrival_time, -1, SQLITE_STATIC);
        sqlite3_bind_double(stmt, 6, price);
        sqlite3_bind_text(stmt, 7, company, -1, SQLITE_STATIC);
        sqlite3_bind_int(stmt, 8, atoi(total_seats));

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            fprintf(stderr, "��������ʧ��: %s\n", sqlite3_errmsg(db));
        }
        sqlite3_reset(stmt);
        sqlite3_clear_bindings(stmt);
    }

    sqlite3_finalize(stmt);
    fclose(file);
}

int main() {
    sqlite3* db;
    char* errMsg = 0;
    int rc;

    rc = sqlite3_open("flights.db", &db);// �򿪻򴴽����ݿ���Ϊ"flights.db"
    if (rc) {
        fprintf(stderr, "�޷������ݿ�: %s\n", sqlite3_errmsg(db));
        return 1;
    }
    else {
        printf("���ݿ�򿪳ɹ�\n");
    }

    const char* sql_create_table =
        "CREATE TABLE IF NOT EXISTS Flights ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "//id
        "FOREIGN KEY(name) REFRENCES usermsg.db.users(name)"//�û���
        "flight_id TEXT PRIMARY KEY, "  //���
         "departure_time TEXT NOT NULL, "//��ʼʱ��
        "arrival_time TEXT NOT NULL, "  //����ʱ��
         "start TEXT NOT NULL, "         //���
       "destination TEXT NOT NULL, "   //�յ�
         "company TEXT NOT NULL, "        //����
       "price REAL NOT NULL, "          //�۸�
        "total_seats INTEGER NOT NULL,"//����λ
       "seat_number INTEGER NOT NULL )";//ʣ����λ��
        

    rc = sqlite3_exec(db, sql_create_table, 0, 0, &errMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "������ʧ��: %s\n", errMsg);
        sqlite3_free(errMsg);
        sqlite3_close(db);
        return 1;
    }
    else {
        printf("�������ɹ�\n");
    }

    import_csv_to_db(db, "   ");//�ո�λ����дCSV�ļ���ȥ������Ϣ�����ݿ�

    sqlite3_close(db);//�ر�

    return 0;
}