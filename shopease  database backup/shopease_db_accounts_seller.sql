-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: shopease_db
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_seller`
--

DROP TABLE IF EXISTS `accounts_seller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_seller` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `is_approved` tinyint(1) NOT NULL DEFAULT '1',
  `face_data` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_seller`
--

LOCK TABLES `accounts_seller` WRITE;
/*!40000 ALTER TABLE `accounts_seller` DISABLE KEYS */;
INSERT INTO `accounts_seller` VALUES (1,'TechWorld Store','seller1@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000001',1,NULL),(2,'FashionHub','seller2@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000002',1,NULL),(3,'GadgetZone','seller3@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000003',1,NULL),(4,'HomeEssentials','seller4@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000004',1,NULL),(5,'SportsMart','seller5@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000005',1,NULL),(6,'BookCorner','seller6@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000006',1,NULL),(7,'BeautyBliss','seller7@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000007',1,NULL),(8,'KidsTreasure','seller8@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000008',1,NULL),(9,'FurnitureKing','seller9@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000009',1,NULL),(10,'HealthPlus','seller10@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000010',1,NULL),(11,'AutoAccessories','seller11@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000011',1,NULL),(12,'GroceryFresh','seller12@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000012',1,NULL),(13,'JewelryWorld','seller13@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000013',1,NULL),(14,'PetParadise','seller14@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000014',1,NULL),(15,'GardenGreen','seller15@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000015',1,NULL),(16,'StationeryPro','seller16@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000016',1,NULL),(17,'ToyLand','seller17@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000017',1,NULL),(18,'FootwearFirst','seller18@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000018',1,NULL),(19,'MobileMantra','seller19@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000019',1,NULL),(20,'LaptopLane','seller20@shopease.com','pbkdf2_sha256$260000$qqXWv7ew0aZi$7DzAFrGq4twYlDt8TwlFg4pRmEmUYGivg/DbC/8/BQ4=','9800000020',1,NULL);
/*!40000 ALTER TABLE `accounts_seller` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-24 12:06:10
