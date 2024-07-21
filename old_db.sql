-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 16, 2024 at 10:17 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `studentweb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int NOT NULL,
  `unit_status` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `unit_status`, `username`, `password`) VALUES
(1, 1, 'XMEET', 'XOMMEET');

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `day` varchar(20) NOT NULL,
  `present_lectures` int NOT NULL,
  `absent_lectures` int NOT NULL,
  `late_lectures` int NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int NOT NULL,
  `attendance_id` int NOT NULL,
  `PB_status` tinyint(1) DEFAULT NULL,
  `LB_status` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`day`, `present_lectures`, `absent_lectures`, `late_lectures`, `time`, `user_id`, `attendance_id`, `PB_status`, `LB_status`) VALUES
('2024-06-18', 4, 2, 0, '2024-06-18 06:25:57', 1, 3, 1, 1),
('2024-06-18', 4, 2, 0, '2024-06-18 06:29:23', 6, 4, 1, 1),
('2024-06-18', 4, 2, 0, '2024-06-18 08:03:34', 7, 5, 1, 1),
('2024-06-19', 6, 0, 0, '2024-06-19 05:05:28', 1, 6, 1, 0),
('2024-06-19', 4, 0, 2, '2024-06-19 06:09:44', 6, 7, 1, 1),
('2024-06-19', 2, 2, 1, '2024-06-19 10:32:38', 7, 8, 1, 1),
('2024-06-20', 6, 0, 0, '2024-06-20 04:43:29', 1, 9, 1, 1),
('2024-06-20', 4, 0, 2, '2024-06-20 04:54:32', 6, 10, 1, 1),
('2024-06-20', 1, 3, 2, '2024-06-20 05:38:40', 7, 11, 1, 1),
('2024-06-20', 2, 0, 4, '2024-06-20 06:27:05', 8, 13, 1, 1),
('2024-06-20', 4, 2, 0, '2024-06-20 06:34:23', 9, 14, 1, 1),
('2024-06-20', 4, 2, 0, '2024-06-20 08:19:27', 13, 15, 1, 1),
('2024-06-20', 4, 2, 0, '2024-06-20 12:17:47', 15, 16, 1, 1),
('2024-06-20', 4, 0, 2, '2024-06-20 13:14:19', 16, 17, 1, 1),
('2024-06-20', 0, 0, 3, '2024-06-20 15:15:33', 17, 18, 1, 1),
('2024-06-20', 2, 2, 2, '2024-06-20 15:59:43', 18, 19, 1, 1),
('2024-06-21', 4, 2, 0, '2024-06-20 18:44:46', 16, 20, 1, 1),
('2024-06-21', 4, 2, 0, '2024-06-20 18:57:25', 19, 21, 1, 1),
('2024-06-21', 6, 0, 0, '2024-06-21 09:50:32', 1, 22, 1, 0),
('2024-06-21', 6, 0, 0, '2024-06-21 09:52:11', 7, 23, 1, 0),
('2024-06-21', 6, 0, 0, '2024-06-21 09:56:23', 8, 24, 1, 0),
('2024-06-22', 6, 0, 0, '2024-06-22 05:25:38', 1, 25, 1, 0),
('2024-06-22', 4, 2, 0, '2024-06-22 05:28:51', 7, 26, 1, 1),
('2024-06-22', 6, 0, 0, '2024-06-22 05:32:39', 16, 27, 1, 0),
('2024-06-22', 4, 2, 0, '2024-06-22 18:18:12', 18, 28, 1, 1),
('2024-06-23', 4, 2, 0, '2024-06-22 18:31:17', 16, 29, 1, 1),
('2024-06-23', 4, 2, 0, '2024-06-22 18:43:55', 20, 30, 1, 1),
('2024-06-23', 6, 0, 0, '2024-06-23 06:08:59', 1, 31, 1, 0),
('2024-06-23', 4, 0, 2, '2024-06-23 06:09:52', 7, 32, 1, 0),
('2024-06-25', 6, 0, 0, '2024-06-24 19:14:18', 16, 33, 1, 0),
('2024-06-25', 6, 0, 0, '2024-06-24 19:26:11', 1, 34, 1, 0),
('2024-06-25', 4, 2, 0, '2024-06-25 07:30:14', 21, 35, 1, 1),
('2024-06-25', 4, 2, 0, '2024-06-25 08:15:13', 17, 36, 1, 1),
('2024-07-04', 4, 2, 0, '2024-07-03 18:49:34', 23, 37, 1, 1),
('2024-07-05', 4, 0, 2, '2024-07-05 06:58:40', 1, 38, 1, 1),
('2024-07-05', 0, 0, 4, '2024-07-05 09:39:48', 24, 39, 1, 1),
('2024-07-07', 6, 0, 0, '2024-07-07 09:07:36', 1, 40, 1, 0),
('2024-07-08', 6, 0, 0, '2024-07-08 16:44:45', 1, 41, 1, 0),
('2024-07-09', 6, 0, 0, '2024-07-09 18:18:54', 1, 42, 1, 0),
('2024-07-10', 6, 0, 0, '2024-07-09 18:58:25', 1, 43, 1, 0),
('2024-07-11', 6, 0, 0, '2024-07-11 08:16:31', 1, 44, 1, 0),
('2024-07-14', 6, 0, 0, '2024-07-13 19:37:23', 1, 45, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `unit_marks`
--

CREATE TABLE `unit_marks` (
  `marks_id` int NOT NULL,
  `subject_1` int DEFAULT NULL,
  `subject_2` int DEFAULT NULL,
  `subject_3` int DEFAULT NULL,
  `subject_4` int DEFAULT NULL,
  `subject_5` int DEFAULT NULL,
  `current_unit` int NOT NULL,
  `user_id` int NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `unit_marks`
--

INSERT INTO `unit_marks` (`marks_id`, `subject_1`, `subject_2`, `subject_3`, `subject_4`, `subject_5`, `current_unit`, `user_id`, `status`) VALUES
(5, 6, 6, 6, 6, NULL, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user_data`
--

