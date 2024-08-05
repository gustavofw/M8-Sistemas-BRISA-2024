const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
const chatbotToggler = document.querySelector(".chatbot-toggler");
const chatbotCloseBtn = document.querySelector(".close-btn");

let userMessage;
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === 'outgoing' ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").innerHTML = message;  
    return chatLi;
}

const generateResponse = () => {
    const message = { texto: userMessage };  // Chave 'texto' para coincidir com o backend
    fetch('http://localhost:5000/process_user_input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(message),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro HTTP! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        let botResponse = '';

        if (data.artigos && data.artigos.length > 0) {
            botResponse += data.mensagem ? data.mensagem + '<br><br>' : '';
            botResponse += data.artigos.map(artigo =>
                `<div>&#8226; <a href='${artigo.link}' target='_blank'>${artigo.nome}</a></div>`
            ).join(' ');
        } else if (data.mensagem) {
            botResponse = data.mensagem;
            if (data.setores) {
                botResponse += '<ul class="setores-lista">';
                botResponse += data.setores.map(setor => 
                    `<li>${setor}</li>`
                ).join(' ');
                botResponse += '</ul>';
            }
        } else {
            botResponse = "Não consegui identificar sua necessidade. Você poderia especificar mais?";
        }

        const responseElement = createChatLi(botResponse, "incoming");
        chatbox.appendChild(responseElement);
        chatbox.scrollTo(0, chatbox.scrollHeight);
    })
    .catch(error => console.error('Erro ao enviar mensagem:', error))
    .finally(() => {
        chatbox.scrollTo(0, chatbox.scrollHeight);
    });
}

const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        chatbox.appendChild(createChatLi("Pensando...", "incoming"));
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse();
    }, 600);
}

chatInput.addEventListener("input", () => {
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", handleChat);

document.body.classList.remove("show-chatbot");


chatbotCloseBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
