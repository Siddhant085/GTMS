/*This table includes all the Bidder details*/
CREATE TABLE IF NOT EXISTS `vender` (
  `vender_id` int NOT NULL AUTO_INCREMENT,
  `firm` varchar(200) NOT NULL,
  `firm_url` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `user_fname` varchar(100) NOT NULL,
  `mobile_no` varchar(12) NOT NULL,
  `pan_no` varchar(100) NOT NULL,
  `tan_no` varchar(100) NOT NULL,
  `vat_no` varchar(100) NOT NULL,
  PRIMARY KEY (`vender_id`)
);

ALTER TABLE vender AUTO_INCREMENT=100;

CREATE TABLE IF NOT EXISTS `admin` (
	`admin_id` int NOT NULL AUTO_INCREMENT,
	`username` varchar(50) NOT NULL,
	`password` varchar(50) NOT NULL,
	PRIMARY KEY (`admin_id`)
);

/*This table includes all the Bidder details*/

CREATE TABLE IF NOT EXISTS `tender` (
    `tender_id` int NOT NULL AUTO_INCREMENT,
    `est_amt` int(10) NOT NULL,
    `tender_pub_date` DATE NOT NULL,
    `tender_last_date` DATE NOT NULL,
    `tender_active` ENUM('a','r','w') NOT NULL,
    PRIMARY KEY (`tender_id`)
);

CREATE TABLE IF NOT EXISTS project (
	title varchar(200) NOT NULL,
	project_id int NOT NULL AUTO_INCREMENT,
	state varchar(100) NOT NULL,
	district varchar(100) NOT NULL,
	project_category int NOT NULL,
	bid_start_date DATE NOT NULL,
	bid_end_date DATE NOT NULL,
	project_desc varchar(1500) NOT NULL,
	project_status ENUM('a','w') NOT NULL,
	PRIMARY KEY(project_id)
);

/*Display Bid’s details.*/

CREATE TABLE IF NOT EXISTS `bidding`(
   `bid_id` int NOT NULL AUTO_INCREMENT,
   `vender_id` int NOT NULL,
   `tender_id` int NOT NULL,
   `project_id` int NOT NULL,
   PRIMARY KEY(`bid_id`)
);

/*Tender categories are stored in this table*/
 
CREATE TABLE IF NOT EXISTS `project_category`(
	`project_category_id` int NOT NULL,
	`project_category_name` varchar(200) NOT NULL,
	PRIMARY KEY(`project_category_id`)
);

/*Display only conatact details*/

CREATE TABLE IF NOT EXISTS `contact`(
	`id` int NOT NULL,
	`name` varchar(20) NOT NULL,
	`email` varchar(50) NOT NULL,
	`mobile` int NOT NULL,
	`message` varchar(200) NOT NULL,
	PRIMARY KEY(`id`)
);



/*Display latest news details*/

CREATE TABLE IF NOT EXISTS `news`(
	`news_id` int NOT NULL,
	`news_title` varchar(200) NOT NULL,
	`news_desc` varchar(200) NOT NULL,
	`desc` varchar(200) NOT NULL,
	`active` ENUM('y','n') NOT NULL,
	`date` date NOT NULL,
	PRIMARY KEY(`news_id`)
);

CREATE TABLE IF NOT EXISTS updates(
	project_id int NOT NULL,
	date date NOT NULL,
	percentage int NOT NULL,
	delays varchar(1000),
	update_id int NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(update_id)
);

ALTER TABLE updates
	ADD FOREIGN KEY (project_id) REFERENCES project(project_id);

ALTER TABLE `project`
   ADD FOREIGN KEY (`project_category`) REFERENCES `project_category` (`project_category_id`);

ALTER TABLE `bidding`
      ADD FOREIGN KEY (`vender_id`) REFERENCES `vender` (`vender_id`);
ALTER TABLE `bidding`
     ADD FOREIGN KEY (`tender_id`) REFERENCES `tender` (`tender_id`);
ALTER TABLE `bidding`
	 ADD FOREIGN KEY (project_id) REFERENCES project (project_id);

CREATE OR REPLACE VIEW login AS SELECT vender_id, username, password, 'vender' FROM vender UNION ALL SELECT admin_id, username, password, 'admin' FROM admin;
