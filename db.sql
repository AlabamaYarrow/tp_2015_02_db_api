DROP TABLE IF EXISTS `tp_db`.`user`;
DROP TABLE IF EXISTS `tp_db`.`forum`;
DROP TABLE IF EXISTS `tp_db`.`thread`;
DROP TABLE IF EXISTS `tp_db`.`post`;
DROP TABLE IF EXISTS `tp_db`.`follower`;
DROP TABLE IF EXISTS `tp_db`.`subscription`;


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
  `likes` INT NULL DEFAULT 0,
  `dislikes` INT NULL DEFAULT 0,
  `points` INT NULL DEFAULT 0,
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
  `likes` INT NULL DEFAULT 0,
  `dislikes` INT NULL DEFAULT 0,
  `points` INT NULL DEFAULT 0,
  `posts` INT NULL DEFAULT 0,
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


CREATE TABLE `tp_db`.`follower` (
  `follower` VARCHAR(45) NULL,
  `following` VARCHAR(45) NULL
) DEFAULT CHARSET=utf8;


CREATE TABLE `tp_db`.`subscription` (
  `subscriber` VARCHAR(45) NULL,
  `thread` INT NULL 
) DEFAULT CHARSET=utf8;
