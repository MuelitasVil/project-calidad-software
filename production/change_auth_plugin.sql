-- Production: change user plugin to mysql_native_password (run as a DB admin)
ALTER USER 'admin'@'%' IDENTIFIED WITH mysql_native_password BY 'teamb321**';
FLUSH PRIVILEGES;