CREATE TABLE `user_data` (
  `user_id` int NOT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(150) NOT NULL,
  `f_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `l_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `profile_photo` varchar(150) DEFAULT NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user_data`
--

INSERT INTO `user_data` (`user_id`, `username`, `email`, `password`, `f_name`, `l_name`, `profile_photo`, `time`) VALUES
(1, 'meet17', 'meetoza1706@gmail.com', '$2b$12$CbF2iQ2il5g8QGTgXDiS7uL.YqNUfTgJ9cIH9ixezeKHvKJJ0bRWC', 'Meet', 'Oza', 'IMG_3708.jpeg', '2024-06-14 13:33:41'),
(4, 'vedoza', 'meetoza2006@gmail.com', '$2b$12$YOBAyZCegu.lGgttjyNKtObzc3ert.QSOVSVWMJ/DhWCR8V5.HG8K', NULL, NULL, NULL, '2024-06-14 22:38:47'),
(6, 'krina', 'krinaoza18@gmail.com', '$2b$12$OU9Tu3oMf56r5IlJHyoEdeKfvedo6uEBM0/LxjIGtPOUzprTy8W3a', 'Krina', 'Oza', 'Screenshot_2024-06-16_201829.png', '2024-06-15 00:38:58'),
(7, 'parth', 'vaghelaparth693@gmail.com', '$2b$12$MgtaJjcrdMeVV/rbFPFjo.uVASXiMAHvN8tg8hvAo469DayZrPwH6', 'Parth', 'Vaghela', 'icon.jpg', '2024-06-18 13:25:50'),
(8, 'vihar__ramavat', 'viharramavat@gmail.com', '$2b$12$2CJdgaBOiByp1spsQ8u7yeftgtsquU0NJv2DHEZjDxv4EdVDGC5Xe', 'Vihar', 'Ramavat', 'valorant-logo-FAB2CA0E55-seeklogo.com.png', '2024-06-20 11:54:29'),
(9, 'dhruv', 'dhruvbhimani2222@gmail.com', '$2b$12$/gbx5BPSPyfPJNmyn1Ve1.DVJHbM0vLnqSVtUcI5NXjePzlPZpBie', 'None', 'None', 'IMG_0665.jpg', '2024-06-20 12:02:35'),
(13, 'premal ', 'premaldhandhukiya1@gmail.com', '$2b$12$zAFK1J3x.nypT79yoauOPuypS2lMDHZlNnDJ3By2wjgCeNyuyviyu', NULL, NULL, NULL, '2024-06-20 13:48:16'),
(15, 'Yug Bhatt', 'yugbhatt1211@gmail.com', '$2b$12$8AZ8iWkiJIKgrB/xBS2UBe4pzLwnxO14edZ2KTMbvxfLgpGwCMqMO', 'Yug', 'Bhatt', 'header-image.jpg', '2024-06-20 17:47:00'),
(16, 'meet', 'ozamee17@gmail.com', '$2b$12$qMofnIBVI0y3DT5cmb7x4esbM.WhscIIL/7UwHjZ90KBeXDqovLBW', 'Meet', 'Oza', 'IMG_3842.jpeg', '2024-06-20 18:38:42'),
(17, 'Meet vyas', 'meetvyas2408@gmail.com', '$2b$12$Ty4K4Xc76OTBNlTEKfWktuZK.dAL6okJRalGmz777JBQIq.VFEpOa', 'meet ', 'vyas', NULL, '2024-06-20 20:42:52'),
(18, 'Krinatest', 'ozakrina18@gmail.com', '$2b$12$NxRQAN2hu35egAPxOZfbWuXBXCkjvR4MVIEkKqsoDDBa6zIkHleg.', NULL, NULL, NULL, '2024-06-20 21:29:14'),
(19, 'valayoza', 'andhariadevarshi4@gmail.com', '$2b$12$4JjsfqwqsXy/9q4ItcVbzejyPQfhcOqJ.6VPOwBvsHuP/T6fGQecq', NULL, NULL, NULL, '2024-06-21 00:25:33'),
(20, 'gamer', 'gamershub17115@gmail.com', '$2b$12$HzdIe/udVPaW.qrp7NTK7ODwuL6qAx59Bwqz7a8.G.0/ME.T9/uye', NULL, NULL, '1000030893.jpg', '2024-06-23 00:13:35'),
(21, 'Vinit-007', 'vinitpathak16@gmail.com', '$2b$12$tThh1v.EvEnR.enwuTrYROzjqtyq5VEU8YBCkJDbGfg4do5tKNjnq', NULL, NULL, NULL, '2024-06-25 12:59:24'),
(22, 'Naughty Gazhiabad', 'mandeepthakkar22@gmail.com', '$2b$12$yjtwdHFf.2vTkJVn5x.xau1xHN5DWlR4qzX/Q4W.p.ChvsO1ruL0u', NULL, NULL, NULL, '2024-06-25 13:29:37'),
(23, 'Utkarsh', 'pandey.utkarsh.08.11@gmail.com', '$2b$12$b26FoXya.77Qlkang4aVh.1GTS5VSulpp8ZivtGjexJaIvy9kAXl.', NULL, NULL, 'IMG_20240703_121549.jpg', '2024-07-04 00:18:32'),
(24, 'Mukund', 'mukundkachhadiya34@gmail.com', '$2b$12$dQWByheYiMmF9oZT3DLMaOGxc1N/hJsJuYbw0hm4X92MaktTnKVw.', NULL, NULL, NULL, '2024-07-05 15:03:52');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`attendance_id`),
  ADD KEY `user_id_fk` (`user_id`);

--
-- Indexes for table `unit_marks`
--
ALTER TABLE `unit_marks`
  ADD PRIMARY KEY (`marks_id`);

--
-- Indexes for table `user_data`
--
ALTER TABLE `user_data`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `attendance_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `unit_marks`
--
ALTER TABLE `unit_marks`
  MODIFY `marks_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `user_data`
--
ALTER TABLE `user_data`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
