SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `movie_ticketbooking`
--

-- --------------------------------------------------------

--
-- Table structure for table `acc`
--

DROP TABLE IF EXISTS `acc`;
CREATE TABLE IF NOT EXISTS `acc` (
  `username` varchar(255) NOT NULL,
  `phno` varchar(255) DEFAULT NULL,
  `pass` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `acc`
--

INSERT INTO `acc` (`username`, `phno`, `pass`) VALUES
('Abhik', '9822924582', '123456'),
('Admin', '9821024582', '123456'),
('Dhruv', '9822724582 ', '123456'),
('Glad432', '9902671253', '123456'),
('Harshith', '9821924582', '123456'),
('Joshua', '9822245582', '123456'),
('Mrinal', '9822245822', '123456'),
('Peter', '9822284582', '123456'),
('Pranit', '9892224582', '123456'),
('Rashmi', '9821224582', '123456'),
('Tanishk', '9820229482', '123456'),
('Tnok', '9872224582', '123456'),
('Vidhya', '9822245829', '123456'),
('William', '9820224582', '123456');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
