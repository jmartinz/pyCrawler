SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `pce` DEFAULT CHARACTER SET utf8 ;
USE `pce` ;

-- -----------------------------------------------------
-- Table `pce`.`pce_organo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pce`.`pce_organo` ;

CREATE TABLE IF NOT EXISTS `pce`.`pce_organo` (
  `id_organo` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(500) NULL,
  `url` VARCHAR(1000) NULL,
  PRIMARY KEY (`id_organo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pce`.`pce_ministerio`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pce`.`pce_ministerio` ;

CREATE TABLE IF NOT EXISTS `pce`.`pce_ministerio` (
  `id_ministerio` INT NOT NULL,
  `Nombre` VARCHAR(200) NULL,
  `Nombre_corto` VARCHAR(45) NULL,
  PRIMARY KEY (`id_ministerio`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pce`.`pce_expediente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pce`.`pce_expediente` ;

CREATE TABLE IF NOT EXISTS `pce`.`pce_expediente` (
  `id_expediente` INT NOT NULL AUTO_INCREMENT,
  `id_licitacion` INT NULL COMMENT 'En los expedientes sirve para abrir el detalle del mismo.\n',
  `num_expediente` VARCHAR(45) NULL,
  `desc_expediente` VARCHAR(500) NULL,
  `tipo_contrato_1` VARCHAR(150) NULL COMMENT 'Debería ir contra tabla',
  `tipo_contrato_2` VARCHAR(250) NULL COMMENT 'Debería depender del anterior/ir contra tabla',
  `importe` VARCHAR(45) NULL COMMENT 'Cambiar a tipo numérico',
  `estado` VARCHAR(45) NULL COMMENT 'Debería ser un id contra tabla',
  `id_organo` INT NULL,
  `fec_presentacion` VARCHAR(45) NULL COMMENT 'Pasar a fecha',
  `fec_adj_prov` VARCHAR(45) NULL COMMENT 'Pasar a fecha',
  `fec_adjudicacion` VARCHAR(45) NULL COMMENT 'Pasar a fecha',
  `fec_formalizacion` VARCHAR(45) NULL COMMENT 'Pasar a fecha',
  `fec_adj_definitiva` VARCHAR(45) NULL,
  `id_ministerio` INT NULL,
  PRIMARY KEY (`id_expediente`),
  INDEX `fk_pce_expediente_1_idx` (`id_organo` ASC),
  INDEX `fk_pce_expediente_2_idx` (`id_ministerio` ASC),
  CONSTRAINT `fk_pce_expediente_1`
    FOREIGN KEY (`id_organo`)
    REFERENCES `pce`.`pce_organo` (`id_organo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pce_expediente_2`
    FOREIGN KEY (`id_ministerio`)
    REFERENCES `pce`.`pce_ministerio` (`id_ministerio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
