import { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const roles = [
    {
      role: "ADMIN",
      label: "Administrator",
      description: "Full platform management access",
      username: "admin",
      password: "admin123",
      icon: "🛡️",
    },
    {
      role: "RESEARCHER",
      label: "Researcher",
      description: "Research, datasets & evidence",
      username: "researcher",
      password: "research123",
      icon: "🔬",
    },
    {
      role: "POLICY_MAKER",
      label: "Policy Maker",
      description: "Policies, simulation & insights",
      username: "policymaker",
      password: "policy123",
      icon: "🏛️",
    },
  ];

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    if (!username.trim() || !password.trim()) {
      setError("Please enter both username and password.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username.trim(),
          password,
        }),
      });

      let data = null;

      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        throw new Error(
          data?.detail || "Invalid username or password."
        );
      }

      if (!data?.access_token || !data?.user) {
        throw new Error(
          "Authentication server returned an incomplete response."
        );
      }

      onLogin(data.user, data.access_token);
    } catch (err) {
      setError(
        err?.message ||
          "Unable to connect to the authentication server."
      );
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = (user, pass) => {
    setUsername(user);
    setPassword(pass);
    setError("");
  };

  return (
    <>
      <style>{`
        @keyframes landLoginFadeUp {
          from { opacity: 0; transform: translateY(18px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes landLoginSpin {
          to { transform: rotate(360deg); }
        }

        .land-login-root {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          overflow: hidden;
          padding: 28px;
          box-sizing: border-box;
          font-family: Inter, ui-sans-serif, system-ui, sans-serif;
          background:
            radial-gradient(circle at 12% 15%, rgba(37,99,235,.22), transparent 30%),
            radial-gradient(circle at 88% 82%, rgba(14,165,233,.18), transparent 32%),
            linear-gradient(135deg, #07111f 0%, #0f172a 45%, #102a43 100%);
        }

        .land-login-grid {
          position: absolute;
          inset: 0;
          opacity: .16;
          background-image:
            linear-gradient(rgba(148,163,184,.12) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,.12) 1px, transparent 1px);
          background-size: 44px 44px;
          pointer-events: none;
        }

        .land-login-shell {
          width: min(1080px, 100%);
          display: grid;
          grid-template-columns: 1.08fr .92fr;
          background: rgba(255,255,255,.98);
          border: 1px solid rgba(255,255,255,.3);
          border-radius: 26px;
          overflow: hidden;
          box-shadow: 0 30px 90px rgba(0,0,0,.38);
          animation: landLoginFadeUp .55s ease-out;
          position: relative;
          z-index: 1;
        }

        .land-login-brand {
          padding: 52px 48px;
          color: white;
          background:
            radial-gradient(circle at 80% 18%, rgba(56,189,248,.24), transparent 28%),
            linear-gradient(145deg, #0b1f38, #123c63 55%, #0b2945);
        }

        .land-login-logo {
          width: 62px;
          height: 62px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 17px;
          background: linear-gradient(135deg, #2563eb, #06b6d4);
          box-shadow: 0 12px 30px rgba(37,99,235,.35);
          font-size: 30px;
          margin-bottom: 26px;
        }

        .land-login-kicker {
          display: inline-flex;
          align-items: center;
          gap: 7px;
          padding: 7px 10px;
          border: 1px solid rgba(186,230,253,.2);
          background: rgba(255,255,255,.07);
          border-radius: 999px;
          color: #bae6fd;
          font-size: 10px;
          font-weight: 800;
          letter-spacing: .08em;
          text-transform: uppercase;
          margin-bottom: 18px;
        }

        .land-login-brand h1 {
          margin: 0;
          max-width: 520px;
          font-size: clamp(30px, 4vw, 46px);
          line-height: 1.05;
          letter-spacing: -.035em;
        }

        .land-login-brand p {
          max-width: 510px;
          margin: 18px 0 0;
          color: #cbd5e1;
          line-height: 1.7;
          font-size: 14px;
        }

        .land-login-flow {
          margin-top: 36px;
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 8px;
        }

        .land-login-flow-item {
          padding: 12px 10px;
          border: 1px solid rgba(148,163,184,.18);
          background: rgba(255,255,255,.055);
          border-radius: 12px;
        }

        .land-login-flow-item strong {
          display: block;
          font-size: 11px;
          color: #f8fafc;
        }

        .land-login-flow-item span {
          display: block;
          margin-top: 4px;
          color: #94a3b8;
          font-size: 9px;
        }

        .land-login-form-panel {
          padding: 46px 44px;
          background: #fff;
        }

        .land-login-form-header h2 {
          margin: 0;
          color: #0f172a;
          font-size: 27px;
        }

        .land-login-form-header p {
          margin: 8px 0 0;
          color: #64748b;
          font-size: 13px;
        }

        .land-login-form {
          margin-top: 28px;
        }

        .land-login-field {
          margin-bottom: 17px;
        }

        .land-login-label {
          display: block;
          margin-bottom: 7px;
          color: #334155;
          font-size: 12px;
          font-weight: 800;
        }

        .land-login-input-wrap {
          position: relative;
        }

        .land-login-input {
          width: 100%;
          box-sizing: border-box;
          padding: 13px 14px;
          border: 1px solid #cbd5e1;
          border-radius: 10px;
          outline: none;
          color: #0f172a;
          background: #fff;
          font-size: 14px;
          transition: border-color .18s, box-shadow .18s;
        }

        .land-login-input:focus {
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59,130,246,.12);
        }

        .land-login-password-input {
          padding-right: 76px;
        }

        .land-login-show-btn {
          position: absolute;
          right: 8px;
          top: 50%;
          transform: translateY(-50%);
          border: 0;
          background: transparent;
          color: #64748b;
          font-size: 11px;
          font-weight: 800;
          cursor: pointer;
          padding: 7px;
        }

        .land-login-error {
          margin: 14px 0;
          padding: 11px 12px;
          border: 1px solid #fecaca;
          border-radius: 10px;
          background: #fef2f2;
          color: #b91c1c;
          font-size: 12px;
          line-height: 1.45;
        }

        .land-login-submit {
          width: 100%;
          border: 0;
          border-radius: 11px;
          padding: 13px 16px;
          background: linear-gradient(135deg, #2563eb, #0891b2);
          color: white;
          font-size: 14px;
          font-weight: 800;
          cursor: pointer;
          box-shadow: 0 10px 24px rgba(37,99,235,.2);
          transition: transform .18s, box-shadow .18s, opacity .18s;
        }

        .land-login-submit:hover:not(:disabled) {
          transform: translateY(-1px);
          box-shadow: 0 14px 30px rgba(37,99,235,.26);
        }

        .land-login-submit:disabled {
          cursor: not-allowed;
          opacity: .65;
        }

        .land-login-divider {
          display: flex;
          align-items: center;
          gap: 10px;
          margin: 24px 0 16px;
          color: #94a3b8;
          font-size: 10px;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: .08em;
        }

        .land-login-divider::before,
        .land-login-divider::after {
          content: "";
          height: 1px;
          flex: 1;
          background: #e2e8f0;
        }

        .land-login-role-grid {
          display: grid;
          gap: 8px;
        }

        .land-login-role {
          width: 100%;
          display: flex;
          align-items: center;
          gap: 10px;
          text-align: left;
          border: 1px solid #e2e8f0;
          background: #f8fafc;
          border-radius: 10px;
          padding: 9px 10px;
          cursor: pointer;
          transition: border-color .18s, background .18s, transform .18s;
        }

        .land-login-role:hover {
          border-color: #93c5fd;
          background: #eff6ff;
          transform: translateY(-1px);
        }

        .land-login-role-icon {
          width: 31px;
          height: 31px;
          flex: 0 0 31px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 8px;
          background: white;
          border: 1px solid #e2e8f0;
        }

        .land-login-role-main {
          min-width: 0;
          flex: 1;
        }

        .land-login-role-main strong {
          display: block;
          color: #1e293b;
          font-size: 11px;
        }

        .land-login-role-main span {
          display: block;
          margin-top: 2px;
          color: #64748b;
          font-size: 9px;
        }

        .land-login-role-arrow {
          color: #94a3b8;
          font-size: 14px;
        }

        .land-login-footer {
          margin-top: 24px;
          color: #94a3b8;
          text-align: center;
          font-size: 10px;
          line-height: 1.5;
        }

        @media (max-width: 860px) {
          .land-login-shell {
            grid-template-columns: 1fr;
            max-width: 540px;
          }

          .land-login-brand {
            padding: 34px;
          }

          .land-login-brand h1 {
            font-size: 32px;
          }
        }

        @media (max-width: 520px) {
          .land-login-root {
            padding: 14px;
          }

          .land-login-brand,
          .land-login-form-panel {
            padding: 28px 22px;
          }

          .land-login-flow {
            grid-template-columns: repeat(2, 1fr);
          }
        }
      `}</style>

      <div className="land-login-root">
        <div className="land-login-grid" />

        <div className="land-login-shell">
          <section className="land-login-brand">
            <div className="land-login-logo">🌐</div>

            <div className="land-login-kicker">
              <span>●</span>
              Secure Decision Platform
            </div>

            <h1>
              LAND
              <br />
               SIGHT
            </h1>

            <p>
              A unified intelligence platform connecting
              land data, GIS, research evidence, AI analysis,
              policy simulation and traceable decision support.
            </p>

            <div className="land-login-flow">
              <div className="land-login-flow-item">
                <strong>DATA</strong>
                <span>Land & GIS</span>
              </div>
              <div className="land-login-flow-item">
                <strong>EVIDENCE</strong>
                <span>Research + RAG</span>
              </div>
              <div className="land-login-flow-item">
                <strong>INSIGHT</strong>
                <span>AI Analytics</span>
              </div>
              <div className="land-login-flow-item">
                <strong>POLICY</strong>
                <span>Simulation</span>
              </div>
            </div>
          </section>

          <section className="land-login-form-panel">
            <div className="land-login-form-header">
              <h2>Welcome back</h2>
              <p>
                Sign in to access your authorized workspace.
              </p>
            </div>

            <form className="land-login-form" onSubmit={handleLogin}>
              <div className="land-login-field">
                <label
                  className="land-login-label"
                  htmlFor="land-username"
                >
                  USERNAME
                </label>

                <input
                  id="land-username"
                  className="land-login-input"
                  type="text"
                  value={username}
                  onChange={(e) => {
                    setUsername(e.target.value);
                    setError("");
                  }}
                  placeholder="Enter your username"
                  autoComplete="username"
                  autoFocus
                />
              </div>

              <div className="land-login-field">
                <label
                  className="land-login-label"
                  htmlFor="land-password"
                >
                  PASSWORD
                </label>

                <div className="land-login-input-wrap">
                  <input
                    id="land-password"
                    className="land-login-input land-login-password-input"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => {
                      setPassword(e.target.value);
                      setError("");
                    }}
                    placeholder="Enter your password"
                    autoComplete="current-password"
                  />

                  <button
                    type="button"
                    className="land-login-show-btn"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? "HIDE" : "SHOW"}
                  </button>
                </div>
              </div>

              {error && (
                <div className="land-login-error">
                  <strong>Authentication failed</strong>
                  <br />
                  {error}
                </div>
              )}

              <button
                type="submit"
                className="land-login-submit"
                disabled={loading}
              >
                {loading ? (
                  <span
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "8px",
                    }}
                  >
                    <span
                      style={{
                        width: "13px",
                        height: "13px",
                        borderRadius: "50%",
                        border:
                          "2px solid rgba(255,255,255,.4)",
                        borderTopColor: "#ffffff",
                        animation:
                          "landLoginSpin .7s linear infinite",
                      }}
                    />
                    Authenticating...
                  </span>
                ) : (
                  "Sign in securely →"
                )}
              </button>
            </form>

            <div className="land-login-divider">
              Demo access
            </div>

            <div className="land-login-role-grid">
              {roles.map((item) => (
                <button
                  type="button"
                  key={item.role}
                  className="land-login-role"
                  onClick={() =>
                    fillDemo(
                      item.username,
                      item.password
                    )
                  }
                  title={`Use ${item.label} demo account`}
                >
                  <span className="land-login-role-icon">
                    {item.icon}
                  </span>

                  <span className="land-login-role-main">
                    <strong>{item.label}</strong>
                    <span>{item.description}</span>
                  </span>

                  <span className="land-login-role-arrow">
                    →
                  </span>
                </button>
              ))}
            </div>

            <div className="land-login-footer">
              🔐 Role-based access control enabled
              <br />
              Authentication is verified by the FastAPI backend.
            </div>
          </section>
        </div>
      </div>
    </>
  );
}

export default Login;
