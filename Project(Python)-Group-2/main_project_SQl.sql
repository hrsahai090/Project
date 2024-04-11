CREATE TABLE user_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name varchar(50),
    mobile_number VARCHAR(50) NOT NULL,
    parking_sticker VARCHAR(20) NOT NULL unique
);

drop table user_info;
select * from user_info;
desc user_info;

create table vehicles(
id iNT AUTO_INCREMENT PRIMARY KEY,
user_id INT , FOREIGN KEY(user_id) REFERENCES user_info(id),
vehicle_number VARCHAR(50) UNIQUE,
vehicle_type VARCHAR(30),
entry_time DATETIME,
exit_time DATETIME);

drop table vehicles;
select*from vehicles;
desc vehicles;

CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_type VARCHAR(10) NOT NULL,
    Payment_mode VARCHAR(20) NOT NULL,
    charges_type VARCHAR(10) NOT NULL,
    receipt_number VARCHAR(20) NOT NULL,
    charges int);   
    
drop table payment;
select * from payment;
desc payment;
