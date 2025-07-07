/*
 Navicat Premium Dump SQL

 Source Server         : 123
 Source Server Type    : SQLite
 Source Server Version : 3045000 (3.45.0)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3045000 (3.45.0)
 File Encoding         : 65001

 Date: 07/07/2025 17:25:36
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for game_info
-- ----------------------------
DROP TABLE IF EXISTS "game_info";
CREATE TABLE "game_info" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "game_root_path" TEXT,
  "server_path" TEXT,
  "server_name" TEXT,
  "server_version" TEXT,
  "fika_server_path" TEXT,
  "fika_server_name" TEXT,
  "fika_server_version" TEXT
);

-- ----------------------------
-- Auto increment value for game_info
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 3 WHERE name = 'game_info';

PRAGMA foreign_keys = true;
