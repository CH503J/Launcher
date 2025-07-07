/*
 Navicat Premium Dump SQL

 Source Server         : 123
 Source Server Type    : SQLite
 Source Server Version : 3045000 (3.45.0)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3045000 (3.45.0)
 File Encoding         : 65001

 Date: 07/07/2025 16:39:05
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for about_info
-- ----------------------------
DROP TABLE IF EXISTS "about_info";
CREATE TABLE "about_info" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "app_name" TEXT,
  "version" TEXT,
  "author" TEXT,
  "github_link" TEXT,
  "example_path" TEXT
);

-- ----------------------------
-- Auto increment value for about_info
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 2 WHERE name = 'about_info';

PRAGMA foreign_keys = true;
