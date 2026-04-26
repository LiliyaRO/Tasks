SELECT 
    u.username,
    COALESCE(r.roles_list, '') AS roles,
    COALESCE(a.activity_count, 0) AS activity_count
FROM users u
LEFT JOIN (
    SELECT user_id, STRING_AGG(role, ', ' ORDER BY role) AS roles_list
    FROM user_roles
    GROUP BY user_id
) r ON u.id = r.user_id
LEFT JOIN (
    SELECT user_id, COUNT(*) AS activity_count
    FROM user_activity
-- Перед 31.12.2024, выбираем активность за 30 дней до этой даты
WHERE activity_date >= '2024-10-01' AND activity_date <= '2024-10-31'
    GROUP BY user_id
) a ON u.id = a.user_id
WHERE a.activity_count > 0 -- добавляем условие: активность должна быть больше нуля
ORDER BY u.username;
