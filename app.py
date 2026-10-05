from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

# ============================================================
# GOVERNMENT SCHEMES DATABASE
# ============================================================

schemes = {
    "pm kisan": {
        "name": "PM-KISAN",
        "description": "PM-KISAN provides financial assistance to eligible farmer families.",
        "eligibility": "Eligible landholding farmer families can apply.",
        "documents": "Aadhaar Card, bank account details and land records.",
        "apply": "Apply through the official PM-KISAN portal or a Common Service Centre (CSC)."
    },

    "ayushman bharat": {
        "name": "Ayushman Bharat",
        "description": "Ayushman Bharat provides health coverage to eligible beneficiaries.",
        "eligibility": "Eligibility depends on the applicable government beneficiary criteria.",
        "documents": "Aadhaar Card and other required identity documents.",
        "apply": "Visit an authorized hospital, CSC or the appropriate government portal."
    },

    "pm awas yojana": {
        "name": "PM Awas Yojana",
        "description": "PM Awas Yojana supports eligible families in obtaining housing.",
        "eligibility": "Eligible economically weaker and low-income households.",
        "documents": "Aadhaar Card, income proof and address proof.",
        "apply": "Apply through the appropriate government portal or local authority."
    },

    "beti bachao beti padhao": {
        "name": "Beti Bachao Beti Padhao",
        "description": "This initiative promotes the education, welfare and empowerment of girls.",
        "eligibility": "Girls and families covered under applicable government programs.",
        "documents": "Documents depend on the specific service or program.",
        "apply": "Contact the concerned government department or local authority."
    },

    "digital india": {
        "name": "Digital India",
        "description": "Digital India promotes digital services and digital access for citizens.",
        "eligibility": "Citizens can access various digital government services.",
        "documents": "Documents depend on the specific service.",
        "apply": "Use the relevant official government online service."
    }
}


# ============================================================
# CHATBOT FUNCTION
# ============================================================

def chatbot_response(message):

    message = message.lower().strip()

    # Normalize common variations such as PM-KISAN, PM_KISAN and PM KISAN
    message = re.sub(r"[-_]+", " ", message)
    message = re.sub(r"\s+", " ", message).strip()

    # Greeting
    if re.search(r"\b(hello|hi|hey)\b", message):
        return "Hello! 👋 I am the Government Services AI Chatbot. How can I help you?"

    # Help
    if "help" in message:
        return (
            "I can provide information about:\n\n"
            "• PM-KISAN\n"
            "• Ayushman Bharat\n"
            "• PM Awas Yojana\n"
            "• Beti Bachao Beti Padhao\n"
            "• Digital India\n\n"
            "You can ask about eligibility, documents or application procedure."
        )

    # Find government scheme
    selected_scheme = None

    # Check scheme names and common aliases
    scheme_aliases = {
        "pm kisan": "pm kisan",
        "pmkisan": "pm kisan",
        "pradhan mantri kisan samman nidhi": "pm kisan",
        "ayushman bharat": "ayushman bharat",
        "pm awas yojana": "pm awas yojana",
        "pmay": "pm awas yojana",
        "beti bachao beti padhao": "beti bachao beti padhao",
        "digital india": "digital india"
    }

    for alias, key in scheme_aliases.items():
        if alias in message:
            selected_scheme = schemes[key]
            break

    # Scheme not found
    if selected_scheme is None:

        return (
            "Sorry, I could not identify the government scheme. ❌\n\n"
            "Please ask about:\n"
            "• PM-KISAN\n"
            "• Ayushman Bharat\n"
            "• PM Awas Yojana\n"
            "• Beti Bachao Beti Padhao\n"
            "• Digital India"
        )

    # Eligibility
    if "eligibility" in message or "eligible" in message:

        return (
            "📋 Eligibility for "
            + selected_scheme["name"]
            + ":\n\n"
            + selected_scheme["eligibility"]
        )

    # Documents
    if "document" in message or "documents" in message:

        return (
            "📄 Documents required for "
            + selected_scheme["name"]
            + ":\n\n"
            + selected_scheme["documents"]
        )

    # Application
    if (
        "apply" in message
        or "application" in message
        or "register" in message
    ):

        return (
            "📝 How to apply for "
            + selected_scheme["name"]
            + ":\n\n"
            + selected_scheme["apply"]
        )

    # General information
    return (
        "🏛️ " + selected_scheme["name"] + "\n\n"
        "ℹ️ Description:\n"
        + selected_scheme["description"]
        + "\n\n"
        "📋 Eligibility:\n"
        + selected_scheme["eligibility"]
        + "\n\n"
        "📄 Documents Required:\n"
        + selected_scheme["documents"]
        + "\n\n"
        "📝 How to Apply:\n"
        + selected_scheme["apply"]
    )


# ============================================================
# WEBSITE HTML + CSS + JAVASCRIPT
# ============================================================

