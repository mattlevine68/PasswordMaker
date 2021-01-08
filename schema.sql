DROP SCHEMA IF EXISTS matt_pass CASCADE;
CREATE SCHEMA matt_pass;

DROP TABLE IF EXISTS website;
DROP TABLE IF EXISTS old_passwords;

CREATE TABLE website(
    url VARCHAR(512) PRIMARY KEY,
    name VARCHAR(127),
    password text UNIQUE
);

CREATE TABLE old_passwords(
    url VARCHAR(512) REFERENCES website,
    last_used TIMESTAMP,
    passwords text,
    PRIMARY KEY(url, last_used)
);

GRANT ALL PRIVILEGES ON website, old_passwords TO matt_password;

-- Creates a random password
DROP FUNCTION IF EXISTS random_password;
CREATE FUNCTION random_password(length INTEGER) RETURNS text
AS $$
DECLARE
  chars text[] := '{0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,!,@,#,$,%,^,&,*,(,),-,+}';
  result text := '';
  i integer := 0;
BEGIN
  IF length < 0
    THEN RAISE EXCEPTION 'Given length cannot be less than 0';
  END IF;
  FOR i in 1..length LOOP
    result := result || chars[1+random()*(array_length(chars, 1)-1)];
  END LOOP;
  RETURN result;
END;
$$ LANGUAGE plpgsql;


-- add the random password to the insert
DROP FUNCTION IF EXISTS password_maker;
CREATE FUNCTION password_maker() RETURNS TRIGGER
AS $$
BEGIN
  NEW.password = random_password(31);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER password_maker_trigger
BEFORE INSERT ON website
FOR EACH ROW
EXECUTE PROCEDURE password_maker();


-- when a new password is added makes a row in old_passwords
CREATE FUNCTION old_password_maker() RETURNS TRIGGER
AS $$
BEGIN
  INSERT INTO old_passwords VALUES(NEW.url, now(), NEW.password);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER old_password_maker_trigger
AFTER INSERT ON website
FOR EACH ROW
EXECUTE PROCEDURE old_password_maker();


-- on updates creates a new random password
DROP FUNCTION IF EXISTS password_update;
CREATE FUNCTION password_update() RETURNS TRIGGER
AS $$
BEGIN
  NEW.password = random_password(31);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER password_update_trigger
BEFORE UPDATE ON website
FOR EACH ROW
EXECUTE PROCEDURE password_update();
-- create view to look at old passwords


DROP FUNCTION IF EXISTS old_password_update;
CREATE FUNCTION old_password_update() RETURNS TRIGGER
AS $$
BEGIN
  INSERT INTO old_passwords VALUES(NEW.url, now(), NEW.password);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER old_password_update_trigger
AFTER UPDATE ON website
FOR EACH ROW
EXECUTE PROCEDURE old_password_update();
