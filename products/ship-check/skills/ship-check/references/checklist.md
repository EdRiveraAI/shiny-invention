# Ship Check manual review checklist

Work through the sections that apply to the detected stack. Each item is a question; a "no"
or "unsure" is a candidate finding. Suggested severity is in brackets.

## 1. Authentication and authorization

- Is every route that reads or writes user data behind authentication? [critical]
- Does each handler check that the current user owns or may access the specific record
  (no IDOR: `/invoices/:id` returning anyone's invoice)? [critical]
- Are admin routes protected by a role check on the server, not just hidden in the UI? [critical]
- Are passwords hashed with bcrypt, scrypt, or argon2 (never MD5/SHA1/plain)? [critical]
- Do sessions/JWTs expire, and are JWT signatures verified with a fixed algorithm? [high]
- Are cookies `HttpOnly`, `Secure`, and `SameSite` set? [medium]
- Is there rate limiting on login, signup, password reset, and OTP endpoints? [high]
- Do password reset tokens expire and become single-use? [high]

## 2. Input handling

- Are all SQL queries parameterized or built with an ORM (no string concatenation)? [critical]
- Is user input ever passed to a shell, `eval`, template rendering, or a deserializer? [critical]
- Is HTML output escaped by default; any `dangerouslySetInnerHTML`, `v-html`, `|safe`,
  `html_safe`, or `innerHTML` with user data? [high]
- Are request bodies validated with a schema (zod, pydantic, Joi, etc.)? [medium]
- File uploads: size limits, type checks, stored outside the web root or in object
  storage, random names? [high]
- Does the server fetch user-supplied URLs (SSRF) without an allowlist? [high]
- Are state-changing requests protected against CSRF where cookies are used? [high]

## 3. Secrets and configuration

- Are all secrets loaded from environment variables or a secret manager? [critical]
- Are debug modes, verbose errors, and dev tooling off in production config? [high]
- Is there a documented list of required environment variables (`.env.example`)? [medium]
- Does the app fail fast at startup when a required variable is missing? [medium]
- Are CORS origins restricted to known domains? [medium]
- Are security headers set (HSTS, CSP or at least `X-Content-Type-Options`, `frame-ancestors`)? [medium]

## 4. Data safety

- Are database migrations versioned and reversible, and run as part of deploy? [high]
- Are automated backups configured, and has a restore ever been tested? [high]
- Do destructive operations (delete account, bulk delete) require confirmation and get logged? [medium]
- Is personal data minimized, and is there a way to export/delete a user's data (GDPR/CCPA)? [medium]
- Are payment and webhook handlers idempotent and signature-verified? [critical]

## 5. Error handling, logging, observability

- Is there a global error handler that returns generic messages (no stack traces to users)? [high]
- Is an error tracker configured (Sentry, Rollbar, Bugsnag, etc.)? [medium]
- Are logs structured and free of passwords, tokens, and full card numbers? [high]
- Is there a health-check endpoint for the load balancer/orchestrator? [medium]
- Is uptime monitoring and alerting set up for the production URL? [medium]

## 6. Performance and reliability

- Do all outbound HTTP/database calls have timeouts? [high]
- Are retries bounded and backed off? [medium]
- Any N+1 query patterns in list endpoints? [medium]
- Are list endpoints paginated with a maximum page size? [medium]
- Is long-running work moved to a background job/queue? [medium]
- Are static assets cached/CDN-served and bundles minified? [low]
- Are database indexes present for columns used in frequent `WHERE`/`JOIN`? [medium]

## 7. Deployment and operations

- Is deployment automated and repeatable (CI/CD, IaC, or a documented script)? [medium]
- Can you roll back a bad release quickly? [medium]
- Is HTTPS enforced everywhere? [high]
- Are dependencies free of known critical vulnerabilities (`npm audit`, `pip-audit`,
  `govulncheck`, `bundle audit`)? Run the one for the stack if available. [high]
- Does the README explain setup, environment variables, tests, and deploy? [low]
- Are there tests covering auth, payments, and the main user flow? [high]

## Stack-specific spot checks

- **Node.js/Express:** `helmet` used? `express.json({ limit })` set? `trust proxy` correct behind a proxy?
- **Next.js:** server actions/API routes check auth? No secrets in `NEXT_PUBLIC_*` variables?
- **Django:** `DEBUG=False`, `ALLOWED_HOSTS` set, `SECURE_*` settings on, `SECRET_KEY` from env?
- **Flask/FastAPI:** debug off, CORS restricted, dependency-injected auth on every router?
- **Rails:** `force_ssl`, strong parameters, `protect_from_forgery`?
- **Go:** `http.Server` with Read/Write timeouts (not bare `http.ListenAndServe`)?
- **Docker:** non-root user, pinned base image, no secrets in `ENV` or build args, `.dockerignore` present?
- **Terraform:** no public S3 buckets / open `0.0.0.0/0` security groups on databases, state stored remotely and encrypted?
- **Mobile/frontend-only:** no secret API keys shipped in the client bundle?
