import { useEffect, useState } from "react";
import type { Message } from "./types";
import MessagesWindow from "./components/MessagesWindow";
import InputBar from "./components/InputBar";



function App() {

  const [messages, setMessages] = useState<Message[]>([]);
  const [api,setApi] = useState<"message"|"response">("message");

  const [questions,setQuestions] = useState<any[]>([]);

  const mockMssages = [
  {
    id: crypto.randomUUID(),
    owner: "AI",
    value: "Exemple comenzi:" 
  +" 'genereaza minmax', 'intrebare nash', 'despre n-queens'" 
  +" 'selectie problema' - pentru intrebare cu alegere din lista de 4+ probleme"
  +" 'exit - pentru a iesi",
  },

];
  useEffect(() => {
    setMessages(mockMssages);
  },[]);

  useEffect(() => {
    console.info(messages);
  },[messages]);

  useEffect(() => {
    if(questions.length === 0) setApi("message");
    console.info(questions);
  },[questions])

const addUserMessage = async (message: string) => {

  if(api === "message"){
    try {
      const response = await fetch("http://localhost:3000/api/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      if (!response.ok) {
        console.error("Eroare la server:", response.status);
        return;
      }

      const serverMessage = await response.json();

      // construire mesaj AI
      let aiMessage = "";


      if (serverMessage.questions && serverMessage.questions.length > 0) {

        setQuestions(serverMessage.questions);

        serverMessage.questions.forEach((q: any, index: number) => {
          aiMessage += `📝 Întrebarea ${index + 1}:\n`;

          // Arbore ASCII
          if (q.topic?.tree_ascii) {
            aiMessage += "🌳 Arbore:\n";
            aiMessage += "```\n" + q.topic.tree_ascii + "\n```\n";
          }

          // Întrebarea
          aiMessage += `${q.question}\n\n`;

          // Răspuns
          if (q.answer) {
            aiMessage += `✅ Răspuns: ${q.answer}\n`;
          }

          // Topic și info extra
          if (q.topic) {
            aiMessage += `📚 Topic: ${q.topic.description || ""}\n`;
            if (q.topic.strategies?.length) {
              aiMessage += `Strategii: ${q.topic.strategies.join(", ")}\n`;
            }
            if (q.topic.optimizations?.length) {
              aiMessage += `Optimizări: ${q.topic.optimizations.join(", ")}\n`;
            }
          }

          aiMessage += "\n--------------------------------\n\n";
        });
      } else {
        aiMessage = "Server-ul nu a generat nicio întrebare.";
      }

      // Adaugă mesajele în state
      setMessages([
        ...messages,
        {
          id: crypto.randomUUID(),
          owner: "USER",
          value: message
        },
        {
          id: crypto.randomUUID(),
          owner: "AI",
          value: aiMessage
        }
      ]);

      setApi("response");
    } catch (error) {
      console.error("Eroare la fetch:", error);
    }
  }else {
  try {

    const currentQuestion = questions[0];  // prima întrebare din array
    if (!currentQuestion) return;          // dacă nu există, oprește funcția


        const response = await fetch("http://localhost:3000/api/evaluate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            response: message,
            bundle: {
                question_text: currentQuestion.question,
                correct_answer_text: currentQuestion.answer,
                topic_info: currentQuestion.topic
            }
        })

        });

        if (!response.ok) {
          console.error("Eroare la server:", response.status);
          return;
        }

        const serverMessage = await response.json();

        // # print("\n--- REZULTAT ---")
        //     # print(f"Scor: {result['score']}")
        //     # print(f"Feedback: {result['feedback']}")
        //     # print(f"Răspunsul corect era: {result['correct_answer']}")

        // Adaugă mesajele în state
        setMessages([
          ...messages,
          {
            id: crypto.randomUUID(),
            owner: "USER",
            value: message
          },
          {
            id: crypto.randomUUID(),
            owner: "AI",
            value: `Score: ${serverMessage.score}
          Feedback: ${serverMessage.feedback}
          Răspuns corect: ${serverMessage.correct_answer}
          ${questions.length > 1 ? "Răspunde la următoarea întrebare." : ""}`
          }

        ]);

        setQuestions(prev => prev.slice(1));


      } catch (error) {
        console.error("Eroare la fetch:", error);
      }

  }
};



  return (
    <div className="w-full h-screen flex flex-col justify-between items-center bg-[#e1e1e1]">
      <h1 className="text-xl w-full p-3 bg-white text-center font-bold">
        === AI TEACHING ASSISTANT (GAME THEORY & SEARCH) ===
      </h1>
      <MessagesWindow messages={messages}/>
      <InputBar update={addUserMessage} />
    </div>
  )
}

export default App