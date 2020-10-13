-- MySQL dump 10.13  Distrib 5.7.31, for Linux (x86_64)
--
-- Host: localhost    Database: loopvideo
-- ------------------------------------------------------
-- Server version	5.7.31-0ubuntu0.16.04.1

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
-- Current Database: `loopvideo`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `loopvideo` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `loopvideo`;

--
-- Table structure for table `channel`
--

DROP TABLE IF EXISTS `channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channel` (
  `channel_id` int(32) NOT NULL COMMENT '频道的ID，每建一个频道都需要生成一个32位的频道号；\n外部通过访问此频道来访问相关的内容；\n其为全局的主键；',
  `channel_type` varchar(5) CHARACTER SET utf8 DEFAULT NULL COMMENT '频道的类型\nLoop 可以设置轮播的内容，可以定时插入直播和点播的内容；\nLive 主要设置直播的内容，可以定时插入直播或者点播的内容；\n',
  `channel_name` varchar(100) CHARACTER SET utf8 NOT NULL COMMENT '频道名称，每个频道都有专有的名称；最长为100个字符，大约30多个字',
  `lasttime` datetime NOT NULL COMMENT '每次update记录时，都需要把当前的时间填写进该字段中；',
  `user_id` int(32) NOT NULL COMMENT '专属的用户的编号ID，32位；',
  `status` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT '频道的状态：10个字符；缺省状态：normal\n1、normal\n2、stop\n3、delete',
  PRIMARY KEY (`channel_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel`
--

LOCK TABLES `channel` WRITE;
/*!40000 ALTER TABLE `channel` DISABLE KEYS */;
/*!40000 ALTER TABLE `channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program` (
  `channel_id` int(32) NOT NULL COMMENT '频道的ID，频道ID+视频ID+日期 组成主键；',
  `media_id` int(32) NOT NULL AUTO_INCREMENT COMMENT '媒体ID，其为自动生成，如果有ID，则更改，如果没有则征建；',
  `media_type` varchar(10) CHARACTER SET latin1 NOT NULL COMMENT '媒体的类型:\n\n1、live 直播流\n2、file 文件流',
  `media_order` int(2) NOT NULL DEFAULT '0' COMMENT '循环的序号：对于循环的媒体排序号，默认为0;如果都为0，则为按记录顺序;\n其它类型的记录不起作用;\n\n默认:0',
  `media_name` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '媒体文件的名称',
  `media_url` varchar(255) CHARACTER SET latin1 NOT NULL COMMENT '轮播内容的地址，因为通过m3u8来实现，所以保存的是m3u8的地址；',
  `last_time` datetime NOT NULL COMMENT '最后修改时间，每次修改记录都需把该字段更新为当前时间',
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `delay` int(10) NOT NULL DEFAULT '0' COMMENT '延时时间调整；秒',
  `isloop` int(11) NOT NULL DEFAULT '1' COMMENT '循环标志\n1：循环，所设置的start-time和end-time都不起作用；\n其它为非循环播放，按start-time和end-time进行播放；',
  `status` varchar(10) CHARACTER SET latin1 NOT NULL COMMENT '记录的状态：10个字符；缺省状态：normal\n1、normal\n2、stop\n3、delete',
  PRIMARY KEY (`media_id`) USING BTREE,
  KEY `program_index` (`channel_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2031574 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(32) NOT NULL COMMENT '用户编号，该用户编号为32位的长度，不能够重复;',
  `login_name` varchar(255) COLLATE latin1_general_ci DEFAULT NULL,
  `user_name` varchar(40) CHARACTER SET utf8 NOT NULL COMMENT '用户的姓名；\n最长为40个字符；',
  `passwd` varchar(255) COLLATE latin1_general_ci DEFAULT NULL,
  `company_id` varchar(40) COLLATE latin1_general_ci DEFAULT NULL,
  `last_time` datetime NOT NULL COMMENT '每一次update操作都需要变更此内容；\n',
  `status` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT '用户的状态：10个字符；缺省状态：normal\n1、normal\n2、stop\n3、delete',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-13  0:03:28
