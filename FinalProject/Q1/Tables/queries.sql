--R1
--select count(*) from Observations as o join Data as d on o.ID == d.ObservationID where o.MJD > 56800 and o.MJD < 57300 and d.Flux1/d.dFlux1 > 5

--R2
--select J.StarID, J.Mag1, H.Mag1, J.Mag1 - H.Mag1 as J_H from J join H on J.StarID == H.StarID where J_H > 1.5

--R3
--select Ks.StarID, Ks.Flux1, Ks.dFlux1, Ks.Flux1 - (select AVG(Ks.Flux1) from Ks) as dev from Ks where dev > 20*Ks.dFlux1

select Ks.StarID, Ks.Flux1, Ks.dFlux1, 
(select avg(d.Flux1) from data as d  join Observations o on d.ObservationID == o.ID where d.StarID == Ks.StarID) as c
from Ks 


 --(SELECT IFNULL(ROUND(AVG(d.Flux1), 4) ,0) FROM  
   --  WHERE d2.id = d1.id AND pass = 1) as val_1,

--R4
--select * from Observations where FieldID == 1

--R5
/* 
select Y.StarID as StarID, Y.Mag1 as M_Y, Z.Mag1 as M_Z, J.Mag1 as M_Y, H.Mag1 as M_H, Ks.Mag1 as M_Ks
from (((Y join Z on Y.StarID == Z.StarID ) as a join J on J.StarID == a.StarID) as b join H on H.StarID == b.StarID) as c join Ks on Ks.StarID == c.StarID
where Y.Flux1/Y.dFlux1 > 30 and Z.Flux1/Z.dFlux1 > 30 and J.Flux1/J.dFlux1 > 30 and H.Flux1/H.dFlux1 > 30 and Ks.Flux1/Ks.dFlux1 > 30
*/