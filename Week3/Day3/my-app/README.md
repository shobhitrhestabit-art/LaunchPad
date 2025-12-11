# Day 3 — Routing, Layouts & Client Components

## Objective
Create multiple pages using Next.js routing and nested layouts.

##  Topics Covered
- Route structure of the App Router
- Nested layouts
- Client vs Server components
- Shared UI across routes

##  Tasks / Exercises
Implement routes:
- /
- /about
- /dashboard
- /dashboard/profile

##  Folder Structure
/app/page.jsx  
/app/about/page.jsx  
/app/dashboard/page.jsx  
/app/dashboard/profile/page.jsx  
/app/dashboard/layout.jsx  

## ▶ How to Run
npm install
npm run dev


##  Features Built
- Layout with persistent sidebar
- Profile page UI
- Navigation using `<Link />`



##  Notes / Learnings
- Layouts help prevent re-rendering shared UI.
- Client components are needed for interactivity.
