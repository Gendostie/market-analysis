-- MySQL dump 10.13  Distrib 5.7.15, for Win64 (x86_64)
--
-- Host: localhost    Database: market_analysis
-- ------------------------------------------------------
-- Server version	5.7.15-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `historic_value`
--

DROP TABLE IF EXISTS `historic_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historic_value` (
  `date_historic_value` datetime NOT NULL,
  `id_symbol` varchar(10) NOT NULL,
  `revenu_usd_mil` decimal(3,0) DEFAULT '0',
  `gross_margin_pct` decimal(3,0) DEFAULT '0',
  `net_income_usd_mil` decimal(3,0) DEFAULT '0',
  `earning_per_share_usd` decimal(3,0) DEFAULT '0',
  `dividends_usd` decimal(3,0) DEFAULT '0',
  `book_value_per_share_usd` decimal(3,0) DEFAULT '0',
  `free_cash_flow_per_share_usd` decimal(3,0) DEFAULT '0',
  PRIMARY KEY (`date_historic_value`,`id_symbol`),
  KEY `id_symbol_idx` (`id_symbol`),
  CONSTRAINT `id_symbol_fk_historic_value` FOREIGN KEY (`id_symbol`) REFERENCES `company` (`symbol`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historic_value`
--

LOCK TABLES `historic_value` WRITE;
/*!40000 ALTER TABLE `historic_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `historic_value` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-30 20:15:43
