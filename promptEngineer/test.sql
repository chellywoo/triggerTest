DROP user IF EXISTS user1;
create user user1 identified by 123456789;
grant create table, create trigger to user1;
CONNECT USER1/123456789;
CREATE TABLE USER1.TEMP_TABLE
(
    ID NUMBER(10),
    NAME VARCHAR2(50)
);
CREATE OR REPLACE TRIGGER USER1.TRIGGER_CHECK_MAX_SIZE
    BEFORE INSERT OR UPDATE ON USER1.TEMP_TABLE FOR EACH ROW
BEGIN
     
    IF :NEW.NAME IS NOT NULL THEN
        UPDATE USER1.TEMP_TABLE SET ID = ID * 2 + 1 WHERE NAME = :NEW.NAME;END IF;END;
INSERT INTO USER1.TEMP_TABLE (ID, NAME) VALUES (1, 'SampleName');
CONNECT USER1/123456789;
DROP TRIGGER USER1.TRIGGER_CHECK_MAX_SIZE;
DROP TABLE USER1.TEMP_TABLE;
DROP TRIGGER IF EXISTS USER1.TRIGGER_CHECK_MAX_SIZE;
DROP TABLE IF EXISTS USER1.TEMP_TABLE;
DROP user IF EXISTS user1;