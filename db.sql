--FORUM:
---------------
CREATE TABLE `tp_db`.`forum` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `short_name` VARCHAR(45) NULL,
  `user` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
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
  `message` TINYTEXT NULL,
  `parent` VARCHAR(45) NULL,
  `thread` INT NULL,
  `user` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
---------------


--THREAD:
---------------
CREATE TABLE `tp_db`.`thread` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATETIME NULL,
  `forum` VARCHAR(45) NULL,
  `isClosed` VARCHAR(45) NULL,
  `isDeleted` VARCHAR(45) NULL,
  `message` TINYTEXT NULL,
  `slug` TINYTEXT NULL,
  `title` TINYTEXT NULL,
  `user` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
---------------


--USER:
---------------
CREATE TABLE `tp_db`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `about` VARCHAR(45) NULL,
  `isAnonymous` TINYINT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
---------------

--FOLLOW:
