from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-2.5-flash")


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

# 🔥 ROTA DO CHATBOT
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensagem = data.get('mensagem')

    try:
        # 🧠 PROMPT INTELIGENTE (ENGENHARIA DE PROMPT)
        prompt = f"""
Você é um assistente oficial do evento Tech Future 2026.

INFORMAÇÕES DO EVENTO:
- Local: São Paulo
- Data: 12 a 14 de novembro de 2026
- Público: iniciantes e programadores
- Conteúdo: programação, IA, tecnologia, workshops

REGRAS:
- Responda de forma curta e clara
- Seja amigável
- Responda apenas sobre o evento
- Se não for sobre o evento diga:
  "Posso ajudar apenas com informações do evento Tech Future 2026."

PERGUNTA:
{mensagem}
"""

        response = model.generate_content(prompt)

        resposta = response.text if response.text else "Não consegui responder isso agora."

    except Exception as e:
        print("ERRO REAL:", e)
        resposta = "Erro ao gerar resposta 😢"

    return jsonify({"resposta": resposta})

@app.route('/inscricao', methods=['POST'])
def inscricao():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    tipo = request.form.get('tipo_ingresso')

    print(nome, email, telefone, tipo)

    mensagem = "Inscrição realizada com sucesso! 🚀"

    return render_template('index.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run()