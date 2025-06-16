CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    cluster_points FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE student_subjects (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    subject_id INTEGER REFERENCES subjects(id)
);

CREATE TABLE interests (
    id SERIAL PRIMARY KEY,
    label VARCHAR(255) NOT NULL
);

CREATE TABLE student_interests (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    interest_id INTEGER REFERENCES interests(id)
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    min_cluster FLOAT,
    expected_pay VARCHAR(100),
    industries TEXT,
    skills_needed TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course_subject_requirements (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id),
    subject_id INTEGER REFERENCES subjects(id)
);

CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    course_id INTEGER REFERENCES courses(id),
    reason TEXT,
    rank INTEGER CHECK (rank IN (1, 2)),
    suggested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    comment TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
