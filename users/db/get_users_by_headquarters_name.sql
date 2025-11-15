DELIMITER //

CREATE PROCEDURE GetUsersByHeadquartersName(IN p_headquarters_name VARCHAR(255))
BEGIN
    SELECT 
        u.email_unal,
        u.full_name AS user_name,
        uu.cod_unit,
        uu.name AS unit_name,
        s.cod_school,
        s.name AS school_name,
        h.cod_headquarters,
        h.name AS headquarters_name,
        p.cod_period
    FROM user_unal u
    INNER JOIN user_unit_associate uua 
        ON u.email_unal = uua.email_unal
    INNER JOIN unit_unal uu 
        ON uua.cod_unit = uu.cod_unit
    INNER JOIN unit_school_associate usa 
        ON uu.cod_unit = usa.cod_unit
    INNER JOIN school s 
        ON usa.cod_school = s.cod_school
    INNER JOIN school_headquarters_associate sha 
        ON s.cod_school = sha.cod_school
    INNER JOIN headquarters h 
        ON sha.cod_headquarters = h.cod_headquarters
    INNER JOIN period p 
        ON uua.cod_period = p.cod_period
        AND usa.cod_period = p.cod_period
        AND sha.cod_period = p.cod_period
    WHERE h.name = p_headquarters_name;  -- Ahora buscamos por nombre de la sede
END //

DELIMITER ;
