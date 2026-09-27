FROM python:3.12-slim
WORKDIR /app
# get the requirements.txt file and install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# get tje rest of the app code
COPY . .
# run the transform.py 
CMD ["python", "src/transform.py"]