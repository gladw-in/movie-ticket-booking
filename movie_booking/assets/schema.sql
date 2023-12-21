-- Customer accounts. `pass` holds a salted PBKDF2 hash (older rows may still
-- hold plaintext until their owner next logs in; see security.needs_rehash).
CREATE TABLE IF NOT EXISTS acc (
  username VARCHAR(255) NOT NULL,
  phno     VARCHAR(255) DEFAULT NULL,
  `pass`   VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
