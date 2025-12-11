# @app.get("/get-all-students", response_model=List[StudentRead])
# async def get_all_students(db: AsyncSession = Depends(get_db)):
#     students = await student_crud.get_students(db)
#     return students

# @app.get("/get-students-by-mail", response_class=JSONResponse)
# async def get_students_by_mail(email: str, db: AsyncSession = Depends(get_db())):
#     student = await student_crud.get_student_by_email(db,email)

#     if student:
#         return JSONResponse(content={
#             "id": student.id,
#             "name": student.name,
#             "age": student.age,
#             "grade": student.grade,
#             "email": student.email
#         })
#     else:
#         return JSONResponse(content={"error": "Student not found"}, status_code=404)
