# 机票管理系统
电子科技大学**程序与算法设计I**大作业

## 项目介绍

本项目是一个机票管理系统，系统包括用户信息管理、航班查询、订单管理等功能，采用 PyQt 和 C 语言相结合的方式进行开发。前端使用 PyQt 设计图形界面，后端使用 C 语言实现核心功能模块，并通过 DLL 进行与 Python 的交互。

## 说明
- 大作业要求c语言代码量大于70%，本项目的大多数Python代码都是由Pyuic生成的，实际上的Python代码仅为主函数和爬虫小工具等的部分，因此是符合大作业的要求的。
- 因为本项目打包的exe文件过大，因此打包好的`.exe`只放在提交的压缩包中(如果无法使用请进入`src`目录运行`TicketManager.exe`)，使用clone仓库方式部署请参考下方[使用方法2](#如何使用)
- 邮件发送功能需要在`./src`目录下的`sendemail.py`中配置发送人信息再重新打包，否则邮件发送功能默认不启用。

## 系统架构

### 前端
- **PyQt5**：用于设计图形化界面，界面设计采用 `.ui` 文件，并通过 `pyuic` 转换为 Python 文件。
- **功能**：用户界面包括个人信息管理、航班查询、订单管理等。

### 后端
- 代码原始部分存储在`./c_code`中，`.dll`存储在`./src`中
    - **C 语言**：核心功能模块使用 C 语言实现，特别是与数据库交互和数据处理部分。
    - **DLL**：C 语言编写的 DLL 用于与 Python 进行交互，提供一些底层的操作（如修改用户信息）。

### 数据库
- **SQLite**：使用 SQLite 数据库存储用户信息、航班数据和订单信息。存储在`./data`
- 具体数据库文件包括：
  - `flights.db`
  - `orders.db`
  - `passengers.db`
  - `comments.db`


## 安装与使用

### 环境要求
- PyQt5==5.15.7
- ctypes
- sqlite3
- pygame==2.1.3
- asyncio
- aiohttp==3.8.1
- lxml==4.9.1
- pandas==1.3.3
- numpy==1.21.2
- tqdm==4.62.3
- python==3.12
- Windows11

### 如何使用
 - 直接运行TicketManager
 - 你也可以
     1. 克隆本仓库：
    ```bash
    git clone https://github.com/ABLingss/  UESTC-PBLF--PlaneticketManagement.git
    cd UESTC-PBLF--PlaneticketManagement
    ```
 2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
 3. 运行项目：
    使用 PyCharm 或命令行运行 `.\src\mainmain.py` 文件：
    ```bash
    python src/mainmain.py
    ```
-  如果你需要从源代码部署  
 1. 进入资源文件夹
 ```bash
 cd src
 ```
 2. 依照`.\src\TicketManger.spec`文件进行部署
 ```bash
 pyinstaller TicketManager.spec
 ```
 3. 构建的`TicketManager.exe`位于`./dist/`中



## 贡献

若要贡献，请遵循以下步骤：
1. Fork 本仓库
2. 创建你的分支 (`git checkout -b feature-xyz`)
3. 提交你的修改 (`git commit -am 'Add new feature'`)
4. 推送到分支 (`git push origin feature-xyz`)
5. 创建 Pull Request

## 许可

此项目采用 [MIT 许可证](https://opensource.org/licenses/MIT)。



