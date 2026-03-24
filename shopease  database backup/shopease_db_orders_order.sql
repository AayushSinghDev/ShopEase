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
-- Table structure for table `orders_order`
--

DROP TABLE IF EXISTS `orders_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) NOT NULL DEFAULT 'pending',
  `payment_method` varchar(20) NOT NULL DEFAULT 'cod',
  `payment_id` varchar(200) DEFAULT NULL,
  `discount_code` varchar(50) DEFAULT NULL,
  `discount_amount` decimal(10,2) NOT NULL DEFAULT '0.00',
  `subtotal` decimal(10,2) NOT NULL DEFAULT '0.00',
  `shipping` decimal(10,2) NOT NULL DEFAULT '0.00',
  `tax` decimal(10,2) NOT NULL DEFAULT '0.00',
  `total` decimal(10,2) NOT NULL DEFAULT '0.00',
  `created_at` datetime(6) NOT NULL,
  `customer_id` bigint NOT NULL,
  `address_id` bigint DEFAULT NULL,
  `payment_status` varchar(20) NOT NULL,
  `razorpay_order_id` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_order_customer_id` (`customer_id`),
  KEY `orders_order_address_id` (`address_id`),
  CONSTRAINT `orders_order_address_id_fk` FOREIGN KEY (`address_id`) REFERENCES `orders_address` (`id`) ON DELETE SET NULL,
  CONSTRAINT `orders_order_customer_id_fk` FOREIGN KEY (`customer_id`) REFERENCES `accounts_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_order`
--

