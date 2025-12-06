-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 17, 2025 at 08:29 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `491`
--

-- --------------------------------------------------------

--
-- Table structure for table `indikator`
--

CREATE TABLE `indikator` (
  `id` int(11) NOT NULL,
  `nama_indikator` varchar(100) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `satuan` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `indikator`
--

INSERT INTO `indikator` (`id`, `nama_indikator`, `deskripsi`, `satuan`, `created_at`, `updated_at`) VALUES
(1, 'Inflasi', 'Inflasi Year-to-Year di Provinsi Sumatera Selatan', 'Persen', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(2, 'Nilai Tukar Petani', 'Perkembangan NTP dan NTUP', 'Persen', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(3, 'Nilai Impor', 'Nilai Impor Bulanan Provinsi Sumatera Selatan', 'US Dollar', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(4, 'Kedalaman Kemiskinan', 'Indeks Kedalaman Kemiskinan per Kabupaten/Kota', 'Indeks', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(5, 'Penduduk Menurut Umur Sekolah', 'Persentase Penduduk Menurut Kelompok Umur Sekolah', 'Persen', '2025-11-15 11:26:37', '2025-11-15 11:26:37');

-- --------------------------------------------------------

--
-- Table structure for table `inflasi`
--

CREATE TABLE `inflasi` (
  `id` int(11) NOT NULL,
  `indikator_id` int(11) NOT NULL DEFAULT 1,
  `tahun` int(11) NOT NULL,
  `kota` varchar(100) NOT NULL,
  `januari` decimal(10,2) DEFAULT NULL,
  `februari` decimal(10,2) DEFAULT NULL,
  `maret` decimal(10,2) DEFAULT NULL,
  `april` decimal(10,2) DEFAULT NULL,
  `mei` decimal(10,2) DEFAULT NULL,
  `juni` decimal(10,2) DEFAULT NULL,
  `juli` decimal(10,2) DEFAULT NULL,
  `agustus` decimal(10,2) DEFAULT NULL,
  `september` decimal(10,2) DEFAULT NULL,
  `oktober` decimal(10,2) DEFAULT NULL,
  `november` decimal(10,2) DEFAULT NULL,
  `desember` decimal(10,2) DEFAULT NULL,
  `tahunan` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inflasi`
--

INSERT INTO `inflasi` (`id`, `indikator_id`, `tahun`, `kota`, `januari`, `februari`, `maret`, `april`, `mei`, `juni`, `juli`, `agustus`, `september`, `oktober`, `november`, `desember`, `tahunan`, `created_at`, `updated_at`) VALUES
(3, 1, 2024, 'Kota Palembang', '2.54', '2.63', '2.90', '2.97', '3.03', '2.64', '2.09', '1.85', '1.41', '1.01', '0.95', '1.24', NULL, '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(4, 1, 2024, 'Kota Lubuk Linggau', '2.11', '2.15', '2.36', '2.45', '2.51', '2.16', '1.45', '1.31', '1.11', '0.89', '0.68', '1.02', NULL, '2025-11-15 11:26:37', '2025-11-15 12:06:06');

-- --------------------------------------------------------

--
-- Table structure for table `kedalaman_kemiskinan`
--

CREATE TABLE `kedalaman_kemiskinan` (
  `id` int(11) NOT NULL,
  `indikator_id` int(11) NOT NULL DEFAULT 4,
  `tahun` int(11) NOT NULL,
  `kabupaten_kota` varchar(100) NOT NULL,
  `indeks` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kedalaman_kemiskinan`
--

INSERT INTO `kedalaman_kemiskinan` (`id`, `indikator_id`, `tahun`, `kabupaten_kota`, `indeks`, `created_at`, `updated_at`) VALUES
(1, 4, 2025, 'Sumatera Selatan', '1.64', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(2, 4, 2025, 'Ogan Komering Ulu', '1.48', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(3, 4, 2025, 'Ogan Komering Ilir', '1.36', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(4, 4, 2025, 'Muara Enim', '1.28', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(5, 4, 2025, 'Lahat', '2.55', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(6, 4, 2025, 'Musi Rawas', '1.33', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(7, 4, 2025, 'Musi Banyuasin', '1.49', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(9, 4, 2025, 'Ogan Komering Ulu Selatan', '1.27', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(10, 4, 2025, 'Ogan Komering Ulu Timur', '0.97', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(11, 4, 2025, 'Ogan Ilir', '1.45', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(12, 4, 2025, 'Empat Lawang', '2.44', '2025-11-15 11:26:37', '2025-11-15 12:02:17'),
(13, 4, 2025, 'Pali', '1.01', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(14, 4, 2025, 'Musi Rawas Utara', '2.22', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(15, 4, 2025, 'Palembang', '1.40', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(16, 4, 2025, 'Prabumulih', '1.19', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(17, 4, 2025, 'Pagar Alam', '0.82', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(18, 4, 2025, 'Lubuk Linggau', '1.10', '2025-11-15 11:26:37', '2025-11-15 11:26:37');

-- --------------------------------------------------------

--
-- Table structure for table `nilai_impor`
--

CREATE TABLE `nilai_impor` (
  `id` int(11) NOT NULL,
  `indikator_id` int(11) NOT NULL DEFAULT 3,
  `tahun` int(11) NOT NULL,
  `bulan` varchar(20) NOT NULL,
  `nilai` decimal(15,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nilai_impor`
--

INSERT INTO `nilai_impor` (`id`, `indikator_id`, `tahun`, `bulan`, `nilai`, `created_at`, `updated_at`) VALUES
(1, 3, 2024, 'Januari', '221433470.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(2, 3, 2024, 'Februari', '228532193.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(3, 3, 2024, 'Maret', '194224514.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(4, 3, 2024, 'April', '167854458.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(5, 3, 2024, 'Mei', '157776714.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(6, 3, 2024, 'Juni', '139842889.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(7, 3, 2024, 'Juli', '237101870.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(8, 3, 2024, 'Agustus', '291838944.00', '2025-11-15 11:26:37', '2025-11-15 12:06:13'),
(9, 3, 2024, 'September', '165567987.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(10, 3, 2024, 'Oktober', '110624144.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(11, 3, 2024, 'November', '176843578.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(12, 3, 2024, 'Desember', '105509296.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(13, 3, 2026, 'Januari', '0.00', '2025-11-15 11:57:56', '2025-11-15 11:57:56'),
(14, 3, 2024, 'asdsadas', '0.00', '2025-11-15 12:06:17', '2025-11-15 12:06:17');

-- --------------------------------------------------------

--
-- Table structure for table `nilai_tukar_petani`
--

CREATE TABLE `nilai_tukar_petani` (
  `id` int(11) NOT NULL,
  `indikator_id` int(11) NOT NULL DEFAULT 2,
  `tahun` int(11) NOT NULL,
  `jenis_ntp` varchar(50) NOT NULL COMMENT 'NTP atau NTUP',
  `januari` decimal(10,2) DEFAULT NULL,
  `februari` decimal(10,2) DEFAULT NULL,
  `maret` decimal(10,2) DEFAULT NULL,
  `april` decimal(10,2) DEFAULT NULL,
  `mei` decimal(10,2) DEFAULT NULL,
  `juni` decimal(10,2) DEFAULT NULL,
  `juli` decimal(10,2) DEFAULT NULL,
  `agustus` decimal(10,2) DEFAULT NULL,
  `september` decimal(10,2) DEFAULT NULL,
  `oktober` decimal(10,2) DEFAULT NULL,
  `november` decimal(10,2) DEFAULT NULL,
  `desember` decimal(10,2) DEFAULT NULL,
  `tahunan` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nilai_tukar_petani`
--

INSERT INTO `nilai_tukar_petani` (`id`, `indikator_id`, `tahun`, `jenis_ntp`, `januari`, `februari`, `maret`, `april`, `mei`, `juni`, `juli`, `agustus`, `september`, `oktober`, `november`, `desember`, `tahunan`, `created_at`, `updated_at`) VALUES
(1, 2, 2025, 'NTP', '109.33', '111.88', '115.20', '116.28', '117.98', '122.40', '124.18', '123.70', '124.44', '127.20', '128.84', '128.53', NULL, '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(2, 2, 2025, 'NTUP', '110.44', '113.63', '118.05', '119.82', '121.09', '125.60', '126.20', '125.10', '125.40', '128.02', '130.28', '130.68', NULL, '2025-11-15 11:26:37', '2025-11-15 11:26:37');

-- --------------------------------------------------------

--
-- Table structure for table `penduduk_umur_sekolah`
--

CREATE TABLE `penduduk_umur_sekolah` (
  `id` int(11) NOT NULL,
  `indikator_id` int(11) NOT NULL DEFAULT 5,
  `tahun` int(11) NOT NULL,
  `kelompok_umur` varchar(50) NOT NULL,
  `tidak_belum_sekolah` decimal(10,2) DEFAULT NULL,
  `masih_sekolah` decimal(10,2) DEFAULT NULL,
  `tidak_sekolah_lagi` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `penduduk_umur_sekolah`
--

INSERT INTO `penduduk_umur_sekolah` (`id`, `indikator_id`, `tahun`, `kelompok_umur`, `tidak_belum_sekolah`, `masih_sekolah`, `tidak_sekolah_lagi`, `created_at`, `updated_at`) VALUES
(1, 5, 2024, '7-12', '0.00', '99.39', '0.61', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(2, 5, 2024, '13-15', '4.42', '95.45', '0.13', '2025-11-15 11:26:37', '2025-11-15 11:57:14'),
(3, 5, 2024, '16-18', '29.20', '70.80', '0.00', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(4, 5, 2024, '19-24', '80.51', '19.39', '0.11', '2025-11-15 11:26:37', '2025-11-15 11:26:37'),
(5, 5, 2024, '7-24', '29.88', '69.84', '0.28', '2025-11-15 11:26:37', '2025-11-15 11:26:37');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `indikator`
--
ALTER TABLE `indikator`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nama_indikator` (`nama_indikator`);

--
-- Indexes for table `inflasi`
--
ALTER TABLE `inflasi`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_tahun_kota` (`tahun`,`kota`),
  ADD KEY `indikator_id` (`indikator_id`);

--
-- Indexes for table `kedalaman_kemiskinan`
--
ALTER TABLE `kedalaman_kemiskinan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_tahun_wilayah` (`tahun`,`kabupaten_kota`),
  ADD KEY `indikator_id` (`indikator_id`);

--
-- Indexes for table `nilai_impor`
--
ALTER TABLE `nilai_impor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_tahun_bulan` (`tahun`,`bulan`),
  ADD KEY `indikator_id` (`indikator_id`);

--
-- Indexes for table `nilai_tukar_petani`
--
ALTER TABLE `nilai_tukar_petani`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_tahun_jenis` (`tahun`,`jenis_ntp`),
  ADD KEY `indikator_id` (`indikator_id`);

--
-- Indexes for table `penduduk_umur_sekolah`
--
ALTER TABLE `penduduk_umur_sekolah`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_tahun_kelompok` (`tahun`,`kelompok_umur`),
  ADD KEY `indikator_id` (`indikator_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `indikator`
--
ALTER TABLE `indikator`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `inflasi`
--
ALTER TABLE `inflasi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `kedalaman_kemiskinan`
--
ALTER TABLE `kedalaman_kemiskinan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `nilai_impor`
--
ALTER TABLE `nilai_impor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `nilai_tukar_petani`
--
ALTER TABLE `nilai_tukar_petani`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `penduduk_umur_sekolah`
--
ALTER TABLE `penduduk_umur_sekolah`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `inflasi`
--
ALTER TABLE `inflasi`
  ADD CONSTRAINT `inflasi_ibfk_1` FOREIGN KEY (`indikator_id`) REFERENCES `indikator` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `kedalaman_kemiskinan`
--
ALTER TABLE `kedalaman_kemiskinan`
  ADD CONSTRAINT `kedalaman_kemiskinan_ibfk_1` FOREIGN KEY (`indikator_id`) REFERENCES `indikator` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_impor`
--
ALTER TABLE `nilai_impor`
  ADD CONSTRAINT `nilai_impor_ibfk_1` FOREIGN KEY (`indikator_id`) REFERENCES `indikator` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_tukar_petani`
--
ALTER TABLE `nilai_tukar_petani`
  ADD CONSTRAINT `nilai_tukar_petani_ibfk_1` FOREIGN KEY (`indikator_id`) REFERENCES `indikator` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `penduduk_umur_sekolah`
--
ALTER TABLE `penduduk_umur_sekolah`
  ADD CONSTRAINT `penduduk_umur_sekolah_ibfk_1` FOREIGN KEY (`indikator_id`) REFERENCES `indikator` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
