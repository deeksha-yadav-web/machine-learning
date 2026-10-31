// import { useState } from "react";
// import "./App.css";

// const initialForm = {
//   no_of_dependents: 0,
//   education: "Graduate",
//   self_employed: "No",
//   income_annum: 500000,
//   loan_amount: 1000000,
//   loan_term: 10,
//   cibil_score: 700,
//   residential_assets_value: 1000000,
//   commercial_assets_value: 500000,
//   luxury_assets_value: 200000,
//   bank_asset_value: 300000,
// };

// const numericFields = [
//   ["no_of_dependents", "Number of Dependents", 0],
//   ["income_annum", "Annual Income", 0],
//   ["loan_amount", "Loan Amount", 1],
//   ["loan_term", "Loan Term (years)", 1],
//   ["cibil_score", "Credit Score", 0],
//   ["residential_assets_value", "Residential Assets Value", 0],
//   ["commercial_assets_value", "Commercial Assets Value", 0],
//   ["luxury_assets_value", "Luxury Assets Value", 0],
//   ["bank_asset_value", "Bank Asset Value", 0],
// ];

// function App() {
//   const [form, setForm] = useState(initialForm);
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");

//   function handleChange(event) {
//     const { name, value } = event.target;

//     setForm((previous) => ({
//       ...previous,
//       [name]: value,
//     }));
//   }

//   async function handleSubmit(event) {
//     event.preventDefault();
//     setResult(null);
//     setError("");

//     // Empty values check karo
//     for (const [key, label] of numericFields) {
//       if (form[key] === "" || form[key] === null) {
//         setError(`${label} is required.`);
//         return;
//       }
//     }

//     // HTML form values strings hoti hain; numeric fields ko numbers banao
//     const payload = { ...form };

//     for (const [key] of numericFields) {
//       payload[key] = Number(form[key]);
//     }

//     // Basic validation
//     if (payload.income_annum < 0 || payload.loan_amount <= 0) {
//       setError("Income cannot be negative and loan amount must be positive.");
//       return;
//     }

//     if (payload.cibil_score < 0 || payload.cibil_score > 900) {
//       setError("Please enter a credit score between 0 and 900.");
//       return;
//     }

//     setLoading(true);

