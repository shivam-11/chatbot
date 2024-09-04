1. Activate virtual environment by using this command <source myenv/bin/activate>
2. To run server use this command <python manage.py runserver>
3. use this curl for api
curl --location --request POST 'http://127.0.0.1:8000/api/qna/' \
--header 'Content-Type: application/json' \
--form 'pdf_file=@"Poojitha_Pakala_47cdf84c-5b7f-4a8c-87b6-550518365a8f.pdf"' \
--form 'questions="[\"who is poojitha\"]"'