LOCK TABLES `orders_order` WRITE;
/*!40000 ALTER TABLE `orders_order` DISABLE KEYS */;
INSERT INTO `orders_order` VALUES (1,'delivered','razorpay','pay_D001','',0.00,45999.00,0.00,8279.82,54278.82,'2025-10-01 10:00:00.000000',1,1,'pending',NULL),(2,'delivered','cod','','',0.00,2999.00,49.00,539.82,3587.82,'2025-10-02 10:00:00.000000',2,3,'pending',NULL),(3,'delivered','razorpay','pay_D003','SAVE10',299.90,2999.00,0.00,539.82,3238.92,'2025-10-03 10:00:00.000000',3,5,'pending',NULL),(4,'delivered','cod','','',0.00,1499.00,49.00,269.82,1817.82,'2025-10-04 10:00:00.000000',4,7,'pending',NULL),(5,'delivered','razorpay','pay_D005','',0.00,29999.00,0.00,5399.82,35398.82,'2025-10-05 10:00:00.000000',5,9,'pending',NULL),(6,'delivered','cod','','',0.00,8999.00,49.00,1619.82,10667.82,'2025-10-06 10:00:00.000000',6,11,'pending',NULL),(7,'delivered','razorpay','pay_D007','FLAT200',200.00,5999.00,0.00,1079.82,6878.82,'2025-10-07 10:00:00.000000',7,13,'pending',NULL),(8,'delivered','cod','','',0.00,499.00,49.00,89.82,637.82,'2025-10-08 10:00:00.000000',8,15,'pending',NULL),(9,'delivered','razorpay','pay_D009','',0.00,64999.00,0.00,11699.82,76698.82,'2025-10-09 10:00:00.000000',9,17,'pending',NULL),(10,'delivered','cod','','',0.00,1299.00,49.00,233.82,1581.82,'2025-10-10 10:00:00.000000',10,19,'pending',NULL),(11,'shipped','razorpay','pay_D011','',0.00,109999.00,0.00,19799.82,129798.82,'2025-11-01 10:00:00.000000',11,21,'pending',NULL),(12,'shipped','cod','','',0.00,799.00,49.00,143.82,991.82,'2025-11-02 10:00:00.000000',12,23,'pending',NULL),(13,'shipped','razorpay','pay_D013','SAVE10',449.90,4499.00,0.00,809.82,4858.92,'2025-11-03 10:00:00.000000',13,25,'pending',NULL),(14,'shipped','cod','','',0.00,3499.00,49.00,629.82,4177.82,'2025-11-04 10:00:00.000000',14,27,'pending',NULL),(15,'shipped','razorpay','pay_D015','',0.00,14999.00,0.00,2699.82,17698.82,'2025-11-05 10:00:00.000000',15,29,'pending',NULL),(16,'processing','razorpay','pay_D016','',0.00,18999.00,0.00,3419.82,22418.82,'2025-11-15 10:00:00.000000',16,31,'pending',NULL),(17,'processing','cod','','',0.00,599.00,49.00,107.82,755.82,'2025-11-16 10:00:00.000000',17,33,'pending',NULL),(18,'processing','razorpay','pay_D018','FLAT200',200.00,9999.00,0.00,1799.82,11598.82,'2025-11-17 10:00:00.000000',18,35,'pending',NULL),(19,'processing','cod','','',0.00,2499.00,49.00,449.82,2997.82,'2025-11-18 10:00:00.000000',19,37,'pending',NULL),(20,'processing','razorpay','pay_D020','',0.00,49999.00,0.00,8999.82,58998.82,'2025-11-19 10:00:00.000000',20,39,'pending',NULL),(21,'shipped','cod','','',0.00,999.00,49.00,179.82,1227.82,'2025-12-01 10:00:00.000000',21,41,'pending',NULL),(22,'pending','razorpay','pay_D022','',0.00,1499.00,0.00,269.82,1768.82,'2025-12-02 10:00:00.000000',22,43,'pending',NULL),(23,'pending','cod','','',0.00,3999.00,49.00,719.82,4767.82,'2025-12-03 10:00:00.000000',23,45,'pending',NULL),(24,'pending','razorpay','pay_D024','SAVE10',129.90,1299.00,0.00,233.82,1403.92,'2025-12-04 10:00:00.000000',24,47,'pending',NULL),(25,'cancelled','cod','','',0.00,8999.00,49.00,1619.82,10667.82,'2025-12-05 10:00:00.000000',25,49,'pending',NULL),(26,'delivered','razorpay','pay_D026','',0.00,2499.00,0.00,449.82,2948.82,'2025-12-06 10:00:00.000000',26,51,'pending',NULL),(27,'delivered','cod','','',0.00,799.00,49.00,143.82,991.82,'2025-12-07 10:00:00.000000',27,53,'pending',NULL),(28,'delivered','razorpay','pay_D028','',0.00,4999.00,0.00,899.82,5898.82,'2025-12-08 10:00:00.000000',28,55,'pending',NULL),(29,'delivered','cod','','',0.00,299.00,49.00,53.82,401.82,'2025-12-09 10:00:00.000000',29,57,'pending',NULL),(30,'delivered','razorpay','pay_D030','FLAT200',200.00,18999.00,0.00,3419.82,22218.82,'2025-12-10 10:00:00.000000',30,59,'pending',NULL),(31,'delivered','cod','','',0.00,1499.00,49.00,269.82,1817.82,'2026-01-05 10:00:00.000000',31,61,'pending',NULL),(32,'delivered','razorpay','pay_D032','',0.00,84999.00,0.00,15299.82,100298.82,'2026-01-06 10:00:00.000000',32,63,'pending',NULL),(33,'shipped','cod','','',0.00,5999.00,49.00,1079.82,7127.82,'2026-01-10 10:00:00.000000',33,65,'pending',NULL),(34,'shipped','razorpay','pay_D034','',0.00,8999.00,0.00,1619.82,10618.82,'2026-01-11 10:00:00.000000',34,67,'pending',NULL),(35,'processing','cod','','',0.00,12999.00,49.00,2339.82,15387.82,'2026-01-15 10:00:00.000000',35,69,'pending',NULL),(36,'processing','razorpay','pay_D036','SAVE10',449.90,4499.00,0.00,809.82,4858.92,'2026-01-16 10:00:00.000000',36,71,'pending',NULL),(37,'pending','cod','','',0.00,2999.00,49.00,539.82,3587.82,'2026-01-20 10:00:00.000000',37,73,'pending',NULL),(38,'pending','razorpay','pay_D038','',0.00,6999.00,0.00,1259.82,8258.82,'2026-01-21 10:00:00.000000',38,75,'pending',NULL),(39,'delivered','cod','','',0.00,1799.00,49.00,323.82,2171.82,'2026-01-25 10:00:00.000000',39,77,'pending',NULL),(40,'delivered','razorpay','pay_D040','',0.00,35999.00,0.00,6479.82,42478.82,'2026-01-26 10:00:00.000000',40,79,'pending',NULL),(41,'delivered','cod','','',0.00,999.00,49.00,179.82,1227.82,'2026-02-01 10:00:00.000000',41,81,'pending',NULL),(42,'delivered','razorpay','pay_D042','FLAT200',200.00,3999.00,0.00,719.82,4518.82,'2026-02-02 10:00:00.000000',42,83,'pending',NULL),(43,'shipped','cod','','',0.00,1299.00,49.00,233.82,1581.82,'2026-02-05 10:00:00.000000',43,85,'pending',NULL),(44,'shipped','razorpay','pay_D044','',0.00,5499.00,0.00,989.82,6488.82,'2026-02-06 10:00:00.000000',44,87,'pending',NULL),(45,'processing','cod','','',0.00,2999.00,49.00,539.82,3587.82,'2026-02-10 10:00:00.000000',45,89,'pending',NULL),(46,'processing','razorpay','pay_D046','',0.00,17999.00,0.00,3239.82,21238.82,'2026-02-11 10:00:00.000000',46,91,'pending',NULL),(47,'pending','cod','','',0.00,1999.00,49.00,359.82,2407.82,'2026-02-15 10:00:00.000000',47,93,'pending',NULL),(48,'pending','razorpay','pay_D048','SAVE10',399.90,3999.00,0.00,719.82,4318.92,'2026-02-16 10:00:00.000000',48,95,'pending',NULL),(49,'delivered','cod','','',0.00,499.00,49.00,89.82,637.82,'2026-02-20 10:00:00.000000',49,97,'pending',NULL),(50,'delivered','razorpay','pay_D050','',0.00,8999.00,0.00,1619.82,10618.82,'2026-02-21 10:00:00.000000',50,99,'pending',NULL),(51,'delivered','razorpay','pay_D051','',0.00,4999.00,0.00,899.82,5898.82,'2026-03-01 10:00:00.000000',1,1,'pending',NULL),(52,'shipped','cod','','',0.00,1499.00,49.00,269.82,1817.82,'2026-03-02 10:00:00.000000',2,3,'pending',NULL),(53,'processing','razorpay','pay_D053','FLAT200',200.00,7999.00,0.00,1439.82,9238.82,'2026-03-03 10:00:00.000000',3,5,'pending',NULL),(54,'pending','cod','','',0.00,2999.00,49.00,539.82,3587.82,'2026-03-04 10:00:00.000000',4,7,'pending',NULL),(55,'delivered','razorpay','pay_D055','',0.00,39999.00,0.00,7199.82,47198.82,'2026-03-05 10:00:00.000000',5,9,'pending',NULL),(56,'delivered','cod','','',0.00,499.00,49.00,89.82,637.82,'2026-03-06 10:00:00.000000',6,11,'pending',NULL),(57,'shipped','razorpay','pay_D057','',0.00,9999.00,0.00,1799.82,11798.82,'2026-03-07 10:00:00.000000',7,13,'pending',NULL),(58,'processing','cod','','',0.00,1299.00,49.00,233.82,1581.82,'2026-03-08 10:00:00.000000',8,15,'pending',NULL),(59,'pending','razorpay','pay_D059','SAVE10',174.90,1749.00,0.00,314.82,1888.92,'2026-03-09 10:00:00.000000',9,17,'pending',NULL),(60,'delivered','cod','','',0.00,6999.00,49.00,1259.82,8307.82,'2026-03-10 10:00:00.000000',10,19,'pending',NULL),(61,'cancelled','cod',NULL,'',0.00,4999.00,0.00,249.95,5248.95,'2026-03-18 13:42:45.498890',1,2,'pending',NULL),(62,'pending','cod',NULL,'',0.00,1299.00,0.00,64.95,1363.95,'2026-03-23 16:30:03.556039',1,1,'pending',NULL),(63,'pending','cod',NULL,'',0.00,3697.00,0.00,184.85,3881.85,'2026-03-23 16:40:05.772182',1,1,'pending',NULL),(64,'pending','cod',NULL,'',0.00,199.00,49.00,9.95,257.95,'2026-03-23 17:36:58.891197',1,2,'pending',NULL),(65,'pending','cod',NULL,'',0.00,6999.00,0.00,349.95,7348.95,'2026-03-23 17:39:02.326139',1,2,'pending',NULL),(66,'pending','cod',NULL,'',0.00,8999.00,0.00,449.95,9448.95,'2026-03-24 06:17:25.496626',1,2,'pending',NULL);
/*!40000 ALTER TABLE `orders_order` ENABLE KEYS */;
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
