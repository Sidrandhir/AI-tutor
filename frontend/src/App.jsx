import { useState, useRef, useEffect } from "react";

const API_BASE = "";

// ─── Design Tokens ────────────────────────────────────────────────────────────
const colors = {
  bg: "#0A0C10",
  surface: "#10141C",
  surfaceElevated: "#161B27",
  border: "#1E2736",
  borderAccent: "#2A3A52",
  emerald: "#10B981",
  emeraldDim: "#059669",
  emeraldGlow: "rgba(16,185,129,0.12)",
  emeraldGlowStrong: "rgba(16,185,129,0.25)",
  text: "#E2E8F0",
  textMuted: "#64748B",
  textDim: "#94A3B8",
  amber: "#F59E0B",
  red: "#EF4444",
  blue: "#3B82F6",
  purple: "#8B5CF6",
};

// ─── Helpers ─────────────────────────────────────────────────────────────────
const gradeColor = (g) => ({
  A: colors.emerald,
  B: colors.blue,
  C: colors.amber,
  D: "#F97316",
  F: colors.red,
}[g] || colors.textMuted);

const statusLabel = {
  awaiting_question: "Ready",
  processing_rag: "Retrieving context…",
  tutor_generating: "Tutor thinking…",
  awaiting_student_answer: "Awaiting your answer",
  evaluating: "Evaluating…",
  awaiting_human_review: "Awaiting review",
  completed: "Completed",
};

// ─── Components ───────────────────────────────────────────────────────────────
function Badge({ label, color }) {
  return (
    <span style={{
      background: `${color}22`,
      border: `1px solid ${color}44`,
      color,
      padding: "2px 10px",
      borderRadius: 20,
      fontSize: 11,
      fontWeight: 600,
      letterSpacing: "0.05em",
      textTransform: "uppercase",
      fontFamily: "IBM Plex Mono, monospace",
    }}>{label}</span>
  );
}

function Card({ children, style = {} }) {
  return (
    <div style={{
      background: colors.surface,
      border: `1px solid ${colors.border}`,
      borderRadius: 12,
      padding: "20px 24px",
      ...style,
    }}>{children}</div>
  );
}

function SectionTitle({ step, title, icon }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
      <div style={{
        width: 28, height: 28, borderRadius: "50%",
        background: colors.emeraldGlow,
        border: `1px solid ${colors.emerald}55`,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 12, fontWeight: 700, color: colors.emerald,
        fontFamily: "IBM Plex Mono, monospace",
      }}>{step}</div>
      <span style={{ fontSize: 14, fontWeight: 600, color: colors.text }}>{icon} {title}</span>
    </div>
  );
}

function Textarea({ value, onChange, placeholder, rows = 4, disabled }) {
  return (
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      rows={rows}
      disabled={disabled}
      style={{
        width: "100%",
        background: colors.bg,
        border: `1px solid ${disabled ? colors.border : colors.borderAccent}`,
        borderRadius: 8,
        color: colors.text,
        padding: "12px 14px",
        fontSize: 14,
        lineHeight: 1.6,
        fontFamily: "IBM Plex Mono, monospace",
        resize: "vertical",
        outline: "none",
        boxSizing: "border-box",
        opacity: disabled ? 0.5 : 1,
        transition: "border-color 0.2s",
      }}
    />
  );
}

function Button({ label, onClick, disabled, variant = "primary", loading }) {
  const variants = {
    primary: { bg: colors.emerald, color: "#000", border: colors.emerald },
    secondary: { bg: "transparent", color: colors.emerald, border: colors.emerald },
    danger: { bg: colors.red, color: "#fff", border: colors.red },
    ghost: { bg: colors.surfaceElevated, color: colors.textDim, border: colors.border },
  };
  const v = variants[variant];
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      style={{
        background: v.bg,
        color: v.color,
        border: `1px solid ${v.border}`,
        padding: "10px 20px",
        borderRadius: 8,
        fontSize: 13,
        fontWeight: 600,
        fontFamily: "IBM Plex Mono, monospace",
        cursor: disabled || loading ? "not-allowed" : "pointer",
        opacity: disabled || loading ? 0.5 : 1,
        transition: "all 0.15s",
        letterSpacing: "0.03em",
      }}
    >{loading ? "⏳ Loading…" : label}</button>
  );
}

function SourceChip({ source }) {
  return (
    <div style={{
      background: colors.emeraldGlow,
      border: `1px solid ${colors.emerald}33`,
      borderRadius: 6,
      padding: "4px 10px",
      fontSize: 11,
      color: colors.emeraldDim,
      fontFamily: "IBM Plex Mono, monospace",
    }}>
      📄 {source.title}
      <span style={{ color: colors.textMuted, marginLeft: 6 }}>
        {(source.similarity_score * 100).toFixed(1)}%
      </span>
    </div>
  );
}