//     try {
//       const response = await fetch("http://127.0.0.1:8000/predict", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify(payload),
//       });

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(
//           typeof data.detail === "string"
//             ? data.detail
//             : JSON.stringify(data.detail)
//         );
//       }

//       setResult(data);
//     } catch (err) {
//       setError(
//         err.message ||
//           "Backend se connection nahi hua. Check karo ki FastAPI server running hai."
//       );
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <main className="page">
//       <section className="app-card">
//         <header className="header">
//           <p className="eyebrow">MACHINE LEARNING PROJECT</p>
//           <h1>Loan Approval Predictor</h1>
//           <p className="subtitle">
//             Enter applicant details to view a model prediction.
//           </p>
//         </header>

//         <form onSubmit={handleSubmit}>
//           <div className="form-grid">
//             {numericFields.map(([name, label, min]) => (
//               <label className="field" key={name}>
//                 <span>{label}</span>
//                 <input
//                   type="number"
//                   name={name}
//                   value={form[name]}
//                   min={min}
//                   step="any"
//                   onChange={handleChange}
//                   required
//                 />
//               </label>
//             ))}

//             <label className="field">
//               <span>Education</span>
//               <select
//                 name="education"
//                 value={form.education}
//                 onChange={handleChange}
//               >
//                 <option value="Graduate">Graduate</option>
//                 <option value="Not Graduate">Not Graduate</option>
//               </select>
//             </label>

//             <label className="field">
//               <span>Self Employed</span>
//               <select
//                 name="self_employed"
//                 value={form.self_employed}
//                 onChange={handleChange}
//               >
//                 <option value="No">No</option>
//                 <option value="Yes">Yes</option>
//               </select>
//             </label>
//           </div>

//           <button type="submit" disabled={loading}>
//             {loading ? "Checking..." : "Check Loan Approval"}
//           </button>
//         </form>

//         {error && (
//           <div className="message error" role="alert">
//             {error}
//           </div>
//         )}

//         {result && (
//           <section className="result" aria-live="polite">
//             <h2>
//               Prediction:{" "}
//               <span
//                 className={
//                   result.prediction === "Approved" ? "approved" : "rejected"
//                 }
//               >
//                 {result.prediction}
//               </span>
//             </h2>

//             {result.estimated_probability_percent !== null && (
//               <p>
//                 Estimated model probability:{" "}
//                 <strong>{result.estimated_probability_percent}%</strong>
//               </p>
//             )}

//             <p className="model-name">
//               Model used: {result.model_name}
//             </p>

//             <h3>Input observations</h3>
//             <ul>
//               {result.explanations.map((item, index) => (
//                 <li key={index}>{item}</li>
//               ))}
//             </ul>

//             <p className="disclaimer">{result.disclaimer}</p>
//           </section>
//         )}

//         <footer>
//           Student project only. This prediction is not a real bank decision.
//         </footer>
//       </section>
//     </main>
//   );
// }

// export default App;







































import { useState } from "react";
import "./App.css";

const initialForm = {
  no_of_dependents: 0,
  education: "Graduate",
  self_employed: "No",
  income_annum: 500000,
  loan_amount: 1000000,
  loan_term: 10,
  cibil_score: 700,
  residential_assets_value: 1000000,
  commercial_assets_value: 500000,
  luxury_assets_value: 200000,
  bank_asset_value: 300000,
};

const numericFields = [
  ["no_of_dependents", "Number of Dependents", 0],
  ["income_annum", "Annual Income", 0],
  ["loan_amount", "Loan Amount", 1],
  ["loan_term", "Loan Term (years)", 1],
  ["cibil_score", "Credit Score", 0],
  ["residential_assets_value", "Residential Assets Value", 0],
  ["commercial_assets_value", "Commercial Assets Value", 0],
  ["luxury_assets_value", "Luxury Assets Value", 0],
  ["bank_asset_value", "Bank Asset Value", 0],
];

function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setResult(null);
    setError("");

    // Check required numeric fields
    for (const [key, label] of numericFields) {
      if (form[key] === "" || form[key] === null) {
        setError(`${label} is required.`);
        return;
      }
    }

    // Convert numeric form values into numbers
    const payload = { ...form };

    for (const [key] of numericFields) {
      payload[key] = Number(form[key]);
    }

    // Validate input values
    if (payload.no_of_dependents < 0 || payload.no_of_dependents > 20) {
      setError("Number of dependents must be between 0 and 20.");
      return;
    }

    if (payload.income_annum < 0) {
      setError("Annual income cannot be negative.");
      return;
    }

    if (payload.loan_amount <= 0) {
      setError("Loan amount must be greater than zero.");
      return;
    }

    if (payload.loan_term <= 0 || payload.loan_term > 50) {
      setError("Loan term must be between 1 and 50 years.");
      return;
    }

    if (payload.cibil_score < 0 || payload.cibil_score > 1000) {
      setError("Credit score must be between 0 and 1000.");
      return;
    }

    const assetFields = [
      "residential_assets_value",
      "commercial_assets_value",
      "luxury_assets_value",
      "bank_asset_value",
    ];

    for (const key of assetFields) {
      if (payload[key] < 0) {
        setError("Asset values cannot be negative.");
        return;
      }
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        const errorMessage =
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail || data);

        throw new Error(errorMessage);
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Backend connection failed. Please check whether FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  }

  const loanStatus = String(result?.loan_status || "").toLowerCase();

  return (
    <main className="page">
      <section className="app-card">
        <header className="header">
          <p className="eyebrow">MACHINE LEARNING PROJECT</p>

          <h1>Loan Approval Predictor</h1>

          <p className="subtitle">
            Enter applicant details to view a machine learning prediction.
          </p>
        </header>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            {numericFields.map(([name, label, min]) => (
              <label className="field" key={name}>
                <span>{label}</span>

                <input
                  type="number"
                  name={name}
                  value={form[name]}
                  min={min}
                  step="any"
                  onChange={handleChange}
                  required
                />
              </label>
            ))}

            <label className="field">
              <span>Education</span>

              <select
                name="education"
                value={form.education}
                onChange={handleChange}
                required
              >
                <option value="Graduate">Graduate</option>
                <option value="Not Graduate">Not Graduate</option>
              </select>
            </label>

            <label className="field">
              <span>Self Employed</span>

              <select
                name="self_employed"
                value={form.self_employed}
                onChange={handleChange}
                required
              >
                <option value="No">No</option>
                <option value="Yes">Yes</option>
              </select>
            </label>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Checking..." : "Check Loan Approval"}
          </button>
        </form>

        {error && (
          <div className="message error" role="alert">
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && (
          <section className="result" aria-live="polite">
            <h2>
              Prediction:{" "}
              <span
                className={
                  loanStatus === "approved" ? "approved" : "rejected"
                }
              >
                {result.loan_status || "Unknown"}
              </span>
            </h2>

            {result.approval_probability != null && (
              <p>
                Estimated approval probability:{" "}
                <strong>{result.approval_probability}%</strong>
              </p>
            )}

            <p className="model-name">
              Model used: {result.model_used || "Machine Learning Model"}
            </p>

            <h3>Applicant Details</h3>

            <ul>
              <li>
                Number of dependents: {form.no_of_dependents}
              </li>

              <li>
                Education: {form.education}
              </li>

              <li>
                Self employed: {form.self_employed}
              </li>

              <li>
                Annual income: ₹
                {Number(form.income_annum).toLocaleString("en-IN")}
              </li>

              <li>
                Loan amount: ₹
                {Number(form.loan_amount).toLocaleString("en-IN")}
              </li>

              <li>
                Credit score: {form.cibil_score}
              </li>

              <li>
                Loan term: {form.loan_term} years
              </li>
            </ul>

            <p className="disclaimer">
              {result.note ||
                "This is a machine learning prediction, not an official bank decision."}
            </p>
          </section>
        )}

        <footer>
          Student project only. This prediction is not a real bank decision.
        </footer>
      </section>
    </main>
  );
}

export default App;