create table if not exists MagTable( Name varchar(10), Ra varchar(10), Dec varchar(10), B float, R float);

insert into MagTable values ("VO-001", "12:34:04.2", "-00:00:23.4", 15.4, 13.5);
insert into MagTable values ("VO-002", "12:15:00.0", "-14:23:15", 15.9, 13.6);
insert into MagTable values ("VO-003", "11:55:43.1", "-02:34:17.2", 17.2, 16.8);
insert into MagTable values ("VO-004", "11:32:42.1", "-00:01:17.3", 16.5, 14.3);

create table if not exists PhysTable( Name varchar(10), Teff varchar(10), FeH float);

insert into PhysTable values ("VO-001", "4501 K", 0.13);
insert into PhysTable values ("VO-002", "5321 K", -0.53);
insert into PhysTable values ("VO-003", "6600 K", -0.32);

