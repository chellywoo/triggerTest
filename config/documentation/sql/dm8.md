## 触发器问题总结：

### 1 自主访问控制中问题

- 自主访问控制在安全模型中的规定如下：
  - 主体必须拥有对客体的访问权限才能访问客体
  - 权限的授予和传播情况需要记录在系统中
  - 权限的传播范围：只限于该对象本身，不会影响其他对象的访问权限

​	针对触发器进行关于自主访问控制的测试的目的是：用户在触发器的使用过程中是否会直接或间接的获取到某些信息，或者使用其他用户的权限，从而间接的获取到自己未曾拥有的权限，乃至获取到DBA权限。

### 2 强制访问控制中的问题

- 强制访问控制在安全模型中的规定如下：

  - 安全管理员可以通过设置安全策略和标签策略来限制被授权者的标签，对数据库的主体和客体授予对应的标签。
  - 用户安全性标签的安全分级 >= 数据库数据表的行、列和属性值安全性标签的安全分级，才可以读数据
  - 用户安全性标签的安全分级 <= 数据库数据表的行、列和属性值安全性标签的安全分级，才可以写数据

- 强制访问控制的实现，是通过SYSSSO来创建策略，对用户、表施加策略，从而达到强制访问控制的目的。而在达梦中，如果SYSSSO用户仅对用户施加策略，该用户创建表之后，还是普通表，任意用户拥有该表的查询权限，就可以查看数据，若要满足强制访问控制的要求，还需要SYSSSO用户来对该用户的表施加策略。

  - 创建策略的函数

    ```
    VOID
    MAC_CREATE_POLICY(
        POLICY_NAME VARCHAR(128)
    );
    参数说明：
    
    POLICY_NAME 新创建的策略名称
    ```

  - 为策略创建等级的函数

    ```
    VOID
    MAC_CREATE_LEVEL(
        POLICY_NAME VARCHAR(128),
        LEVEL_NUM INT,
        LEVEL_NAME VARCHAR(128)
    );
    参数说明：
    POLICY_NAME 要添加等级的策略名
    LEVEL_NUM 创建的等级编号，在 0－9999 之间的整数
    LEVEL_NAME 创建的等级名称
    ```

  - 为策略创建标记的函数

    ```
    VOID
    MAC_CREATE_LABEL(
        POLICY_NAME VARCHAR(128),
        LABEL_TAG INT,
        LABEL_VALUE VARCHAR(4000)
    );
    参数说明：
    POLICY_NAME 要创建的标记所在的策略名
    LABEL_TAG 标记值，有效范围为 0~999999999
    LABEL_VALUE 标记串
    ```

  - 对表应用策略的函数:

    ```
    VOID
    MAC_APPLY_TABLE_POLICY（
        POLICY_NAME VARCHAR(128),
        SCHEMANAME VARCHAR(128),
        TABLENAME VARCHAR(128),
        COLNAME VARCHAR(128),
        LABELVALUE VARCHAR(4000),
        OPTION INT
    ）;
    参数说明：
    POLICY_NAME 应用于指定表的策略名
    SCHEMANAME 表所属模式名称
    TABLENAME 策略所应用的表名称
    COLNAME 用于记录标记的列名称
    LABELVALUE 用于说明被应用了策略的表中，已有元组的等级、范围和组
    OPTION 1 代表隐藏标记列，0 代表不隐藏标记列，缺省为 0
    ```

  - 对用户设置策略的函数：

    ```
    VOID
    MAC_USER_SET_LEVELS(
        POLICY_NAME VARCHAR(128),
        USER_NAME VARCHAR(128),
        MAX_LEVEL VARCHAR(128),
        MIN_LEVEL VARCHAR(128),
        DEF_LEVEL VARCHAR(128),
        ROW_LEVEL VARCHAR(128)
    );
    参数说明：
    POLICY_NAME 应用于用户的策略名称
    USER_NAME 策略所应用的用户名称
    MAX_LEVEL 应用于用户的最大等级
    MIN_LEVEL 应用于用户的最小等级
    DEF_LEVEL 应用于用户的默认等级
    ROW_LEVEL 应用于用户的行等级
    ```

    

  - ```sql
    --创建策略
    MAC_CREATE_POLICY('POL2');
    --创建等级
    MAC_CREATE_LEVEL('POL2', 13, 'L_03');
    MAC_CREATE_LEVEL('POL2', 14, 'L_04');
    --授予用户策略
    MAC_USER_SET_LEVELS('POL2', 'U_POL1', 'L_04', 'L_04', 'L_04', 'L_04');
    MAC_USER_SET_LEVELS('POL2', 'U_POL2', 'L_03', 'L_03', 'L_03', 'L_03');
    --授予表策略
    MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'T1', 'LABEL_COL', 'L_04::',0);
    MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'T2', 'LABEL_COL', 'L_04::',0);
    
    MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL2', 'T1', 'LABEL_COL', 'L_03::',0);
    ```

