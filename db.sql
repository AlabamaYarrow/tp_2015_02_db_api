
DROP TABLE `tp_db`.`user`;
DROP TABLE `tp_db`.`forum`;
DROP TABLE `tp_db`.`thread`;
DROP TABLE `tp_db`.`post`;


CREATE TABLE `tp_db`.`forum` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `short_name` VARCHAR(45) NULL,
  `user` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  UNIQUE KEY `short_name_UNIQUE` (`short_name`))
  DEFAULT CHARSET=utf8;

CREATE TABLE `tp_db`.`post` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `forum` VARCHAR(45) NULL,
  `date` DATETIME NULL,
  `isApproved` TINYINT NULL,
  `isDeleted` TINYINT NULL,
  `isEdited` TINYINT NULL,
  `isHighlighted` TINYINT NULL,
  `isSpam` TINYINT NULL,
  `message` TEXT NULL,
  `parent` INT NULL,
  `thread` INT NULL,
  `user` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
  DEFAULT CHARSET=utf8;
 

CREATE TABLE `tp_db`.`thread` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATETIME NULL,
  `forum` VARCHAR(45) NULL,
  `isClosed` TINYINT NULL,
  `isDeleted` TINYINT NULL,
  `message` TEXT NULL,
  `slug` TEXT NULL,
  `title` TEXT NULL,
  `user` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
  DEFAULT CHARSET=utf8;


CREATE TABLE `tp_db`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `about` TEXT NULL,
  `isAnonymous` TINYINT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`))
  DEFAULT CHARSET=utf8;

