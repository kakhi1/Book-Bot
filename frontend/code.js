const reloadButton = document.getElementById("reload-button");
reloadButton.addEventListener("click", function () {
  // Start the .iconName animation
  const iconName = document.querySelector(".iconName");
  this.classList.toggle("spin");
  // Clear the chatMessages div to remove all chat history
  chatMessages.innerHTML = "";
  reloadPage();
});

const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
displayMessage(
  "Chatbot",
  "Hello, I am the Book Bot. I can provide you with information about an author's books, including their price, description, and even share the direct link for you to purchase them."
);
userInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    sendMessage(userInput.value);
    userInput.value = "";
  }
});
window.addEventListener("DOMContentLoaded", () => {
  localStorage.removeItem("sender");
});

function reloadPage() {
  localStorage.removeItem("sender");
  location.reload();
}
function getRandomNumber() {
  return Math.floor(Math.random() * 10000) + 1;
}

function getSender() {
  let sender = localStorage.getItem("sender");
  if (!sender && !localStorage.getItem("reloadClicked")) {
    sender = "test" + getRandomNumber();
    localStorage.setItem("sender", sender);
  }
  return sender;
}

function scrollChatToBottom() {
  var chatContainer = document.getElementById("chat-messages");
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage(message) {
  const sender = getSender();
  displayMessage("User", message);

  try {
    const response = await fetch(
      "https://bookbot-6an3ogkgka-uc.a.run.app/webhooks/rest/webhook",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sender: sender,
          message: message,
        }),
      }
    );

    const data = await response.json();
    console.log(data);
    const botResponse = data.map((message) => {
      if (message.text !== undefined) {
        return message.text;
      } else if (message.image !== undefined) {
        return message.image;
      }
    });
    displayMessage("Chatbot", botResponse);
  } catch (error) {
    console.error("Error:", error);
  }
}

function displayMessage(sender, message) {
  const messageElement = document.createElement("div");
  const iconElement = document.createElement("img");
  iconElement.classList.add("icon");
  const textElement = document.createElement("div");
  textElement.classList.add("message-text");

  if (sender === "Chatbot") {
    iconElement.src = "assets/botIcon.png";
    if (isValidHttpUrl(message)) {
      displayMessage("Chatbot", "This is your book");
      const linkElement = document.createElement("a");
      linkElement.href = message;
      linkElement.innerHTML = message;
      // Open the link in a new tab when clicked
      linkElement.addEventListener("click", (event) => {
        event.preventDefault();
        window.open(message, "_blank");
      });
      textElement.appendChild(linkElement);
    } else {
      textElement.innerHTML = message;
    }
    messageElement.appendChild(iconElement);
    messageElement.appendChild(textElement);
  } else if (sender === "User") {
    textElement.innerHTML = message;
    if (isValidHttpUrl(message)) {
      const linkElement = document.createElement("a");
      linkElement.href = message;
      linkElement.innerHTML = message;
      // Open the link in a new tab when clicked
      linkElement.addEventListener("click", (event) => {
        event.preventDefault();
        window.open(message, "_blank");
      });
      textElement.appendChild(linkElement);
    } else {
      textElement.innerHTML = message;
    }
    messageElement.appendChild(textElement);
    iconElement.src = "assets/userIcon.png";
    messageElement.appendChild(iconElement);
  }

  messageElement.classList.add("message");
  chatMessages.appendChild(messageElement);
  scrollChatToBottom();
}

function isValidHttpUrl(string) {
  try {
    const newUrl = new URL(string);
    return newUrl.protocol === "http:" || newUrl.protocol === "https:";
  } catch (err) {
    return false;
  }
}
