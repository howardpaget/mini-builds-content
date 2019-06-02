DROP TABLE IF EXISTS Entry;

DROP TABLE IF EXISTS Category;

CREATE TABLE IF NOT EXISTS Entry (
    `id` VARCHAR(32) NOT NULL UNIQUE,
    `title` VARCHAR(256) NOT NULL,
    `snippet` VARCHAR(1024) NOT NULL,
    `body` TEXT NOT NULL,
    `date` DATETIME NOT NULL,
    `category` VARCHAR(32) NOT NULL,
    `metadata` VARCHAR(2048)
);

CREATE TABLE IF NOT EXISTS Category (
    `id` VARCHAR(32) NOT NULL UNIQUE,
    `title` VARCHAR(32) NOT NULL,
    `colour` VARCHAR(8) NOT NULL
);