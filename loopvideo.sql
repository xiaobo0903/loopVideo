/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50728
 Source Host           : localhost:3306
 Source Schema         : loopvideo

 Target Server Type    : MySQL
 Target Server Version : 50728
 File Encoding         : 65001

 Date: 28/09/2020 18:38:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for channel
-- ----------------------------
DROP TABLE IF EXISTS `channel`;
CREATE TABLE `channel` (
  `channel_id` int(32) NOT NULL COMMENT '频道的ID，每建一个频道都需要生成一个32位的频道号；\n外部通过访问此频道来访问相关的内容；\n其为全局的主键；',
  `channel_type` varchar(5) CHARACTER SET utf8 DEFAULT NULL COMMENT '频道的类型\nLoop 可以设置轮播的内容，可以定时插入直播和点播的内容；\nLive 主要设置直播的内容，可以定时插入直播或者点播的内容；\n',
  `channel_name` varchar(100) CHARACTER SET utf8 NOT NULL COMMENT '频道名称，每个频道都有专有的名称；最长为100个字符，大约30多个字',
  `lasttime` datetime NOT NULL COMMENT '每次update记录时，都需要把当前的时间填写进该字段中；',
  `user_id` int(32) NOT NULL COMMENT '专属的用户的编号ID，32位；',
  `status` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT '频道的状态：10个字符；缺省状态：normal\n1、normal\n2、stop\n3、delete',
  PRIMARY KEY (`channel_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for program
-- ----------------------------
DROP TABLE IF EXISTS `program`;
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

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(32) NOT NULL COMMENT '用户编号，该用户编号为32位的长度，不能够重复;',
  `user_name` varchar(40) CHARACTER SET utf8 NOT NULL COMMENT '用户的姓名；\n最长为40个字符；',
  `last_time` datetime NOT NULL COMMENT '每一次update操作都需要变更此内容；\n',
  `status` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT '用户的状态：10个字符；缺省状态：normal\n1、normal\n2、stop\n3、delete',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

SET FOREIGN_KEY_CHECKS = 1;
