-- Знайти оцінки студентів у окремій групі з певного предмета
SELECT Students.name AS student_name, Grades.grade
FROM Students
JOIN Grades ON Students.id = Grades.student_id
WHERE Students.group_id = 1 AND Grades.subject_id = 2;