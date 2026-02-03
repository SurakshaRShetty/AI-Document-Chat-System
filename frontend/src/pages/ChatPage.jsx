// import { useState } from "react";
// import api from "../api/axios";
// import Header from "../components/Header";

// export default function ChatPage() {
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [error, setError] = useState("");

//   const ask = async () => {
//     const documentId = localStorage.getItem("document_id");

//     if (!documentId) {
//       setError("Please upload a document first");
//       return;
//     }

//     try {
//       const res = await api.post("/chat/ask", {
//         document_id: Number(documentId),
//         question,
//       });

//       setAnswer(res.data.answer);
//       setError("");
//     } catch {
//       setError("Failed to get answer");
//     }
//   };

//   return (
//     <>
//       <Header />

//       <div style={styles.page}>
//         <div style={styles.card}>
//           <h2>Chat with your Document</h2>

//           <textarea
//             style={styles.input}
//             rows="3"
//             placeholder="Ask a question..."
//             value={question}
//             onChange={(e) => setQuestion(e.target.value)}
//           />

//           <button style={styles.button} onClick={ask}>
//             Ask
//           </button>

//           {error && <p style={styles.error}>{error}</p>}

//           {answer && (
//             <div style={styles.answerBox}>
//               <b>Answer:</b>
//               <p>{answer}</p>
//             </div>
//           )}
//         </div>
//       </div>
//     </>
//   );
// }

// const styles = {
//   page: {
//     background: "#f5f7fb",
//     minHeight: "100vh",
//     display: "flex",
//     justifyContent: "center",
//     alignItems: "center",
//   },
//   card: {
//     background: "#fff",
//     padding: "30px",
//     width: "600px",
//     borderRadius: "8px",
//     boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
//   },
//   input: {
//     width: "100%",
//     padding: "10px",
//     marginBottom: "10px",
//     borderRadius: "4px",
//     border: "1px solid #ccc",
//   },
//   button: {
//     padding: "10px 20px",
//     background: "#2563eb",
//     color: "#fff",
//     border: "none",
//     borderRadius: "4px",
//     cursor: "pointer",
//   },
//   error: {
//     color: "red",
//   },
//   answerBox: {
//     marginTop: "20px",
//     background: "#f1f5f9",
//     padding: "15px",
//     borderRadius: "6px",
//   },
// };
import { useState } from "react";
import api from "../api/axios";
import Header from "../components/Header";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");

  const ask = async () => {
    const documentId = localStorage.getItem("document_id");

    if (!documentId) {
      setError("Please upload a document first");
      return;
    }

    try {
      const res = await api.post("/chat/ask", {
        document_id: Number(documentId),
        question,
      });

      setAnswer(res.data.answer);
      setError("");
    } catch {
      setError("Failed to get answer");
    }
  };

  return (
    <>
      <Header />

      <div style={styles.page}>
        <div style={styles.card}>
          <h2>Chat with your Document</h2>

          <textarea
            style={styles.textarea}
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <button style={styles.button} onClick={ask}>
            Ask
          </button>

          {error && <p style={styles.error}>{error}</p>}

          {answer && (
            <div style={styles.answerBox}>
              <b>Answer:</b>
              <p>{answer}</p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

const styles = {
  page: {
    background: "#f5f7fb",
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    paddingTop: "40px",
  },
  card: {
    background: "#fff",
    width: "700px",
    padding: "30px",
    borderRadius: "10px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
  },
  textarea: {
    width: "100%",
    height: "120px",
    padding: "12px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    marginBottom: "12px",
  },
  button: {
    background: "#2563eb",
    color: "#fff",
    border: "none",
    padding: "10px 18px",
    borderRadius: "6px",
    cursor: "pointer",
  },
  error: {
    color: "red",
    marginTop: "10px",
  },
  answerBox: {
    background: "#f1f5f9",
    padding: "15px",
    borderRadius: "6px",
    marginTop: "20px",
  },
};