HTML = """

<!DOCTYPE html>

<html>

<head>

    <title>Government Services AI Chatbot</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {

            font-family: Arial, sans-serif;

            background:
            linear-gradient(
                135deg,
                #e8f5e9,
                #ffffff,
                #fff3e0
            );

            min-height: 100vh;
        }

        /* HEADER */

        header {

            background: #0b5d3b;

            color: white;

            text-align: center;

            padding: 25px 15px;

            box-shadow:
            0 3px 10px rgba(0,0,0,0.2);
        }

        header h1 {

            font-size: 30px;

            margin-bottom: 8px;
        }

        header p {

            font-size: 16px;
        }


        /* MAIN CONTAINER */

        .container {

            width: 90%;

            max-width: 900px;

            margin: 35px auto;

            background: white;

            border-radius: 15px;

            overflow: hidden;

            box-shadow:
            0 5px 25px rgba(0,0,0,0.15);
        }


        /* CHAT HEADER */

        .chat-header {

            background: #f5f5f5;

            padding: 15px 20px;

            border-bottom: 1px solid #ddd;
        }

        .chat-header h2 {

            color: #0b5d3b;

            font-size: 20px;
        }


        /* CHAT AREA */

        #chatBox {

            height: 450px;

            padding: 20px;

            overflow-y: auto;

            background: #fafafa;
        }


        /* MESSAGES */

        .message {

            max-width: 80%;

            padding: 14px 17px;

            margin-bottom: 15px;

            border-radius: 12px;

            line-height: 1.5;

            white-space: pre-line;
        }

        .bot {

            background: #e8f5e9;

            margin-right: auto;

            border-left: 4px solid #0b5d3b;
        }

        .user {

            background: #e3f2fd;

            margin-left: auto;

            border-right: 4px solid #1976d2;
        }


        /* QUICK BUTTONS */

        .suggestions {

            padding: 15px;

            border-top: 1px solid #ddd;

            display: flex;

            gap: 10px;

            flex-wrap: wrap;
        }

        .suggestions button {

            border: none;

            padding: 10px 15px;

            border-radius: 20px;

            background: #0b5d3b;

            color: white;

            cursor: pointer;

            font-size: 14px;
        }

        .suggestions button:hover {

            background: #06452c;
        }


        /* INPUT */

        .input-area {

            display: flex;

            padding: 15px;

            gap: 10px;

            border-top: 1px solid #ddd;

            background: white;
        }

        #userInput {

            flex: 1;

            padding: 14px;

            border: 1px solid #bbb;

            border-radius: 8px;

            font-size: 16px;

            outline: none;
        }

        #userInput:focus {

            border-color: #0b5d3b;
        }

        .send-button {

            padding: 14px 25px;

            border: none;

            border-radius: 8px;

            background: #ff9933;

            color: white;

            font-size: 16px;

            cursor: pointer;
        }

        .send-button:hover {

            background: #e67e00;
        }


        /* FOOTER */

        footer {

            text-align: center;

            padding: 20px;

            color: #555;

            font-size: 14px;
        }


        /* MOBILE */

        @media (max-width: 600px) {

            header h1 {

                font-size: 22px;
            }

            .container {

                width: 95%;

                margin: 20px auto;
            }

            #chatBox {

                height: 400px;
            }

            .message {

                max-width: 90%;
            }

            .input-area {

                flex-direction: column;
            }

            .send-button {

                width: 100%;
            }
        }

    </style>

</head>


<body>


<header>

    <h1>🇮🇳 Government Services AI Chatbot</h1>

    <p>
        Your Assistant for Government Schemes and Services
    </p>

</header>


<div class="container">


    <div class="chat-header">

        <h2>🤖 AI Government Assistant</h2>

    </div>


    <div id="chatBox">

        <div class="message bot">

            <b>AI Assistant:</b>

            <br><br>

            Hello! 👋 Welcome to the Government Services
            AI Chatbot.

            <br><br>

            I can provide information about government
            schemes, eligibility, documents and application
            procedures.

            <br><br>

            Try asking:

            <br>
            • What is PM-KISAN?
            <br>
            • PM-KISAN eligibility
            <br>
            • Documents required for Ayushman Bharat
            <br>
            • How to apply for PM Awas Yojana?

        </div>

    </div>


    <div class="suggestions">

        <button onclick="sendSuggestion('What is PM-KISAN?')">
            PM-KISAN
        </button>

        <button onclick="sendSuggestion('Ayushman Bharat eligibility')">
            Ayushman Bharat
        </button>

        <button onclick="sendSuggestion('PM Awas Yojana')">
            PM Awas Yojana
        </button>

        <button onclick="sendSuggestion('Digital India')">
            Digital India
        </button>

    </div>


    <div class="input-area">

        <input
            type="text"
            id="userInput"
            placeholder="Ask about a government scheme..."
        >

        <button
            class="send-button"
            onclick="sendMessage()">

            Send

        </button>

    </div>


</div>


<footer>

    Government Services & Schemes AI Chatbot
    <br>
    Educational Project

</footer>


<script>


function addMessage(text, sender) {

    let chatBox =
        document.getElementById("chatBox");

    let message =
        document.createElement("div");

    message.className =
        "message " + sender;

    let formattedText =
        text.replace(/\\n/g, "<br>");

    if (sender === "user") {

        message.innerHTML =
            "<b>You:</b><br>" +
            formattedText;

    } else {

        message.innerHTML =
            "<b>AI Assistant:</b><br>" +
            formattedText;
    }

    chatBox.appendChild(message);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


function sendMessage() {

    let input =
        document.getElementById("userInput");

    let message =
        input.value.trim();

    if (message === "") {

        return;
    }

    addMessage(message, "user");

    input.value = "";

    fetch("/chat", {

        method: "POST",

        headers: {

            "Content-Type":
            "application/json"
        },

        body: JSON.stringify({

            message: message
        })

    })

    .then(response => response.json())

    .then(data => {

        addMessage(
            data.response,
            "bot"
        );

    })

    .catch(error => {

        addMessage(
            "Sorry! Something went wrong. Please try again.",
            "bot"
        );

    });
}


function sendSuggestion(text) {

    document.getElementById(
        "userInput"
    ).value = text;

    sendMessage();
}


document.getElementById(
    "userInput"
).addEventListener(
    "keypress",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);


</script>


</body>

</html>

"""


# ============================================================
# FLASK ROUTES
# ============================================================

@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "")

    response = chatbot_response(message)

    return jsonify({
        "response": response
    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )