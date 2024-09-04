import os
import logging
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from PyPDF2 import PdfReader
from .utils import answer_question


logger = logging.getLogger("qna")

class QuestionAnswerView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        questions = request.data.get('questions')
        pdf_file = request.FILES.get('pdf_file')
        logger.info(f"#qna#views#QuestionAnswerView# Question list: {questions} and PDF_File: {pdf_file}")
        if not questions or not pdf_file:
            return Response({"error": "Please provide both 'question' and a PDF file."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the uploaded PDF file
            file_path = f"/tmp/{pdf_file.name}"
            logger.info(f"#qna#views#QuestionAnswerView# File temporary path: {file_path}")
            with open(file_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            # Extract text from the PDF
            logger.info(f"#qna#views#QuestionAnswerView# PDF file reader started")
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            logger.info(f"#qna#views#QuestionAnswerView# PDF file reader done and text is {text}")

            # Remove the file after processing
            os.remove(file_path)
            logger.info(f"#qna#views#QuestionAnswerView# PDF File removed")

            # Use Langchain to answer the question based on the extracted text
            question_answer = {}
            for question in questions:
                answer = answer_question(questions, text)
                question_answer[question] = answer
                logger.info(f"Question: {question}, Answer: {answer}")

            logger.info(f"#qna#views#QuestionAnswerView# Response which we are returning: {question_answer}")
            return Response(question_answer, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
