#set page(paper: "us-letter", margin: 1.5cm)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true)

// Header
#align(center)[
  #text(size: 24pt, weight: "bold")[<< firstname >> << lastname >>]
  
  #text(size: 10pt)[
    #box(link("mailto:<< email >>")[`<< email >>`]) | #box[`<< phone >>`]<% if github %> | #box[`<< github >>`]<% endif %><% if linkedin %> | #box[`<< linkedin >>`]<% endif %>
  ]
  
  #text(size: 10pt)[#box[`<< address >>`]]
]

#v(0.5cm)

// Resumen
#text(size: 14pt, weight: "bold")[Resumen]
#line(length: 100%, stroke: 0.5pt)
#v(0.2cm)

<< summary >>

#v(0.5cm)

// Experiencia
#text(size: 14pt, weight: "bold")[Experiencia]
#line(length: 100%, stroke: 0.5pt)
#v(0.2cm)

<% for exp in experiences %>
#grid(
  columns: (1fr, auto),
  [*<< exp.title >>*], [_<< exp.date >>_]
)
_<< exp.company >>_

<< exp.description >>

#v(0.3cm)
<% endfor %>

// Educación
#text(size: 14pt, weight: "bold")[Educación]
#line(length: 100%, stroke: 0.5pt)
#v(0.2cm)

<% for edu in education %>
#grid(
  columns: (1fr, auto),
  [*<< edu.degree >>*], [_<< edu.date >>_]
)
_<< edu.institution >>_

<< edu.description >>

#v(0.3cm)
<% endfor %>

// Habilidades
#text(size: 14pt, weight: "bold")[Habilidades]
#line(length: 100%, stroke: 0.5pt)
#v(0.2cm)

<% for skill in skills %>
- *<< skill.category >>*: << skill.skill_list >>
<% endfor %>

