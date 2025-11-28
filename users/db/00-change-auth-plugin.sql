-- Set authentication plugin for admin to mysql_native_password to avoid JDBC public key retrieval requirement
ALTER USER 'admin'@'%' IDENTIFIED WITH mysql_native_password BY 'teamb321**';
FLUSH PRIVILEGES;
