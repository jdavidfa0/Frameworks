-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 15-03-2024 a las 14:36:47
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `agenda`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `canciones`
--

CREATE TABLE `canciones` (
  `id_can` int(11) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `artista` varchar(50) NOT NULL,
  `genero` varchar(50) NOT NULL,
  `precio` decimal(10,0) NOT NULL,
  `duracion` varchar(20) NOT NULL,
  `lanzamiento` date NOT NULL,
  `img` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `canciones`
--

INSERT INTO `canciones` (`id_can`, `titulo`, `artista`, `genero`, `precio`, `duracion`, `lanzamiento`, `img`) VALUES
(1, 'Cry baby', 'Melanie Martinez', 'Indie', 200000, '5', '2017-02-13', 0x5265637572736f2036372e706e67);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

CREATE TABLE `compras` (
  `id_compra` int(11) NOT NULL,
  `fechacompra` date NOT NULL,
  `preciototal` decimal(10,0) NOT NULL,
  `user_id` int(11) NOT NULL,
  `id_cancion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personas`
--

CREATE TABLE `personas` (
  `idpersona` int(11) NOT NULL,
  `Nombreper` varchar(60) DEFAULT NULL,
  `Apellidoper` varchar(60) DEFAULT NULL,
  `emailper` varchar(60) DEFAULT NULL,
  `dirreccionper` varchar(60) DEFAULT NULL,
  `telefonoper` varchar(12) DEFAULT NULL,
  `usuarioper` varchar(60) DEFAULT NULL,
  `contraper` varchar(260) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `personas`
--

INSERT INTO `personas` (`idpersona`, `Nombreper`, `Apellidoper`, `emailper`, `dirreccionper`, `telefonoper`, `usuarioper`, `contraper`) VALUES
(4, 'Juana', 'Castro', 'juana@hotmail.com', 'San Carlos', '312549413', 'Juana71', 'dagdhgdfhfgh'),
(5, 'Juliana', 'Velazques', 'juli@outlook.es', 'Venecia', '34651684521', 'Juli.09', 'jkhfddfghjkj'),
(6, 'Juan', 'Juanito', 'juanjuaniojuana@juanito.com', 'San Juanito', '3548651651', 'Juanajuanitojuanoso', '$2b$12$KYfVOAHefLhZTah3YXTUvOl0S2G1jsdGLvIOlJHW8Q56Dgaq23XDe'),
(7, 'CARLA', 'CASTRO', 'CARLACASTRO12@GMAIL.COM', 'San vicente', '3123657841', 'CARLAC12', '$2b$12$GMwnKwtzGIHBK2BAOIdQwe6OMf1w35/ZF0ia8D2/.YOztRryUtlHO'),
(8, 'Yudy', 'Benosa', 'yudy.be@hotmail.es', 'Usme', '312547896411', 'Yudybene.15', 'Encriptado:scrypt:32768:8:1$4BVAhqyMdzDUaga1$c88545ce66e610e'),
(9, 'Milena', 'MIlanesa', 'MILE@GMAIL.COM', 'tUNAL', '518416861', 'mile.23', 'Encriptado:scrypt:32768:8:1$LICSokuREMGj8GRh$9de534e8850118f'),
(10, 'Lorena', 'Pulido', 'jadjiufgcsdk@gmail.com', 'Usaquuen', '237856415', 'lorelore', 'Encriptado:scrypt:32768:8:1$9iKxumFch7JXF94D$d1b8a8432c9645dc024bdcc4fc75d6de4aaa4aa0f90425bf7f4918b5516d55e7b6914451ad7f7545adddece7ae65ff314ea28173f972e8b1efbbf8de3b06b00e | coincide:True'),
(11, 'Johanna', 'cifuentes', 'cifuentes0903@gmail.com', 'ver', '7007', 'ljcm2023', 'scrypt:32768:8:1$MyXuQYjOWK7H5VZh$6bba69fb3e76fc80f944d93b61ee0ce6b54c2596b24d5049399a4905b1e5faa1e985107d5b2bd3b6934dc8b0cdbece413ba7776a931ad428cbb263a75e5a89df');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `canciones`
--
ALTER TABLE `canciones`
  ADD PRIMARY KEY (`id_can`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`id_compra`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `id_cancion` (`id_cancion`);

--
-- Indices de la tabla `personas`
--
ALTER TABLE `personas`
  ADD PRIMARY KEY (`idpersona`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `canciones`
--
ALTER TABLE `canciones`
  MODIFY `id_can` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `compras`
--
ALTER TABLE `compras`
  MODIFY `id_compra` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `personas`
--
ALTER TABLE `personas`
  MODIFY `idpersona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `compras`
--
ALTER TABLE `compras`
  ADD CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `personas` (`idpersona`),
  ADD CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`id_cancion`) REFERENCES `canciones` (`id_can`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
