# 🛰️ FSEA Database Portal

> A fictional database management system for the Federal Space Exploration Association. Built to explore full stack design, database modeling, and role-based data access architecture.

---

## 🚀 Overview

This project began as a lore-driven build, based on a fictional universe I created. Beneath the aesthetic, it functions as a fully structured data management app, developed to deepen my understanding of:

- PostgreSQL schema design
- API architecture with GraphQL
- Role-based access control
- Backend logic integration with a frontend SPA

The project is currently offline due to hosting constraints, but the architecture and schema remain core to the work.

---

## 🧰 Tech Stack

### 🔹 Frontend
- [Vue 3](https://vuejs.org/) with [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/) (v4)

### 🔸 Backend
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Graphene (GraphQL)](https://docs.graphene-python.org/en/latest/) *(planned migration to [Strawberry](https://strawberry.rocks/))*
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)

### 🗄️ Database
- [PostgreSQL](https://www.postgresql.org/)
- Well-structured schema with logical entity relationships and normalization

---

## ✨ Features

### ✅ Implemented
- 🔐 Auth system with token-based session expiration (4-hour limit)
- 📄 Entity modeling with GraphQL queries
- 🔍 Basic search across key data fields

### 🧪 Planned
- 📊 Admin dashboard with real-time metrics
- 🔒 Fine-grained permission layers
- 📎 PDF export for page/document content
- 📚 File indexing and deep search

---

## 🧠 What I Learned

- Designing normalized, scalable database schemas
- Structuring GraphQL APIs with query efficiency in mind
- Integrating backend logic cleanly into a modular frontend
- Thinking through access patterns and user session lifecycles

This project laid the foundation for deeper backend fluency and architectural thinking that I’ve carried into other full stack work.

---

## 📬 Contact

Want to chat about backend architecture or database design?

- **LinkedIn:** [linkedin.com/in/zariaburton](https://www.linkedin.com/in/zariaburton/)
- **Email:** zaria.burton2000@gmail.com

---

## 🗃️ Repo TODO
- [ ] Migrate GraphQL backend to Strawberry for async and type-safety
- [ ] Add automated tests and CI pipeline
- [ ] Rework access control layer
- [ ] Optional lightweight deployment (Supabase / Railway)
