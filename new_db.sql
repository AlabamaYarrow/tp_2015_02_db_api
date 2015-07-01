DROP TABLE IF EXISTS `new_tp_db`.`user`;
DROP TABLE IF EXISTS `new_tp_db`.`forum`;
DROP TABLE IF EXISTS `new_tp_db`.`thread`;
DROP TABLE IF EXISTS `new_tp_db`.`post`;
DROP TABLE IF EXISTS `new_tp_db`.`follower`;
DROP TABLE IF EXISTS `new_tp_db`.`subscription`;


CREATE TABLE `new_tp_db`.`follower` (
  `follower` VARCHAR(45) NOT NULL,
  `following` VARCHAR(45) NOT NULL,
  KEY `fer_fing` (`follower`, `following`), 
  KEY `fing` (`following`)
) DEFAULT CHARSET=utf8;


CREATE TABLE `new_tp_db`.`forum` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `short_name` VARCHAR(45) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  UNIQUE KEY `short_name_UNIQUE` (`short_name`)
) DEFAULT CHARSET=utf8;


CREATE TABLE `new_tp_db`.`post` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `forum` VARCHAR(45) NULL,
  `date` DATETIME NULL,
  `isApproved` TINYINT NOT NULL,
  `isDeleted` TINYINT NOT NULL,
  `isEdited` TINYINT NOT NULL,
  `isHighlighted` TINYINT NOT NULL,
  `isSpam` TINYINT NOT NULL,
  `message` TEXT NOT NULL,
  `likes` INT NOT NULL DEFAULT 0,
  `dislikes` INT NOT NULL DEFAULT 0,
  `points` INT NOT NULL DEFAULT 0,
  `parent` INT NULL,
  `thread` INT NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),  
  KEY `post_forum_user` (`forum`, `user`), 
  KEY `post_user_date` (`user`, `date`), 
  KEY `post_forum_date` (`forum`, `date`),
  KEY `post_thread_date` (`thread`, `date`)
) DEFAULT CHARSET=utf8;
 

CREATE TABLE `new_tp_db`.`subscription` (
  `subscriber` VARCHAR(45) NOT NULL,
  `thread` INT NOT NULL,  
  KEY `subscriber` (`subscriber`) 
) DEFAULT CHARSET=utf8;


CREATE TABLE `new_tp_db`.`thread` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL,
  `forum` VARCHAR(45) NOT NULL,
  `isClosed` TINYINT NOT NULL,
  `isDeleted` TINYINT NOT NULL,
  `message` TEXT NOT NULL,
  `slug` TEXT NOT NULL,
  `title` TEXT NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `likes` INT NOT NULL DEFAULT 0,
  `dislikes` INT NOT NULL DEFAULT 0,
  `points` INT NOT NULL DEFAULT 0,
  `posts` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `thread_user_date` (`user`, `date`), 
  KEY `thread_forum_date` (`forum`, `date`)
) DEFAULT CHARSET=utf8;


CREATE TABLE `new_tp_db`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NULL,
  `about` TEXT NULL,
  `isAnonymous` TINYINT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `user_name_email` (`name`, `email`) 
) DEFAULT CHARSET=utf8;


