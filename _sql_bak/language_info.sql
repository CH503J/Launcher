/*
 Navicat Premium Dump SQL

 Source Server         : 123
 Source Server Type    : SQLite
 Source Server Version : 3045000 (3.45.0)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3045000 (3.45.0)
 File Encoding         : 65001

 Date: 09/07/2025 11:14:26
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for language_info
-- ----------------------------
DROP TABLE IF EXISTS "language_info";
CREATE TABLE "language_info" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "item_id" text,
  "name" TEXT,
  "short_name" TEXT,
  "description" TEXT,
  "fail_message" TEXT,
  "success_message" TEXT,
  "accept_player_message" TEXT,
  "decline_player_message" TEXT,
  "complete_player_message" TEXT,
  "other_value" TEXT
);

-- ----------------------------
-- Auto increment value for language_info
-- ----------------------------

PRAGMA foreign_keys = true;
