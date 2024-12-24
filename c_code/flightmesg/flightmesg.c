#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>


// 读取CSV文件并插入数据到数据库的函数
void import_csv_to_db(sqlite3* db, const char* csv_file) {
    FILE* file = fopen(csv_file, "r");
    if (!file) {
        fprintf(stderr, "无法打开CSV文件\n");
        return;
    }

    char line[1024];//保证缓冲区足够大
    sqlite3_stmt* stmt;
    //const char* sql_insert = "INSERT INTO Flights (flight_id,  departure_time, arrival_time,start, destination,company, price,  total_seats) VALUES (?, ?, ?, ?, ?, ?, ?, ?);";

    if (sqlite3_prepare_v2(db, sql_insert, -1, &stmt, 0) != SQLITE_OK) {
        fprintf(stderr, "准备插入语句失败: %s\n", sqlite3_errmsg(db));
        fclose(file);
        return;
    }

    fgets(line, sizeof(line), file);//跳过标题行

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
            fprintf(stderr, "插入数据失败: %s\n", sqlite3_errmsg(db));
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

    rc = sqlite3_open("flights.db", &db);// 打开或创建数据库名为"flights.db"
    if (rc) {
        fprintf(stderr, "无法打开数据库: %s\n", sqlite3_errmsg(db));
        return 1;
    }
    else {
        printf("数据库打开成功\n");
    }

    const char* sql_create_table =
        "CREATE TABLE IF NOT EXISTS Flights ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "//id
        "FOREIGN KEY(name) REFRENCES usermsg.db.users(name)"//用户名
        "flight_id TEXT PRIMARY KEY, "  //编号
         "departure_time TEXT NOT NULL, "//起始时间
        "arrival_time TEXT NOT NULL, "  //到达时间
         "start TEXT NOT NULL, "         //起点
       "destination TEXT NOT NULL, "   //终点
         "company TEXT NOT NULL, "        //机场
       "price REAL NOT NULL, "          //价格
        "total_seats INTEGER NOT NULL,"//总座位
       "seat_number INTEGER NOT NULL )";//剩余座位量
        

    rc = sqlite3_exec(db, sql_create_table, 0, 0, &errMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "创建表失败: %s\n", errMsg);
        sqlite3_free(errMsg);
        sqlite3_close(db);
        return 1;
    }
    else {
        printf("表创建成功\n");
    }

    import_csv_to_db(db, "   ");//空格位置填写CSV文件名去导入信息到数据库

    sqlite3_close(db);//关闭

    return 0;
}