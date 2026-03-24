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
-- Table structure for table `orders_orderitem`
--

DROP TABLE IF EXISTS `orders_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_name` varchar(200) NOT NULL,
  `product_price` decimal(10,2) NOT NULL,
  `quantity` int unsigned NOT NULL DEFAULT '1',
  `subtotal` decimal(10,2) NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_orderitem_order_id` (`order_id`),
  KEY `orders_orderitem_product_id` (`product_id`),
  CONSTRAINT `orders_orderitem_order_id_fk` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`) ON DELETE CASCADE,
  CONSTRAINT `orders_orderitem_product_id_fk` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_orderitem`
--

LOCK TABLES `orders_orderitem` WRITE;
/*!40000 ALTER TABLE `orders_orderitem` DISABLE KEYS */;
INSERT INTO `orders_orderitem` VALUES (1,'Sony 55\" 4K Smart TV',45999.00,1,45999.00,1,1),(2,'Levis 511 Slim Jeans',2999.00,1,2999.00,2,30),(3,'Lenovo ThinkPad E14',65999.00,1,2999.00,3,23),(4,'Aurelia Women Kurti',899.00,1,1499.00,4,42),(5,'Sony WH-1000XM5',29999.00,1,29999.00,5,10),(6,'Ergonomic Office Chair',8999.00,1,8999.00,6,73),(7,'Sapiens Harari',599.00,1,5999.00,7,82),(8,'Organic India Tulsi Tea',299.00,1,499.00,8,127),(9,'OnePlus 12',64999.00,1,64999.00,9,13),(10,'HealthSense Scale',1299.00,1,1299.00,10,97),(11,'Samsung Galaxy S24 Ultra',109999.00,1,109999.00,11,11),(12,'Flying Machine Tee',599.00,1,799.00,12,38),(13,'JBL Bluetooth Speaker',4999.00,1,4499.00,13,7),(14,'Pigeon Non-Stick Set',2999.00,1,3499.00,14,61),(15,'Kent RO Purifier',14999.00,1,14999.00,15,65),(16,'Nothing Phone 2',44999.00,1,18999.00,16,20),(17,'The Alchemist',299.00,2,599.00,17,80),(18,'PowerMax Dumbbell',9999.00,1,9999.00,18,93),(19,'Prestige Cooker 5L',2499.00,1,2499.00,19,59),(20,'DJI Mini 3 Drone',74999.00,1,49999.00,20,310),(21,'Pedigree Dog Food',999.00,1,999.00,21,191),(22,'Milton Bottle 1L',799.00,1,1499.00,22,62),(23,'Camping Tent 4P',5999.00,1,3999.00,23,154),(24,'Resistance Band Set',799.00,1,1299.00,24,98),(25,'Cosco Treadmill',8999.00,1,8999.00,25,94),(26,'Himalaya Face Wash',199.00,1,2499.00,26,102),(27,'Parle-G Biscuits',149.00,1,799.00,27,128),(28,'Urban Ladder Bookshelf',6999.00,1,4999.00,28,74),(29,'Ikigai Book',349.00,1,299.00,29,86),(30,'Pepperfry Sofa',18999.00,1,18999.00,30,70),(31,'Mothercare Baby Set',1499.00,1,1499.00,31,52),(32,'MacBook Air M2',114999.00,1,84999.00,32,24),(33,'Biba Lehenga Choli',4999.00,1,5999.00,33,40),(34,'Ergonomic Office Chair',8999.00,1,8999.00,34,73),(35,'LG 43\" LED TV',28999.00,1,12999.00,35,2),(36,'Philips Air Fryer',8999.00,1,4499.00,36,9),(37,'Allen Solly Shirt',1499.00,2,2999.00,37,29),(38,'IKEA Kallax Shelf',9999.00,1,6999.00,38,77),(39,'Boldfit Yoga Mat',1299.00,1,1799.00,39,91),(40,'Godrej Refrigerator',28999.00,1,35999.00,40,67),(41,'Royal Canin Cat Food',1499.00,1,999.00,41,192),(42,'BBQ Grill Portable',2499.00,1,3999.00,42,155),(43,'Everest Garam Masala',299.00,1,1299.00,43,126),(44,'WD 2TB HDD',5499.00,1,5499.00,44,220),(45,'Pigeon Non-Stick Set',2999.00,1,2999.00,45,61),(46,'Fossil Gen 6 Watch',17999.00,1,17999.00,46,211),(47,'Peter England Polo',799.00,2,1999.00,47,32),(48,'Multivitamin 60ct',599.00,1,3999.00,48,113),(49,'Rich Dad Poor Dad',399.00,1,499.00,49,81),(50,'Bose Soundbar 700',49999.00,1,8999.00,50,6),(51,'Kindle Paperwhite',14999.00,1,4999.00,51,205),(52,'Milton Bottle 1L',799.00,1,1499.00,52,62),(53,'Bajaj Mixer Grinder',3499.00,2,7999.00,53,60),(54,'H&M Crop Top',499.00,2,2999.00,54,45),(55,'GoPro Hero 11',39999.00,1,39999.00,55,204),(56,'Parle-G Biscuits',149.00,1,499.00,56,128),(57,'PowerMax Dumbbell',9999.00,1,9999.00,57,93),(58,'Resistance Band Set',799.00,1,1299.00,58,98),(59,'Psychology of Money',449.00,1,1749.00,59,83),(60,'IKEA Kallax Shelf',9999.00,1,6999.00,60,77),(61,'Skullcandy Indy ANC',4999.00,1,4999.00,61,401),(62,'My Little Pony Playset',1299.00,1,1299.00,62,485),(63,'Fossil Leather Bracelet',1799.00,1,1799.00,63,293),(64,'Fastrack Sunglasses UV400',1299.00,1,1299.00,63,168),(65,'Ayesha Ring Set 6pc',599.00,1,599.00,63,169),(66,'Chanakya Neeti Hindi',199.00,1,199.00,64,249),(67,'Urban Ladder Bookshelf 5T',6999.00,1,6999.00,65,74),(68,'Arrow Men Business Suit',8999.00,1,8999.00,66,31);
/*!40000 ALTER TABLE `orders_orderitem` ENABLE KEYS */;
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
