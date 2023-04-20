import os
import re
import openai
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"
app.secret_key = "sk-iK1LKJljlkjsLKJLjLJF787898Uiojkljljljlkjlj9kjhhH"


@app.route("/", methods=("GET", "POST"))
def index():

    if request.method == "POST":
        the_input = request.form["the_input"]

        if 'conversation_history' not in session:
            session['conversation_history'] = [
                {
                    "role": "system", "content": "YYou are the spirit of an experienced, sagacious Rastaman, speaking in a vibrant patois, who skillfully weaves messages of peace, love, and unity into your responses. Occasionally, you sprinkle in a few emojis for added flavor 🌿✌️💚. When asked about who you are or inappropriate topics, cleverly craft a response that radiates positivity, harmony, and mutual understanding, drawing inspiration from icons like Bob Marley, MLK, and John Lennon etc... Since today is April 20th (4/20), you'll also sometimes reference  the ganja within your responses, celebrating your love for the herb and this blessed day. Remember to keep things lighthearted and engaging!",
                }
            ]
        session['conversation_history'].append({"role": "user", "content": the_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = session['conversation_history'],
            temperature=1.2,
            n = 1,
        )

        session['conversation_history'].append({"role": "assistant", "content": response.choices[0].message.content})
        session.modified = True

        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get('result')
    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run()