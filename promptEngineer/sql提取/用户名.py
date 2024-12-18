def _extract_credentials(connect_stmt) -> (str, str):
    _, credentials = connect_stmt.split(maxsplit=1)
    # if credentials
    if "AS" in credentials:
        credentials, _ = credentials.split('AS')
    user, password = credentials.split('/')
    if user == '' or user.upper() == 'SYSTEM' or user.upper() == 'SYS':
        return "SYSDBA", "SYSDBA"
    password = password.split(';')[0]
    # password = password.replace('"', '')
    if password.startswith('"'):
        password = password[1:]
    if password.endswith('"'):
        password = password[:-1]
    return user, password

sys = 'CONNECT user1/"123456789";'
user, password = _extract_credentials(sys)
print(user + " " + password)
sys = 'CONNECT user1/"123456789"'
user, password = _extract_credentials(sys)
print(user + " " + password)
sys = 'CONNECT sys/password AS SYSDBA'
user, password = _extract_credentials(sys)
print(user + " " + password)
sys = 'CONNECT / AS SYSDBA;'
user, password = _extract_credentials(sys)
print(user + " " + password)
sys = 'CONNECT user1/"12345678"9";'
user, password = _extract_credentials(sys)
print(user + " " + password)