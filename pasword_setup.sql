DROP DATABASE IF EXISTS password_holder;
CREATE DATABASE password_holder;

DROP USER IF EXISTS matt_password;
CREATE USER matt_password WITH PASSWORD 'PasswordMaker';

GRANT ALL PRIVILEGES ON DATABASE password_holder TO matt_password;
ALTER USER matt_password SET search_path = matt_pass;
