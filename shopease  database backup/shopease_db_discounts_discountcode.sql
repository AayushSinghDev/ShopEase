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
-- Table structure for table `discounts_discountcode`
--

DROP TABLE IF EXISTS `discounts_discountcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discounts_discountcode` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `discount_type` varchar(20) NOT NULL DEFAULT 'percentage',
  `discount_value` decimal(10,2) NOT NULL,
  `minimum_order_value` decimal(10,2) NOT NULL DEFAULT '0.00',
  `expiry_date` date NOT NULL,
  `usage_limit` int NOT NULL DEFAULT '0',
  `used_count` int NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `discounts_discountcode_created_by_id_fk` (`created_by_id`),
  CONSTRAINT `discounts_discountcode_created_by_id_fk` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_seller` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts_discountcode`
--

LOCK TABLES `discounts_discountcode` WRITE;
/*!40000 ALTER TABLE `discounts_discountcode` DISABLE KEYS */;
INSERT INTO `discounts_discountcode` VALUES (1,'SAVE10','percentage',10.00,500.00,'2026-12-31',1000,120,1,'2025-01-01 10:00:00.000000',1),(2,'FLAT200','fixed',200.00,1500.00,'2026-12-31',500,85,1,'2025-01-02 10:00:00.000000',2),(3,'WELCOME15','percentage',15.00,1000.00,'2026-12-31',200,45,1,'2025-01-03 10:00:00.000000',3),(4,'SUMMER20','percentage',20.00,2000.00,'2026-08-31',300,210,1,'2025-04-01 10:00:00.000000',4),(5,'FESTIVE25','percentage',25.00,5000.00,'2026-10-31',100,67,1,'2025-09-01 10:00:00.000000',5),(6,'NEWUSER50','fixed',50.00,299.00,'2026-12-31',2000,0,1,'2025-01-05 10:00:00.000000',6),(7,'GADGET500','fixed',500.00,10000.00,'2026-06-30',100,33,1,'2025-03-01 10:00:00.000000',7),(8,'BOOK30','percentage',30.00,300.00,'2026-12-31',500,15,1,'2025-05-01 10:00:00.000000',8),(9,'HEALTH10','percentage',10.00,500.00,'2026-12-31',300,28,1,'2025-06-01 10:00:00.000000',9),(10,'EXPIRED10','percentage',10.00,500.00,'2024-12-31',100,5,0,'2024-01-01 10:00:00.000000',10);
/*!40000 ALTER TABLE `discounts_discountcode` ENABLE KEYS */;
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
