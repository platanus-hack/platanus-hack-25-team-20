#set page(paper: "us-letter", margin: 1.5cm)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true)

// Header
#align(center)[
  #text(size: 24pt, weight: "bold")[Juan Pérez]
  
  #text(size: 10pt)[
    #box(link("mailto:juan.perez@example.com")[`juan.perez@example.com`]) | #box[`+56 9 1234 5678`] | #box[`github.com/juanperez`] | #box[`linkedin.com/in/juanperez`]
  ]
  
  #text(size: 10pt)[#box[`Santiago, Chile`]]
]

#v(0.5cm)

// Summary
#text(size: 14pt, weight: "bold")[Summary]
#line(length: 100%, stroke: 0.5pt)
#v(0.2cm)

Experienced software developer with 5+ years in Python and web development.

#v(0.5cm)

// Experience
#text(size: 14pt, weight: "bold")[Experience]
#line(length: 100%, stroke: 0.5pt)
#v(0.2cm)


#grid(
  columns: (1fr, auto),
  [*Senior Software Engineer*], [_2020 - Present_]
)
_Tech Company Inc._

Led development of microservices architecture using FastAPI and Docker.

#v(0.3cm)

#grid(
  columns: (1fr, auto),
  [*Software Developer*], [_2018 - 2020_]
)
_StartupXYZ_

Developed REST APIs and frontend applications with React.

#v(0.3cm)


// Education
#text(size: 14pt, weight: "bold")[Education]
#line(length: 100%, stroke: 0.5pt)
#v(0.2cm)


#grid(
  columns: (1fr, auto),
  [*Computer Science*], [_2014 - 2018_]
)
_Universidad de Chile_

Bachelor's degree with focus on software engineering.

#v(0.3cm)


// Skills
#text(size: 14pt, weight: "bold")[Skills]
#line(length: 100%, stroke: 0.5pt)
#v(0.2cm)


- *Programming Languages*: Python, JavaScript, TypeScript

- *Frameworks*: FastAPI, React, Django

- *Tools*: Docker, PostgreSQL, Git

