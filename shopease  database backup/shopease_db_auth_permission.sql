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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_fk` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Customer',7,'add_customer'),(26,'Can change Customer',7,'change_customer'),(27,'Can delete Customer',7,'delete_customer'),(28,'Can view Customer',7,'view_customer'),(29,'Can add Seller',8,'add_seller'),(30,'Can change Seller',8,'change_seller'),(31,'Can delete Seller',8,'delete_seller'),(32,'Can view Seller',8,'view_seller'),(33,'Can add Super Admin',9,'add_superadmin'),(34,'Can change Super Admin',9,'change_superadmin'),(35,'Can delete Super Admin',9,'delete_superadmin'),(36,'Can view Super Admin',9,'view_superadmin'),(37,'Can add Category',10,'add_category'),(38,'Can change Category',10,'change_category'),(39,'Can delete Category',10,'delete_category'),(40,'Can view Category',10,'view_category'),(41,'Can add Product',11,'add_product'),(42,'Can change Product',11,'change_product'),(43,'Can delete Product',11,'delete_product'),(44,'Can view Product',11,'view_product'),(45,'Can add Review',14,'add_review'),(46,'Can change Review',14,'change_review'),(47,'Can delete Review',14,'delete_review'),(48,'Can view Review',14,'view_review'),(49,'Can add Wishlist',15,'add_wishlist'),(50,'Can change Wishlist',15,'change_wishlist'),(51,'Can delete Wishlist',15,'delete_wishlist'),(52,'Can view Wishlist',15,'view_wishlist'),(53,'Can add product image',12,'add_productimage'),(54,'Can change product image',12,'change_productimage'),(55,'Can delete product image',12,'delete_productimage'),(56,'Can view product image',12,'view_productimage'),(57,'Can add product variant',13,'add_productvariant'),(58,'Can change product variant',13,'change_productvariant'),(59,'Can delete product variant',13,'delete_productvariant'),(60,'Can view product variant',13,'view_productvariant'),(61,'Can add Address',16,'add_address'),(62,'Can change Address',16,'change_address'),(63,'Can delete Address',16,'delete_address'),(64,'Can view Address',16,'view_address'),(65,'Can add Order',17,'add_order'),(66,'Can change Order',17,'change_order'),(67,'Can delete Order',17,'delete_order'),(68,'Can view Order',17,'view_order'),(69,'Can add Order Item',18,'add_orderitem'),(70,'Can change Order Item',18,'change_orderitem'),(71,'Can delete Order Item',18,'delete_orderitem'),(72,'Can view Order Item',18,'view_orderitem'),(73,'Can add Discount Code',19,'add_discountcode'),(74,'Can change Discount Code',19,'change_discountcode'),(75,'Can delete Discount Code',19,'delete_discountcode'),(76,'Can view Discount Code',19,'view_discountcode'),(77,'Can add Chat Log',20,'add_chatlog'),(78,'Can change Chat Log',20,'change_chatlog'),(79,'Can delete Chat Log',20,'delete_chatlog'),(80,'Can view Chat Log',20,'view_chatlog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-24 12:06:09
