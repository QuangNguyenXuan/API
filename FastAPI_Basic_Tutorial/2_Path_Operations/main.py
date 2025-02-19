from fastapi import FastAPI

db = [
    {
        'student_id': '20240001',
        'student_name': 'A'
    },
    {
        'student_id': '20240002',
        'student_name': 'B'
    }
]

app = FastAPI()

# GET Method
@app.get('/student_db/{student_id}')
def get_student(student_id: str):
    for record in db:
        if record['student_id'] == student_id:
            return record


# POST Method
@app.post('/student_db')
def create_student(student_id: str, student_name: str):
    record = {
        'student_id': student_id,
        'student_name': student_name
    }

    db.append(record)


@app.put('/student_db/{student_id}')
def update_student(student_id: str, student_name: str):
    for record in db:
        if record['student_id'] == student_id:
            record['student_name'] = student_name


@app.delete('/student_db/{student_id}')
def delete_student(student_id: str):
    for record in db:
        if record['student_id'] == student_id:
            db.remove(record)