-- (a) все сдачи студента по фамилии (JOIN);
SELECT
    u.full_name,
    u.group_name,
    a.pair_number,
    a.title,
    s.link,
    s.status,
    s.created_at
FROM submissions s
JOIN users u
    ON s.student_id = u.id
JOIN assignment a
    ON s.assignment_id = a.id
WHERE u.full_name ILIKE 'Иванов %'
ORDER BY s.created_at DESC;
-- выводит все сдачи студентов с указанной фамилией, включая повторные отправки, 
-- с информацией о задании, ссылке на работу, статусе и дате сдачи.

-- (b) сколько сдач пришло на каждое задание (JOIN + COUNT + GROUP BY);
SELECT
    a.id,
    a.pair_number,
    a.title,
    COUNT(s.id) AS submission_count
FROM assignment a
LEFT JOIN submissions s
    ON s.assignment_id = a.id
GROUP BY
    a.id,
    a.pair_number,
    a.title
ORDER BY a.pair_number;
-- Что делает: подсчитывает общее количество отправленных работ по каждому домашнему заданию, 
-- в том числе показывает задания без единой сдачи.

-- (c) студенты, не сдавшие ни одной работы (LEFT JOIN … IS NULL или NOT EXISTS, + роль)
SELECT
    u.id,
    u.full_name,
    u.group_name,
    u.email,
    u.telegram
FROM users u
LEFT JOIN submissions s
    ON s.student_id = u.id
WHERE s.id IS NULL
  AND u.role = 'STUDENT'
ORDER BY u.full_name;
-- Что делает: находит всех зарегистрированных студентов, 
-- которые ещё не отправили ни одной работы, исключая преподавателей.

