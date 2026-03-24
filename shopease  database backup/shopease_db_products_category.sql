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
-- Table structure for table `products_category`
--

DROP TABLE IF EXISTS `products_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_category`
--

LOCK TABLES `products_category` WRITE;
/*!40000 ALTER TABLE `products_category` DISABLE KEYS */;
INSERT INTO `products_category` VALUES (1,'Electronics','https://images.unsplash.com/photo-1593359677879-a4bb92f4c2a9?w=300'),(2,'Mobile Phones','https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=300'),(3,'Laptops & Computers','https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=300'),(4,'Fashion - Men','https://images.unsplash.com/photo-1607345366928-199ea26cfe3e?w=300'),(5,'Fashion - Women','https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=300'),(6,'Kids & Baby','https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300'),(7,'Home & Kitchen','https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300'),(8,'Furniture','https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=300'),(9,'Books','https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300'),(10,'Sports & Fitness','https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=300'),(11,'Beauty & Personal Care','https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300'),(12,'Health & Wellness','https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300'),(13,'Grocery & Food','https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=300'),(14,'Toys & Games','https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300'),(15,'Automotive','https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=300'),(16,'Garden & Outdoors','https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300'),(17,'Jewellery & Accessories','https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=300'),(18,'Footwear','https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300'),(19,'Stationery & Office','https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=300'),(20,'Pet Supplies','https://images.unsplash.com/photo-1601758125946-6ec2ef64daf8?w=300');
/*!40000 ALTER TABLE `products_category` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-24 12:06:12
