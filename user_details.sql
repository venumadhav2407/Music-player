-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2024 at 05:37 PM
-- Server version: 10.1.40-MariaDB
-- PHP Version: 7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `user_details`
--

-- --------------------------------------------------------

--
-- Table structure for table `playlist`
--

CREATE TABLE `playlist` (
  `id` int(11) NOT NULL,
  `username` varchar(60) DEFAULT NULL,
  `playlistname` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `playlist`
--

INSERT INTO `playlist` (`id`, `username`, `playlistname`) VALUES
(11, 'ram33', 'pops'),
(30, 'venu07', 'mylikes'),
(31, 'venu07', 'hiphop'),
(32, 'venu07', 'track2');

-- --------------------------------------------------------

--
-- Table structure for table `playlist_song`
--

CREATE TABLE `playlist_song` (
  `id` int(11) NOT NULL,
  `playlist_id` int(11) DEFAULT NULL,
  `song_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `playlist_song`
--

INSERT INTO `playlist_song` (`id`, `playlist_id`, `song_id`) VALUES
(1, 30, 10),
(2, 31, 7);

-- --------------------------------------------------------

--
-- Table structure for table `songs`
--

CREATE TABLE `songs` (
  `id` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `artist` varchar(255) NOT NULL,
  `album` varchar(255) NOT NULL,
  `language` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `songs`
--

INSERT INTO `songs` (`id`, `path`, `title`, `artist`, `album`, `language`) VALUES
(1, 'uploads\\Alayaaga_Vanthaai_Neeye.mp3', 'Alayaaga Vanthaai Neeye', 'Karthik, Najim Arshad, Arif Ansar', 'BEHINDD', 'TAMIL'),
(2, 'uploads\\Ente_Omane.mp3', 'Ente Omane', 'Shakthisree Gopalan, Harsha Vardhan', 'Ente Omane', 'TAMIL'),
(3, 'uploads\\Kutty_Pisasey.mp3', 'Kutty Pisasey', 'Hiphop Tamizha', 'PT Sir', 'TAMIL'),
(4, 'uploads\\Money_In_The_Bank.mp3', 'Money In The Bank', 'Yuvan Shankar Raja, IC 9nerz, Bank Rolls Young, S Ghost', 'Money in the Bank', 'TAMIL'),
(5, 'uploads\\Pei_Kadhal.mp3', 'Pei Kadhal ', 'Dharan Kumar', 'Pei Kaadhal', 'TAMIL'),
(6, 'uploads\\Justin_Bieber_-_Never_Let_You_Go_CeeNaija.com_.mp3', 'Never Let You Go', 'Justin Bieber', 'IG: @ Cee_Naija', 'ENGLISH'),
(7, 'uploads\\Sorry.mp3', 'Sorry', 'Justin Bieber', 'Justin Bieber', 'ENGLISH'),
(8, 'uploads\\Baby.mp3', 'Baby', 'Justin Bieber', 'Justin Bieber', 'ENGLISH'),
(9, 'uploads\\Intentions.mp3', 'Intentions (Tropical House Remix) Dj Dalal London', 'Justin Bieber', 'Justin Bieber', 'ENGLISH'),
(10, 'uploads\\Let-Me-Love-You.mp3', 'Let Me Love You', 'Justin Bieber', 'Justin Bieber', 'ENGLISH'),
(11, 'uploads\\I-Need-You-To-Stay.mp3', 'I Need You To Stay', 'Justin Bieber', 'Justin Bieber', 'ENGLISH'),
(12, 'uploads\\Heeriye.mp3', 'Heeriye', 'Arijit Singh , Jasleen Royal', 'Heeriye', 'PUNJABI'),
(13, 'uploads\\Neethane-Neethane.mp3', 'Neethane Neethane', 'A R Rahman , Shreya Ghoshal', 'Neethane Neethane', 'TAMIL'),
(14, 'uploads\\Vaa_En_Uyire.mp3', 'Vaa En Uyire ', 'Stephen Zechariah, Srinisha Jayaseelan', 'Vaa En Uyire', 'TAMIL'),
(15, 'uploads\\Thai_Thai.mp3', 'Thai Thai ', 'Thaman S, Roshini', 'Rasavathi', 'TAMIL');

-- --------------------------------------------------------

--
-- Table structure for table `userprofile`
--

CREATE TABLE `userprofile` (
  `id` int(11) NOT NULL,
  `username` varchar(60) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `passwd` varchar(60) DEFAULT NULL,
  `usertype` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `userprofile`
--

INSERT INTO `userprofile` (`id`, `username`, `email`, `passwd`, `usertype`) VALUES
(3, 'admin', 'admin@gmail.com', 'admin@123', 'admin'),
(2, 'ram33', 'ram@gmail.com', 'ram33', 'user'),
(1, 'venu07', 'venu@gmail.com', 'venu06', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `playlist`
--
ALTER TABLE `playlist`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `playlist_song`
--
ALTER TABLE `playlist_song`
  ADD PRIMARY KEY (`id`),
  ADD KEY `playlist_id` (`playlist_id`),
  ADD KEY `song_id` (`song_id`);

--
-- Indexes for table `songs`
--
ALTER TABLE `songs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `userprofile`
--
ALTER TABLE `userprofile`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `playlist`
--
ALTER TABLE `playlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `playlist_song`
--
ALTER TABLE `playlist_song`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `songs`
--
ALTER TABLE `songs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `userprofile`
--
ALTER TABLE `userprofile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `playlist`
--
ALTER TABLE `playlist`
  ADD CONSTRAINT `playlist_ibfk_1` FOREIGN KEY (`username`) REFERENCES `userprofile` (`username`);

--
-- Constraints for table `playlist_song`
--
ALTER TABLE `playlist_song`
  ADD CONSTRAINT `playlist_song_ibfk_1` FOREIGN KEY (`playlist_id`) REFERENCES `playlist` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `playlist_song_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