function ScoreRing({ score, grade }) {
  const pct = score / 100;
  const r = 36, cx = 44, cy = 44;
  const circumference = 2 * Math.PI * r;
  const dashOffset = circumference * (1 - pct);
  const color = gradeColor(grade);

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
      <svg width={88} height={88} style={{ transform: "rotate(-90deg)" }}>
        <circle cx={cx} cy={cy} r={r} fill="none" stroke={colors.border} strokeWidth={6} />
        <circle
          cx={cx} cy={cy} r={r} fill="none"
          stroke={color} strokeWidth={6}
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
          strokeLinecap="round"
          style={{ transition: "stroke-dashoffset 0.8s ease" }}
        />
      </svg>
      <div style={{ marginTop: -68, textAlign: "center" }}>
        <div style={{ fontSize: 22, fontWeight: 700, color, fontFamily: "IBM Plex Mono, monospace" }}>
          {score}
        </div>
        <div style={{ fontSize: 12, color: colors.textMuted }}>/ 100</div>
      </div>
      <div style={{ marginTop: 32 }}>
        <Badge label={`Grade ${grade}`} color={color} />
      </div>
    </div>
  );
}

function ListSection({ title, items, color = colors.emerald, icon = "✓" }) {
  if (!items || items.length === 0) return null;
  return (
    <div style={{ marginTop: 12 }}>
      <div style={{ fontSize: 12, fontWeight: 600, color: colors.textMuted, marginBottom: 6, letterSpacing: "0.08em", textTransform: "uppercase" }}>{title}</div>
      {items.map((item, i) => (
        <div key={i} style={{ display: "flex", gap: 8, marginBottom: 4, fontSize: 13, color: colors.textDim, lineHeight: 1.5 }}>
          <span style={{ color, flexShrink: 0 }}>{icon}</span>
          <span>{item}</span>
        </div>
      ))}
    </div>
  );
}

function AuditLog({ log }) {
  if (!log || log.length === 0) return null;
  return (
    <div style={{ marginTop: 8 }}>
      {log.map((entry, i) => (
        <div key={i} style={{
          borderLeft: `2px solid ${colors.border}`,
          paddingLeft: 12,
          marginBottom: 8,
          fontSize: 12,
          color: colors.textMuted,
          fontFamily: "IBM Plex Mono, monospace",
        }}>
          <span style={{ color: colors.emeraldDim }}>{entry.event}</span>
          <span style={{ marginLeft: 8, color: colors.border }}>{new Date(entry.timestamp).toLocaleTimeString()}</span>
        </div>
      ))}
    </div>
  );
}

// ─── Suggested Questions ──────────────────────────────────────────────────────
const SUGGESTED = [
  "What is a neural network and how does it work?",
  "Explain the difference between supervised and unsupervised learning",
  "What is Big O notation and why is it important?",
  "How does binary search work?",
  "What is the difference between TCP and UDP?",
];

