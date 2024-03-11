create database agenda;
use agenda;

create table personas(
idpersona int auto_increment primary key,
Nombreper varchar(60),
Apellidoper varchar (60),
emailper varchar (60),
dirreccionper varchar (60),
telefonoper int (12),
usuarioper varchar (60),
contraper varchar (60)
);

alter table personas modify telefonoper varchar(12);
select*from personas;