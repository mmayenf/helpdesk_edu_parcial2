INSERT INTO users (name, email, role) VALUES
 ('Ana Lopez', 'ana@edu.com', 'REQUESTER'),
 ('Bruno Perez', 'bruno@edu.com', 'REQUESTER'),
 ('Carlos Diaz', 'carlos@edu.com', 'TECHNICIAN'),
 ('Diana Ruiz', 'diana@edu.com', 'TECHNICIAN');

-- id 1..4 = Ana, Bruno, Carlos, Diana

INSERT INTO tickets (title, description, category, priority, status, requester_id, assignee_id) VALUES
 ('No imprime', 'La impresora no responde', 'Hardware', 'Medium', 'Open', 1, 3),
 ('No enciende', 'El equipo no enciende', 'Hardware', 'High', 'Open', 2, 3),
 ('Error de login', 'No puede iniciar sesion', 'Software', 'Low', 'Resolved', 1, 4),
 ('Pantalla azul', 'Falla al iniciar Windows', 'Hardware', 'Critical', 'Open', 2, NULL),
 ('Falta licencia', 'No tiene licencia de Office', 'Software', 'Medium', 'Closed', 1, 4);

-- id 1..5

INSERT INTO comments (ticket_id, author_id, text) VALUES
 (1, 3, 'Reviso mañana a primera hora'),
 (3, 4, 'Se reseteo la contraseña, resuelto');

-- tickets sin comentarios: 2, 4, 5

INSERT INTO ticket_history (ticket_id, field, old_value, new_value) VALUES
 (1, 'status', 'Open', 'Open'),
 (1, 'assignee_id', NULL, '3'),
 (3, 'status', 'Open', 'Resolved');
