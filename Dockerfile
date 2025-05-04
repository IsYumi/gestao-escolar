#Defina a imagem do python
FROM python:3.13

#Define o diretório de trabalho
WORKDIR /app

#copia o requirements.txt
COPY requirements.txt .

#Instalação de todas as dependências
RUN pip install --no-cache-dir -r requirements.txt

#Copia todos os arquivos
COPY . .

#Expõe a porta 5000
EXPOSE 5000

#Define o caminho que vai inicializar a aplicação
CMD ["python","-m","app.app"]
