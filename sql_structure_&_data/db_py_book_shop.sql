/*
 Navicat Premium Data Transfer

 Source Server         : MariaDataBase
 Source Server Type    : MariaDB
 Source Server Version : 101102 (10.11.2-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : db_py_book_shop

 Target Server Type    : MariaDB
 Target Server Version : 101102 (10.11.2-MariaDB)
 File Encoding         : 65001

 Date: 24/05/2023 23:07:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for authors
-- ----------------------------
DROP TABLE IF EXISTS `authors`;
CREATE TABLE `authors`  (
  `Code_author` int(11) NOT NULL AUTO_INCREMENT,
  `name_author` char(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `Birthday` date NULL DEFAULT NULL,
  PRIMARY KEY (`Code_author`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of authors
-- ----------------------------
INSERT INTO `authors` VALUES (1, 'Erich Maria Remarque', '1898-06-22');
INSERT INTO `authors` VALUES (2, 'George Orwell', '1903-06-25');
INSERT INTO `authors` VALUES (3, 'Lev Nikolayevich Tolstoy', '1828-09-09');
INSERT INTO `authors` VALUES (4, 'Jules Verne', '1828-02-08');
INSERT INTO `authors` VALUES (5, 'Fyodor Mikhailovich Dostoyevsky', '1821-11-11');

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books`  (
  `Code_book` int(11) NOT NULL AUTO_INCREMENT,
  `Title_book` char(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'BLANK',
  `Code_author` int(11) NULL DEFAULT NULL,
  `Pages` int(11) NULL DEFAULT NULL,
  `Code_publish` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`Code_book`) USING BTREE,
  INDEX `Code_author`(`Code_author`) USING BTREE,
  INDEX `Code_publish`(`Code_publish`) USING BTREE,
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`Code_author`) REFERENCES `authors` (`Code_author`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `books_ibfk_2` FOREIGN KEY (`Code_publish`) REFERENCES `publishing_house` (`Code_publish`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `CONSTRAINT_1` CHECK (`Pages` >= 5)
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of books
-- ----------------------------
INSERT INTO `books` VALUES (1, '1984', 2, 358, 4);
INSERT INTO `books` VALUES (2, 'Around the World in Eighty Days', 4, 383, 1);
INSERT INTO `books` VALUES (3, 'War and peace', 3, 832, 5);
INSERT INTO `books` VALUES (4, 'Arch of Triumph', 1, 221, 1);
INSERT INTO `books` VALUES (5, 'Crime and Punishment', 5, 608, 4);

-- ----------------------------
-- Table structure for deliveries
-- ----------------------------
DROP TABLE IF EXISTS `deliveries`;
CREATE TABLE `deliveries`  (
  `Code_delivery` int(11) NOT NULL AUTO_INCREMENT,
  `Name_delivery` char(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `Name_company` char(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `Address` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `Phone` bigint(20) NULL DEFAULT NULL,
  `OGRN` bigint(13) NULL DEFAULT NULL,
  PRIMARY KEY (`Code_delivery`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of deliveries
-- ----------------------------
INSERT INTO `deliveries` VALUES (1, 'DHL', 'Arvesso', 'Malaya Bronnaya St, 78', 79155590507, 1082615134117);
INSERT INTO `deliveries` VALUES (2, 'DPD', 'Thrivematrix', 'Ulitsa Ostozhenka, 63', 79255508819, 4065305163447);
INSERT INTO `deliveries` VALUES (3, 'IML', 'Synerys', 'Taganskaya Ulitsa, 28', 79355556771, 2152451466726);
INSERT INTO `deliveries` VALUES (4, 'Pickpoint', 'Veloxainc', 'New Arbat Ave, 64', 79255508819, 7028885742868);
INSERT INTO `deliveries` VALUES (5, 'EMS', 'Lumosia', 'Sarinskiy Proyezd, 49', 79355556771, 3082925110892);

-- ----------------------------
-- Table structure for publishing_house
-- ----------------------------
DROP TABLE IF EXISTS `publishing_house`;
CREATE TABLE `publishing_house`  (
  `Code_publish` int(11) NOT NULL AUTO_INCREMENT,
  `Publish` char(30) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `City` char(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Code_publish`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of publishing_house
-- ----------------------------
INSERT INTO `publishing_house` VALUES (1, 'AST Publishing Group', 'Moscow');
INSERT INTO `publishing_house` VALUES (2, 'Prosveshcheniye', 'Moscow');
INSERT INTO `publishing_house` VALUES (3, 'Rosman Publishing', 'Moscow');
INSERT INTO `publishing_house` VALUES (4, 'Izdatelstvo VES MIR', 'Moscow');
INSERT INTO `publishing_house` VALUES (5, 'Text Publishers', 'Moscow');

-- ----------------------------
-- Table structure for purchases
-- ----------------------------
DROP TABLE IF EXISTS `purchases`;
CREATE TABLE `purchases`  (
  `Code_purchase` int(11) NOT NULL AUTO_INCREMENT,
  `Code_book` int(11) NULL DEFAULT NULL,
  `Date_order` date NULL DEFAULT NULL,
  `Code_delivery` int(11) NULL DEFAULT NULL,
  `Amount` float NOT NULL,
  PRIMARY KEY (`Code_purchase`) USING BTREE,
  INDEX `Code_book`(`Code_book`) USING BTREE,
  INDEX `Code_delivery`(`Code_delivery`) USING BTREE,
  CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`Code_book`) REFERENCES `books` (`Code_book`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`Code_delivery`) REFERENCES `deliveries` (`Code_delivery`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of purchases
-- ----------------------------
INSERT INTO `purchases` VALUES (1, 4, '2013-07-07', 2, 1600.68);
INSERT INTO `purchases` VALUES (2, 1, '2021-07-18', 4, 799.54);
INSERT INTO `purchases` VALUES (3, 3, '2000-02-08', 4, 2900.29);
INSERT INTO `purchases` VALUES (4, 3, '2021-06-28', 5, 230.81);
INSERT INTO `purchases` VALUES (5, 1, '2002-09-23', 3, 472.87);

-- ----------------------------
-- Function structure for AddInAuthors
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInAuthors`;
delimiter ;;
CREATE FUNCTION `AddInAuthors`(IN value_name_author CHAR(30), value_birthday DATETIME)
 RETURNS int(11)
BEGIN
	INSERT INTO authors (name_author, Birthday)
	VALUES (value_name_author, value_birthday);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for AddInBooks
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInBooks`;
delimiter ;;
CREATE FUNCTION `AddInBooks`(IN value_title_book CHAR(40), IN value_code_author INT(11), IN value_pages INT(11), value_code_publish INT(11))
 RETURNS int(11)
BEGIN
	INSERT INTO books (title_book, code_author, pages, code_publish)
	VALUES (value_title_book, value_code_author, value_pages, value_code_publish);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for AddInDeliveries
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInDeliveries`;
delimiter ;;
CREATE FUNCTION `AddInDeliveries`(IN value_name_delivery CHAR(30), IN value_name_company CHAR(20), IN value_address VARCHAR(100), IN value_phone BIGINT(20), IN value_OGRN BIGINT(13))
 RETURNS int(11)
BEGIN
	INSERT INTO deliveries (Name_delivery, Name_company, Address, Phone, OGRN)
	VALUES (value_name_delivery, value_name_company, value_address, value_phone, value_OGRN);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for AddInPublishingHouse
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInPublishingHouse`;
delimiter ;;
CREATE FUNCTION `AddInPublishingHouse`(IN value_publish CHAR(30), IN value_city CHAR(20))
 RETURNS int(11)
BEGIN
	INSERT INTO publishing_house (Publish, City)
	VALUES (value_publish, value_city);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for AddInPurchases
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInPurchases`;
delimiter ;;
CREATE FUNCTION `AddInPurchases`(IN value_code_book INT(11), IN value_date_order DATE, IN value_code_delivery INT(11), IN value_amount FLOAT)
 RETURNS int(11)
BEGIN
	INSERT INTO purchases (Code_book, Date_order, Code_delivery, Amount)
	VALUES (value_code_book, value_date_order, value_code_delivery, value_amount);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for AvgPurchase
-- ----------------------------
DROP FUNCTION IF EXISTS `AvgPurchase`;
delimiter ;;
CREATE FUNCTION `AvgPurchase`()
 RETURNS float
BEGIN
	DECLARE avg FLOAT(10,2);
	SELECT AVG(Amount) INTO avg FROM purchases;
	RETURN avg;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for delete_from_authors
-- ----------------------------
DROP FUNCTION IF EXISTS `delete_from_authors`;
delimiter ;;
CREATE FUNCTION `delete_from_authors`(IN value_code_author INT(11))
 RETURNS float
BEGIN
	DELETE FROM `authors`
	WHERE code_author=value_code_author;
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for delete_from_books
-- ----------------------------
DROP FUNCTION IF EXISTS `delete_from_books`;
delimiter ;;
CREATE FUNCTION `delete_from_books`(IN value_code_book INT(11))
 RETURNS float
BEGIN
	DELETE FROM `books`
	WHERE code_book=value_code_book;
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for delete_from_deliveries
-- ----------------------------
DROP FUNCTION IF EXISTS `delete_from_deliveries`;
delimiter ;;
CREATE FUNCTION `delete_from_deliveries`(IN value_code_delivery INT(11))
 RETURNS float
BEGIN
	DELETE FROM `deliveries`
	WHERE code_delivery=value_code_delivery;
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for delete_from_publishing_house
-- ----------------------------
DROP FUNCTION IF EXISTS `delete_from_publishing_house`;
delimiter ;;
CREATE FUNCTION `delete_from_publishing_house`(IN value_code_publish INT(11))
 RETURNS float
BEGIN
	DELETE FROM `publishing_house`
	WHERE code_publish=value_code_publish;
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for delete_from_purchases
-- ----------------------------
DROP FUNCTION IF EXISTS `delete_from_purchases`;
delimiter ;;
CREATE FUNCTION `delete_from_purchases`(IN value_code_purchase INT(11))
 RETURNS float
BEGIN
	DELETE FROM `purchases`
	WHERE code_purchase=value_code_purchase;
	RETURN 0;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
