'''
ALTER DATABASE tp_db DEFAULT COLLATE utf8_general_ci; 
ALTER TABLE [tablename] CONVERT TO CHARACTER SET utf8
'''

--FORUM:
---------------
CREATE TABLE `tp_db`.`forum` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `short_name` VARCHAR(45) NULL,
  `user` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  UNIQUE KEY `short_name_UNIQUE` (`short_name`))
  CHARACTER SET utf8 COLLATE utf8_general_ci;

---------------


--POST:
---------------
CREATE TABLE `tp_db`.`post` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `forum` VARCHAR(45) NULL,
  `date` DATETIME NULL,
  `isApproved` VARCHAR(45) NULL,
  `isDeleted` VARCHAR(45) NULL,
  `isEdited` VARCHAR(45) NULL,
  `isHighlighted` VARCHAR(45) NULL,
  `isSpam` VARCHAR(45) NULL,
  `message` TEXT NULL,
  `parent` VARCHAR(45) NULL,
  `thread` INT NULL,
  `user` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
  CHARACTER SET utf8 COLLATE utf8_general_ci;
---------------


--THREAD:
---------------
CREATE TABLE `tp_db`.`thread` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATETIME NULL,
  `forum` VARCHAR(45) NULL,
  `isClosed` VARCHAR(45) NULL,
  `isDeleted` VARCHAR(45) NULL,
  `message` TEXT NULL,
  `slug` TEXT NULL,
  `title` TEXT NULL,
  `user` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
  CHARACTER SET utf8 COLLATE utf8_general_ci;
---------------


--USER:
---------------
CREATE TABLE `tp_db`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `about` TEXT NULL,
  `isAnonymous` TINYINT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`)),
  UNIQUE KEY `email_UNIQUE` (`email`)
  CHARACTER SET utf8 COLLATE utf8_general_ci;
---------------

--FOLLOW:
