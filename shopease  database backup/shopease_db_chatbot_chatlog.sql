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
-- Table structure for table `chatbot_chatlog`
--

DROP TABLE IF EXISTS `chatbot_chatlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chatbot_chatlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `session_key` varchar(100) NOT NULL,
  `user_role` varchar(20) NOT NULL DEFAULT 'guest',
  `user_id` bigint DEFAULT NULL,
  `user_message` longtext NOT NULL,
  `bot_response` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatbot_chatlog`
--

LOCK TABLES `chatbot_chatlog` WRITE;
/*!40000 ALTER TABLE `chatbot_chatlog` DISABLE KEYS */;
INSERT INTO `chatbot_chatlog` VALUES (1,'sess_001','customer',1,'Where is my order?','Your order #1 has been delivered. Thank you!','2026-03-18 18:25:19.000000'),(2,'sess_002','customer',2,'What is the return policy?','You can return within 7 days from My Orders.','2026-03-18 18:25:19.000000'),(3,'sess_003','guest',NULL,'Do you have Samsung phones?','Yes! Browse our Mobile Phones category.','2026-03-18 18:25:19.000000'),(4,'bfvb3uiek5eb15yhgjulvigr0uab31qm','customer',1,'pen','Hmm, not sure about that, Rahul Sharma! ? Try asking about products, orders, shipping, or payments!','2026-03-18 13:21:36.746177'),(5,'bfvb3uiek5eb15yhgjulvigr0uab31qm','customer',1,'help','? +91 96879 07055 | ✉️ support@shopease.com — We\'re happy to help!','2026-03-18 13:21:43.476225'),(6,'bfvb3uiek5eb15yhgjulvigr0uab31qm','customer',1,'retuen','I didn\'t quite get that! ? You can ask me about orders, products, delivery, discounts, or any ShopEase help.','2026-03-18 13:21:46.522860'),(7,'bfvb3uiek5eb15yhgjulvigr0uab31qm','customer',1,'order','Track your orders here ? <a href=\'/cart/my-orders/\' style=\'color:#f5a623;font-weight:700;\'>My Orders →</a> Need help with a specific order?','2026-03-18 13:21:54.371842'),(8,'bfvb3uiek5eb15yhgjulvigr0uab31qm','customer',1,'product','Browse our products at <a href=\'/products/\' style=\'color:#f5a623;font-weight:700;\'>Shop Now →</a> Categories: Automotive, Beauty & Personal Care, Books, Electronics! ?️','2026-03-18 13:21:58.262827'),(9,'zifaz0rn1luzqeql08zvlx4a7wlprji1','customer',1,'kaise ho','I\'m great, always ready to help! ? What can I do for you?','2026-03-24 05:03:49.132471'),(10,'zifaz0rn1luzqeql08zvlx4a7wlprji1','customer',1,'product','Browse our products at <a href=\'/products/\' style=\'color:#f5a623;font-weight:700;\'>Shop Now →</a> Categories: Automotive, Beauty & Personal Care, Books, Electronics! ?️','2026-03-24 05:03:54.459064'),(11,'yr2p2quqsnhzxt4uvx58ndwv8t0grfy8','customer',1,'product','Browse our products at <a href=\'/products/\' style=\'color:#f5a623;font-weight:700;\'>Shop Now →</a> Categories: Automotive, Beauty & Personal Care, Books, Electronics! ?️','2026-03-24 05:14:54.421547'),(12,'yr2p2quqsnhzxt4uvx58ndwv8t0grfy8','customer',1,'admin','Hmm, not sure about that, Rahul Sharma! ? Try asking about products, orders, shipping, or payments!','2026-03-24 05:14:57.209545'),(13,'yr2p2quqsnhzxt4uvx58ndwv8t0grfy8','customer',1,'payments','We currently support ? Cash on Delivery (COD). Online payment coming soon! ?','2026-03-24 05:15:06.498969'),(14,'yr2p2quqsnhzxt4uvx58ndwv8t0grfy8','customer',1,'payment','We support two payment methods: ? <strong>Cash on Delivery (COD)</strong> — pay at your door, and ? <strong>Online Payment via Razorpay</strong> — UPI, Cards, Net Banking, Wallets (256-bit SSL secured). Choose at checkout! ?','2026-03-24 05:17:14.627271'),(15,'yr2p2quqsnhzxt4uvx58ndwv8t0grfy8','customer',1,'product','Browse our products at <a href=\'/products/\' style=\'color:#f5a623;font-weight:700;\'>Shop Now →</a> Categories: Automotive, Beauty & Personal Care, Books, Electronics! ?️','2026-03-24 06:17:40.331613'),(16,'yr2p2quqsnhzxt4uvx58ndwv8t0grfy8','customer',1,'cart','Your cart ? <a href=\'/cart/\' style=\'color:#f5a623;font-weight:700;\'>View Cart →</a> Add products and checkout when ready!','2026-03-24 06:17:56.274502');
/*!40000 ALTER TABLE `chatbot_chatlog` ENABLE KEYS */;
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