// ─── Main App ─────────────────────────────────────────────────────────────────
export default function App() {
  const [phase, setPhase] = useState("ask"); // ask | answer | review | done
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [question, setQuestion] = useState("");
  const [askData, setAskData] = useState(null);

  const [studentAnswer, setStudentAnswer] = useState("");
  const [answerData, setAnswerData] = useState(null);

  const [reviewerName, setReviewerName] = useState("Prof. Sharma");
  const [approved, setApproved] = useState(true);
  const [overrideScore, setOverrideScore] = useState("");
  const [overrideFeedback, setOverrideFeedback] = useState("");
  const [finalData, setFinalData] = useState(null);

  const callApi = async (url, body) => {
    setError(null);
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}${url}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "API error");
      return data;
    } catch (e) {
      setError(e.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    const data = await callApi("/ask", { question });
    if (data) { setAskData(data); setPhase("answer"); }
  };

  const handleAnswer = async () => {
    const data = await callApi("/answer", {
      session_id: askData.session_id,
      student_answer: studentAnswer,
    });
    if (data) { setAnswerData(data); setPhase("review"); }
  };

  const handleReview = async () => {
    const body = {
      session_id: askData.session_id,
      reviewer_name: reviewerName,
      approved,
      override_score: !approved && overrideScore ? parseInt(overrideScore) : null,
      override_feedback: !approved && overrideFeedback ? overrideFeedback : null,
    };
    const data = await callApi("/review", body);
    if (data) { setFinalData(data); setPhase("done"); }
  };

  const handleReset = () => {
    setPhase("ask"); setQuestion(""); setAskData(null);
    setStudentAnswer(""); setAnswerData(null);
    setOverrideScore(""); setOverrideFeedback(""); setFinalData(null);
    setApproved(true); setError(null);
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: colors.bg,
      color: colors.text,
      fontFamily: "'IBM Plex Sans', sans-serif",
      padding: "0 0 60px",
    }}>
      <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />

      {/* Header */}
      <div style={{
        borderBottom: `1px solid ${colors.border}`,
        padding: "18px 40px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        background: colors.surface,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 8,
            background: colors.emeraldGlow,
            border: `1px solid ${colors.emerald}55`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 18,
          }}>🎓</div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 16, letterSpacing: "-0.01em" }}>AI Tutor + Evaluator</div>
            <div style={{ fontSize: 11, color: colors.textMuted, fontFamily: "IBM Plex Mono, monospace" }}>RAG · Multi-Agent · Human-in-the-Loop</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          {phase !== "ask" && <Button label="↺ Reset" onClick={handleReset} variant="ghost" />}
          <Badge label={statusLabel[{
            ask: "awaiting_question",
            answer: "awaiting_student_answer",
            review: "awaiting_human_review",
            done: "completed",
          }[phase]] || "awaiting_question"} color={colors.emerald} />
        </div>
      </div>

      {/* Pipeline Steps */}
      <div style={{ padding: "16px 40px 0", display: "flex", gap: 6, alignItems: "center" }}>
        {["Ask Question", "RAG + Tutor", "Student Answer", "Evaluator", "Human Review", "Final Output"].map((s, i) => {
          const phaseIdx = { ask: 0, answer: 2, review: 4, done: 5 }[phase];
          const active = i <= phaseIdx;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <div style={{
                fontSize: 11,
                color: active ? colors.emerald : colors.textMuted,
                fontFamily: "IBM Plex Mono, monospace",
                fontWeight: active ? 600 : 400,
                transition: "color 0.3s",
              }}>{s}</div>
              {i < 5 && <div style={{ width: 16, height: 1, background: active && i < phaseIdx ? colors.emerald : colors.border, transition: "background 0.3s" }} />}
            </div>
          );
        })}
      </div>

      <div style={{ maxWidth: 900, margin: "24px auto 0", padding: "0 40px" }}>
        {error && (
          <div style={{
            background: `${colors.red}11`, border: `1px solid ${colors.red}33`,
            borderRadius: 8, padding: "12px 16px", marginBottom: 16,
            fontSize: 13, color: colors.red, fontFamily: "IBM Plex Mono, monospace",
          }}>⚠️ {error}</div>
        )}

        {/* ── PHASE: ASK ─────────────────────────────────────── */}
        {phase === "ask" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <Card>
              <SectionTitle step="1" title="Ask a Question" icon="❓" />
              <Textarea
                value={question}
                onChange={setQuestion}
                placeholder="What is a neural network and how does it learn?"
                rows={3}
              />
              <div style={{ marginTop: 12, display: "flex", gap: 8, justifyContent: "flex-end" }}>
                <Button label="Ask Tutor →" onClick={handleAsk} disabled={question.length < 5} loading={loading} />
              </div>
            </Card>
            <div>
              <div style={{ fontSize: 12, color: colors.textMuted, marginBottom: 8, fontFamily: "IBM Plex Mono, monospace" }}>💡 Try these questions:</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                {SUGGESTED.map((q, i) => (
                  <button key={i} onClick={() => setQuestion(q)} style={{
                    background: colors.surface, border: `1px solid ${colors.border}`,
                    borderRadius: 20, padding: "6px 14px", fontSize: 12,
                    color: colors.textDim, cursor: "pointer", fontFamily: "IBM Plex Sans, sans-serif",
                    transition: "border-color 0.15s, color 0.15s",
                  }}>{q}</button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ── PHASE: ANSWER ──────────────────────────────────── */}
        {(phase === "answer" || phase === "review" || phase === "done") && askData && (
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <Card style={{ borderColor: colors.borderAccent }}>
              <div style={{ fontSize: 12, color: colors.textMuted, fontFamily: "IBM Plex Mono, monospace", marginBottom: 6 }}>YOUR QUESTION</div>
              <div style={{ fontSize: 15, color: colors.text, fontWeight: 500 }}>{askData.question}</div>
            </Card>

            <Card>
              <SectionTitle step="2" title="AI Tutor Answer (RAG)" icon="🤖" />
              <div style={{ fontSize: 14, color: colors.textDim, lineHeight: 1.7, whiteSpace: "pre-wrap" }}>
                {askData.ai_answer}
              </div>

              {askData.key_concepts?.length > 0 && (
                <div style={{ marginTop: 16, display: "flex", flexWrap: "wrap", gap: 6 }}>
                  <span style={{ fontSize: 12, color: colors.textMuted, marginRight: 4 }}>Key concepts:</span>
                  {askData.key_concepts.map((c, i) => (
                    <Badge key={i} label={c} color={colors.purple} />
                  ))}
                </div>
              )}

              {askData.sources?.length > 0 && (
                <div style={{ marginTop: 14 }}>
                  <div style={{ fontSize: 12, color: colors.textMuted, marginBottom: 6, fontFamily: "IBM Plex Mono, monospace", letterSpacing: "0.08em" }}>RETRIEVED SOURCES</div>
                  <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                    {askData.sources.map((s, i) => <SourceChip key={i} source={s} />)}
                  </div>
                </div>
              )}

              <div style={{ marginTop: 12, display: "flex", gap: 6, alignItems: "center" }}>
                <Badge label={askData.difficulty_level || "intermediate"} color={colors.amber} />
                <span style={{ fontSize: 11, color: colors.textMuted, fontFamily: "IBM Plex Mono, monospace" }}>session: {askData.session_id?.slice(0, 8)}…</span>
              </div>
            </Card>

            <Card>
              <SectionTitle step="3" title="Your Answer" icon="✍️" />
              <Textarea
                value={studentAnswer}
                onChange={setStudentAnswer}
                placeholder="Type your answer here to be evaluated…"
                rows={5}
                disabled={phase !== "answer"}
              />
              {phase === "answer" && (
                <div style={{ marginTop: 12, display: "flex", justifyContent: "flex-end" }}>
                  <Button label="Submit for Evaluation →" onClick={handleAnswer} disabled={studentAnswer.length < 5} loading={loading} />
                </div>
              )}
            </Card>
          </div>
        )}

        {/* ── PHASE: REVIEW ──────────────────────────────────── */}
        {(phase === "review" || phase === "done") && answerData && (
          <div style={{ display: "flex", flexDirection: "column", gap: 16, marginTop: 16 }}>
            <Card>
              <SectionTitle step="4" title="AI Evaluator Results" icon="📊" />
              <div style={{ display: "flex", gap: 24, alignItems: "flex-start" }}>
                <ScoreRing
                  score={answerData.ai_evaluation?.score}
                  grade={answerData.ai_evaluation?.grade}
                />
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 13, color: colors.textDim, lineHeight: 1.7 }}>
                    {answerData.ai_evaluation?.feedback}
                  </div>
                  <ListSection
                    title="✓ Correct"
                    items={answerData.ai_evaluation?.correct_aspects}
                    color={colors.emerald}
                    icon="✓"
                  />
                  <ListSection
                    title="✗ Missing"
                    items={answerData.ai_evaluation?.missing_aspects}
                    color={colors.red}
                    icon="✗"
                  />
                  <ListSection
                    title="💡 Suggestions"
                    items={answerData.ai_evaluation?.improvement_suggestions}
                    color={colors.amber}
                    icon="→"
                  />
                </div>
              </div>
            </Card>

            {phase === "review" && (
              <Card style={{ borderColor: colors.amber + "44" }}>
                <SectionTitle step="5" title="Human Review (HIL)" icon="👤" />
                <div style={{ marginBottom: 12 }}>
                  <label style={{ fontSize: 12, color: colors.textMuted, fontFamily: "IBM Plex Mono, monospace" }}>REVIEWER NAME</label>
                  <input
                    value={reviewerName}
                    onChange={(e) => setReviewerName(e.target.value)}
                    style={{
                      display: "block", width: "100%", marginTop: 4,
                      background: colors.bg, border: `1px solid ${colors.borderAccent}`,
                      borderRadius: 8, padding: "10px 14px",
                      color: colors.text, fontSize: 14,
                      fontFamily: "IBM Plex Mono, monospace",
                      boxSizing: "border-box", outline: "none",
                    }}
                  />
                </div>

                <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
                  <button
                    onClick={() => setApproved(true)}
                    style={{
                      flex: 1, padding: "12px", borderRadius: 8, fontSize: 13, fontWeight: 600,
                      fontFamily: "IBM Plex Mono, monospace", cursor: "pointer",
                      background: approved ? colors.emeraldGlow : "transparent",
                      border: `2px solid ${approved ? colors.emerald : colors.border}`,
                      color: approved ? colors.emerald : colors.textMuted,
                      transition: "all 0.2s",
                    }}
                  >✓ Approve AI Evaluation</button>
                  <button
                    onClick={() => setApproved(false)}
                    style={{
                      flex: 1, padding: "12px", borderRadius: 8, fontSize: 13, fontWeight: 600,
                      fontFamily: "IBM Plex Mono, monospace", cursor: "pointer",
                      background: !approved ? `${colors.amber}22` : "transparent",
                      border: `2px solid ${!approved ? colors.amber : colors.border}`,
                      color: !approved ? colors.amber : colors.textMuted,
                      transition: "all 0.2s",
                    }}
                  >✎ Override Score</button>
                </div>

                {!approved && (
                  <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 16 }}>
                    <div>
                      <label style={{ fontSize: 12, color: colors.textMuted, fontFamily: "IBM Plex Mono, monospace" }}>OVERRIDE SCORE (0–100)</label>
                      <input
                        type="number" min={0} max={100}
                        value={overrideScore}
                        onChange={(e) => setOverrideScore(e.target.value)}
                        placeholder={`AI said: ${answerData.ai_evaluation?.score}`}
                        style={{
                          display: "block", width: "100%", marginTop: 4,
                          background: colors.bg, border: `1px solid ${colors.amber}55`,
                          borderRadius: 8, padding: "10px 14px",
                          color: colors.text, fontSize: 14,
                          fontFamily: "IBM Plex Mono, monospace",
                          boxSizing: "border-box", outline: "none",
                        }}
                      />
                    </div>
                    <div>
                      <label style={{ fontSize: 12, color: colors.textMuted, fontFamily: "IBM Plex Mono, monospace" }}>OVERRIDE FEEDBACK</label>
                      <Textarea
                        value={overrideFeedback}
                        onChange={setOverrideFeedback}
                        placeholder="Enter your custom feedback…"
                        rows={3}
                      />
                    </div>
                  </div>
                )}

                <div style={{ display: "flex", justifyContent: "flex-end" }}>
                  <Button
                    label="Submit Review & Finalize →"
                    onClick={handleReview}
                    disabled={!reviewerName || (!approved && !overrideScore)}
                    loading={loading}
                  />
                </div>
              </Card>
            )}
          </div>
        )}

        {/* ── PHASE: DONE ────────────────────────────────────── */}
        {phase === "done" && finalData && (
          <div style={{ display: "flex", flexDirection: "column", gap: 16, marginTop: 16 }}>
            <Card style={{
              borderColor: colors.emerald + "44",
              background: colors.emeraldGlow,
            }}>
              <SectionTitle step="6" title="Final Output" icon="🎯" />
              <div style={{ display: "flex", gap: 24, alignItems: "flex-start" }}>
                <div>
                  <ScoreRing
                    score={finalData.evaluation?.final_score}
                    grade={finalData.evaluation?.final_grade}
                  />
                  {finalData.evaluation?.human_override && (
                    <div style={{ marginTop: 8, textAlign: "center" }}>
                      <Badge label="Human Override" color={colors.amber} />
                    </div>
                  )}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 13, color: colors.textDim, lineHeight: 1.7, marginBottom: 8 }}>
                    {finalData.evaluation?.final_feedback}
                  </div>
                  <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginTop: 8 }}>
                    <Badge label={`AI: ${finalData.evaluation?.ai_score}`} color={colors.blue} />
                    <Badge label={`Final: ${finalData.evaluation?.final_score}`} color={colors.emerald} />
                    <Badge label={`Reviewer: ${finalData.evaluation?.reviewer}`} color={colors.purple} />
                  </div>
                </div>
              </div>
            </Card>

            <Card>
              <div style={{ fontSize: 12, color: colors.textMuted, fontFamily: "IBM Plex Mono, monospace", marginBottom: 8 }}>📋 AUDIT LOG</div>
              <AuditLog log={finalData.audit_log} />
            </Card>

            <Card>
              <div style={{ fontSize: 12, color: colors.textMuted, fontFamily: "IBM Plex Mono, monospace", marginBottom: 8 }}>📦 FULL JSON OUTPUT</div>
              <pre style={{
                background: colors.bg, border: `1px solid ${colors.border}`,
                borderRadius: 8, padding: "12px 14px",
                fontSize: 11, color: colors.emeraldDim,
                fontFamily: "IBM Plex Mono, monospace",
                overflowX: "auto", lineHeight: 1.6,
              }}>{JSON.stringify(finalData, null, 2)}</pre>
            </Card>

            <div style={{ display: "flex", justifyContent: "center" }}>
              <Button label="↺ Start New Session" onClick={handleReset} variant="secondary" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