针对触发器进行关于强制访问控制的测试的目的是：低等级用户在触发器的使用过程中是否会获取到高等级的数据，影响数据库中的数据流向。

## 3 审计中的问题

- 审计在安全模型中的规定如下：

  - 需要对数据库对象结构修改事件、数据库安全功能审计级别的所有可审计事件、其他面向数据库安全审计员的，并且可绕过访问控制策略的特殊定义的可审计事件、未指定审计级别的所有可审计事件产生审计记录。
  - 每个审计记录中至少记录事件的日期和时间、事件类型、主体身份和关联组或角色、事件结果，根据评估对象和规定的格式生成审计数据。
  - 对于已标识用户行为所产生的审计事件，需要将每个审计事件和引起该审计的用户身份关联起来。
  - 安全审计员可以从审计记录中获取到用户、用户组或角色标识，审计事件类型，数据库对象标识，主体、主机标识，数据库权限的审计信息。使用授权用户理解的方式提供审计记录。
  - 安全审计员有明确的阅读访问审计数据的权限，禁止所有授权用户对审计记录进行读访问。
  - 保护审计迹中所存储的审计记录，以避免未授权的删除。

- 审计的设置是通过SYSAuditor用户来操作的，

  - 审计函数的定义：SP_AUDIT_OBJECT/SP_NOAUDIT_OBJECT    设置对象级审计/取消对象级审计

    ```sql
    VOID SP_AUDIT_OBJECT (
        TYPE VARCHAR(30),
        USERNAME VARCHAR (128),
        SCHNAME VARCHAR (128),
        TVNAME VARCHAR (128),
        COLNAME VARCHAR (128),--若不是表、视图，可以没有这个行
        WHENEVER VARCHAR (20)
    )
    参数说明：
    TYPE 对象级审计选项，即上表中的第一列
    USERNAME 用户名
    SCHNAME 模式名，为空时置‘null’
    TVNAME 表、视图、存储过程名不能为空
    COLNAME 列名
    WHENEVER 审计时机，可选的取值为：
    ALL：所有的
    SUCCESSFUL：操作成功时
    FAIL：操作失败时
    ```

  - 设置审计的具体的例子

    ```
    --对execute trigger的操作进行审计，审计的用户是user1,对象的模式是user1,对象名是INS_B，审计时机是所有
    SP_AUDIT_OBJECT('EXECUTE TRIGGER', 'USER1', 'USER1', 'INS_B', 'ALL');
    SP_NOAUDIT_OBJECT('EXECUTE TRIGGER', 'USER1', 'USER1', 'INS_B', 'ALL');
    ```


​	针对触发器关于审计的测试主要的目的是：查看触发器的触发信息是否会被审计所记录，如果没有记录，那么就违反了审计的要求。

一个完整的测试用例的流程：
  --创建user1用户，用户密码不少于9位，否则创建用户失败;授予权限
  CREATE USER USER1 IDENTIFIED BY 123456789;
  GRANT CREATE TABLE TO USER1;
  --用户1连接
  CONNECT 用户1/密码
  --用户1操作
  SQL
  --切换用户2
  CONNECT 用户2/密码
  --用户2操作
  SQL
在生成测试用例时，按照上述的格式来生成，才能保证代码一定能运行成功


关键词：触发器、自主访问控制、强制访问控制、审计、格式